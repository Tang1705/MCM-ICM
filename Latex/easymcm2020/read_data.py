import nltk
import tqdm
import json
import string
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

data = pd.read_csv('data/hair_dryer.tsv', sep='\t', header=0, encoding="utf-8")

fre = {}
review = data['product_title']
for i in tqdm.tqdm(range(0, data.shape[0])):
    tags = {'RB', 'RBR', 'RBS'}
    remove = str.maketrans('', '', string.punctuation)
    without_punctuation = review[i].translate(remove)
    value = nltk.sent_tokenize(without_punctuation)
    words = nltk.word_tokenize(text=value[0])
    without_stopwords = [w for w in words if w not in stopwords.words('english')]
    pos_tags = nltk.pos_tag(without_stopwords)

    prepare_word = []
    for word, pos in pos_tags:
        if (pos in tags):
            prepare_word.append(word)

    for word in prepare_word:
        if len(fre) == 0:
            fre[word] = 1
        elif word not in fre.keys():
            fre[word] = 1
        else:
            fre[word] = fre[word] + 1

with open('data.json', 'w') as f:
    json.dump(fre, f)
with open('data.json', 'r') as f:
    dict = json.load(f)
name = dict.keys()
for item in name:
    dict[item] = float(dict[item])

wordcloud = WordCloud(
    font_path="mine.ttf", background_color="white", width=1000, height=880).generate_from_frequencies(dict)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

wordcloud.to_file('title1.png')
