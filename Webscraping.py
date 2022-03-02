import requests
from bs4 import BeautifulSoup
'''#get the url
url ='https://www.amazon.in/boAt-Bassheads-242-Earphones-Carbon/product-reviews/B09FSWY5BP/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'


#1) get the html
r = requests.get(url)
htmlContent = r.content
#print(htmlContent)

#2)Parse the html
soup = BeautifulSoup(htmlContent,'html.parser')
#print(soup.prettify())

#3) HTML tree traversal
#commonly used objects are:tag,navigablestring,Beautifulsoup,comments
#get the title
title = soup.title
#print(title)

#get the paragraphs
parag = soup.find_all('p')
#print(parag)
#print(soup.find('p'),['class'])

#get the anchor tags
anchors = soup.find_all('a')
#print(anchors)

#get the text from the tags/soup
#print(soup.get_text())


#get classes of any elements in the html page
#print(soup.find_all("paragraphs"))

#get all the  links on the page:
#for link in anchors:
    #print(link.get('href'))'''


reviewlist=[]
def get_url(url):
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook':'review'})
        #print(reviews)
    try:
        for item in reviews:
            review={
            'product_name': soup.title.text.replace('Amazon.in:Customer reviews:','').strip(),
            'title' : item.find('a',{'data-hook':'review-title'}).text.strip(),
            'stars' : float(item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars','').strip()),
            'body' : item.find('span',{'data-hook':'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass


for i in range(1,200):
    soup = get_url(f'https://www.amazon.in/boAt-Bassheads-242-Earphones-Carbon/product-reviews/B09FSWY5BP/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={i}')
    print(f'Getting page: {i}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break

#exporting the data
import pandas as pd

df = pd.DataFrame(reviewlist)
df.to_csv('boat_Bassheads_242.csv',index=False)
print("Finish")