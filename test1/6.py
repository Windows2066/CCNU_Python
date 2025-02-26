e = 1.0          
term = 1.0     
n = 1            
while term >= 1e-6:
    term /= n  
    e += term  
    n += 1     
print(e)