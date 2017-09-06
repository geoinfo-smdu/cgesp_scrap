#!/usr/bin/python
# coding: utf8
# from datetime import timedelta, date
# from urllib.request import urlopen as uReq
# from bs4 import BeautifulSoup as soup
# import json
import geocoder
# start_date = date(2005, 2, 16)
# end_date = date(2005, 2, 18)

# def daterange(start_date, end_date):
#     for n in range(int ((end_date - start_date).days)):
#        yield start_date + timedelta(n)


def convertAscii(valor):
    utf8_ansi2 = [
        ("\u00c0", "À"),
        ("\u00c1", "Á"),
        ("\u00c2", "Â"),
        ("\u00c3", "Ã"),
        ("\u00c4", "Ä"),
        ("\u00c5", "Å"),
        ("\u00c6", "Æ"),
        ("\u00c7", "Ç"),
        ("\u00c8", "È"),
        ("\u00c9", "É"),
        ("\u00ca", "Ê"),
        ("\u00cb", "Ë"),
        ("\u00cc", "Ì"),
        ("\u00cd", "Í"),
        ("\u00ce", "Î"),
        ("\u00cf", "Ï"),
        ("\u00d1", "Ñ"),
        ("\u00d2", "Ò"),
        ("\u00d3", "Ó"),
        ("\u00d4", "Ô"),
        ("\u00d5", "Õ"),
        ("\u00d6", "Ö"),
        ("\u00d8", "Ø"),
        ("\u00d9", "Ù"),
        ("\u00da", "Ú"),
        ("\u00db", "Û"),
        ("\u00dc", "Ü"),
        ("\u00dd", "Ý"),
        ("\u00df", "ß"),
        ("\u00e0", "à"),
        ("\u00e1", "á"),
        ("\u00e2", "â"),
        ("\u00e3", "ã"),
        ("\u00e4", "ä"),
        ("\u00e5", "å"),
        ("\u00e6", "æ"),
        ("\u00e7", "ç"),
        ("\u00e8", "è"),
        ("\u00e9", "é"),
        ("\u00ea", "ê"),
        ("\u00eb", "ë"),
        ("\u00ec", "ì"),
        ("\u00ed", "í"),
        ("\u00ee", "î"),
        ("\u00ef", "ï"),
        ("\u00f0", "ð"),
        ("\u00f1", "ñ"),
        ("\u00f2", "ò"),
        ("\u00f3", "ó"),
        ("\u00f4", "ô"),
        ("\u00f5", "õ"),
        ("\u00f6", "ö"),
        ("\u00f8", "ø"),
        ("\u00f9", "ù"),
        ("\u00fa", "ú"),
        ("\u00fb", "û"),
        ("\u00fc", "ü"),
        ("\u00fd", "ý"),
        ("\u00ff", "ÿ")]
    for el in utf8_ansi2:
        if valor.lower() == el[0]:
            return el[1]


def correctToGeocode(logradouro):
    correcoes = [
        ('AV ', 'Avenida '),
        ('AV. ', 'Avenida '),
        ('AV CEL ', 'Avenida Coronel '),
        ('VD ', 'Viaduto '),
        ('R ', 'Rua '),
        ('R. ', 'Rua '),
        ('PTE ', 'Ponte '),
        ('PTE. ', 'Ponte '),
        ('LG ', 'Largo '),
        ('LG. ', 'Largo '),
        ('PC ', 'Praça '),
        ('PC. ', 'Praça '),
        ('R CEL ', 'Rua Coronel')]
    for el in correcoes:
        if logradouro == el[0]:
            return el[1]

# enchentes = []

# for single_date in daterange(start_date, end_date):
#     year = single_date.strftime("%Y")
#     month = single_date.strftime("%m")
#     day = single_date.strftime("%d")
#     #exemplo de url sem concatenacao: "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=19%2F05%2F2017"
#     my_url="http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="+day+"%2F"+month+"%2F"+year
#     data = int(year+month+day)

#     # abrindo conexao, puxando pagina
#     uClient = uReq(my_url)
#     page_html = uClient.read()

#     # html parsing
#     page_soup = soup(page_html, "html.parser")

#     nao_alagou = page_soup.find_all(string='Não há registros de alagamentos para essa data.')
#     if nao_alagou:
#        enchentes.append({'data':data})

#     if not nao_alagou:# ou seja, alagou.

#        # tb-pontos-de-alagamentos
#        tabelas_com_tudo = page_soup.findAll('table', {"class":"tb-pontos-de-alagamentos"})

#        for enchente in tabelas_com_tudo:
#          local_hora_html = enchente.tr.find_next_sibling('tr').td.div.ul.li.find_next_sibling('li').find_next_sibling('li')
#          referencia_sentido_html = enchente.tr.find_next_sibling('tr').td.div.ul.li.find_next_sibling('li').find_next_sibling('li').find_next_sibling('li').find_next_sibling('li')

