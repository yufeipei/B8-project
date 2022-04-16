#---SINGLE PHOTON COUNTING-----------------------

#Set the number of strips to cut
norm_cut_num = 128

# Set the threshold:
thres = 30

# Set the step length for each parameters
step_x = 0.01
step_y = 0.01
step_sx = 0.005
step_sy = 0.005
step_A = 0.3

# Set the descent factor: a factor to be multiplied when deciding the amount of change of parameters in each iteration
descent_factor = 0.2

# We require the standard errors to be bounded; define the minimum and maximum allowed values:
s_min = 0.2
s_max = 0.6

# Set the other parameters described above
iter_diff = 10
conv_crit = 1/40
err_max = 1600

# Set the miximum number of iterations
max_iter = 400

# Set the maximum # of photons allowed in each event:
max_photon = 20

# Specify the boundaries of the region with which we are going to fit the Gaussian.
gauss_min = 12
gauss_max = 30

# Specify the number of bins that is going to be used in the following function to bin the events
_bins = 400

#---BRAGG'S SPECTROSCOPY-------------------

# Set the parameters for finding the spectral lines
fit_cut_num = 32
half_width = 10
peak_width = 100

# The order of diffraction as well as the double of the lattice spacing, in angstrom
fit_n = 1
fit_2d = 15.96

# Set the initial values of the fitting parameters: see the report or the Jupyter notebook.
l_init = 6000
alpha_init = 1
phi_init = 0
x0_init = 800
y0_init = 600