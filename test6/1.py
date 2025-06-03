import jieba
import collections
import re

def count_word_frequency(text):
    text = re.sub(r'[^\u4e00-\u9fa5]', ' ', text)
    words = jieba.lcut(text)
    words = [word for word in words if len(word) > 1 and word.strip()]
    word_counts = collections.Counter(words)
    return word_counts

def display_word_frequency(word_counts, top_n=10):
    print(f"文本中共有 {len(word_counts)} 个不同的词")
    print("\n出现频率最高的{}个词:".format(top_n))
    for word, count in word_counts.most_common(top_n):
        print(f"{word}: {count}次")

def main():
    file_path = input("请输入中文文本文件路径: ")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        word_counts = count_word_frequency(text)
        display_word_frequency(word_counts)
        while True:
            query = input("\n请输入要查询的词(输入q退出): ")
            if query.lower() == 'q':
                break
            print(f"'{query}' 出现次数: {word_counts.get(query, 0)}次")
            
    except FileNotFoundError:
        print("文件不存在，请检查文件路径!")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()