import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import os

def generate_wordcloud(text_path, output_path='wordcloud.png', font_path=None):
    """
        text_path: 文本文件路径
        output_path: 输出图片路径
        font_path: 字体文件路径（中文需要指定字体）
    """
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        word_list = jieba.cut(text)
        text = ' '.join(word_list)
        wc = WordCloud(
            width=800, 
            height=600,
            background_color='white',
            max_words=200,
            max_font_size=100,
            random_state=42,
            font_path=font_path
        )
        wc.generate(text)
        wc.to_file(output_path)
        plt.figure(figsize=(10, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('词云图')
        plt.show()
        print(f"词云图已保存到: {output_path}")
    except Exception as e:
        print(f"生成词云图时出错: {e}")

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    text_file = os.path.join(base_path, "text.txt")
    font_path = "C:/Windows/Fonts/simfang.ttf"  
    generate_wordcloud(text_file, font_path=font_path)