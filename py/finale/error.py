from gaussian import *
from tag import *

def error(event,dat_tag,input_dat):
    matrix=np.array(input_dat[(dat_tag.param()[0]):(dat_tag.param()[2]+1),(dat_tag.param()[1]):(dat_tag.param()[3]+1)])
    
    return sum(((matrix-np.array(event.intensity_matrix))**2).flatten())

def error_multi(spe__array,dat_tag,input_dat):
    matrix=np.array(input_dat[(dat_tag.param()[0]):(dat_tag.param()[2]+1),(dat_tag.param()[1]):(dat_tag.param()[3]+1)])
    
    tot_intensity_matrix=sum([event.intensity_matrix for event in spe__array])
    return sum(((matrix-tot_intensity_matrix)**2).flatten())

