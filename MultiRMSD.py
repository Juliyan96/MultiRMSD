import argparse
import os
import numpy as np
from Bio.SVDSuperimposer import SVDSuperimposer
from Bio.PDB import PDBParser, PDBIO
from rdkit import Chem
from rdkit.Chem import AllChem

def calculate_rmsd(reference_coords, coords):
    sup = SVDSuperimposer()
    sup.set(reference_coords, coords)
    sup.run()
    return sup.get_rms()

def align_structures(reference_coords, coords):
    sup = SVDSuperimposer()
    sup.set(reference_coords, coords)
    sup.run()
    aligned_coords = sup.get_transformed()
    return aligned_coords

def read_sdf(file_path):
    supplier = Chem.SDMolSupplier(file_path)
    molecules = [mol for mol in supplier if mol is not None]
    return molecules

def main():
    parser = argparse.ArgumentParser(description="Calculate and save aligned coordinates.")
    parser.add_argument("-r", "--reference", required=True, help="Path to the reference PDB or SDF file")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing PDB or SDF files for comparison")
    parser.add_argument("-a", "--align", action="store_true", help="Align structures only, do not calculate RMSD")
    args = parser.parse_args()

    # File Format Extension
    file_extension = os.path.splitext(args.reference)[-1].lower()

    if file_extension not in {".pdb", ".sdf"}:
        raise ValueError("Unsupported file format. Only PDB and SDF files are supported.")

    parser = PDBParser(QUIET=True)
    reference_structure = parser.get_structure("reference", args.reference)
    reference_coords = np.array([atom.get_coord() for atom in reference_structure.get_atoms()])

    output_file = "RMSD_Out.log"
    with open(output_file, "w") as f:
        f.write("*******************************************************************************************\n")
        f.write("Thank you for using MultiRMSD. A tool to calculate RMSD of multiple PDB and SDF Structures.\n")
        f.write("*******************************************************************************************\n\n")

        f.write(f"Reference Structure ID: {args.reference}\n\n")
        if not args.align:
          f.write("Mobile Structure ID     RMSD (A)\n")

        if not os.path.exists("Aligned_structures"):
            os.makedirs("Aligned_structures")

        for filename in os.listdir(args.directory):
            if filename.endswith(".pdb"):
                file_path = os.path.join(args.directory, filename)
                structure = parser.get_structure("mobile", file_path)
                coords = np.array([atom.get_coord() for atom in structure.get_atoms()])
                aligned_coords = align_structures(reference_coords, coords)

                # Save PDB files in Aligned_structures
                output_filename = os.path.join("Aligned_structures", f"aligned_{filename}")
                io = PDBIO()
                aligned_structure = structure.copy()  # Make a copy of the original structure
                for i, atom in enumerate(aligned_structure.get_atoms()):
                    atom.set_coord(aligned_coords[i])
                io.set_structure(aligned_structure)
                io.save(output_filename)

                if not args.align:
                    rmsd = calculate_rmsd(reference_coords, coords)
                    f.write(f"{filename:<25}{rmsd:.3f}\n")

            elif filename.endswith(".sdf"):
                file_path = os.path.join(args.directory, filename)
                molecules = read_sdf(file_path)
                if len(molecules) != 1:
                    print(f"Skipping {filename}: SDF should contain only one molecule.")
                    continue
                mol = molecules[0]
                # Convert the molecule to a PDB-compatible format
                mol = Chem.MolToMolBlock(mol)
                mol = Chem.MolFromMolBlock(mol)
                mol_block = Chem.MolToPDBBlock(mol)
                structure = PDBParser(PERMISSIVE=True).get_structure("mobile", io.StringIO(mol_block))
                coords = np.array([atom.get_coord() for atom in structure.get_atoms()])
                aligned_coords = align_structures(reference_coords, coords)

                # Save SDF files in Aligned_structures
                output_filename = os.path.join("Aligned_structures", f"aligned_{filename}")
                io = Chem.SDWriter(output_filename)
                io.write(mol)

                if not args.align:
                    rmsd = calculate_rmsd(reference_coords, coords)
                    f.write(f"{filename:<25}{rmsd:.3f}\n")

    print("RMSD Calculation is Done. Please find results in RMSD_Out.log file" if not args.align else "Structure Alignment Completed! Check the Aligned_structures folder for the Aligned Structures.")

if __name__ == "__main__":
    main()
