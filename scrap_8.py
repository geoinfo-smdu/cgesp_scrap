#!/usr/bin/python
# coding: utf8
from datetime import timedelta, date
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import geocoder

start_date = date(2015, 4, 13)
end_date = date(2015, 4, 15)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
       yield start_date + timedelta(n)

enchentes = []
failed_geocoding = []
geocoded = 0

for single_date in daterange(start_date, end_date):
    year = single_date.strftime("%Y")
    month = single_date.strftime("%m")
    day = single_date.strftime("%d")
    #exemplo de url sem concatenacao: "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=19%2F05%2F2017"
    my_url="http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="+day+"%2F"+month+"%2F"+year
    data = int(year+month+day)

    # abrindo conexao, puxando pagina
    uClient = uReq(my_url)
    page_html = uClient.read()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    nao_alagou = page_soup.find_all(string='Não há registros de alagamentos para essa data.')
    if nao_alagou:
       enchentes.append({'data':data})

    if not nao_alagou:# ou seja, alagou.

       # tb-pontos-de-alagamentos
       tabelas_com_tudo = page_soup.findAll('div', {"class":"ponto-de-alagamento"})
       for enchente in tabelas_com_tudo:
         local_hora_html = enchente.find('li',{"class":"arial-descr-alag col-local"})
         referencia_sentido_html = enchente.ul.li.find_next_sibling('li').find_next_sibling('li').find_next_sibling('li').find_next_sibling('li')

         checa_local = local_hora_html.text[11:13]
         if checa_local.isdigit():
           local = local_hora_html.text[16:]
         elif not checa_local.isdigit():
           local = local_hora_html.text[11:]

         if local[-1] == ',':
          local = local[:-1]

         index_referencia = referencia_sentido_html.text.find('Referência:')
         referencia = referencia_sentido_html.text[index_referencia+12:]

         # se referencia tem alt e palavra numerica retorna apenas o numero
         if not referencia.find('ALT'):
          refArr = referencia.split()
          for number in refArr:
            if number.isdigit():
              referencia = number 

         sentido = referencia_sentido_html.text[9:index_referencia]
         bairro = enchente.parent.parent.parent.tr.td.text.strip()

         hora_inicio = local_hora_html.text[3:8]
         hora_fim = local_hora_html.text[11:16]

         if not hora_fim[:2].isdigit():
           hora_fim = 'sem hora fim'
           # local = local_hora_html.text[11:]

         print('pontos:',local,'/', bairro)

         enchentes.append({
          'data':data,
          'local':local.lower(),
          'referencia':referencia.lower(),
          'sentido':sentido.lower(),
          'bairro':bairro.lower(),
          'hora_inicio':hora_inicio,
          'hora_fim':hora_fim,
          'geocode_address':'',
          'latlgd':''
          })


correcoes = [
    ('ponte hirant sanazar', 'ponte do jaguare '),
    ('av. prof. ', 'avenida professor '),
    ('av. prof ', 'avenida professor '),
    ('av prof ', 'avenida professor '),
    ('av. gal. ', 'avenida general '),
    ('av. gal ', 'avenida general '),
    ('av gal ', 'avenida general '),
    ('av. eng. ', 'avenida engenheiro '),
    ('av. eng ', 'avenida engenheiro '),
    ('av eng ', 'avenida engenheiro '),
    ('av. cel. ', 'avenida coronel '),
    ('av. cel ', 'avenida coronel '),
    ('av cel ', 'avenida coronel '),
    ('av. dr. ', 'avenida doutor '),
    ('av. dr ', 'avenida doutor '),
    ('av dr ', 'avenida doutor '),
    ('av. ', 'avenida '),
    ('av ', 'avenida '),

    ('vd. gal. ', 'viaduto general '),
    ('vd. gal ', 'viaduto general '),
    ('vd gal ', 'viaduto general '),
    ('vd. eng. ', 'viaduto engenheiro '),
    ('vd. eng ', 'viaduto engenheiro '),
    ('vd eng ', 'viaduto engenheiro '),
    ('vd. dr. ', 'viaduto doutor '),
    ('vd. dr ', 'viaduto doutor '),
    ('vd dr ', 'viaduto doutor '),
    ('vd. ', 'viaduto '),
    ('vd ', 'viaduto '),

    ('pte. ', 'ponte '),
    ('pte ', 'ponte '),

    ('tn. ', 'túnel '),
    ('tn ', 'túnel '),

    ('lgo. ', 'largo '),
    ('lgo ', 'largo '),
    ('lg. ', 'largo '),
    ('lg ', 'largo '),

    ('pca. ', 'praça '),
    ('pca ', 'praça '),
    ('pc. ', 'praça '),
    ('pc ', 'praça '),

    ('altura do nº', ' '),
    ('altura do n.', ' '),
    ('altura do n', ' '),

    ('rua prof. ', 'rua professor '),
    ('rua prof ', 'rua professor '),    
    ('rua gal. ', 'rua general '),
    ('rua gal ', 'rua general '),
    ('rua eng. ', 'rua engenheiro '),
    ('rua eng ', 'rua engenheiro '),
    ('rua dr. ', 'rua doutor '),
    ('rua dr ', 'rua doutor '),
    ('r. dr. ', 'rua doutor '),
    ('r. cel. ', 'rua coronel '),
    ('r cel ', 'rua coronel '),

    ('r olivia', 'rua olívia'),
    ('r samarita', 'rua samritá'),
    ('r sumidouro', 'rua sumidouro'),
    ('avenida das nacoes unidas', 'avenida das nações unidas'),
    ('r. ', 'rua ')
]

