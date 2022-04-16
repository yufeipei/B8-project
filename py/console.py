from run_bragg import *

def run():
    _plot_bin = 400
    _min_e = 1100
    _max_e = 1600
    _plot_loc = "1.png"
    _save_csv_loc = "data.csv"
    h = 12
    w = 12
    plt.rcParams["figure.figsize"]=[w, h];    
    #print("This is a console by Yufei Pei.")
    print(
"""
*************************************************************************************************
* This is a program for the B8 project "X-ray Single-Photon Energy-Dispersive Spectroscopy".    *
* Author: Yufei Pei                            Supervisor: Sam Vinko                            *
*                                                                                               *
* The program takes in an array of images collected from the CCD camera used in the experiment, *
* and processes it using the algorithms of single photon counting and Bragg's spectroscopy.     *
*                                                                                               *
* In the end, a spectrum of emission intensity vs. photon energy will be generated and saved.   *
* This process, if start from scratch, is expected to take 1-2 hours.                           *
*                                                                                               *
* Before first time of running, please first check the parameter settings to make sure that     *
* they are what you desired.                                                                    *
*************************************************************************************************""")
    while(True):

        s = input("""
1: Start from scratch with a .h5 file. The program will save the single photon counting result 
   in a .csv file.
2: Start from a single-photon counting data generated in (1), in .csv format
3: Parameter settings
Any other input: Quit
Your input: """)

        if(s == '1'):
            file_loc = input("Please input path of file here: ")
            energies_input = input("Please input the energy(s) of the spectral lines, from small to large, separated by space: ")
            _spec_energies = [float(n) for n in energies_input.split()]
            spc_result = spc_running(file_loc, csv_loc = _save_csv_loc)
            bragg_running(spc_result, plot_bin = _plot_bin, spec_energies = _spec_energies, min_e = _min_e, max_e = _max_e, plot_loc = _plot_loc)
        elif(s == '2'):
            csv_loc = input("Please input path of the csv file here: ")
            energies_input = input("Please input the energy(s) of the spectral lines, from small to large, separated by space: ")
            _spec_energies = [float(n) for n in energies_input.split()]
            spc_result = read_from_csv(csv_loc)
            bragg_running(spc_result, plot_bin = _plot_bin, spec_energies = _spec_energies, min_e = _min_e, max_e = _max_e, plot_loc = _plot_loc)
        elif(s == '3'):
            print('''
The parameters used are as follow:
1. # of energy bins in the plot: %d
2. minimum energy in the plot: %d eV
3. maximum energy in the plot: %d eV
4. name of the plot file: %s
5. name of the csv file used to save spc data: %s
6. height and width of the final plot: %din * %din
''' % (_plot_bin, _min_e, _max_e, _plot_loc, _save_csv_loc, h, w))
            
            while(True):
                print("Please input the number of the parameter you would like to change")
                par = input("Any other input = return to main menu: ")
                if(par == '1'):
                    _plot_bin = input("New value: ")
                elif(par == '2'):
                    _min_e = input("New value: ")
                elif(par == '3'):
                    _max_e = input("New value: ")
                elif(par == '4'):
                    _plot_loc = input("New path: ")
                elif(par == '5'):
                    _save_csv_loc = input("New path: ")
                elif(par == '6'):
                    h = int(input("New height: "))
                    w = int(input("New width: "))
                    plt.rcParams["figure.figsize"]=[w, h];    
                else:
                    break
                other = input("Do you want to change other parametes?(y/n); ")
                if(other != 'y'):
                    break
        else:
            break

if __name__ == "__main__":
    run()