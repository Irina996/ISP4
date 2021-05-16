# the Gauss method with data from "matrix.txt" and "vector.txt"

import numpy as np
import os

def error():
	print("Error. Check text files and try again. Bye...")
	f = open('answer.txt', 'w')
	f.write("Error. Check matrix.txt and vector.txt and try again.")
	f.close()
	pass	

#get matrix from file
if os.path.isfile("matrix.txt") and os.path.getsize("matrix.txt")>0:
	try:
		A = np.loadtxt("matrix.txt", delimiter=' ', dtype=float)
		n=np.shape(A)[0]
		m=np.shape(A)[1]
		print("Matrix A:\n", A)
	except Exception:
		error()
		quit()	
else:
	error()
	quit()

#get vector from file
if os.path.isfile("vector.txt") and os.path.getsize("vector.txt")>0:
	try:
		b = np.loadtxt("vector.txt", delimiter=' ', dtype=float)
	except Exception:
		error()
		quit()	
	if np.shape(b)[0]!=n:
		error()
		quit()
	print("Vector b:", b)
else:
	error()
	quit()

#checking possibility of solving	
i=0
while i<n:
	if A[i][i]==0.:
		error()
		quit()
	i+=1

# solving system of linear algebraic equations
t=0
while t < n:
    i=t+1
    while i < n:
        q=A[i][t]/A[t][t]
        b[i]=b[i]-b[t]*q
        j=t
        while j < m:
            A[i][j]=A[i][j]-A[t][j]*q
            j=j+1
        i=i+1
    t=t+1
t=t-1
x=np.zeros(n)
while t > -1:
    x[t]=b[t]/A[t][t]
    i=t-1
    while i > -1:
        b[i]-=x[t]*A[i][t]
        i=i-1
    t=t-1

#print answer
print("Solve of the SLAE:", np.round((x), 4))
f = open('answer.txt', 'w')
for xn in x:
	a =  str(np.round(xn, 4))
	f.write(a+' ')
f.close()

