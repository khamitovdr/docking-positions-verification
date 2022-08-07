#!/home/hamit/jupyter_env/venv/bin/python

###########

# Usage:
# python optimize_ligand.py (</path/to/ligand.mol> | </path/to/ligands/dir/>) (</path/to/output.pdb> | </path/to/output/dir/>)

###########

from rdkit import Chem
from rdkit.Chem import AllChem


def mol_with_atom_index(mol):
    '''
    Indexes the atoms of the structure obtained from the mol file.

    Parameters
    ----------
    mol : rdkit.Chem.rdchem.Mol
        Chemical structure.

    Returns
    -------
    mol : rdkit.Chem.rdchem.Mol
        Indexed chemical structure.
    '''
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(atom.GetIdx())
    return mol

def optimize_ligand(ligand_path, output_path):
    '''
    Uses RDKit to add hydrogen atoms and 3d optimize ligand structures.

    Parameters
    ----------
    ligand_path : str
        Path to ligand mol file.
    output_path : str
        Path to output optimized ligand.

    Returns
    -------
    mol_H : rdkit.Chem.rdchem.Mol
        Optimized structure.
    '''
    mol = Chem.MolFromMolFile(ligand_path)
    mol_H = Chem.AddHs(mol)

    while AllChem.EmbedMolecule(mol_H):
        pass

    while AllChem.MMFFOptimizeMolecule(mol_H):
        pass
    
    Chem.MolToPDBFile(mol_with_atom_index(mol_H), output_path)
    return mol_H


if __name__ == '__main__':
    import os
    import sys

    INPUT_PATH = sys.argv[1]
    OUTPUT_PATH = sys.argv[2]

    if INPUT_PATH.endswith('.mol'):
        optimize_ligand(INPUT_PATH, OUTPUT_PATH)
        print(f'Optimized: {os.path.basename(INPUT_PATH)}')
    else:
        for ligand_file in os.listdir(INPUT_PATH):
            if not ligand_file.endswith('.mol'):
                continue

            optimize_ligand(f'{INPUT_PATH}/{ligand_file}', f'{OUTPUT_PATH}/{ligand_file[:-3]}pdb')
            print(f'Optimized: {ligand_file}')
