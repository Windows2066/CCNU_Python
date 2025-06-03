class Histogram:
    def __init__(self, n):
        self.data = [0] * n
    
    def addDataPoint(self, i):
        if 0 <= i < len(self.data):
            self.data[i] += 1
        else:
            print(f"索引 {i} 超出范围")
    
    def count(self):
        return sum(self.data)
    
    def mean(self):
        if len(self.data) == 0:
            return 0
        return sum(self.data) / len(self.data)
    
    def max(self):
        if len(self.data) == 0:
            return 0
        return max(self.data)
    
    def min(self):
        if len(self.data) == 0:
            return 0
        return min(self.data)
    
    def draw(self):
        for count in self.data:
            print('#' * count)



import random

hist = Histogram(10)

for _ in range(100):
    hist.addDataPoint(random.randint(0, 9))

print(f"数据点个数：{hist.count()}")
print(f"数据点个数的平均值：{hist.mean()}")
print(f"数据点个数的最大值：{hist.max()}")
print(f"数据点个数的最小值：{hist.min()}")

hist.draw()