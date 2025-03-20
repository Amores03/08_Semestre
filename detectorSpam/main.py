from complements.removeHTML import strip_tags 
from complements.steamming import Parser
from complements.parser import parse_index

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

    indexes = parse_index("full/index", 10)
    print(indexes)



if __name__ == "__main__":
    main()
