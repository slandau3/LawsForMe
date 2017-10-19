# import scrapy
import requests
import psycopg2
from bs4 import BeautifulSoup
# import sys
# import threading

# lock = threading.Lock()

# class Lawyer(scrapy.Spider):
    # name = 'lawyer'
    # start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_federal_legislation,_2001%E2%80%93present']

    # def parse(self, response):
        # self.conn = psycopg2.connect("dbname='p32004b' user='p32004b' host='reddwarf.cs.rit.edu' password='Ahx5peeyaeCh1chiingi'")
        # self.curr = self.conn.cursor()
        # print ( self.curr.execute("select * from federal_law") )
        # for law in response.xpath("//div/div/div[@id='mw-content-text']/div/ul/li"):
            # link = law.css('a ::attr(href)').extract_first()
            # yield response.follow("https://en.wikipedia.org" + link, callback=self.parse2)

        # # self.curr.close()
        # # self.conn.close()

    # def parse2(self, response):
        # title = response.xpath("//div/h1").css('h1 ::text').extract()
        # everything_else = response.xpath("//div/div[@id='bodyContent']").css('div ::text').extract()
        # with lock:
            # self.curr.execute("INSERT INTO federal_law VALUES (%s, %s)",  (title[0], everything_else[0].strip()))
            # self.conn.commit()
        
        # yield {}
        # # yield {"title" : title,
                # # "body" : everything_else}


# TODO: fuck scrappy. tomrrow make a real web crawler with bs4 and requrests

conn = psycopg2.connect("dbname='p32004b' user='p32004b' host='reddwarf.cs.rit.edu' password='Ahx5peeyaeCh1chiingi'")
curr = conn.cursor()

#url = "https://en.wikipedia.org/wiki/List_of_United_States_federal_legislation,_2001%E2%80%93present"
#url = "https://en.wikipedia.org/wiki/List_of_United_States_federal_legislation,_1901%E2%80%932001"
url = "https://en.wikipedia.org/wiki/List_of_United_States_federal_legislation,_1789%E2%80%931901"
base_url = "https://en.wikipedia.org"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
i= 1400
for j in soup.find(id='bodyContent').find_all('div'):
    for k in j.find_all('ul'):
        for l in k.find_all('li'):
            a = l.find('a')
            if a is None: continue
            t = a.get('title', False)
            h = a.get('href', False)
            if (h and t):
                # get each of the inner links
                r = requests.get(base_url + h)
                soup = BeautifulSoup(r.text, 'html.parser')
                text = soup.find(id='bodyContent').text.strip()

                print("len of title is", len(t), "i is", i)
                curr.execute("INSERT INTO public.federal_law VALUES (%s, %s, %s)", (i, t, text))
                i += 1
                conn.commit()

curr.close()
conn.close()
