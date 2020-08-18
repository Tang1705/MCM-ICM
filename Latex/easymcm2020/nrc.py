import os
import sys
import json
import nltk
import numpy as np
import pandas as pd
from tqdm import tqdm
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer

data = pd.read_csv('original.csv')
data = pd.DataFrame(data)
data = data[["review_headline", "review_body"]]
nrc_lex = pd.read_csv("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt", sep='\t')
def get_emotion(data, name):
    emotions = []
    for review in tqdm(data[name]):
        total = [0, 0, 0, 0, 0, 0, 0, 0]
        anger = 0
        fear = 0
        anticipation = 0
        trust = 0
        surprise = 0
        sadness = 0
        joy = 0
        disgust = 0
        if not review is np.nan:
            lyrics_text = review
            token_lyrics = sent_tokenize(lyrics_text)
            for sentence in token_lyrics:
                lyric_words = TreebankWordTokenizer().tokenize(sentence)
                for word in lyric_words:
                    anger_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'anger'].index.tolist()
                    if len(anger_list) == 1:
                        anger += int(nrc_lex.iloc[int(anger_list[0])]['association'])
                    fear_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'fear'].index.tolist()
                    if len(fear_list) == 1:
                        fear += int(nrc_lex.iloc[int(fear_list[0])]['association'])
                    anticipation_list = nrc_lex[nrc_lex['word'] == word][
                        nrc_lex['emotion'] == 'anticipation'].index.tolist()
                    if len(anticipation_list) == 1:
                        anticipation += int(nrc_lex.iloc[int(anticipation_list[0])]['association'])
                    trust_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'trust'].index.tolist()
                    if len(trust_list) == 1:
                        trust += int(nrc_lex.iloc[int(trust_list[0])]['association'])
                    surprise_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'surprise'].index.tolist()
                    if len(surprise_list) == 1:
                        surprise += int(nrc_lex.iloc[int(surprise_list[0])]['association'])
                    sadness_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'sadness'].index.tolist()
                    if len(sadness_list) == 1:
                        sadness += int(nrc_lex.iloc[int(sadness_list[0])]['association'])
                    joy_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'joy'].index.tolist()
                    if len(joy_list) == 1:
                        joy += int(nrc_lex.iloc[int(joy_list[0])]['association'])
                    disgust_list = nrc_lex[nrc_lex['word'] == word][nrc_lex['emotion'] == 'disgust'].index.tolist()
                    if len(disgust_list) == 1:
                        disgust += int(nrc_lex.iloc[int(disgust_list[0])]['association'])
            total = [anger, fear, anticipation, trust, surprise, sadness, joy, disgust]
            emotions.append(total)
        else:
            emotions.append(total)
    return emotions
def gather(data, emotions):
    result = {"id": [], "anger": [], "fear": [], "anticipation": [], "trust": [], "surprise": [], "sadness": [],
              "joy": [], "disgust": []}
    i = 0
    data = pd.DataFrame(data[["review_id"]])
    print(data)
    for row in data.values:
        result["id"].append(row[0])
        result["anger"].append(emotions[i][0])
        result["fear"].append(emotions[i][1])
        result["anticipation"].append(emotions[i][2])
        result["trust"].append(emotions[i][3])
        result["surprise"].append(emotions[i][4])
        result["sadness"].append(emotions[i][5])
        result["joy"].append(emotions[i][6])
        result["disgust"].append(emotions[i][7])
        i += 1
    result = pd.DataFrame(result)
    return result
if __name__ == '__main__':
    data_tmp = pd.read_csv('original.csv')
    data_tmp = pd.DataFrame(data_tmp)
    result_body = gather(data_tmp, emotion_body)
    result_body.to_csv('result_body.csv', index=None, sep=',')
    result_title = gather(data_tmp, emotion_title)
    result_title.to_csv('result_title.csv', index=None, sep=',')
    emotion_body = get_emotion(data, 'review_body')
    emotion_title = get_emotion(data, 'review_headline')
    data_tmp = pd.read_csv('original.csv')
    data_tmp = pd.DataFrame(data_tmp)
    result_body = gather(data_tmp, emotion_body)
    result_body.to_csv('result_body.csv', index=None, sep=',')
    result_title = gather(data_tmp, emotion_title)
    result_title.to_csv('result_title.csv', index=None, sep=',')