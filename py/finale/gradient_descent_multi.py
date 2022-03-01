from error import *
from gaussian import *


def gradient_descent_multi(dat_tag,photon_n,input_dat,output='verbose'):
    l=dat_tag.param()[0]
    r=dat_tag.param()[2]+1
    t=dat_tag.param()[1]
    b=dat_tag.param()[3]+1
    dat=input_dat[l:r,t:b]
    #return dat
    
    h=dat_tag.hw()[0]
    w=dat_tag.hw()[1]
    
    if(output=='verbose'):
        print(dat)
    #[i0,i1]=np.unravel_index(dat.argmax(),dat.shape)
    
    x_init=np.zeros(photon_n)
    y_init=np.zeros(photon_n)
    s_x=np.zeros(photon_n)
    s_y=np.zeros(photon_n)
    A=np.zeros(photon_n)
    
    dat_tmp=deepcopy(dat)
    spe_array=[]
    
    for n in range(photon_n):
        tmp=0
        x=0
        y=0
        for i in range(dat.shape[0]):
            for j in range(dat.shape[1]):
                if(dat_tmp[i,j]>tmp):
                    tmp=dat[i,j]
                    x=i
                    y=j
                    
        x_init[n]=x+0.5
        y_init[n]=y+0.5
        
        #s_x[n]=0.25+0.25*(input_dat[x+l+1,y+t]+input_dat[x+l-1,y+t]+input_dat[x+l+1,y+t+1]+input_dat[x+l-1,y+t+1]+input_dat[x+l+1,y+t-1]+input_dat[x+l-1,y+t-1])/(input_dat[x+l,y+t+1]+input_dat[x+l,y+t-1]+input_dat[x+l,y+t])
        #s_y[n]=0.25+0.25*(input_dat[x+l,y+t+1]+input_dat[x+l,y+t-1]+input_dat[x+l+1,y+t+1]+input_dat[x+l-1,y+t+1]+input_dat[x+l+1,y+t-1]+input_dat[x+l-1,y+t-1])/(input_dat[x+l-1,y+t]+input_dat[x+l+1,y+t]+input_dat[x+l,y+t])
        
        if(x < dat.shape[0]-1):
            s_x[n]=0.25+0.25*(dat[x+1,y]+dat[x-1,y])/dat[x,y]
        else:
            s_x[n]=0.25+0.25*(dat[x-1,y])/dat[x,y]
            
        if(y < dat.shape[1]-1):
            s_y[n]=0.25+0.25*(dat[x,y+1]+dat[x,y-1])/dat[x,y]
        else:
            s_y[n]=0.25+0.25*dat[x,y-1]/dat[x,y]
    
        #s_x[n]=0.4
        #s_y[n]=0.4
        
        A[n]=20        
        
        spe=gaussian_spe(y_init[n],x_init[n],s_x[n],s_y[n],h,w,A[n])
        spe_array.append(spe)
        dat_tmp[x,y]=0
        #print(dat_tmp)
        if(output=='verbose'):
            print([x,y,s_x[n],s_y[n],A[n]])
            print(spe.intensity_matrix.astype(int))
        
    if(output is not 'nothing'):
        print(x_init,y_init)
    #print(spe_array)
    
    #print(err)
    
    step_xy=0.01
    step_s=0.005
    step_A=0.3
    descent_factor=0.1
    
    err_array=[]
    
    #print([x,y,s_x,s_y,A])
    
    #s_x[1]=0.5
    
    p_x=np.zeros(photon_n)
    p_y=np.zeros(photon_n)
    p_sx=np.zeros(photon_n)
    p_sy=np.zeros(photon_n)
    p_A=np.zeros(photon_n)
        
    for i in range(400):
        err=error_multi(spe_array,dat_tag,input_dat)
        
        for n in range(photon_n):
            spe_array[n].new_value(y_init[n]+step_xy,x_init[n],s_x[n],s_y[n],A[n])
            p_y[n]=error_multi(spe_array,dat_tag,input_dat)-err
            spe_array[n].new_value(y_init[n],x_init[n]+step_xy,s_x[n],s_y[n],A[n])
            p_x[n]=error_multi(spe_array,dat_tag,input_dat)-err
            """
            spe_array[n].new_value(y_init[n],x_init[n],s_x[n]+step_s,s_y[n],A[n])
            p_sx[n]=error_multi(spe_array,dat_tag,input_dat)-err
            spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n]+step_s,A[n])
            p_sy[n]=error_multi(spe_array,dat_tag,input_dat)-err
            """
            if(s_x[n]<0.6):
                spe_array[n].new_value(y_init[n],x_init[n],s_x[n]+step_s,s_y[n],A[n])
                p_sx[n]=error_multi(spe_array,dat_tag,input_dat)-err
            else:
                p_sx[n]=0
                    
            if(s_y[n]<0.6):
                spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n]+step_s,A[n])
                p_sy[n]=error_multi(spe_array,dat_tag,input_dat)-err
            else:
                p_sy[n]=0
            spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n],A[n]+step_A)
            p_A[n]=error_multi(spe_array,dat_tag,input_dat)-err
        
        x_init=x_init-p_x*descent_factor*step_xy
        y_init=y_init-p_y*descent_factor*step_xy
        s_x=s_x-p_sx*descent_factor*step_s
        s_y=s_y-p_sy*descent_factor*step_s
        A=A-p_A*descent_factor*step_A
        
        for n in range(photon_n):
            spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n],A[n])

        err_array.append(err)
        if(output=='verbose'):
            print(y_init,x_init,s_x,s_y,A)
        if(i>=11 and np.abs(err-err_array[i-11])<=err/40):
            #print('convergence achieved in step', i)
            break
            
    if(output=='verbose'):
        plt.plot(err_array)
        print(x_init,y_init,s_x,s_y,A)
        print(err)

    if(output is not 'nothing'):
        for spe in spe_array:
            print(spe.intensity_matrix.astype(int))        
    
    return [x_init,y_init,s_x,s_y,A,err]

