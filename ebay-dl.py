import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_price(text):
    numbers=''
    if text[0]=='$':
        for char in text:
            if char in '1234567890':
                numbers+=char
            elif char==' ':
                break
        return int(numbers)
    else:
        return None

def parse_shipping(text):
    numbers=''
    if text[0]=='+':
        for char in text:
            if char in '1234567890':
                numbers+=char
            elif char==' ':
                break
        return int(numbers)
    else:
        return 0

def parse_items_sold(text):
    numbers=''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return None

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action='store_true')
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    # list of all items found in all ebay webpages
    items = []

    #loop for each ebay webpage
    for page_number in range(1,int(args.num_pages)+1): 

        # building the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
        url += args.search_term 
        url += '&_sacat=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print ('url=', url)

        # download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html = r.text

        # proces the html
        soup = BeautifulSoup(html, 'html.parser')

        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            status = None
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                status = tag.text

            shipping = None
            tags_shipping = tag_item.select('.s-item__shipping, .s-item__freeXDays')
            for tag in tags_price:
                shipping = parse_shipping(tag.text)

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True
            
            items_sold = None
            tags_items_sold = tag_item.select('.s-item__hotness, .s-item__additionalItemHotness')
            for tag in tags_items_sold:
                items_sold=parse_items_sold(tag.text)
                

            item={
                'name': name,
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': freereturns,
                'items_sold': items_sold
                }
            items.append(item)

    filename='_'.join(args.search_term.split(' '))
    if args.csv:
        with open(filename+'.csv', 'w') as f:
            header=items[0].keys()
            writer = csv.DictWriter(f, fieldnames = header)
            writer.writeheader()
            writer.writerows(items[1:])
                
    else:
        with open(filename+'.json', 'w', encoding='ascii') as f:
            f.write(json.dumps(items[1:]))

    