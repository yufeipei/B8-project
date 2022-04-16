# NB: This part of the code is provided by the supervisor at the beginning of the project.
from imports import *

def import_images(f_name = "sxro6416-r0504.h5"):
    
    # Name of the hdf file that contain the data we need
    # Open the hdf5 file, use the path to the images to extrate the data and place
    # it in the image data object for further manipulation and inspection.
    datafile = h5py.File(f_name, 'r')

    print('\r', 'Loading Images...', end = '', flush = True)

    image_data = []
    for i in itertools.count(start=0):
        d = datafile.get(f'Configure:0000/Run:0000/CalibCycle:{i:04d}/Princeton::FrameV2/SxrEndstation.0:Princeton.0/data')
        if d is not None:
            # actual image is at first index
            image_data.append(d[0])
        else:
            break

    # Tell me how many images were contained in the datafile
    print('\r', f"Loaded {len(image_data)} images", flush = True)
    return image_data

if __name__=="__main__":
    import_images("D:\\Oxford 2019-2023\\22-1HT\\B8\\py\\sxro6416-r0504.h5")