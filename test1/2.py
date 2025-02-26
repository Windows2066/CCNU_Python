n = int(input())
start = n
fac = []
i = 2
while i * i <= n:
    while n % i == 0:
        fac.append(i)
        n //= i
    i += 1
if n > 1:
    fac.append(n)
print(f"{start}=" + "*".join(map(str, fac)))