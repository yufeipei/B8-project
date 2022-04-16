from imports import *
from hyperparams import *

def image_normalisation(im, cut_num):
    
    # Input: the image; the number of strips to cut
    # Output: the normalised image
    
    # Make a copy of the input data, using the deepcopy function to ensure that im remains unchanged:
    dat = deepcopy(im.astype(int))
    # NB: astype(int) is added to convert the entries of im from unsigned int (0-65536) to signed int.
    
    # Make sure that cut_num is a factor of the size of the image, i.e. 2048. If not, raise an error.
    try:
        cut_height = int(2048/cut_num)
        if(cut_height * cut_num != 2048):
            raise ValueError('Invalid norm_cut_num')
    except ValueError as e:
        print('Error: ', e)
    
    # Normalise the image
    for i in range(32):
        # Find the mode of the strip; if multiple modes are found, select the minimum of them
        im_mode = min(mode(dat[i*64:(i+1)*64,:].flatten())[0])
        
        dat[i*64:(i+1)*64,:] = dat[i*64:(i+1)*64,:].astype(int) - im_mode
    
    return dat

def boundary_setting(im):
    
    # Input: a normalised image
    # Output: the image, with the entries near the edges set to 0
    
    # Find the height and width of im
    h = im.shape[0]
    w = im.shape[1]
    
    dat = deepcopy(im.astype(int))
    
    # Set the entries near the boundary to 0
    for i in range(h):
        for j in range(w):
            if((i < 2 or i > h - 2) or (j < 4 or j > w - 2)):
                dat[i, j]=0
                
    return dat


# The thresholding algorithm.

def thresholding(data, threshold):
    
    # Input: a normalised image
    # Output: A matrix, having the same dimensions of the input image, with each entry being 0 if the corresponding entry in the input 
    #         matrix is < threshold, and 1 if it's >= threshold
    
    def compare(val):
        if(val >= threshold):
            return 1
        else:
            return 0
    
    label_matrix = [[compare(data[i, j]) for j in range(data.shape[1])] for i in range(data.shape[0])]
    
    return label_matrix

def boundary_setting(im):
    
    # Input: a normalised image
    # Output: the image, with the entries near the edges set to 0
    
    # Find the height and width of im
    h = im.shape[0]
    w = im.shape[1]
    
    dat = deepcopy(im.astype(int))
    
    # Set the entries near the boundary to 0
    for i in range(h):
        for j in range(w):
            if((i < 2 or i > h - 2) or (j < 4 or j > w - 2)):
                dat[i, j]=0
                
    return dat

# The thresholding algorithm.

def thresholding(data, threshold):
    
    # Input: a normalised image
    # Output: A matrix, having the same dimensions of the input image, with each entry being 0 if the corresponding entry in the input 
    #         matrix is < threshold, and 1 if it's >= threshold
    
    def compare(val):
        if(val >= threshold):
            return 1
        else:
            return 0
    
    label_matrix = [[compare(data[i, j]) for j in range(data.shape[1])] for i in range(data.shape[0])]
    
    return label_matrix

# Establish a class of box, containing the coordinate of the edges, as well as the width and height of it.

class box:
    'used to enclose photon events'
    
    def __init__(self, xmin, ymin, xmax, ymax):
        self.x_min = xmin
        self.y_min = ymin
        self.x_max = xmax
        self.y_max = ymax
        
        self.width = xmax - xmin + 1
        self.height = ymax - ymin + 1
    
    def params(self):
        # Return the parameters of the box
        return [self.x_min, self.y_min, self.x_max, self.y_max]
    
    def hw(self):
        # Find the shape of the box
        return [self.height, self.width]

# The box assignment function

