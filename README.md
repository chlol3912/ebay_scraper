# Ebay Scraper
 
This project involves a Python file `ebay-dl.py` that, when given a search term, scrapes eBay pages for items and their corresponding attributes: `name`, `price` (in cents), `status` (condition of item: new, used, etc.), `shipping` (cost for shipping in cents), `free_returns` (whether there are free returns available), and `items_sold` (# of the item that has already been sold). After processing all the items under the search term, the program then converts the list of item dictionaries into either a `.json` file or a `.csv` file. 

Since ebay-dl.py is a command prompt script, users must input the following in their command prompt software (Command Prompt or Terminal), where "search term" is the desired item:
```
$ python3 ebay-dl.py "search term"
```
*Note: quotations required when the search term has a space*

This will then generate a json file for the "search term", or item, which will parse the first 10 eBay webpages for that specific item. By default, the program will download the first 10 pages, but if you want to change the number of pages downloaded, use the following command: 
```
$ python3 ebay-dl.py "search term" --num_pages=4
```
By changing what `--num_pages` is equal to, the program will now only download the first 4 pages for the searched item. 

Note that the program will defaultly convert the information on the search item into `.json` files. To create `.csv` files, just add the command line flag `--csv`:
```
$ python3 ebay-dl.py "search term" --csv
```

[Here](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03) is a link to the instructions for this project.