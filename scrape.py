import requests
from bs4 import BeautifulSoup

url = "https://towardsdatascience.com/the-ultimate-guide-to-data-cleaning-3969843991d4"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

text = soup.get_text()

clean_text = text.replace('\n', '').replace('\r', '').replace('\t', '')

print(clean_text)