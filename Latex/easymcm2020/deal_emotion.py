import nltk
import re
import tqdm
import pandas as pd
from sklearn import preprocessing

class SentimentAnalysis(object):
    def __init__(self, filename='SentiWordNet.txt'):
        self.swn_pos = {'a': {}, 'v': {}, 'r': {}, 'n': {}}
        self.swn_all = {}
        self.build_swn(filename)
    def geometric_weighted(self, score_list):
        weighted_sum = 0
        num = 1
        for el in score_list:
            weighted_sum += (el * (1 / float(2 ** num)))
            num += 1
        return weighted_sum
    def build_swn(self, filename):
        records = [line.split('\t') for line in open(filename)]
        for rec in records:
            words = rec[4].split()
            pos = rec[0]
            for word_num in words:
                word = word_num.split('#')[0]
                try:
                    sense_num = int(word_num.split('#')[1])
                except:
                    continue
                if word not in self.swn_pos[pos]:
                    self.swn_pos[pos][word] = {}
                self.swn_pos[pos][word][sense_num] = float(
                    rec[2]) - float(rec[3])
                if word not in self.swn_all:
                    self.swn_all[word] = {}
                self.swn_all[word][sense_num] = float(rec[2]) - float(rec[3])
        for pos in self.swn_pos.keys():
            for word in self.swn_pos[pos].keys():
                newlist = [self.swn_pos[pos][word][k] for k in sorted(
                    self.swn_pos[pos][word].keys())]
                self.swn_pos[pos][word] = self.geometric_weighted(newlist)
        for word in self.swn_all.keys():
            newlist = [self.swn_all[word][k] for k in sorted(
                self.swn_all[word].keys())]
            self.swn_all[word] = self.geometric_weighted(newlist)
    def score_word(self, word, pos):
        try:
            return self.swn_pos[pos][word]
        except KeyError:
            try:
                return self.swn_all[word]
            except KeyError:
                return 0
    def score(self, sentence):
        impt = {'JJ', 'JJR', 'JJS', 'CC'}
        non_base = {'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'NNS', 'NNPS'}
        word_database = pd.read_csv('data/word_database.csv', encoding="utf-8")
        extend_word = word_database['extend_word']
        limited_word = word_database['limited_word']
        negations = {'not', 'n\'t', 'less', 'no', 'never', 'nothing', 'nowhere', 'hardly', 'barely', 'scarcely',
                     'nobody', 'none'}
        stopwords = nltk.corpus.stopwords.words('english')
        wnl = nltk.WordNetLemmatizer()
        scores = []
        tokens = [w.lower() for w in nltk.tokenize.word_tokenize(sentence)]
        tagged = nltk.pos_tag(tokens)
        new_token = []
        new_tag = []
        for word, pos in tagged:
            if (pos not in impt and word not in negations and word.lower() not in extend_word) or word in limited_word:
                continue
            else:
                new_tag.append((word, pos))
                new_token.append(word)
        if len(tagged) == 1:
            return self.score_word(tagged[0][0].lower(), self.pos_short(tagged[0][1])), 1
        index = 0
        for el in tagged:
            pos = el[1]
            try:
                word = re.match('(\w+)', el[0]).group(0).lower()
                start = index - 5
                if start < 0:
                    start = 0
                neighborhood = tokens[start:index]
                if ((pos in impt) and (word not in stopwords) or word in extend_word) and word not in limited_word:
                    if pos in non_base:
                        word = wnl.lemmatize(word, self.pos_short(pos))
                    score = self.score_word(word, self.pos_short(pos))
                    if word == 'if':
                        score -= 0.3
                    if word == 'supposed':
                        score -= 0.2
                    if len(negations.intersection(set(neighborhood))) > 0:
                        r = negations.intersection(set(neighborhood))
                        a = list(r)
                        i_n = tokens.index(a[0])
                        if tagged[i_n + 1][0] in impt or tagged[i_n + 1][0] in extend_word:
                            score = -score
                    scores.append(score)
            except AttributeError:
                pass
            index += 1
        if len(scores) > 0:
            return sum(scores) / float(len(scores)), len(scores)
        else:
            return 0, 0


def decontracted(phrase):
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
if __name__ == '__main__':
    s = SentimentAnalysis(filename='SentiWordNet.txt')
    data = pd.read_csv('data/microwave.tsv', sep='\t', header=0, encoding="utf-8")
    review = data['review_body']
    review_title = data['review_headline']
    review_id = data['review_id']
    star = data['star_rating']
    star_dict = {}
    title_reviews = {}
    preprocessed_reviews = {}
    score = {}
    for index in tqdm.tqdm(range(0, data.shape[0])):
        star_dict[review_id[index]] = star[index]
        title_reviews[review_id[index]] = review_title[index]
        try:
            if '<br />' in review[index]:
                tmp = review[index].copy()
                review[index] = tmp.replace('<br />', '')
            without_short = decontracted(review[index])
            without_short1 = decontracted(review_title[index])
            without_number = re.sub("\S*\d\S*", "", without_short).strip()
            without_number1 = re.sub("\S*\d\S*", "", without_short1).strip()
            score1, len1 = s.score(without_number)
            score2, len2 = s.score(without_number1 + " machine")
            if len1 == 0 and len2 == 0:
                continue
            if len2 == 0:
                preprocessed_reviews[review_id[index]] = score1
            elif len1 == 0:
                preprocessed_reviews[review_id[index]] = score2
            else:
                preprocessed_reviews[review_id[index]] = 0.1 * score1 + 0.9 * score2
        except:
            continue
    del preprocessed_reviews[min(preprocessed_reviews, key=preprocessed_reviews.get)]
    del preprocessed_reviews[max(preprocessed_reviews, key=preprocessed_reviews.get)]
    min_value = preprocessed_reviews[min(preprocessed_reviews, key=preprocessed_reviews.get)]
    max_value = preprocessed_reviews[max(preprocessed_reviews, key=preprocessed_reviews.get)]
    ndict = {}
    nstar = {}
    s = pd.Series(preprocessed_reviews)
    ndf = pd.DataFrame(s, columns=['score'])
    std_scaler = preprocessing.StandardScaler()
    std_label_data = std_scaler.fit_transform(ndf)
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_label_data = min_max_scaler.fit_transform(std_label_data)
    index = 0
    for key in preprocessed_reviews.keys():
        ndict[key] = min_max_label_data[index][0]
        if 'Five Stars' in title_reviews[key]:
            ndict[key] = 1
        elif 'Four Stars' in title_reviews[key]:
            ndict[key] = 0.75
        elif 'Three Stars' in title_reviews[key]:
            ndict[key] = 0.5
        elif 'Two Stars' in title_reviews[key]:
            ndict[key] = 0.25
        elif 'One Star' in title_reviews[key]:
            ndict[key] = 0
        elif 'zero star' in title_reviews[key]:
            ndict[key] = 0
        index += 1
        nstar[key] = (star_dict[key] - 1) / 4
    key1 = list(ndict.keys())
    value2 = list(ndict.values())
    value3 = list(nstar.values())
    dataframe = pd.DataFrame({'review_id': key1, 'review_score': value2, 'star_rate': value3, })
    dataframe.to_csv("nor_score2.csv", index=False, sep=',')