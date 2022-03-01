from tables import *
from hyperparams import *


class gaussian_spe:
    'A distribution of intensity caused by a single photon event within a given tag(region that is influenced by photons).'
    
    def __init__(self, y0, x0, s1, s2, w, h, A):

        #Width and height of the given tag.
        w = w + 1
        h = h + 1
        
        self.x0 = x0
        self.y0 = y0
        self.s1 = s1
        self.s2 = s2
        self.A = A
        self.h = h
        self.w = w
        
        ls1=[Erf[math.floor(max(-10,min(10,(-self.x0+i)/Sqrt2/s1))*100000)]-Erf[math.floor(max(-10,min(10,(-self.x0+i+1)/Sqrt2/s1))*100000)] for i in range(h)]
        ls2=[Erf[math.floor(max(-10,min(10,(-self.y0+j)/Sqrt2/s2))*100000)]-Erf[math.floor(max(-10,min(10,(-self.y0+j+1)/Sqrt2/s2))*100000)] for j in range(w)]
        self.intensity_matrix=1/2*Pi*self.A*np.outer(ls1,ls2)
        """
        self.intensity_matrix=np.zeros((h,w))
        
        for i in range(h):
            for j in range(w):
                
                #The MUCH SIMPLER erf method
                
                self.intensity_matrix[i,j]=1/2*Pi*self.A*(math.erf((-self.x0+i)/Sqrt2/s1)-math.erf((-self.x0+i+1)/Sqrt2/s1))*(math.erf((-self.y0+j)/Sqrt2/s2)-math.erf((-self.y0+j+1)/Sqrt2/s2))
        """
    
    def new_value(self, y0, x0, s1, s2, A, t=0, cutoff=2):

        
        self.x0 = x0
        self.y0 = y0
        self.s1 = s1
        self.s2 = s2
        self.A = A
        
        h = self.h
        w = self.w
        #self.h = h
        #self.w = w
        """
        ls1=[math.erf((-self.x0+i)/Sqrt2/s1)-math.erf((-self.x0+i+1)/Sqrt2/s1) for i in range(h)]
        ls2=[math.erf((-self.y0+j)/Sqrt2/s2)-math.erf((-self.y0+j+1)/Sqrt2/s2) for j in range(w)]
        """
        ls1=[Erf[math.floor(max(-10,min(10,(-self.x0+i)/(Sqrt2*s1)))*100000)]-Erf[math.floor(max(-10,min(10,(-self.x0+i+1)/(Sqrt2*s1)))*100000)] for i in range(h)]
        ls2=[Erf[math.floor(max(-10,min(10,(-self.y0+j)/(Sqrt2*s2)))*100000)]-Erf[math.floor(max(-10,min(10,(-self.y0+j+1)/(Sqrt2*s2)))*100000)] for j in range(w)]
        self.intensity_matrix=1/2*Pi*self.A*np.outer(ls1,ls2)
    
    
    def copy(self):
        return self

if(__name__ == "__main__"):
    print('hello world!')
    spe_example=gaussian_spe(2,2,0.4,0.4,4,4,20)
    print(spe_example.intensity_matrix)