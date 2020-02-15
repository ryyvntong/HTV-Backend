import numpy as np

f = open("Captions.text","r")
line1=f.read()
data=line1.splitlines()
data=[i for i in data if len(i) > 0]
data=np.array(data)
data=np.delete(data,np.arange(0,data.size,3))
data=data.tolist()
print(data)





