import math as m 
x = float(input())
if x>=0:
    ans = m.sin(x)+2*m.sqrt(x+m.e**4)-(x+1)**3
else:
    ans = m.log(-5*x)-(m.abs(x**2-8*x))/(7*x)+m.e
print(ans)