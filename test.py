import weather

data,d= weather.getcordinats()
#get the index of the plz in array 
print(d.index('01067'))
x= data[0]
print(x)

