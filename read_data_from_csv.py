f = open("shanghai.csv","r")
g = open("shshopid.txt","w")
a = f.readlines()
lena = len(a)
print lena
for i in range (1,lena):
    k = a[i].split(",")
    g.write(k[11]+"\n")