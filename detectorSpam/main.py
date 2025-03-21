from complements.removeHTML import strip_tags 
from complements.steamming import Parser
from complements.parser import parse_index, parse_email
from algorithms.countVectorizer import vectorize_email
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
    """

    index = parse_index("full/index", 1)
    mail, label = parse_email(index[0])
    print("El correo es: ",label)
    print(mail)

    print('\n')


    prep_email, features, x = vectorize_email(mail)
    print("email:", prep_email, "\n")
    print("features:", features)
    print("x:", x.toarray())



if __name__ == "__main__":
    main()