def gradient_descent_multi_new(dat_tag,input_dat,output='verbose',threshold=30):
    l=dat_tag.param()[0]
    r=dat_tag.param()[2]+1
    t=dat_tag.param()[1]
    b=dat_tag.param()[3]+1
    dat=input_dat[l:r,t:b]
    #return dat
    
    h=dat_tag.hw()[0]
    w=dat_tag.hw()[1]

    if(output=='verbose'):
        print(dat)
    #[i0,i1]=np.unravel_index(dat.argmax(),dat.shape)
    
    photon_n=0
    x_init=np.array([])
    y_init=np.array([])
    
    spe_array=[]
    
    for i in range(w+1):
        for j in range(h+1):
            if(dat[i,j]>=threshold):
                if(i==0 or i==w or j==0 or j==h):
                    dat[i,j]=0
                elif(dat[i,j]>=max(dat[i+1,j]-1,dat[i-1,j],dat[i,j+1]-1,dat[i,j-1],dat[i+1,j+1]-1,dat[i+1,j-1]-1,dat[i-1,j-1],dat[i-1,j+1])):
                    photon_n=photon_n+1
                    x_init=np.append(x_init,i+0.5)
                    y_init=np.append(y_init,j+0.5)
                    spe=gaussian_spe(j+0.5,i+0.5,0.4,0.4,h,w,20)
                    spe_array.append(spe)
                    if(output=='verbose'):
                        print(i+0.5,j+0.5)
                        print(spe.intensity_matrix.astype(int))
    
    s_x=np.zeros(photon_n)+0.4
    s_y=np.zeros(photon_n)+0.4
    A=np.zeros(photon_n)+20
    
    dat_tmp=deepcopy(dat)
    
    if(output is not 'nothing'):
        print(photon_n)
        
    #print(spe_array)
    
    #print(err)
    
    step_xy=0.01
    step_s=0.005
    step_A=0.3
    descent_factor=0.2
    
    err_array=[]
    
    #print([x,y,s_x,s_y,A])
    
    #s_x[1]=0.5
    
    p_x=np.zeros(photon_n)
    p_y=np.zeros(photon_n)
    p_sx=np.zeros(photon_n)
    p_sy=np.zeros(photon_n)
    p_A=np.zeros(photon_n)
        
    #initial phase

    for i in range(400):
        err=error_multi(spe_array,dat_tag,input_dat)
        
        for n in range(photon_n):
            spe_array[n].new_value(y_init[n]+step_xy,x_init[n],s_x[n],s_y[n],A[n])
            p_y[n]=error_multi(spe_array,dat_tag,input_dat)-err
            spe_array[n].new_value(y_init[n],x_init[n]+step_xy,s_x[n],s_y[n],A[n])
            p_x[n]=error_multi(spe_array,dat_tag,input_dat)-err
            if(s_x[n]<0.6):
                spe_array[n].new_value(y_init[n],x_init[n],s_x[n]+step_s,s_y[n],A[n])
                p_sx[n]=error_multi(spe_array,dat_tag,input_dat)-err
            else:
                p_sx[n]=0
                    
            if(s_y[n]<0.6):
                spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n]+step_s,A[n])
                p_sy[n]=error_multi(spe_array,dat_tag,input_dat)-err
            else:
                p_sy[n]=0
            spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n],A[n]+step_A)
            p_A[n]=error_multi(spe_array,dat_tag,input_dat)-err
        
        x_init=x_init-p_x*descent_factor*step_xy
        y_init=y_init-p_y*descent_factor*step_xy
        s_x=s_x-p_sx*descent_factor*step_s
        s_y=s_y-p_sy*descent_factor*step_s
        A=A-p_A*descent_factor*step_A
        
        for n in range(photon_n):
            spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n],A[n])

        err_array.append(err)
        
        if(i>=11 and np.abs(err-err_array[i-11])<=err/40):
            #print('convergence achieved in step', i)
            break
            
    if(output=='verbose'):
        plt.plot(err_array)
        print(x_init,y_init,s_x,s_y,A)
        print(err)
    if(output is not 'nothing'):
        dat_tmp=deepcopy(dat)
        for spe in spe_array:
            dat_tmp=dat_tmp-spe.intensity_matrix.astype(int)
        print(dat_tmp)
    
    if(output is not 'nothing'):
        for spe in spe_array:
            print(spe.intensity_matrix.astype(int))        
    


    return [x_init,y_init,s_x,s_y,A,err]