def boxing(thres_matrix, output = 'None'):
    
    # Input: the threshold matrix, coming from the thresholding() function
    # Output: A list of boxes identified within the image. 
    
    # The 'output' parameter determines whether the function prints some information for 
    # debugging or demonstration purposes.
    
    # Create a copy of the input matrix, so that it will not be changed
    m = np.array(deepcopy(thres_matrix))
    
    # Initialise the box list
    box_list = []
    
    #Prepare for plotting the dataset, if needed
    if(output != 'None'):
        fig, ax = plt.subplots(1)
                               
    # Search for entry 1's in the input matrix
    for i in range(m.shape[0]):
         for j in range(m.shape[1]):
            if(m[i, j] == 1):
                # An entry 1 is found: firstly, the box only contains this entry and its surrounding 3*3.
                x = i
                y = j
                
                x_min = x - 1
                y_min = y - 1
                x_max = x + 1
                y_max = y + 1
                
                # Search for if there is any more entry 1's in the surrounding 5*5:
                while(True):
                    # Flag identifying the presence of entry 1's
                    flag = 0
                    
                    # Set the current entry to 0, in order to avoid double counting
                    m[x, y] = 0
                    
                    for ii in range(x_min - 1, x_max + 2):
                        for jj in range(y_min - 1, y_max + 2):
                            # Check if the search has reached the boundary of the image; if so, skips.
                            if((ii >= m.shape[0]) or (jj >= m.shape[1])): 
                                continue
                            
                            elif(m[ii, jj] == 1): # More entry 1's are found
                                flag = 1
                                
                                # Set this entry to 0, in order to avoid double counting
                                m[ii, jj] = 0
                                
                                # Enlarge the box to accommodate all these entries found in this way,
                                # as they are assumed to be entangled and must be considered simultaneously
                                x_min = min(x_min, ii - 1)
                                y_min = min(y_min, jj - 1)
                                x_max = max(x_max, ii + 1)
                                y_max = max(y_max, jj + 1)
                                
                    # this searching process must be iterated until no more entry 1's are found 
                    # in the box's ambiance, and that it is safe to consider the elements whthin 
                    # this box separately.
                    if(flag == 0):
                        break
                
                #Append our box identified to the box list
                b = box(x_min, y_min, x_max, y_max)
                box_list.append(b)
                
                # Generate output, if needed
                if(output != 'None'):
                    print('box created containing [%d:%d, %d:%d]' % (x_min, x_max, y_min, y_max))
                    
                    # Add a rectangle representing this box to the plot
                    box_rect = patches.Rectangle((y_min - 0.5, x_min - 0.5), b.hw()[0], b.hw()[1],
                                                 linewidth = 1, edgecolor = 'r', facecolor = "none")
                    ax.add_patch(box_rect)

    # Generate output, if needed
    if(output != 'None'):
        plt.imshow(thres_matrix)
        plt.colorbar()
        plt.show()
    
    return box_list

# Defining a function that calculates the part within the square bracket of the above expression:
def entry(i, x0, s):
    
    # Calculate the variable in the first and second pairs of parentheses, applying bounds of [-10, 10] to it from reasons
    # discussed above
    var_1 = max(-10, min(10, (-x0 + i + 1) / (Sqrt2 * s)))
    var_2 = max(-10, min(10, (-x0 + i ) / (Sqrt2 * s)))
    
    # Convert the variables calculated into array indices for Erf[], and obtain the final value
    
    i1 = math.floor(var_1 * 100000)
    i2 = math.floor(var_2 * 100000)
    
    return Erf[i1] - Erf[i2]

class photon_event:
    'A photon event, the box in which it lives, and the ripple of ADU values it creates'
    
    def __init__(self, y0, x0, sx, sy, w, h, A):

        self.x0 = x0
        self.y0 = y0
        self.sx = sx
        self.sy = sy
        self.A = A
        
        # Width and height of the box
        self.h = h
        self.w = w
        
        # Generate the distribution matrix, ADU_G of the photon. 
        ls1=[entry(i, x0, sx) for i in range(w)]
        ls2=[entry(j, y0, sy) for j in range(h)]
        self.dist_matrix=1/2 * Pi * self.A * np.outer(ls1, ls2)

    # A function returning the five parameters of the photon 
    def params(self):
        return [self.x0, self.y0, self.sx, self.sy, self.A]
    
    # A function to change the parameter of the photon itself, but not the box
    def new_value(self, para_ls):
        
        self.x0, self.y0, self.sx, self.sy, self.A = para_ls
        
        # Alter the distribution matrix, ADU_G of the photon. 
        ls1=[entry(i, self.x0, self.sx) for i in range(self.w)]
        ls2=[entry(j, self.y0, self.sy) for j in range(self.h)]
        self.dist_matrix=1/2 * Pi * self.A * np.outer(ls1, ls2)

def error(pe_array, box_dat):
    
    # Input: a list of photon_event objects, as well as the data in the box containing these photons and them only
    
    # Find ADU_G, which is the linear superpositions of contributions from each photon
    tot_dist_matrix = sum([event.dist_matrix for event in pe_array])
    
    # Return the total error
    return sum(((box_dat - tot_dist_matrix)**2).flatten())

