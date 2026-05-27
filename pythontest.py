from bs4 import BeautifulSoup
import requests

url = "https://www.baseball-reference.com/teams/ATL/2026.shtml"
html_page = requests.get(url)
team_html = BeautifulSoup(html_page.text, 'html.parser')

# print(clean_html.prettify())
team_tables = team_html.find_all('table')[8]
print(team_tables)