for s in enchentes:

    if len(s) > 1:

        for r in correcoes:
            if s['local'].find(r[0]) > -1:  # se precisa corrigir local
                local_corrigido = s['local'].replace(r[0], r[1]).lower()
                s['local'] = local_corrigido

            if s['referencia'].find(r[0]) > -1:  # se precisa corrigir referencia
                referencia_corrigida = s['referencia'].replace(r[0], r[1]).lower()
                s['referencia'] = referencia_corrigida

            else:
                s['local'] = s['local'].lower()
                s['referencia'] = s['referencia'].lower()
                s['sentido'] = s['sentido'].lower()

        if s['referencia'].isdigit():
            s['geocode_address'] = s['local'] + ', ' + s['referencia'] + ', ' + s['bairro'] + ', São Paulo - SP, Brazil'
            s['latlgd'] = geocoder.google(s['geocode_address']).latlng

        elif not s['referencia'].isdigit(): # se nao ha numero 
            s['geocode_address'] = s['local'] + ' AND '+ s['referencia'] + ', São Paulo - SP, Brazil'

            if s['referencia'].find(' - ') != -1: #remover - '50 metro apos', '100 metro antes' e outros comentarios que antecedem o endereco 
                index = s['referencia'].find(' - ')
                s['referencia'] = s['referencia'][0:index]
                s['geocode_address'] = s['local'] + ' AND ' + s['referencia'] + ', São Paulo - SP, Brazil'

            elif s['local'][0:5] == 'ponte':
                s['geocode_address'] = s['local'] +', ' +s['bairro'] + ', São Paulo - SP, Brazil' 

            elif s['referencia'][0:5] == 'ponte':
                s['geocode_address'] = s['referencia'] +', ' +s['bairro'] + ', São Paulo - SP, Brazil' 

            elif s['local'][0:5] == 'praça':
                s['geocode_address'] = s['local'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'

            elif s['referencia'][0:5] == 'praça':
                s['geocode_address'] = s['referencia'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'

            s['latlgd'] = geocoder.google(s['geocode_address']).latlng

            if geocoder.google(s['geocode_address']).ok == False:
              if s['local'][0:7] == 'viaduto':
                s['geocode_address'] = s['local'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'
              if s['referencia'][0:7] == 'viaduto':
                s['geocode_address'] = s['referencia'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'

              print('nao-localizados: ' + s['geocode_address'], s['data'])
              failed_geocoding.append(s)
  
            geocoded = geocoded+1

if enchentes!=0:
    nome_do_arquivo = 'enchentes_de_'+str(start_date.year)+'-'+str(start_date.month)+'-'+str(start_date.day)+'_a_'+str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day)+'.js'
    arquivo_js = open(nome_do_arquivo,'w')
    content = json.dumps(enchentes, indent=4, sort_keys=True,ensure_ascii=False)
    arquivo_js.write(content)
    arquivo_js.close()

if failed_geocoding!=0:
    nome_do_arquivo = 'enchentes_de_'+str(start_date.year)+'-'+str(start_date.month)+'-'+str(start_date.day)+'_a_'+str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day)+'_failed.js'          
    arquivo_js = open(nome_do_arquivo,'w')
    content = json.dumps(failed_geocoding, indent=4, sort_keys=True,ensure_ascii=False)
    arquivo_js.write(content)
    arquivo_js.close()

else:
    print('nao alagou neste periodo')

print('localizados: ', geocoded)
print('nao-localizados: ', len(failed_geocoding))

