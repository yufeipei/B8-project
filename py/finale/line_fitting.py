
from tables import *
from hyperparams import *

def spe_read_csv(file_loc):
    with open(file_loc, mode='r') as file:
        csvFile = csv.reader(file)
        x_list=[]
        y_list=[]
        A_list=[]   
        # displaying the contents of the CSV file
        for lines in csvFile:
            x_list.append(float(lines[0]))
            y_list.append(float(lines[1]))
            A_list.append(float(lines[2]))

    return [x_list,y_list,A_list]

def moving_avg(half_width,input_dat):
    start_index=0
    end_index=0
    avg_dat=np.zeros(2048-half_width)
    for i in input_dat:
        ycoor=i[1]

        start=max(0,int(ycoor)-half_width+1)
        end=min(2048-half_width,int(ycoor)+half_width)

        avg_dat[start:end]=avg_dat[start:end]+i[2]
    return avg_dat

def cutting(cut_num,x_list,y_list,A_list):
    data=np.transpose([x_list,y_list,A_list])
    data=data[data[:,0].argsort()]
    x_list,y_list,A_list=np.transpose(data)

    cut_thick=int(2048/cut_num)
    index=0
    l=len(x_list)
    dot=[]
    cut_point=[0]
    for n in range(cut_num):
        for i in range(index,l):
            if(x_list[i]>(n+1)*cut_thick):
                index=i
                cut_point.append(index)
                break
        dat=np.transpose([x_list[cut_point[-2]:cut_point[-1]],y_list[cut_point[-2]:cut_point[-1]],A_list[cut_point[-2]:cut_point[-1]]])
        dat = dat[dat[:,1].argsort()]
        ls=moving_avg(25,dat)[::-1]
        #dot.append([int(n*cut_thick+cut_thick/2),np.argmax(ls)])
        for i in range(len(ls)):
            if(ls[i]-ls[i-50]>160000/cut_num):
                dot.append([int(n*cut_thick+cut_thick/2),2048-25-i])
                break
    return np.transpose(dot)


class fitting:
    'used to get the spectrum.'
    
    def __init__(self,a,b,c,d,x0,y0):
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.x0=x0
        self.y0=y0
        
    def new_value(self,a,b,c,d,x0,y0):
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.x0=x0
        self.y0=y0
        
    def conic_section(self,x,y):
        return self.a*(x-self.x0)**2+self.b*(y-self.y0)**2+2*self.c*x*y-self.d
    
    """
    def error(self):
        count=0
        for i in range(len(x_list)):
            x=x_list[i]
            y=y_list[i]
            if(np.abs(self.conic_section(x,y))<err_range):
                count=count+A_list[i]
                
        return 0-count
    """
    
    def error(self, point_list):
        err=0
        for point in point_list:
            err=err+self.conic_section(point[0],point[1])**2
        return err
    
    
    def plot(self):
        x=range(2048)
        y=range(2048)
        z=np.zeros([2048,2048])
        for i in x:
            for j in y:
                if(np.abs(self.conic_section(i,j))>err_range):
                    z[i,j]=1
                else:
                    z[i,j]=0
        
        plt.contourf(x,y,z,cmap=plt.get_cmap('hot'))
        plt.colorbar()


trial=fitting(1.,1,0,57000000,900,9000) 


def gradient_descent_fitting(cut,ft=trial,output='verbose'):
    points=np.transpose(cut)
    for i in range(100):

        a=ft.a
        b=ft.b
        c=ft.c
        d=ft.d
        x0=ft.x0
        y0=ft.y0
        if(output=='verbose'):
            print('para',[a,b,c,d,x0,y0])
        err=ft.error(points)
        if(output=='verbose'):
            print(err)
        ft.new_value(a+ft_d_a,b,c,d,x0,y0)
        err_a=ft.error(points)-err
        ft.new_value(a,b+ft_d_b,c,d,x0,y0)
        err_b=ft.error(points)-err
        ft.new_value(a,b,c+ft_d_c,d,x0,y0)
        err_c=ft.error(points)-err
        ft.new_value(a,b,c,d+ft_d_d,x0,y0)
        err_d=ft.error(points)-err
        ft.new_value(a,b,c,d,x0+ft_d_x0,y0)
        err_x0=ft.error(points)-err
        ft.new_value(a,b,c,d,x0,y0+ft_d_y0)
        err_y0=ft.error(points)-err
        
        if(output=='verbose'):
            print('err',[err_a,err_b,err_c,err_d,err_x0,err_y0])
        
        a=a-err_a*ft_descent_factor*ft_d_a
        b=b-err_b*ft_descent_factor*ft_d_b
        c=c-err_c*ft_descent_factor*ft_d_c
        d=d-err_d*ft_descent_factor*ft_d_d
        x0=x0-err_x0*ft_descent_factor*ft_d_x0
        y0=y0-err_y0*ft_descent_factor*ft_d_y0
        
        ft.new_value(a,b,c,d,x0,y0)
    
    print(a,b,c,d,x0,y0,err)
    return ft

def energy(value):

    energy=value

    return energy

def generate_plot(ft, x_list, y_list, A_list, bins):
    
    energies=[]
    for i in range(len(x_list)):
        if(energy(ft.conic_section(x_list[i],y_list[i]))!=np.inf):
            energies.append(energy(ft.conic_section(x_list[i],y_list[i])))
    
    min_e=min(energies)
    max_e=max(energies)

    print(min_e,max_e)

    energy_plot=np.zeros(bins+1)

    denom=1/(max_e-min_e)

    for i in range(len(energies)):
        e=energies[i]
        if(not (e<1000000000)):
            print('no')
            continue
        energy_plot[int((e-min_e)*denom*bins)]=energy_plot[int((e-min_e)*denom*bins)]+A_list[i]

    plt.semilogy()
    plt.plot(energy_plot)
    
    return energy_plot