#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta, date
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json

start_date = date(2017, 5, 19)
end_date = date(2017, 5, 20)

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)

for single_date in daterange(start_date, end_date):
	year = single_date.strftime("%Y")
	month = single_date.strftime("%m")
	day = single_date.strftime("%d")
	#exemplo de url sem concatenacao: "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=19%2F05%2F2017"
	my_url="http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="+day+"%2F"+month+"%2F"+year

	# abrindo conexao, puxando pagina
	uClient = uReq(my_url)
	page_html = uClient.read()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	# tb-pontos-de-alagamentos
	tabelas_com_tudo = page_soup.findAll('table', {"class":"tb-pontos-de-alagamentos"})
	enchentes = []

	for enchente in tabelas_com_tudo:
		local_hora_html = enchente.tr.find_next_sibling('tr').td.div.ul.li.find_next_sibling('li').find_next_sibling('li')
		referencia_sentido_html = enchente.tr.find_next_sibling('tr').td.div.ul.li.find_next_sibling('li').find_next_sibling('li').find_next_sibling('li').find_next_sibling('li')
		index_referencia = referencia_sentido_html.text.find('Referência:')

		referencia = referencia_sentido_html.text[index_referencia+12:]

		if not referencia.find('ALTURA DO NÚMERO'):
			numero = referencia[17:]
			referencia = numero

		enchentes.append({
			'data':year+'/'+month+'/'+day,
			'local' : local_hora_html.text[16:], 
			'referencia':referencia,
			'sentido':referencia_sentido_html.text[9:index_referencia],
			'bairro':enchente.tr.td.text.strip(),
			'hora_inicio':local_hora_html.text[3:8],
			'hora_fim':local_hora_html.text[11:16]
			})

if not enchentes:
	print(day,month,year, 'nao alagou')

elif enchentes!=0:
	nome_do_arquivo = 'enchentes_de_'+str(start_date.year)+'-'+str(start_date.month)+'-'+str(start_date.day)+'_a_'+str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day)+'.js'

	arquivo_js = open(nome_do_arquivo,'w')
	arquivo_js.write(json.dumps(enchentes, indent=2, sort_keys=True))
	arquivo_js.close()