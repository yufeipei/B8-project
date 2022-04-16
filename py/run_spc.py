from import_hdf import *
from spc import *

def spc_running(file_loc = 'sxro6416-r0504.h5', csv_loc = "data1.csv"):
    #file_loc = input("Please input path of file here:")

    image_data = import_images(file_loc)

    print("Preparing the images...")
    for i in range(len(image_data)):
        image_data[i] = image_normalisation(image_data[i], norm_cut_num)
        image_data[i] = boundary_setting(image_data[i])

    spc_result = single_photon_counting(image_data)

    write_in_csv(spc_result, name = csv_loc)
    return spc_result

def event_filtering(spc_result, _bins):
    
    # Input: the list of the result; the number of bins into which we divide our result
    # Output: filtered results, as well as their x, y and A for further manipulations
    
    print('\r', 'Filtering events...', end = '', flush=True)

    # Generate the list containing the intensity values
    A_list = [per.A for per in spc_result]

    # Define the edge of the bins; we only use the part of the histogram with A < gauss_max. 
    x_bins = np.linspace(0, gauss_max, _bins)
    
    # Find the value in each bin
    A_bins = np.zeros(_bins)
    for a in A_list:
        if(a < gauss_max):
            A_bins[int(a / gauss_max * _bins)] = A_bins[int(a / gauss_max * _bins)] + 1
        
    # Obtain the part of the histogram that we are going to use to perform the fit:
    start_bins = int(gauss_min / gauss_max * _bins)
    fit_A = A_bins[start_bins: ]
    fit_x = x_bins[start_bins: ]
    
    # Perform the fit
    def gaussian(x, A0, x0, sigma):
        return A0 * np.exp(-(x - x0)**2 / (2 * sigma**2))
    
    popt = curve_fit(
        f = gaussian, # model function
        xdata = fit_x, # x data
        ydata = fit_A, # y data
        p0 = (30000, 20, 10) # initial guess of parameters
    )[0]
    
    # Start event filtering and photon counting:
    
    photon_n = 0 # Photon number
    photon_sigma = 0 # Photon uncertainty
    
    filtered_spc = []
    for per in spc_result:
        if(per.A <= 0): # Filter invalid events
            continue
        elif(per.A < gauss_min): 
            # For low intensity events, the probability of keeping this event 
            # p = value of the Gaussian fit at its intensity / # of events in the bin it belongs to, with a maximum of 1
            p = min(1, 
                    (gaussian(per.A, popt[0], popt[1], popt[2]) / 
                     max(A_bins[int(per.A / gauss_max * _bins)], 0.0000001))) # prevent the possibility of divide by zero
            
            if(np.random.rand() <= p):
                filtered_spc.append(per)
                photon_n = photon_n + per.A / popt[1]
            photon_sigma = photon_sigma + np.sqrt(p * (1 - p))
        else:
            filtered_spc.append(per)
            photon_n = photon_n + per.A / popt[1]
            if(per.A > gauss_max):
                x = min(1, per.A / popt[1] - 1)
                photon_sigma = photon_sigma + np.sqrt(x * (1 - x))
    
    x_list = [per.x for per in filtered_spc]
    y_list = [per.y for per in filtered_spc]
    A_list = [per.A for per in filtered_spc]
    
    print('\r', 'Filtering complete. %d photon events are left.' % len(x_list), flush=True)
    print('Total photon number: %d ± %d' % (photon_n, photon_sigma))
    return [x_list, y_list, A_list]



if __name__ == "__main__":
    spc_running()
