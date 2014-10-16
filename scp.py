# refer to notes_mmgbsa for general comments
# to run: $SCHRODINGER/run scp.py
import os, time

from schrodinger import structure
from schrodinger.structutils import build

SEQ_FILE = "jmol_seqs"

# returns a string of the sequence of residues in a peptide
def get_seq(pep):
	seq = ""
	for res in pep.residue:
		seq = seq + res.getCode()
	return seq

# returns pep.residue[index]
def get_res(pep, index):
	i = 0
	for res in pep.residue:

		if index == i:
			return res
		i = i + 1

# returns the index of the first atom in res
def get_ind(res):
	for at in res.atom:
		return at.index


# pass in a copy of the ligand (structure)
# returns a mutated structure with the sequence in other (string)
def mutate_pep(ligand, other):
	
	native = get_seq(ligand)
	# native and other must be the same length for now
	if len(native) != len(other):
		return None

	resnum_list = []
	for i in range(len(native)):

		# mutate at the position of the different letter
		if native[i] != other[i]: 

			res = get_res(ligand, i) # reference to the Ith residue
			resnum_list.append(res._getResnum())
			# need the index (int) of any atom in the residue to be mutated
			ind = get_ind(res)

			# change the residue containing ind to the residue in other
			build.mutate(ligand, ind, CODES[other[i]])

	return ligand, resnum_list

# create the input file for running a monte carlo side chain prediction job
def write_inp(filename, resnum_list):
	s = "STRUCT_FILE\t" + filename + ".maegz\nJOB_TYPE\tREFINE\nPRIME_TYPE\tMC\n"
	s = s + "SELECT\tpick\n"

	for i, res in enumerate(resnum_list):
		s = s + "RESIDUE_" + str(i) + "\tB:" + str(res) + "\n" # chain is B

	# return 6 conformations
	s = s + '''NUM_OUTPUT_STRUCT\t6\nUSE_CRYSTAL_SYMMETRY\tno\nUSE_RANDOM_SEED\tno
SEED\t0\nOPLS_VERSION\tOPLS2005\nEXT_DIEL\t80.00\nUSE_MEMBRANE\tno\nNSTEPS\t100
PROB_SIDEMC\t1.0\nPROB_RIGIDMC\t0.0\nPROB_HMC\t0.0\nTEMP_SIDEMC\t2000.0
MINIMIZE\tyes\nFIND_BEST_STRUCTURE\tyes\nHOST\tlocalhost'''

	prime = open(filename + ".inp", "w")
	prime.write(s)
	prime.close()

# dictionary of residue abbreviations, CODES["A"] gives "ALA"
CODES = {'A':'ALA', 'R':'ARG', 'N':'ASN', 'D':'ASP', 'C':'CYS', 'Q':'GLN', 'E':'GLU',
		 'G':'GLY', 'H':'HIS', 'I':'ILE', 'L':'LEU', 'K':'LYS', 'M':'MET', 'F':'PHE',
		 'P':'PRO', 'S':'SER', 'T':'THR', 'W':'TRP', 'Y':'TYR', 'V':'VAL'}


# run protein prep and split by chain in maestro, then export as separate files
pro = structure.read_ct("1tp5prepA.mae")
lig = structure.read_ct("1tp5prepB.mae") # KKETWV

# read file of sequences to mutate to
seqs_file = open(SEQ_FILE, "r")

seqs = [] # list of strings, must be in all caps for it to work with CODES
for line in seqs_file:
    seqs.append(line.strip())

seqs_file.close()

# dictionary with key = peptide sequence, and value = reference to the structure
peptides = {}

for entry in seqs:
	# the entry is the file name

	# mutate each peptide to the sequence in entry
	# keep track of the resnums that have been changed
	peptides[entry], resnum_list = mutate_pep(lig.copy(), entry)
	peptides[entry]._setTitle(entry)

	# build the .inp file for prime
	write_inp(entry, resnum_list)

	# merge the mutated peptide to the protein and write it to a file
	merged = peptides[entry].merge(pro)
	writer = structure.StructureWriter(entry + '.maegz')
	writer.append(merged)
	writer.close()

	# run side chain predictions on the mutated residues, get 6 conformations
	os.system("$SCHRODINGER/prime " + entry + ".inp")

	time.sleep(15)

