from sklearn.feature_extraction.text import CountVectorizer


def vectorize_email(mail):
    """
    Prepara y vectoriza un email.

    :param mail: Diccionario con 'subject' y 'body'.
    :return: Características extraídas del email.
    """
    prep_email = [" ".join(mail['subject']) + " " + " ".join(mail['body'])]

    vectorizer = CountVectorizer()
    x = vectorizer.fit(prep_email)
    x = vectorizer.transform(prep_email)

    return prep_email, vectorizer.get_feature_names_out(), x

