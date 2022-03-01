from gradient_descent_multi import *
from gradient_descent_single import *

class single_photon_event_result:
    'this is a commend line.'

    def __init__(self,matrix,event_type,x,y,A):
        self.matrix=matrix
        self.x=x
        self.y=y
        self.A=A
        self.type=event_type

def spe_data_generation_new(input_dat,threshold=30,things_to_say=''):
    tag_list=boxing(thresholding(deepcopy(input_dat),threshold))
    length=len(tag_list)
    xy_list=[]
    i=0
    
    start=time.time()

    Avg_mu=length*1.2/2044/2046
    
    for tag in tag_list:
        matrix=input_dat[(tag.param()[0]):(tag.param()[2]+1),(tag.param()[1]):(tag.param()[3]+1)]
        mx, my=np.unravel_index(matrix.argmax(), matrix.shape)
        if(matrix[mx,my]+matrix[mx-1,my]+matrix[mx,my-1]+matrix[mx-1,my-1]>400):
            continue
        print('-----------------')
        i=i+1
        if(things_to_say is not ''):
            print(things_to_say,end='  ')
        print(i,end=' ')
        print(tag.hw(),end=' ')
        if(tag.hw()[0]<=3 and tag.hw()[1]<=3):
            spe_event=gradient_descent_single(tag, input_dat, 'nothing', avg_mu=Avg_mu)
            [x,y,A,flag]=[spe_event[0]+tag.param()[0],spe_event[1]+tag.param()[1],spe_event[-2],spe_event[-1]]
            print(x,y,A)
            if(flag==1):
                print("This is a mistake.")
                end=time.time()
                print(end-start)
                continue
            elif(flag==0):
                sper=single_photon_event_result(matrix,'s',x,y,A)
                xy_list.append(sper)
                end=time.time()
                print(end-start)
                continue
            
        print('This is a MPE.')
        
        #mpe_list=[]
        
        mpe=gradient_descent_multi_new2(tag,input_dat,'nothing',threshold,avg_mu=Avg_mu)
        #mpe=gradient_descent_multi_new(tag,input_dat,'nothing',threshold)
        n=len(mpe[0])
        print('This event contains ',n,' photons.')
            
        for m in range(n):
            x=mpe[0][m]+tag.param()[0]
            y=mpe[1][m]+tag.param()[1]
            A=mpe[2][m]
            print(x,y,A)
            xy_list.append(single_photon_event_result(matrix,'m',x,y,A))
        
        end=time.time()
        print(end-start)
    return xy_list

def write_in_csv(spe_result,name='data1.csv'):

    with open(name,'w',newline='') as file:
        writer=csv.writer(file)
        for sper in spe_result:
            x=sper.x
            y=sper.y
            A=sper.A
            if(A>0):
                writer.writerow([x,y,A])

def spe_running(image_data):
    start=time.time()
    spe_result=np.array([])
    image_n=0
    for image in image_data:
        image_n=image_n+1
        dat=deepcopy(image.astype(int))
        for i in range(32):
            dat[i*64:(i+1)*64,:]=dat[i*64:(i+1)*64,:].astype(int)-mean(mode(dat[i*64:(i+1)*64,:].flatten())[0])
        th=dat.shape[0]
        tw=dat.shape[1]
        for i in range(th):
            for j in range(tw):
                if((i<2 or i>tw-2) or (j<4 or j>tw-2)):
                    dat[i,j]=0

        spe_result=np.append(spe_result,spe_data_generation_new(dat,things_to_say=str(image_n)))
        
    end=time.time()
    print(end-start)
    print(len(spe_result.flatten()))

    return spe_result.flatten()

def spe_running_test(image_data):
    start=time.time()
    spe_result=np.array([])
    image_n=0
    image=image_data[1]
    dat=deepcopy(image.astype(int))
    for i in range(32):
        dat[i*64:(i+1)*64,:]=dat[i*64:(i+1)*64,:].astype(int)-mean(mode(dat[i*64:(i+1)*64,:].flatten())[0])
    th=dat.shape[0]
    tw=dat.shape[1]
    for i in range(th):
        for j in range(tw):
            if((i<2 or i>tw-2) or (j<4 or j>tw-2)):
                dat[i,j]=0

    spe_result=np.append(spe_result,spe_data_generation_new(dat,things_to_say=str(image_n)))
        
    end=time.time()
    print(end-start)
    print(len(spe_result.flatten()))

    return spe_result.flatten()
