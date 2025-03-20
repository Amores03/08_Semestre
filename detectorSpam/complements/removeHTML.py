from html.parser import HTMLParser

# Esta clase facilita el preprocesamiento de correos electrónicos que poseen código HTML
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

# Esta función se encarga de eliminar los tags HTML que se encuentren en el texto del correo electrónico  
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data() 