#          local = local_hora_html.text[16:]
#          index_referencia = referencia_sentido_html.text.find('Referência:')
#          referencia = referencia_sentido_html.text[index_referencia+12:]
#          # referencia numerica retorna apenas numero
#          if not referencia.find('ALTURA DO NÚMERO'):
#           numero = referencia[17:]
#           referencia = numero

#          if not referencia.find('ALTURA DO N.'):
#           numero = referencia[13:]
#           referencia = numero

#          sentido = referencia_sentido_html.text[9:index_referencia]
#          bairro = enchente.tr.td.text.strip()
#          hora_inicio = local_hora_html.text[3:8]
#          hora_fim = local_hora_html.text[11:16]

#          # execoes para enchentes ativos
#          intransitavel = enchente.tr.find_next_sibling('tr').td.div.ul.findAll('li',{'class':'ativo-intransitavel'})
#          if intransitavel:
#           hora_fim = 'sem hora fim'
#           local = local_hora_html.text[11:]

#          enchentes.append({
#           'data':data,
#           'local':local,
#           'referencia':referencia,
#           'sentido':sentido,
#           'bairro':bairro,
#           'hora_inicio':hora_inicio,
#           'hora_fim':hora_fim,
#           'geocode_address':'',
#           'latlgd':''
#           })


enchentes = [
    {
        "data": 20050216
    },
    {
        "bairro": "S\u00e9",
        "data": 20050217,
        "hora_fim": "17:57",
        "hora_inicio": "16:56",
        "local": "R. MANOEL DUTRA",
        "referencia": "PC. QUATORZE BIS",
        "sentido": "UNICO", 
    },
    {
        "bairro": "Butant\u00e3",
        "data": 20050217,
        "hora_fim": "17:50",
        "hora_inicio": "16:56",
        "local": "AV PROF FRANCISCO MORATO",
        "referencia": "PC. PAULA MOREIRA",
        "sentido": "AMBOS",
    },
    {
        "bairro": "Vila Mariana",
        "data": 20050217,
        "hora_fim": "17:50",
        "hora_inicio": "17:18",
        "local": "AV. DR RICARDO JAFET",
        "referencia": "1734",
        "sentido": "SP/STOS",
    }
]

correcoes = [
    ('AV. PROF. ', 'Avenida Professor '),
    ('AV. PROF ', 'Avenida Professor '),
    ('AV PROF ', 'Avenida Professor '),
    ('AV. CEL. ', 'Avenida Coronel '),
    ('AV. CEL ', 'Avenida Coronel '),
    ('AV CEL ', 'Avenida Coronel '),
    ('AV. DR. ', 'Avenida Doutor '),
    ('AV. DR ', 'Avenida Doutor '),
    ('AV DR ', 'Avenida Doutor '),
    ('AV. ', 'Avenida '),
    ('AV ', 'Avenida '),

    ('VD. ', 'Viaduto '),
    ('VD ', 'Viaduto '),

    ('PTE. ', 'Ponte '),
    ('PTE ', 'Ponte '),

    ('LG. ', 'Largo '),
    ('LG ', 'Largo '),

    ('PCA. ', 'Praça '),
    ('PCA ', 'Praça '),
    ('PC. ', 'Praça '),
    ('PC ', 'Praça '),

    ('R. CEL. ', 'Rua Coronel'),
    ('R CEL ', 'Rua Coronel'),
    ('R. ', 'Rua '),
    ('R ', 'Rua ')

]

for s in enchentes:
    if len(s) > 1:
        for r in correcoes:
            if s['local'].find(r[0]) > -1:  # se precisa corrigir
                local_corrigido = s['local'].replace(r[0], r[1]).lower()
                s['local'] = local_corrigido

            if s['referencia'].find(r[0]) > -1:  # se precisa corrigir
                referencia_corrigida = s[
                    'referencia'].replace(r[0], r[1]).lower()
                s['referencia'] = referencia_corrigida

        if s['referencia'].isdigit():
            s['geocode_address'] = s['local'] + ', ' + s['referencia'] + ', ' + s['bairro'] + ', São Paulo - SP, Brazil'
            s['latlgd'] = geocoder.google(s['geocode_address']).latlng

        elif not s['referencia'].isdigit():
            s['geocode_address'] = s['local'] + ' AND '+ s['referencia'] + ', São Paulo - SP, Brazil'
            s['latlgd'] = geocoder.google(s['geocode_address']).latlng
print(enchentes)


# if enchentes!=0:
#     nome_do_arquivo = 'enchentes_de_'+str(start_date.year)+'-'+str(start_date.month)+'-'+str(start_date.day)+'_a_'+str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day-1)+'.js'
#     arquivo_js = open(nome_do_arquivo,'w')
#     arquivo_js.write(json.dumps(enchentes, indent=4, sort_keys=True))
#     arquivo_js.close()
