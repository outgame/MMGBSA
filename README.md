MMGBSA
======
scp.py:
	Reads in two .pdb files that contain a protein and a corresponding peptide ligand. It also reads in a list of residue sequences that are the same length as the peptide. The peptide file is copied and mutated to each of the new sequences and are merged with the original protein. Then side chain prediction is run to return the 6 best conformations of each mutated peptide in the binding site, and an .inp (input) file is written. This file just contains information about which residues were mutated and their location.

mmgbsa.py:
	Uses the .inp files and runs MM-GBSA on each of the conformations to get the predicted binding affinity for each mutated sequence with the original protein.

Summary:
	Essentially what I have right now is two python files that can read in a bunch of sequences and check how well they bind with a protein. 1TP5 is the protein I’m using right now because it is a PDZ3 domain and there is extensive experimental data for difference sequences. 
Everything works as it should, but the MM-GBSA outputs aren’t correlating well with the experimental data. When the predicted values are plotted against the experimental delta G or H values, there isn’t a clear regression line.

Next Steps:
Obviously the first step would be to try to get the values to correlate. Whether it’s tweaking the way MM-GBSA is running or anything else I can try, it is most important to try to get the values to be at least ranked correctly, otherwise there is no use predicting the values on the computer.
Other minor things are tweaks to the program, include using sequences of different length than the original peptide or incorporating WaterMap evaluations to improve accuracy.
Looking further ahead and bigger picture, I think the program has a lot of potential. First, it would awesome to be able to run the program (which takes around 45 minutes total) and get reliable data on a protein that hasn’t been experimentally evaluated yet. This would save time and narrow down targets for people who have to make them in the lab. Second, since enthalpy is much easier to predict than entropy, there might be a way to use the discrepancy between the MM-GBSA values and the real delta G values to determine a calculation for entropy. I think this would be very difficult and variable, but I didn’t want to count it out. Third, something that was mentioned over the summer was to try to determine an idea scaffold for a protein, which is basically the best possible binding natural peptide. This could be used as a control to compare to unnatural side chains or other types of additions. Fourth, adding onto the program a way to test unnatural amino acids directly would be a huge advance and is something that I don’t think has been done before.
