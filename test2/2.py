def gcd(a,b):
    return a if b==0 else gcd(b,a%b)
def lcm(a,b):
    return a*b//gcd(a,b)
a = input()
b = input()
print(f"最大公约数: {gcd(int(a),int(b))}")
print(f"最小公倍数: {lcm(int(a),int(b))}")