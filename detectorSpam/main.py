from complements.removeHTML import strip_tags 
from complements.steamming import Parser
from complements.parser import parse_index, parse_email
from algorithms.countVectorizer import vectorize_email
from algorithms.oneHotEncoder import EncoderMail
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import os

def main():
    """
    t = '<tr><td align="left"><a href="../../issues/51/16.html#article">Phrack World News</a></td>'
    result = strip_tags(t)
    print(result)

    print('\n')

    inmail = open('data/inmail.1').read()
    print(inmail)

    print('\n')

    p = Parser()
    print(p.parse('data/inmail.1'))

    print('\n')

    indexes = parse_index("full/index", 10)
    print(indexes)
    :return:

        index = parse_index("full/index", 1)
    mail, label = parse_email(index[0])
    print("El correo es: ",label)
    print(mail)

    print('\n')


    prep_email, features, x = vectorize_email(mail)
    print("email:", prep_email, "\n")
    print("features:", features)
    print("x:", x.toarray())

    enc, x_encoder = EncoderMail(mail)
    print("\nFeatures:\n", enc)
    print("\nValues:\n", x_encoder.toarray())
    """

    def create_prep_dataset(index_path, n_elements):
        x = []
        y = []
        indexes = parse_index(index_path, n_elements)
        for i in range(n_elements):
            print("\rParsing email: {0}".format(i + 1), end='')
            try:
                mail, label = parse_email(indexes[i])
                x.append(" ".join(mail['subject']) + " ".join(mail['body']))
                y.append(label)
            except:
                pass
        return x, y

    x_train, y_train = create_prep_dataset('full/index', 100)
    print(x_train)

    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(x_train)

    print("\n",pd.DataFrame(x_train.toarray(), columns=[vectorizer.get_feature_names_out()]))

    print(y_train)

    clf = LogisticRegression()
    print(clf.fit(x_train, y_train))

    



if __name__ == "__main__":
    main()