def descent(pe_ls, step_ls, dat):
    
    # Input: a list of photon events; the list of their step lengths; the data within the box considered.
    # Output: the updated list of parameters.
    
    # Calculate the photon number and the total error
    photon_n = len(pe_ls)
    err = error(pe_ls, dat)
    
    # The list of new parameters
    new_param_ls = []
    
    for n in range(photon_n):
        # Read the parameters of the current photon
        param = pe_ls[n].params()
        
        # Create five lists, in each of which one parameter is altered by its step length
        new_params = param + np.diag(step_ls)
        
        # Create the array storing the error differences and calculate the values of them.
        # NB for efficiency purposes a for loop is not used.
        err_diff = np.zeros(5)
        
        pe_ls[n].new_value(new_params[0])
        err_diff[0] = error(pe_ls, dat) - err
        
        pe_ls[n].new_value(new_params[1])
        err_diff[1] = error(pe_ls, dat) - err
        
        pe_ls[n].new_value(new_params[2])
        err_diff[2] = error(pe_ls, dat) - err
        
        pe_ls[n].new_value(new_params[3])
        err_diff[3] = error(pe_ls, dat) - err
        
        pe_ls[n].new_value(new_params[4])
        err_diff[4] = error(pe_ls, dat) - err
        
        # Generate the updated parameters
        # NB parameters are shifted in this way by an amount proportional to descent_factor, the gradient, and
        # the SQUARE of the step length. This is to accommodate the different ranges of them(e.g. some 0.1s for
        # sx and sy but 0-100 for A)
        new_param_ls.append(-np.array(step_ls) * descent_factor * err_diff + param)
        
        # Check if the standard errors and intensities are within boundary
        new_param_ls[n][2] = max(s_min, min(s_max, new_param_ls[n][2]))
        new_param_ls[n][3] = max(s_min, min(s_max, new_param_ls[n][3]))
        new_param_ls[n][4] = max(0, new_param_ls[n][4])
    
    return new_param_ls, err

step_ls = [step_x, step_y, step_sx, step_sy, step_A]

def gradient_descent_single(b, image_data, output = 'None'):
    
    # Input: a box classified as SPE, and the image data in which it lives
    # Output: the five parameters of the photon, and a boolean flag checking if we have mistaken an MPE as an SPE.
    
    # The 'output' parameter determines whether the function prints some information for 
    # debugging or demonstration purposes.
    
    # Generate the box data
    xmin, ymin, xmax, ymax = b.params()
    xmax = xmax + 1
    ymax = ymax + 1
    dat = np.array(image_data[xmin:xmax, ymin:ymax])
    
    # Generate output, if needed
    if(output != 'None'):
        print('Box data:')
        print(dat)
    
    # Generate initial x0, y0
    xavg = 0
    yavg = 0
    for i in range(dat.shape[0]):
        for j in range(dat.shape[1]):
            xavg = xavg + i * dat[i, j]
            yavg = yavg + j * dat[i, j]
    
    x = xavg / max(sum(dat.flatten()), 1) + 0.5
    y = yavg / max(sum(dat.flatten()), 1) + 0.5
    
    h, w = b.hw()
    # Check if the initial condition determined in such a way is erroneous; if so, use the alternative method
    # and select x, y to be at the center of the pixel with maximum entry 
    [i0, i1] = np.unravel_index(dat.argmax(), dat.shape)
    if(x < 0 or x > h or y < 0 or y > w):
        x = i0 + 0.5
        y = i1 + 0.5
    
    # sx and sy are required to be bounded between smin and smax
    s_x = min(max(0.2 + 0.2 * (dat[i0 + 1, i1] + dat[i0 - 1, i1]) / dat[i0, i1], s_min), s_max)
    s_y = min(max(0.2 + 0.2 * (dat[i0, i1 + 1] + dat[i0, i1 - 1]) / dat[i0, i1], s_min), s_max)
    
    # Generate initial A
    A = 22 + np.random.uniform() * 3
    
    # Generate the photon event
    spe = photon_event(y, x, s_x, s_y, w, h, A)
    if(output != 'None'):
        print('Initial guesses of the parameters are: \n x=%f, y=%f, sx=%f, sy=%f, A=%f' %(x, y, s_x, s_y, A))
        print('with a distribution matrix of:')
        print(spe.dist_matrix.astype(int))
    # Generate the list of parameters and steps
    para_ls = [[x, y, s_x, s_y, A]]
    
    # Create an array to store the errors of each step
    err_array = []
    
    if(output != 'None'):
        print('-----------Iteration starts-------------')
        
    for i in range(max_iter):
        
        # Use descent to obtain the new parameters and the current error, and add the latter to err_array
        new_param_ls, err = descent([spe], step_ls, dat)
        err_array.append(err)
        
        # Alter the photon event
        spe.new_value(new_param_ls[0])
        para_ls[0] = spe.params()
        
        if(output != 'None' and i%10 == 0):
            # Print the parameters every 10 iterations
            print('Iteration #%d: x=%f, y=%f, sx=%f, sy=%f, A=%f' %
                  (i + 1, para_ls[0][0], para_ls[0][1], para_ls[0][2], para_ls[0][3], para_ls[0][4]))
            print('Current error:%f' % err)
        
        # Check if convergence is reached
        if(i >= iter_diff and err_array[i - iter_diff] - err <= err * conv_crit):
            if(output != 'None'):
                print('Convergence reached at iteration #%d: x=%f, y=%f, sx=%f, sy=%f, A=%f' %
                  (i + 1, para_ls[0][0], para_ls[0][1], para_ls[0][2], para_ls[0][3], para_ls[0][4]))
                print('Current error:%f' % err)
                print('-----------Iteration ends-------------')
                print('Final distribution matrix:')
                print(spe.dist_matrix.astype(int))
            break

    # Postprocessing: check if we've mistaken an MPE as an SPE
    flag = 0 
    if(b.hw() == [4,4] and err > err_max):
        flag = 1
    
    x, y, s_x, s_y, A = para_ls[0]   
    return [x, y, s_x, s_y, A, flag]

