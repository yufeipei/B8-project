# B8-project

This is the final code for the B8 project "X-ray Single-Photon Energy-Dispersive Spectroscopy" by Yufei Pei.

To run the program:
- Download the py folder
- Run `main.py`

The program will take in a .h5 file and create a csv file containing data obtained from single photon counting, as well as a .png file which is the final spectrum.

If the program is used to process other data than that provided in the project, some hyperparams may need to be changed. They are stored in `hyperparams.py` with explanations provided. In particular you may want to change those in the Bragg spectroscopy section.

The `main.ipynb` file is a Jupyter notebook containing detailed explanations of each step of the code used, as well as a demonstration of the single photon counting part using the data stored in `demo_data.csv`. Please make sure that the csv file is in the same directory when running the notebook.

Packages required:
- `matplotlib`
- `numpy`
- `h5py`
- `itertools`
- `PIL`
- `scipy`
- `math`
- `copy`
- `statistics`
- `time`
- `csv`
