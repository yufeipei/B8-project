from run_spc import *

def moving_avg(strip_dat):
    
    # Input: data in a single strip, containing the x- and y- coordinates of photons.
    # Output: moving_average, a length (2048 - half_width) array described above.
    
    # Initialise the moving_average array:
    moving_average = np.zeros(2048 - half_width)
    
    # Iterate each photon event, and add a count to all entries in moving_average with distance < half_width
    for e in strip_dat:
        y = e[1]
        
        start = max(0, int(y) - half_width + 1)
        end = min(2048 - half_width, int(y) + half_width)
        
        moving_average[start:end] = moving_average[start:end] + 1
    
    return moving_average

def point_finding(x_list, y_list, spec_n):
    
    print('Finding spectral lines...')
    # Input: the x- and y- coordinates of photons
    # Output: within each strip, the coordinate of n points lying on each of the spectral lines
    
    # Sort the data based on x-coordinates in order to cut it
    data = np.transpose([x_list, y_list])
    x_list, y_list = np.transpose(data[data[:, 0].argsort()])
    
    # Make sure that fit_cut_num is a factor of the size of the image, i.e. 2048. If not, raise an error.
    try:
        cut_height = int(2048/fit_cut_num)
        if(cut_height * fit_cut_num != 2048):
            raise ValueError('Invalid norm_cut_num')
    except ValueError as e:
        print('Error: ', e)
    
    point_ls = [[] for i in range(spec_n)]

    # store the cutting points in the array of coordinates
    cut_points = [0]
    
    for n in range(fit_cut_num):
        # Find the next cutting point
        for i in range(cut_points[-1], len(x_list)):
            if(x_list[i] > (n+1) * cut_height):
                # Store the cut point
                cut_points.append(i)
                break
                
        # Obtain the strip data:
        begin = cut_points[-2]
        end = cut_points[-1]
        dat = np.transpose([x_list[begin:end], y_list[begin:end]])
        moving_average = moving_avg(dat)

        # Find the peaks using methods described above:
        peaks = np.zeros([spec_n, 2]) # A n*2 array, used to store the values and positions of peaks
                
        for i in range(len(moving_average)):
            begin = max(0, i - peak_width)
            end = min(2048, i + peak_width)
            if(moving_average[i] == max(moving_average[begin:end])): # peak found
                if(i >= 5 and moving_average[i] == max(moving_average[i-5:i])): # avoid counting the same peak twice
                    continue
                if(spec_n == 1): # Only one spectral line:
                    if(moving_average[i] > peaks[0][1]):
                        peaks[0][1] = moving_average[i]
                        peaks[0][0] = i
                elif(peaks[-1][1] < moving_average[i]): # The current peak is larger than at least one of the peaks stored
                    # Remove the last entry of peaks, which, upon sorting later, is the smallest
                    peaks[-1] = (i, moving_average[i])
                    peaks = sorted(peaks, key = lambda x: x[1], reverse = True)
        
        # Sort the peaks with their coordinates, to make sure that they corresponds to the correct spectral line
        peaks = sorted(peaks, key = lambda x: x[0], reverse = True)
        # Add the peaks found to the point list; their x-coordinate is taken to be that of the middle of the strip
        for m in range(spec_n):
            point_ls[m].append([int(n * cut_height + cut_height / 2),
                                     np.transpose(peaks)[0][m] + half_width / 2]) 
            # The additional term in the second entry is to compensate for the moving average
            
    return point_ls

