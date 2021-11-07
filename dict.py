#Create a class to build a new dictionary for answer number and play input number
#import rand as r

#secret=r.rnumlistwithoutreplacement(4,0,7)

class dictionary(dict):  
  
    # __init__ function  
    def __init__(self):  
        self = dict()  
          
    # Function to add key:value  
    def add(self, key, value):  
        self[key] = value


# Main Function  
#sdict = dictionary()  

#i=0
#j=len(secret)-1
#print(j)
#for number in secret:
#	sdict.key=i
#	i=i+1
#	sdict.value=number
#	j=j-1
#	sdict.add(sdict.key, sdict.value) 
#  
#print(sdict) 