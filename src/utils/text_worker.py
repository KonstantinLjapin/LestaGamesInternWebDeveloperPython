from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import UploadFile


async def unbound_uf_too_text(file: UploadFile) -> list:
    data = await file.read()
    out: list = data.decode('utf-8').split('\n')
    return out


async def extract_keywords(file: UploadFile) -> list:
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

    return sorted_keywords



