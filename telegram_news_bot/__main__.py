"""Main file of program."""

import requests

base_url = "https://habr.com/ru/articles/page1/"

response = requests.get(base_url)
# if response == 200:
#    print(response.text)
