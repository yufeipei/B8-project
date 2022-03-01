from error import *
from gaussian import *

def gradient_descent_single(dat_tag,input_dat,output='verbose',avg_mu=40000/1024/1026):
    

    
    l=dat_tag.param()[0]
    r=dat_tag.param()[2]+1
    t=dat_tag.param()[1]
    b=dat_tag.param()[3]+1
    dat=input_dat[l:r,t:b]

    
    h=dat_tag.hw()[0]
    w=dat_tag.hw()[1]
    #return dat
    #print(dat)
    size=h*w
    [i0,i1]=np.unravel_index(dat.argmax(),dat.shape)
    
    #return index
    xavg=0
    yavg=0
    for i in range(dat.shape[0]):
        for j in range(dat.shape[1]):
            xavg=xavg+i*dat[i,j]
            yavg=yavg+j*dat[i,j]
    
    x=np.abs(xavg/sum(dat.flatten()))+0.5
    y=np.abs(yavg/sum(dat.flatten()))+0.5
    
    if(x>h-1 or y>w-1):
        x, y=np.unravel_index(dat.argmax(), dat.shape)+np.array([0.5,0.5])

    #x=l+i0+0.5
    #y=t+i1+0.5
    
    if(output=='verbose'):
        print(x,y)    
    
    if(output is not 'nothing'):
        print(dat)
    
    #s_x=random.uniform(smin,smax)
    #s_y=random.uniform(smin,smax)
    #A=random.uniform(Amin,Amax)
    
    s_x=max(0.25+0.25*(dat[i0+1,i1]+dat[i0-1,i1])/dat[i0,i1],0.2)
    s_y=max(0.25+0.25*(dat[i0,i1+1]+dat[i0,i1-1])/dat[i0,i1],0.2)
    
    #s_x=0.4
    #s_y=0.4
    #A=dat.max()
    A=20
    
    null_event=gaussian_spe(y,x,s_x,s_y,h,w,0)
    null_err=error(null_event,dat_tag,input_dat)
    
    spe=gaussian_spe(y,x,s_x,s_y,h,w,A)

    #print(l,r,t,b)
    if(output=='verbose'):
        print(spe.intensity_matrix.astype(int))
    
    err_array=[]
    #print(err)
    
    step_xy=0.01
    step_s=0.005
    step_A=0.3
    descent_factor=0.2
    
    #print([x,y,s_x,s_y,A])
    
    for i in range(400):
        err=error(spe,dat_tag,input_dat)
        spe.new_value(y,x+step_xy,s_x,s_y,A)
        p_x=error(spe,dat_tag,input_dat)-err
        
        spe.new_value(y+step_xy,x,s_x,s_y,A)
        p_y=error(spe,dat_tag,input_dat)-err
        
        spe.new_value(y,x,s_x+step_s,s_y,A)
        p_sx=error(spe,dat_tag,input_dat)-err
        
        spe.new_value(y,x,s_x,s_y+step_s,A)
        p_sy=error(spe,dat_tag,input_dat)-err
        
        spe.new_value(y,x,s_x,s_y,A+step_A)
        p_A=error(spe,dat_tag,input_dat)-err
                
        x=x-p_x*descent_factor*step_xy
        y=y-p_y*descent_factor*step_xy
        s_x=s_x-p_sx*descent_factor*step_s
        s_y=s_y-p_sy*descent_factor*step_s
        A=A-p_A*descent_factor*step_A
        
        if(s_x<smin):
            s_x=smin
        if(s_y<smin):
            s_y=smin
        
        spe.new_value(y,x,s_x,s_y,A)
        
        err_array.append(err)
        
        if(i>=11 and np.abs(err-err_array[i-11])<=err/40):
            if(output is not 'nothing'):
                print('convergence achieved at step ',i)
            if(output=='verbose'):
                print(err,err_array[i-11])
            break
        
        
        if(i%5==0 and output=='verbose'):
            print([x,y,s_x,s_y,A])
        #if(err<=200):
            #print('target reached')
            #break
    
    flag=0

    """
    p_null=chi2.pdf(null_err/100,df=size)*poisson.pmf(k=0, mu=avg_mu)
    p_new=chi2.pdf(err/100,df=size)*poisson.pmf(k=1,mu=avg_mu)
    if(p_new<p_null or A<0):
        flag=1
    """
    
    
    if(output=='verbose'):
        plt.plot(err_array)

    if(output is not 'nothing'):
        print(spe.intensity_matrix.astype(int))
        print(x,y,s_x,s_y,A,flag)
        
    print(err)
    if(dat_tag.hw()==[3,3] and err>1600):
        flag=2
    return [x,y,s_x,s_y,A,flag]



if __name__ == "__main__":
    print('hello  world!')