from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from lxml import etree
import pandas as pd
import nltk
import string

lemmatizer = WordNetLemmatizer()

root = etree.parse(r".\news.xml").getroot()

articles = list()
list_final = list()
for i in range(len(root[0])):
    article = root[0][i][0].text
    articles.append(article)
    text = root[0][i][1].text
    tokenize_list = word_tokenize(text.lower())
    list_lem = [lemmatizer.lemmatize(n) for n in tokenize_list]
    list_pos = [nltk.pos_tag([word]) for word in list_lem]
    list_noun = [word[0][0] for word in list_pos if word[0][1] == "NN"]
    list_without = [word for word in list_noun if word not in list(string.punctuation)]
    list_final.append(" ".join(list_without))

vectorizer = TfidfVectorizer(input="list_final", use_idf=True, stop_words=stopwords.words('english'))
tfidf_matrix = vectorizer.fit_transform(list_final)
terms = vectorizer.get_feature_names_out()

for i in range(len(articles)):
    print(articles[i] + ":")

    word_score = zip(terms, tfidf_matrix.toarray()[i])
    word_score_sort = [key for key, value in sorted(word_score, key=lambda item: (item[1], item[0]), reverse=True)[:5]]
    print(" ".join(word_score_sort) + "\n")