def geometry(point_ls, theta_ls):
    
    # Input: the list of points obtained in previous steps
    # Output: estimation of the five parameters
    
    print('Fitting the expressions of the spectral lines...')

    # Define a function to calculate the error of a single point, defined to be the square of the difference
    # of the LHS and the RHS of the above expression
    def point_error(x, y, l, alpha, phi, x0, y0, theta):
        x = x - x0
        y = y - y0

        calc_theta = np.arctan(np.sqrt(((-l * np.sin(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.cos(alpha))**2
               + (x * np.cos(phi) - y * np.sin(phi))**2 ) /
               ((l * np.cos(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.sin(alpha))**2))**-1)
        calc_energy = fit_n * 12398.4 / fit_2d / np.sin(calc_theta)
        real_energy = fit_n * 12398.4 / fit_2d / np.sin(theta)
        #print(calc_energy, real_energy)
        return (calc_energy - real_energy)**2
    
    # Define a function that calculates the total error, with the only parameter being a list of parameters for fitting,
    # to be used in scipy.optimize.least_squares later
    def total_error(params):
        l, alpha, phi, x0, y0 = params

        err = 0
        for i in range(len(point_ls)):
            points = point_ls[i]
            theta = theta_ls[i]
            for point in points:
                x, y = point
                err = err + point_error(x, y, l, alpha, phi, x0, y0, theta)
        return err
    
    params = np.array([l_init, alpha_init, phi_init, x0_init, y0_init])
    
    fit_step = [3, 0.0001, 0.00001, 0.3, 0.3]
    descent_factor = 0.5
    for i in range(400):
        #print(params+np.diag(fit_step))
        tot_err = total_error(params)
        err = [total_error(p) for p in params + np.diag(fit_step)] - tot_err
        #print('error', err)
        #print('tot_err', tot_err)
        params = params - fit_step * err * descent_factor
        #print('params', params)
        if(tot_err < 20):
            
            break
    res = least_squares(total_error, params, 
                        bounds = ([0, 0, -np.pi, 0, 0],[np.inf, 2 * np.pi, np.pi, 2048, 2048]),
                       verbose = 0, xtol = 1e-10
                 ) 
    return params

def energy(x, y, params, spec_energies, theta_ls):
    
    # Input: coordinates of the photon, the params fitted
    # Output: energy of the photon
    
    l, alpha, phi, x0, y0 = params

    x = x - x0
    y = y - y0
    
    denumerator = (-l * np.sin(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.cos(alpha))**2 + (x *np.cos(phi) - y * np.sin(phi))**2 
    numerator = (l * np.cos(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.sin(alpha))**2

    theta = np.arctan(np.sqrt(numerator / denumerator))
    
    # Use the energy and theta of the first spectral line to deeuce the energy:
    
    e1 = spec_energies [0]
    theta_1 = theta_ls [0]
    
    return e1 * np.sin(theta_1) / np.sin(theta)

def generate_plot(x_list, y_list, A_list, bins, _params, save_loc, spec_energies, theta_ls, max_e, min_e):
    
    print('Generating plot...')
    # Input: lists of coordinates and intensities of photons, as well as the desired # of bins of the plot
    # Output; the plot
    
    l, alpha, phi, x0, y0 = _params
        
    # Initialise the value of each energy bins
    energy_plot=np.zeros(bins)
    
    denom=1 / (max_e - min_e)
    
    def f(y, x, theta):
        x = x - x0
        y = y - y0
        return ((-l * np.sin(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.cos(alpha))**2
                   + (x * np.cos(phi) - y * np.sin(phi))**2 
                   - (l * np.cos(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.sin(alpha))**2 * np.tan(theta)**-2
                   )
    
    correction = []
    # Generate correction
    for i in range(bins):
        e = min_e + (max_e - min_e) / bins * i
        theta = np.arcsin(spec_energies[0] * np.sin(theta_ls[0]) / e)
        y_top = fsolve(f, 1500, args = (2048,theta))[0]
        y_bot = fsolve(f, 1500, args = (0, theta))[0]
        
        psi = []
        for x,y in [[2048, y_top],[0, y_bot]]:
            x = x - x0
            y = y - y0
            #print(x, y)
            x_pp = (-l * np.sin(alpha) + (x * np.sin(phi) + y * np.cos(phi)) * np.cos(alpha))
            y_pp = (x * np.cos(phi) - y * np.sin(phi))
            psi.append(np.arctan(x_pp/y_pp))

        correction.append(np.sin(alpha + theta))
    
    for i in range(len(x_list)):
        e = energy(x_list[i],y_list[i], _params, spec_energies, theta_ls)
        if(e > min_e and e < max_e):
            index = int((e-min_e)*denom*bins)
            energy_plot[index]=energy_plot[index]+A_list[i] / correction[index]
            
    plt.xlim([1100,1600])
    
    plt.semilogy()
    plt.plot(np.linspace(min_e,max_e,len(energy_plot)),energy_plot);
    
    plt.ylabel('Intensity(a.u.)',fontsize = 20);
    plt.xlabel('Energy(eV)',fontsize = 20);
    plt.yticks(fontsize = 15);
    plt.xticks(fontsize = 15);

    plt.savefig(fname = save_loc)
    print('Plot saved at %s' % save_loc)
    
    return 0