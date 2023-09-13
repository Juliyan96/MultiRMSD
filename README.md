# MultiRMSD

MultiRMSD is a Python package that provides tools for calculating Root Mean Square Deviation (RMSD) of multiple PDB and SDF structures. 

## Requirements

Python 3.7 or higher (Google Colab is highly recommended)

## Installation

### Manual Installation by cloning MultiRMSD into your Google Colab Worksheet

1. Clone the repository to your Google Colab worksheet:

 ```bash
 !git clone https://github.com/Juliyan96/MultiRMSD.git

 ```
2. Install the necesarry dependencies to your Google Colab worksheet, Py3DMol and Biopython and RDKit.

 ```bash
!pip install biopython
```
```bash
!pip install py3Dmol
```
```bash
!pip install RDKit
```
## Workflow to calculate RMSD

1. Add all your PDB or SDF files that require RMSD calculation into your desired directory. Preferebly your Google Colab worksheet. Make sure that the reference structure residue numbers and the residue IDs are similar with the mobile strucutres. For SDF files number of bonds (valence) should be similar between the reference structure and the mobile structures.
2. Run MultiRMSD using the code below. Edit the reference structure ID and the Directory path ID as desired.
#### "-r" Reference structure, "-d" Path to working directory
```bash
!python MultiRMSD/MultiRMSD.py -r reference.pdb -d /path/to/working/directory
```
If you only opt to align your PDB or SDF structures without calculating RMSD you can use the following command.
#### "-a" Align only
```bash
!python MultiRMSD/MultiRMSD.py -r reference.pdb -d /path/to/working/directory -a
```
## Results

This will produce a .log file named RMSD_Out.log which would contain the calculated RMSD for each mobile structure with its reference structure. Additionally, the aligned PDB structures will be created in a new folder named "Aligned_structures" in your working directory. You can view these aligned PDB structures by using PyMol or Py3DMol. If you have opted to just align the PDB or SDF structures the aligned structures will be stored in the Aligned_structures directory without the RMSD calculations. The required workflow to view on Py3Dmol is shown below

##### Note: These file generations would take roughly around 20 seconds once the Google Colab cell had been run and completed. All output files will be saved in your working directory that holds the PDB files.

In this py3Dmol code, replace the reference structure ID with your reference structure's ID and run it in a Google colab cell.

```bash
import os
import py3Dmol

def visualize_aligned_structures(aligned_folder):
    viewer = py3Dmol.view(width=800, height=400)
    
    # List all PDB files in the Aligned_structures folder
    aligned_files = [f for f in os.listdir(aligned_folder) if f.endswith(".pdb")]

    for pdb_file in aligned_files:
        pdb_path = os.path.join(aligned_folder, pdb_file)
        with open(pdb_path, "r") as pdb_file:
            pdb_data = pdb_file.read()
        viewer.addModel(pdb_data, format="pdb")

    viewer.setStyle({"cartoon": {"color": "spectrum"}})  # Use cartoon style with a color spectrum
    viewer.zoomTo()
    return viewer

if __name__ == "__main__":
    aligned_folder = "Aligned_structures"  # Change to the actual folder path
    viewer = visualize_aligned_structures(aligned_folder)
    viewer.show()
   
```
###### Juliyan Gunasinghe, 2023
###### This project is licensed under the MIT License - see the LICENSE.txt file for details.

