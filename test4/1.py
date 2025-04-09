with open("text1.txt", "r", encoding="utf-8") as fin, \
         open("text2.txt", "w", encoding="utf-8") as fout:
        for index, line in enumerate(fin, start=1):
            fout.write(f"{index}、{line}")