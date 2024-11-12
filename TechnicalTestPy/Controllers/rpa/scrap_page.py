from bs4 import BeautifulSoup

class Scrapping_Page:
    def __init__(self, page):
        self.page = page

    def parserHTML(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        print(soup.prettify())
        return str(soup)

    def extractTitle(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        title = soup.title.string
        print(f"Título de la página: {title}")
        return f"Título de la página: {title}"
