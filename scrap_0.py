from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url="http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=02%2F02%2F2015"

# opening a connection, grabbing page
uClient = uReq(my_url)
page_html = uClient.read()

# html parsing
page_soup = soup(page_html, "html.parser")

# horario e local
hora_local = page_soup.findAll("li",{"class":"arial-descr-alag col-local"})

enchentes = []

for enchente in hora_local:
	local = enchente.text[16:]	
	hora_inicio = enchente.text[3:8]
	hora_final = enchente.text[11:16]

	enchentes.append({
		'local':local,
		'hora_inicio':hora_inicio,
		'hora_final':hora_final
	})

print(enchentes)
