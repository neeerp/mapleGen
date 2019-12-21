from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.request import urlopen

FAME_RANK_URL = \
    "http://maplestory.nexon.net/rankings/fame-ranking/legendary?rebootIndex=0&pageIndex=%d"

class RankingScraper():
    """
    A scraper for the Maplestory rankings.
    
    :param url: The rankings URL, with an intenger formatter where the index
    should be. 
    :param save: The folder to save the scraped images into.
    "param step: The number of characters to step by per iteration. This is
    5 by default because the ranking pages only have 5 images.
    """


    def __init__(self, url, save, step=5):
        self.url = url
        self.save = save
        self.step = step


    def scrape(self, n, start=1):
        """
        Scrapes character images starting on index <start> and retrieving the
        subsequent <n> pages of characters.
        """
        for i in range(0, n):
            index =  start + i * 5
            page = self._read_page(index)
            avatar_tags = BeautifulSoup(page, "lxml") \
                      .find_all("img", class_="avatar")
            avatars = [self._read_image(tag["src"]) for tag in avatar_tags]

            for j in range(0, len(avatars)):
                avatar = avatars[j]
                avatar.save(self.save + ("/avatar%d.png" % (index + j)))


    def _read_page(self, index):
        """Reads the page with character index <index> and returns it."""
        with urlopen(self.url % index) as url:
            page = url.read()
        return page
    
    def _read_image(self, src):
        """Reads in and returns an image given a <src> url."""
        with urlopen(src) as url:
            file = BytesIO(url.read())
            img = Image.open(file)
        return img


        

if __name__ == "__main__":
    scraper = RankingScraper(FAME_RANK_URL, "./data")
    scraper.scrape(n=4)
