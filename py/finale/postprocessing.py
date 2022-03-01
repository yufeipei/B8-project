from run import single_photon_event_result
import matplotlib.pyplot as plt

def event_generation(spe_result):
    x_list=[]
    y_list=[]
    A_list=[]
    As_list=[]
    Am_list=[]
    for sper in spe_result:
        x_list.append(sper.x)
        y_list.append(sper.y)
        A_list.append(sper.A)
        if(sper.type=='s'):
            As_list.append(sper.A)
        elif(sper.type=='m' and sper.A>0):
            Am_list.append(sper.A)
    
    return [x_list,y_list,A_list,As_list,Am_list]

