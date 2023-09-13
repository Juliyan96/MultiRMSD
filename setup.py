from setuptools import setup

setup(
    name="MultiRMSD",
    version="1.0",
    author="Juliyan Gunasinghe",
    author_email="juliyangunasinghe@gmail.com",
    description="A tool for calculating RMSD of multiple PDB structures",
    url="https://github.com/Juliyan96/MultiRMSD",
    packages=[""],  
    install_requires=["biopython", "numpy", "py3Dmol"],
    entry_points={
        "console_scripts": [
            "MultiRMSD=MultiRMSD.MultiRMSD:main"  
        ]
    },
)


