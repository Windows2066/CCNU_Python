a = input()
b = int(a)
if b<10000 or b>99999:
    print("输入错误")
else:
    if a[0]==a[4] and a[1]==a[3]:
        print("是回文数")
    else:
        print("不是回文数") 