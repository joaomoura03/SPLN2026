import requests
from bs4 import BeautifulSoup
import json

res = {}

for letter in 'abcdefghijklmnopqrstuvwxyz':
    res[letter] = {}
    html_doc = requests.get(f"https://www.atlasdasaude.pt/doencasaaz/{letter}")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    doencas_div = soup.find_all("div", class_ = "views-row")
    for div in doencas_div:
        designacao = div.div.h3.a.text
        descricao = div.find("div", class_ = "views-field-body").div.text
        res[letter][designacao] = descricao

f_out = open("doencas_descricao.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii= False)    