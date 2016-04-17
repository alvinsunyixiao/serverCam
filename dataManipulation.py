import scipy.io as sio
import numpy as np

def savedata(mydata):
    oldData = sio.loadmat('data.mat')['data']
    newData = np.append(oldData,mydata,0)
    sio.savemat('data.mat',{'data':newData})
