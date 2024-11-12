from bs4 import BeautifulSoup

class Scrapping_Page:
    def __init__(self, page):
        self.page = page

    '''Retorna el archivo parseado a string de la pagina web'''
    def parserHTML(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        print(soup.prettify())
        return str(soup)

    '''Extrae el titulo de la pagina web'''
    def extractTitle(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        title = soup.title.string
        print(f"Título de la página: {title}")
        return f"Título de la página: {title}"