def gradient_descent_multi_new2(dat_tag,input_dat,output='verbose',threshold=30,avg_mu=40000/2044/2046):
    l=dat_tag.param()[0]
    r=dat_tag.param()[2]+1
    t=dat_tag.param()[1]
    b=dat_tag.param()[3]+1
    dat=input_dat[l:r,t:b]
    #return dat
    
    h=dat_tag.hw()[0]
    w=dat_tag.hw()[1]
    size=(h+1)*(w+1)
    if(output=='verbose'):
        print(dat)
    #[i0,i1]=np.unravel_index(dat.argmax(),dat.shape)
    
    initial_result=gradient_descent_multi_new(dat_tag,input_dat,'nothing')
    
    initial_photon_n=len(initial_result[0])

    photon_n=20
    
    x_init=np.array(initial_result[0])
    y_init=np.array(initial_result[1])
    s_x=np.array(initial_result[2])
    s_y=np.array(initial_result[3])
    A=np.array(initial_result[4])
    err=initial_result[-1]
    spe_array=[]
    
    for i in range(initial_photon_n):
        spe_array.append(gaussian_spe(initial_result[1][i],initial_result[0][i],initial_result[2][i],initial_result[3][i],h,w,initial_result[4][i]))
    
    
    p_x=np.zeros(initial_photon_n)
    p_y=np.zeros(initial_photon_n)
    p_sx=np.zeros(initial_photon_n)
    p_sy=np.zeros(initial_photon_n)
    p_A=np.zeros(initial_photon_n)
        
    #null_event=gaussian_spe(1,1,1,1,h,w,0)
    #null_err=error(null_event,dat_tag,input_dat)
    
    for num in range(initial_photon_n,photon_n):
        
        step_xy=0.01
        step_s=0.005
        step_A=0.3
        descent_factor=0.1
        
        dat_tmp=deepcopy(dat)
        
        for spe in spe_array:
            dat_tmp=dat_tmp-spe.intensity_matrix.astype(int)
        if(output is not 'nothing'):
            print(dat_tmp)
        
        dat_sorted=sorted(dat_tmp.flatten())
        if((dat_sorted[-1]<threshold and dat_sorted[-2]<threshold-10) or min(A)<=1):
            if(num >= 2):
                break
        
        
        x, y=np.unravel_index(dat_tmp.argmax(), dat_tmp.shape)
        dat_tmp=deepcopy(dat)

        err_array=[]
        
        x_init=np.append(x_init,x+0.5)
        y_init=np.append(y_init,y+0.5)
        s_x=np.zeros(num+1)+0.4
        s_y=np.zeros(num+1)+0.4
        A=np.zeros(num+1)+20
        
        p_x=np.append(p_x,0)
        p_y=np.append(p_y,0)
        p_sx=np.append(p_sx,0)
        p_sy=np.append(p_sy,0)
        p_A=np.append(p_A,0)
        
        if(output is 'verbose'):
            print([x,y])
        
        spe_array=[]
        for n in range(num+1):
            spe_i=gaussian_spe(y_init[n],x_init[n],0.4,0.4,h,w,20)
            spe_array.append(spe_i)
        if(output is 'verbose'):
            for spe_i in spe_array:
                print(spe_i.intensity_matrix.astype(int))
                print('----')
            
        if(output is 'verbose'):
            print(x_init,y_init)
            
        for i in range(400):
            err=error_multi(spe_array,dat_tag,input_dat)
        
            for n in range(num+1):
                spe_array[n].new_value(y_init[n]+step_xy,x_init[n],s_x[n],s_y[n],A[n])
                p_y[n]=error_multi(spe_array,dat_tag,input_dat)-err
                spe_array[n].new_value(y_init[n],x_init[n]+step_xy,s_x[n],s_y[n],A[n])
                p_x[n]=error_multi(spe_array,dat_tag,input_dat)-err
                if(s_x[n]<0.6):
                    spe_array[n].new_value(y_init[n],x_init[n],s_x[n]+step_s,s_y[n],A[n])
                    p_sx[n]=error_multi(spe_array,dat_tag,input_dat)-err
                else:
                    p_sx[n]=0
                    
                if(s_y[n]<0.6):
                    spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n]+step_s,A[n])
                    p_sy[n]=error_multi(spe_array,dat_tag,input_dat)-err
                else:
                    p_sy[n]=0
                spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n],A[n]+step_A)
                p_A[n]=error_multi(spe_array,dat_tag,input_dat)-err
            
            #if(output=='verbose'):
                #print('error', p_y,p_x,p_sx,p_sy,p_A)
            x_init=x_init-p_x*descent_factor*step_xy
            y_init=y_init-p_y*descent_factor*step_xy
            s_x=s_x-p_sx*descent_factor*step_s
            s_y=s_y-p_sy*descent_factor*step_s
            A=A-p_A*descent_factor*step_A
            
            
            if(output=='verbose'):
                print('new pos', y_init[-1],x_init[-1],s_x[-1],s_y[-1],A[-1],err)
            for n in range(num+1):
                spe_array[n].new_value(y_init[n],x_init[n],s_x[n],s_y[n],A[n])

            err_array.append(err)
            
            if(i>=11 and np.abs(err-err_array[i-11])<=err/40):
                if(output is not 'nothing'):
                    print('convergence achieved in step', i)
                break
                
        if(output is not 'nothing'):
            for spe in spe_array:
                print(spe.intensity_matrix.astype(int))
        
        if(output is not 'nothing'):
            print('----------------------------------------',num+2)
            #print(err)
            
        
        
    """
    spe_array.sort(key=lambda spe: spe.A)
    photon_num=len(spe_array)
    count=0
    for i in range(photon_num):
        err_new=error_multi(spe_array[i+1:],dat_tag,input_dat)
        p_null=np.exp(-Lambda*err_new/size)*poisson.pmf(k=photon_num-i-1, mu=avg_mu)
        p=np.exp(-Lambda*err/size)*poisson.pmf(k=photon_num-i,mu=avg_mu)
        if(p_null<=p):
            count=i
            break
        else:
            err=err_new
            print('kicked one point with intensity ', spe_array[i].A)
        #prob=chi2.pdf(err/100,df=size)*poisson.pmf(k=num+1, mu=avg_mu*size)
        
    x_init=[spe.x0 for spe in spe_array[count:]]
    y_init=[spe.y0 for spe in spe_array[count:]]
    A=[spe.A for spe in spe_array[count:]]
    """
        
        
        
        #print('prob: ',prob)
    if(output is not 'nothing'):
        print('Done.')
    #if(output is 'verbose'):
        #plt.plot(err_array)
    return [x_init,y_init,A,err]
    #return [x_old,y_old,A_old,err]

