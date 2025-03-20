from removeHTML import strip_tags 
from steamming import Parser

def main():
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

    index = open('full/index').readlines()
    print(index)



if __name__ == "__main__":
    main()
