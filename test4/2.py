with open("歌词.txt", "r", encoding="utf-8") as fin:
    original_content = fin.read()

header = "千千阙歌\n陈慧娴\n"
footer = "\n由环球唱片发行"

new_content = header + original_content + footer

with open("歌词.txt", "w", encoding="utf-8") as fout:
    fout.write(new_content)

print(new_content)