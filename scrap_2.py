from datetime import timedelta, date
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
# import json

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)
start_date = date(2017, 5, 19)
end_date = date(2017, 5, 22)

# loop funcionando
for single_date in daterange(start_date, end_date):
	year = single_date.strftime("%Y")
	month = single_date.strftime("%m")
	day = single_date.strftime("%d")
	# print(year,month,day)
	my_url="http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="+day+"%2F"+month+"%2F"+year

	# opening a connection, grabbing page
	uClient = uReq(my_url)
	page_html = uClient.read()

	# # html parsing
	page_soup = soup(page_html, "html.parser")

	# # horario e local
	hora_local = page_soup.findAll("li",{"class":"arial-descr-alag col-local"})

	enchentes = []

	for enchente in hora_local:
		local = enchente.text[16:]	
		hora_inicio = enchente.text[3:8]
		hora_final = enchente.text[11:16]

		enchentes.append({
			'data':day+'/'+month+'/'+year, 
			'local':local,
			'hora_inicio':hora_inicio,
			'hora_final':hora_final
		})

	if not enchentes:
		print(day,month,year, 'nao alagou')

	elif enchentes!=0:
		for enchente in enchentes:
			print(day,month,year, enchente)


