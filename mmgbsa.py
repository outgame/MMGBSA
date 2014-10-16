import os
from schrodinger import structure

CONFORMATIONS = 6
SEQ_FILE = "jmol_seqs"

def get_confs(filename):
	reader = structure.StructureReader(filename)

	confs = []
	# every even numbered structure is the peptide conformation (odd is the protein)
	for i in range(CONFORMATIONS):

		# if there were fewer than 6 conformations, don't keep reading
		try: 
			reader.next() # will always be the same protein
			confs.append(reader.next())

		except StopIteration: 
			break

	reader.close()
	return confs

# SHOULD GO IN A DIFFERENT FILE THAT BOTH THIS AND SCP CAN USE
# read file of sequences
seqs_file = open(SEQ_FILE, "r")

seqs = [] # list of strings
for line in seqs_file:
    seqs.append(line.strip())

seqs_file.close()

all_confs = {}

for entry in seqs:
	filename = "all" + entry + ".maegz"

	# split structure by chain, puts 12 structures into ex) allKKETEV.maegz
	os.system("$SCHRODINGER/run split_structure.py " + entry + "-out.maegz " + filename)

	# if side chain prediction didn't work, there won't be an -out file
	if os.path.isfile(filename):
		confs = get_confs(filename)
		all_confs[entry] = confs

pro = structure.read_ct("1tp5prepA.mae")

# debugging
writer = structure.StructureWriter('test.maegz')
writer.append(pro)
for key in all_confs.keys():
	for val in all_confs[key]:
		writer.append(val)
writer.close()

# do NJOBS 2 since I have 2 cores?
os.system("$SCHRODINGER/prime_mmgbsa test.maegz -report_full")

''' IDEAS FOR IMPROVEMENTS
able to run from command line, get args: filename, number of conformations
split original structure in script
protein prep in script?
use os.something to get number of cores, NJOBS #ofcores
comments, make it prettier
have a -h option to see usage
able to check peptide sequences of different length
'''