def gradient_descent_multi(b, image_data, output = 'None'):
    
    # Input: a box classified as MPE, and the image in which it lives
    # Output: the five parameters of the photon, and a boolean flag checking if we have mistaken an MPE as an SPE.
    
    # The 'output' parameter determines whether the function prints some information for 
    # debugging or demonstration purposes.
    
    # Generate the box data
    xmin, ymin, xmax, ymax = b.params()
    xmax = xmax + 1
    ymax = ymax + 1
    dat = np.array(image_data[xmin:xmax, ymin:ymax])
        
    # Generate output, if needed
    if(output != 'None'):
        print('Box data:')
        print(dat)
        
    # ------------Phase 1: initial guess of photon numbers and parameters, gradient descent #1--------------
    
    # Initialise the photon number, the positions of photons and the intensities
    photon_n = 0
    x = np.array([])
    y = np.array([])
    sx = np.array([])
    sy = np.array([])
    A = np.array([])
    pe_array = []
    
    h, w = b.hw()
    for i in range(w):
        for j in range(h):
            if(dat[i, j] >= thres):
                if(i == 0 or i == w - 1 or j == 0 or j == h - 1):
                    # Check if, erroneously, there is a pixel >=30 at the boundary of the box (due to errors in the boxing process);
                    # if so, set this to 0
                    dat[i, j] = 0
                elif(dat[i, j] >= 
                     max(dat[i + 1, j] - 1, #The -1 here and below is to prevent double counting if there exists two equal maxima
                         dat[i - 1 ,j],
                         dat[i, j + 1] - 1,
                         dat[i, j - 1],
                         dat[i + 1, j + 1] - 1,
                         dat[i + 1, j - 1] - 1,
                         dat[i - 1, j - 1],
                         dat[i - 1, j + 1])):
                    photon_n = photon_n + 1
                    x = np.append(x, i + 0.5)
                    y = np.append(y, j + 0.5)
                    sx = np.append(sx, 0.4)
                    sy = np.append(sy, 0.4)
                    A_init = 22 + np.random.uniform() * 3
                    A = np.append(A, A_init)
                    
                    pe = photon_event(j + 0.5, i + 0.5, 0.4, 0.4, w, h, A_init)
                    pe_array.append(pe)
                    
                    # Generate output, if needed
                    if(output != 'None'):
                        print('Photon created at x=%g, y=%g' % (pe.x0, pe.y0))
    
    if(output != 'None'):
        print('%d photon(s) initialised.' % photon_n)
        print('----------Initial iteration starts----------')
        
    para_ls = np.transpose([x, y, sx, sy, A])
    err_array = []
    
    for i in range(max_iter):
        
        # Use descent to obtain the new parameters and the current error, and add the latter to err_array
        new_param_ls, err = descent(pe_array, step_ls, dat)
        err_array.append(err)

        # Change the parameters of the photons
        for n in range(photon_n):
            pe_array[n].new_value(new_param_ls[n])
            para_ls[n] = new_param_ls[n]
            if(output != 'None' and i%10 == 0):
                # Print the parameters every 10 iterations
                print('Iteration #%d: photon no. %d has x=%f, y=%f, sx=%f, sy=%f, A=%f' %
                    (i + 1, n + 1, para_ls[n][0], para_ls[n][1], para_ls[n][2], para_ls[n][3], para_ls[n][4]))
            
        # Check if convergence is reached
        if(i >= iter_diff and err_array[i - iter_diff] - err <= err * conv_crit):
            if(output != 'None'):
                print('Convergence reached at iteration #%d:' % (i + 1))
                for m in range (photon_n):
                    print('Photon no. %d has x=%f, y=%f, sx=%f, sy=%f, A=%f' %
                      (m + 1, para_ls[m][0], para_ls[m][1], para_ls[m][2], para_ls[m][3], para_ls[m][4]))
                    print('Distribution matrix of this photon:')
                    print(pe_array[m].dist_matrix.astype(int))
                print('Current error:%f' % err)
                print('-----------Initial iteration ends-------------')
            break
    
    x, y, sx, sy, A = np.transpose(para_ls)
    
    # ------------Phase 2: attempt to add more photon within the box to further reduce error-------------
    
    for num in range(photon_n, max_photon):
        
        # Store the current values
        err_tmp = error(pe_array, dat) 
        x_tmp ,y_tmp, sx_tmp, sy_tmp, A_tmp = np.transpose(para_ls)
        
        # Calculate the residual distribution 
        dat_res = deepcopy(dat)
        for pe in pe_array:
            dat_res = dat_res - pe.dist_matrix.astype(int)
        
        if(output != 'None'):
            print('The current residual distribution:')
            print(dat_res)
        
        # From the residual matrix, check if another photon can be added
        dat_sorted = sorted(dat_res.flatten())
        if((dat_sorted[-1] < thres and dat_sorted[-2] < thres - 10)):
            if(num >= 2): # Another photon must be added if only one photon exists at this stage.
                if(output != 'None'):
                    print('No more photons to be added. Gradient descent ends.')
                break
                
        # Add one photon at the maximum entry of dat_res
        x_new, y_new = np.unravel_index(dat_res.argmax(), dat_res.shape)
        if(output != 'None'):
            print('One more photon added at x=%g, y=%g; there are currently %d photons in total.' %(x_new + 0.5, y_new + 0.5, num + 1))
        x = np.append(x, x_new + 0.5)
        y = np.append(y, y_new + 0.5)
        
        # Reset all other parameters
        sx = np.zeros(num + 1) + 0.4
        sy = np.zeros(num + 1) + 0.4
        A = np.random.uniform(size = num + 1) * 3 + 22
        para_ls = np.transpose([x, y, sx, sy, A])
        
        # Reset all photon events
        pe_array = []
        for i in range(num+1):
            pe_array.append(photon_event(y[i], x[i], sx[i], sy[i], w, h, A[i]))
        
        err_array = []
        if(output != 'None'):
            print('----------Iteration #%d starts----------' % (num + 1))
        for i in range(max_iter):

            # Use descent to obtain the new parameters and the current error, and add the latter to err_array
            new_param_ls, err = descent(pe_array, step_ls, dat)
            err_array.append(err)

            # Change the parameters of the photons
            for n in range(num + 1):
                # Alter each parameter using the descent function
                # A loop is not used here for efficiency
                pe_array[n].new_value(new_param_ls[n])
                para_ls[n] = new_param_ls[n]
            # Check if convergence is reached
            if(i >= iter_diff and err_array[i - iter_diff] - err <= err * conv_crit):
                if(output != 'None'):
                    print('Convergence reached at iteration #%d:' % (i + 1))
                    for m in range (num + 1):
                        print('Photon no. %d has x=%f, y=%f, sx=%f, sy=%f, A=%f' %
                          (m + 1, para_ls[m][0], para_ls[m][1], para_ls[m][2], para_ls[m][3], para_ls[m][4]))
                        print('Distribution matrix of this photon:')
                        print(pe_array[m].dist_matrix.astype(int))
                    print('Current error:%f' % err)
                    print('-----------Iteration #%d ends-------------' % (num + 1))
                break
                
        # Compare the error: if adding a photon does not reduce the error, select the old arrangements and break
        if(err >= err_tmp - 5):
            err = err_tmp
            x = x_tmp
            y = y_tmp
            sx = sx_tmp
            sy = sy_tmp
            A = A_tmp
            if(output != 'None'):
                print('Adding this photon however did not reduce error. Returning to the older configuration with %d photons. Gradient descent ends.' 
                      % num)
            break
            
        x, y, sx, sy, A = np.transpose(para_ls)
    
    return [x, y, A, err]

