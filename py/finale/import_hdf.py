from tables import *

def import_images(f_name="D:\\Oxford 2019-2023\\22-1HT\\B8\\py\\sxro6416-r0504.h5"):

    # Name of the hdf file that contain the data we need
    # Open the hdf5 file, use the path to the images to extrate the data and place
    # it in the image data object for further manipulation and inspection.
    datafile = h5py.File(f_name, 'r')
    image_data = []
    for i in itertools.count(start=0):
        d = datafile.get(f'Configure:0000/Run:0000/CalibCycle:{i:04d}/Princeton::FrameV2/SxrEndstation.0:Princeton.0/data')
        if d is not None:
            # actual image is at first index
            image_data.append(d[0])
        else:
            break

    #print(image_data[1])
    # Tell me how many images were contained in the datafile
    print(f"loaded {len(image_data)} images")

    return image_data

    #for i in range(20):
        #plt.imshow(image_data[i])
        #plt.savefig('image'+str(i)+'.png',dpi=1000)
        #image = Image.fromarray(image_data[i]).convert("L")
        #image.save("image"+str(i)+".png")

    # Plot a good dataset - here index 8 (but there are others too!)
    #misc.imshow(image_data[0])
    #misc.show()

    #image = Image.fromarray(image_data[0]).convert("L")
    #image.save("out.png")

    # The histogram of the data will help show possible single photon hits

if __name__=="__main__":
    import_images("D:\\Oxford 2019-2023\\22-1HT\\B8\\py\\sxro6416-r0504.h5")