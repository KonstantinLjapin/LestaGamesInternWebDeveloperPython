from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import UploadFile
import re
import pandas as pd


async def to_html(name, val) -> str:
    data = {'name': name[:50], 'val': val[:50]}
    df = pd.DataFrame.from_dict(data)

    return df.to_html()


async def unbound_uf(file: UploadFile) -> list:
    data = await file.read()
    out: list = data.decode('utf-8').split('\n')
    return out


async def filter_text_pack(pack: list) -> list:
    out = list()
    for i in pack:
        if re.search('z', i):
            out += pack[:pack.index(i)]
            break
    return out


async def counter_keys(keys: list, pack: list) -> dict:
    out: dict = dict()
    for i in keys:
        out[i] = pack.count(i)
    return out


async def extract_keywords(document: list) -> list:
    # Создание объекта TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()
    # Применение TF-IDF к текстовым данным
    tfidf_matrix = tfidf_vectorizer.fit_transform(document)

    # Получение списка ключевых слов и их значения TF-IDF для первого документа
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Сортировка слов по значениям TF-IDF
    sorted_keywords = [word for _, word in sorted(zip(tfidf_scores, feature_names), reverse=True)]
    keys: list = await filter_text_pack(sorted_keywords)
    return keys


async def extract_tfidf(documents: list) -> str:

    # Создание объекта TfidfVectorizer с использованием биграмм
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    # Применение TF-IDF к текстовым данным
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Получение списка фичей и их значения TF-IDF для первого документа
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Сортировка фичей по значениям TF-IDF
    sorted_features = [feature for _, feature in sorted(zip(tfidf_scores, feature_names), reverse=True)]
    html_content = await to_html(feature_names, tfidf_scores)
    return html_content

