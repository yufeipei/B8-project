from tables import *

class tag:
    'used to tag SPEs.'
    lx=0
    ly=0
    rx=0
    ry=0
    width=0
    height=0
    
    def __init__(self,lx,ly,rx,ry):
        self.lx=lx
        self.ly=ly
        self.rx=rx
        self.ry=ry
        self.width=rx-lx
        self.height=ry-ly
    
    def param(self):
        return [self.lx,self.ly,self.rx,self.ry]
    
    def hw(self):
        return [self.height,self.width]
    
def thresholding(dataset,threshold):
    label_matrix=np.zeros(dataset.shape)
    for i in range(dataset.shape[0]):
        for j in range(dataset.shape[1]):
            if(dataset[i,j]>=threshold):
                label_matrix[i,j]=1
    return label_matrix

def boxing(thres_matrix):
    
    lm=deepcopy(thres_matrix)
    """
    def search(x,y):
        lefttop_x=x-1
        lefttop_y=y-1
        rightbot_x=x+1
        rightbot_y=y+1
        if(lm[x,y]==0):
            return [lefttop_x,lefttop_y,rightbot_x,rightbot_y]
        else:
            lm[x,y]=0
        for i in [x-2,x-1,x,x+1,x+2]:
            for j in [y-2,y-1,y,y+1,y+2]:
                if((i>=lm.shape[0]) or (j>=lm.shape[1])):
                    continue
                elif(lm[i,j]==1):
                    [a,b,c,d]=search(i,j)
                    #print([a,b,c,d])
                    lm[i,j]=0
                    lefttop_x=min([lefttop_x,a])
                    lefttop_y=min([lefttop_y,b])
                    rightbot_x=max([rightbot_x,c])
                    rightbot_y=max([rightbot_y,d])
                    #print('a',[lefttop_x,lefttop_y,rightbot_x,rightbot_y])
       
        return [lefttop_x,lefttop_y,rightbot_x,rightbot_y]
    #[lx,ly,rx,ry]=search(17,20,lm)
    #thres_matrix[lx,ly]=2
    #thres_matrix[rx,ry]=2
    #plt.imshow(thres_matrix)    
    """
    
    tag_list=[]
    


    for i in range(thres_matrix.shape[0]):
         for j in range(thres_matrix.shape[1]):
            if(lm[i,j]==1):
                x=i
                y=j
                #[lx,ly,rx,ry]=search(i,j)
                lx=x-1
                ly=y-1
                rx=x+1
                ry=y+1
                while(True):
                    flag=0
                    
                    lm[x,y]=0
                    for ii in range(lx-1,rx+2):
                        for jj in range(ly-1,ry+2):
                            if((ii>=lm.shape[0]) or (jj>=lm.shape[1])):
                                continue
                            elif(lm[ii,jj]==1):
                                flag=1
                                lm[ii,jj]=0
                                lx=min(lx,ii-1)
                                ly=min(ly,jj-1)
                                rx=max(rx,ii+1)
                                ry=max(ry,jj+1)
                    if(flag==0):
                        break
                thres_matrix[lx,ly]=2
                thres_matrix[rx,ry]=2
                t=tag(lx,ly,rx,ry)
                tag_list.append(t)
    return tag_list

