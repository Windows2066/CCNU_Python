import random

def play_game(word_list):
    ans = random.choice(word_list).strip()
    word = list(ans)
    random.shuffle(word)
    tmp = ''.join(word)
    
    print(f"乱序后的单词： {tmp}")
    guess = input("请输入您猜测的结果：").strip()

    while True:
        if guess.lower() == ans.lower():
            print("恭喜您，猜对了！")
            break
        else:
            guess=input("结果不对，请重新猜测：")

file_name = "words.txt"
with open(file_name, "r", encoding="utf-8") as fin:
    word_list = fin.readlines()

print("欢迎参加猜单词游戏!\n请把乱序后的字母组成一个单词")

while True:
    play_game(word_list)
    answer = input("是否继续(Y/N)？ ").strip().lower()
    if answer != 'y':
        break

print("谢谢参与，欢迎下次再玩！")

