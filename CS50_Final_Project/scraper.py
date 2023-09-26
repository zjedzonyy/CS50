import requests
from bs4 import BeautifulSoup
import re
import csv

from dynamic import urls

def quote(value):
    return f"'{value}'"

#"i'm not a robot"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

with open('dane2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['flavor', 'description', 'image', 'price', 'producer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        response = requests.get(url, headers=headers)

        #check if the request was done right
        if response.status_code == 200:
            #create object from BeautifulSoup from received HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            data = {}

            # get url address of an image
            a_tag = soup.find('a', class_='photos__link')
            if a_tag and 'href' in a_tag.attrs:
                href_url = a_tag['href']
                data['image'] = a_tag['href']
            else:
                data['image'] = "unknown"

            # get product description
            product_description = soup.find('div', class_='product_name__block --description mt-3')
            if product_description is None:
                data['description'] = "unknown"
            else:
                cleaned_description = product_description.text.replace('"', '')
                data['description'] = cleaned_description



            # get product name
            product_name = soup.find('h1', class_='product_name__name m-0')
            if product_name is None:
                data['flavor'] = "unknown"
            else:
                cleaned_name = re.sub(r'\s*\d+,\d+\s*kg', '', product_name.text)
                data['flavor'] = cleaned_name

            # get product price
            product_price = soup.find('strong', class_='projector_prices__price')
            if product_price is None:
                data['price'] = "unknown"
            else:
                cleaned_name = re.sub(r'\s*zł', '', product_price.text).replace(',', '.')
                data['price'] = cleaned_name

            # get producer
            producer = soup.find('div', class_='dictionary__value')
            if producer is None:
                data['producer'] = "unknown"
            else:
                data['producer'] = producer.text



            #save data in CSV file
            writer.writerow(data)


        else:
            print(f"Failed to scrape {url}")

print("Scraping completed")


#jezeli jest duzo <span> albo generalnie takich samych naglowkow to trzeba dodatkowej informacji o nich, np. id albo class ich dywizji, dojsc jakos do nich. tutaj sie nie da
#niestety dojsc w zaden sposob, do mocy, buttona i innych.
#tak samo jest z krajem pochodzenia
    #get country of origin
    #country_of_origin = soup.find('b', text="Kraj pochodzenia")
    #if country_of_origin is None:
        #print("Country of origin: unknown")
    #else:
        #print(country_of_origin)