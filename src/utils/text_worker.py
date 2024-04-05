from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import UploadFile
import re

async def unbound_uf_too_text(file: UploadFile) -> list:
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


async def extract_keywords(file: UploadFile) -> dict:
    # Создание объекта TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()
    document: list = await unbound_uf_too_text(file)
    # Применение TF-IDF к текстовым данным
    tfidf_matrix = tfidf_vectorizer.fit_transform(document)

    # Получение списка ключевых слов и их значения TF-IDF для первого документа
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Сортировка слов по значениям TF-IDF
    sorted_keywords = [word for _, word in sorted(zip(tfidf_scores, feature_names), reverse=True)]
    keys: list = await filter_text_pack(sorted_keywords)
    out: dict = await counter_keys(keys, sorted_keywords)
    return out



