#!/home/hamit/jupyter_env/venv/bin/python

###########

# Usage:
# python fix_pdb.py </path/to/original_ligand.pdb> </path/to/leadfinder_output_poses.pdb>

###########

import re


def fix_pdb(original_ligand_pdb, docked_poses_pdb):
    '''
    Restores information about atoms based on the original pdb file.

    Parameters
    ----------
    original_ligand_pdb : str
        Path to incomplete pdb file
    docked_poses_pdb : str
        Path to original pdb file
    '''
    pdbatom_pattern = re.compile('((ATOM|HETATM)\s+)(\d+)(\s+)([A-Z]+)(.+\n)')
                
    atom_lines = {}
    with open(original_ligand_pdb, 'r') as pdb:
        for line in pdb:
            match = pdbatom_pattern.match(line)
            if match:
                atom = match.groups()[2]
                atom_lines[atom] = line

    pdb_content = []
    with open(docked_poses_pdb, 'r') as pdb:
        for line in pdb:
            match = pdbatom_pattern.match(line)
            if match:
                if match.groups()[4].startswith('H'):
                    continue
                atom = match.groups()[2]
                patch = line[30:66]
                template = atom_lines[atom]
                line = template[:30] + patch + template[66:]
            pdb_content.append(line)
            
    with open(docked_poses_pdb, 'w') as pdb:
        pdb.writelines(pdb_content)


if __name__ == '__main__':
    import sys

    ORIGINAL_PDB, DOCKED_PDB = sys.argv[1:3]
    fix_pdb(ORIGINAL_PDB, DOCKED_PDB)
    