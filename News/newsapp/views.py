from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from newsapp.models import Headline
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create your views here.

def scrape(request):
  #Headline.objects.all().delete()
  #url = "https://www.investigacionyciencia.es/materias/biologia/biotecnologia/mas-noticias?page=1"
  page = requests.post('https://www.investigacionyciencia.es/materias/biologia/biotecnologia/mas-noticias?page=1')

  #content = session.get(url).content

  soup = BSoup(page.content, "html.parser")
  News = soup.find_all('div', attrs={"class":"iyc-views-DocumentEntry iyc-views-NewsItemEntry"})

  logging.info(News) 
  
  for article in News:
    #obteniendo title: 
    titlex = article.find('a', attrs={"class":"bound"})
    #obteniendo image: 
    main = article.find_all('img',href=True)
    imgagex=main[0].find('img', attrs={"class":"articleImage"})
    #obteniendo url: 
    linkx = article.find('a', attrs={"class":"articleImageLink bound"})
    #obteniendo summary: 
    summaryx = article.find_all('div',attrs={"class":"abstract"})
    #obteniendo author: 
    authorx = article.find('li',attrs={"class":"authoring"})
    #obteniendo discipline
    disciplinex = article.find('p',attrs={"class":"discipline"})
    
    title = titlex.text
    image_src=imgagex['src'].split(" ")[-4]
    link=linkx['href']
    summary=summaryx.text
    author=authorx.text
    discipline=disciplinex.text
    
    
    new_headline = Headline()
    new_headline.title = title
    logging.info(title)
    new_headline.image = image_src
    new_headline.url = link
    new_headline.summary =summary
    new_headline.author = author 
    new_headline.discipline = discipline
    new_headline.save()
  return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "newsapp/home.html", context)



