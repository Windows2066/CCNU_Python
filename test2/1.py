a = input()
english = 0 
digit = 0
space = 0
other = 0

for ch in a:
    if ch.isalpha():
        english += 1
    elif ch.isdigit():
        digit += 1
    elif ch.isspace():
        space += 1
    else:
        other += 1


print(f"英文字符: {english}")
print(f"数字字符: {digit}")
print(f"空格: {space}")
print(f"其他字符: {other}")