# Establish a class to store the results:
class photon_event_result:
    'The result of photon event processed. This includes the coordinates and intensity of the event, as well as its classification.'

    def __init__(self, event_type, x, y, A):
        self.x = x
        self.y = y
        self.A = A
        self.type = event_type # event_type is 's' for SPEs and 'm' for MPEs

def single_photon_counting(im_array):
    
    # Input: an array of normalised image to be processed
    # Output: an array of photon_event_result objects, containing the photons identified.
    
    # an index to count the number of images
    image_no = 0
    
    photon_n = 0 # No. of photons found
    s_n = 0 # No. of single photons found
    m_n = 0 # No. of photons in MPEs found
    
    # Start timing
    start = time.time()
    
    #Initialize the photon event result object list
    per_list = []
    
    for im in im_array:
        image_no = image_no + 1
        print('\r', 'Processing image #%d' % image_no, end = '', flush = True)
        
        # Find the list of boxes in this image
        box_list = boxing(thresholding(im, thres))
        box_count = 0
        box_photon_count = 0

        for b in box_list:
            box_count = box_count + 1
            
            # Display some information
            end = time.time()
            #clear()
            print('\r','Image %d / %d, box %d / %d; # of photons in this image: %d; Total time elapsed: %.1f sec.' 
            % (image_no, len(im_array), box_count, len(box_list), box_photon_count, end - start), end = '', flush = True)
            #print('Processing image %d / %d' % (image_no, len(im_array)))
            #print('Processing box %d / %d' % (box_count, len(box_list)))
            #print('%d SPEs found; %d MPEs found; total number of photons: %d' % (s_n, m_n, photon_n))
            #print('Time elapsed: %d seconds' % (end - start))

            if(b.hw()[0] <= 4 and b.hw()[1] <= 4): # Single photon events
                
                spe_event = gradient_descent_single(b, im)
                x, y, sx, sy, A, flag = spe_event
                
                if(flag == 0): # SPE confirmed
                    # Transform the x and y coordinates to that of the image
                    x = x + b.x_min - 0.5
                    y = y + b.y_min - 0.5
                    
                    per = photon_event_result('s', x, y, A)
                    per_list.append(per)
                    
                    photon_n = photon_n + 1
                    box_photon_count = box_photon_count + 1
                    s_n = s_n + 1
                    
                    continue
            
            #MPE confirmed
            mpe_event = gradient_descent_multi(b, im)
            
            for n in range(len(mpe_event[0])): # Iterate all photons found
                # Transform the x and y coordinates to that of the image
                x = mpe_event[0][n] + b.x_min - 0.5
                y = mpe_event[1][n] + b.y_min - 0.5
                A = mpe_event[2][n]
                
                per = photon_event_result('m', x, y, A)
                per_list.append(per)
                    
                photon_n = photon_n + 1
                box_photon_count = box_photon_count + 1
                m_n = m_n + 1 
    
        # Display some information
        print(" Image Done.")

        #clear()
        #print('Finished processing image #%d' % image_no)
        #print('%d SPEs found; %d MPEs found; total number of photons: %d' % (s_n, m_n, photon_n))
        #end = time.time()
        #print('Time elapsed: %d seconds' % (end - start))

    #clear()
    print('Single photon counting finished.')
    print('%d SPEs found; %d MPEs found; total number of photons: %d' % (s_n, m_n, photon_n))
    print('Time elapsed: %f seconds' % (end - start))
    return per_list    

def write_in_csv(spc_result, name):
    with open(name, 'w', newline = '') as file:
        writer = csv.writer(file)
        for per in spc_result:
            x = per.x
            y = per.y
            A = per.A
            t = per.type
            writer.writerow([x, y, A, t])
    print('Photon data saved to %s' % name)

def read_from_csv(file_loc):
    with open(file_loc, mode = 'r') as file:
        csvFile = csv.reader(file)
        spc_result = []
        for lines in csvFile:
            x, y, A, t = lines
            spc_result.append(photon_event_result(t, float(x), float(y), float(A)))
    print("Successfully read %d lines of data from the file" % len(spc_result))
    return spc_result