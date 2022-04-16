from bragg_spec import *

def bragg_running(spc_result, _bins = 400, plot_bin = 400, spec_energies = [1188, 1218.5], min_e = 1100, max_e = 1600, plot_loc = "1.png"):

    spec_n = len(spec_energies)

    theta_ls = [np.arcsin(fit_n * 12398.4 / (energy * fit_2d)) for energy in spec_energies]

    x_list, y_list, A_list = event_filtering(spc_result, _bins)

    point_ls = point_finding(x_list, y_list, spec_n)

    params = geometry(point_ls, theta_ls)

    generate_plot(x_list, y_list, A_list, plot_bin,  params, plot_loc, spec_energies, theta_ls, max_e, min_e)

    print('Done and done.')

    time.sleep(1)
    print("---------------------------------------------")
    return 0

if __name__ == '__main__':
    plt.rcParams["figure.figsize"]=[12, 12];
    spc_result = read_from_csv("data1.csv")
    bragg_running(spc_result)

