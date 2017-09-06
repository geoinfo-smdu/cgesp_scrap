#!/usr/bin/python
# coding: utf8
from datetime import timedelta, date
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import geocoder

start_date = date(2017, 5, 5)
end_date = date(2017, 5, 6) 

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
       yield start_date + timedelta(n)

enchentes = []
failed_geocoding = []

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
       tabelas_com_tudo = page_soup.findAll('table', {"class":"tb-pontos-de-alagamentos"})

       for enchente in tabelas_com_tudo:
         local_hora_html = enchente.tr.find_next_sibling('tr').td.div.ul.li.find_next_sibling('li').find_next_sibling('li')
         referencia_sentido_html = enchente.tr.find_next_sibling('tr').td.div.ul.li.find_next_sibling('li').find_next_sibling('li').find_next_sibling('li').find_next_sibling('li')

         local = local_hora_html.text[16:]
         index_referencia = referencia_sentido_html.text.find('Referência:')
         referencia = referencia_sentido_html.text[index_referencia+12:]
#          # referencia numerica retorna apenas numero
         if not referencia.find('ALTURA DO NÚMERO'):
          numero = referencia[17:]
          referencia = numero

         if not referencia.find('ALTURA DO N.'):
          numero = referencia[13:]
          referencia = numero

         sentido = referencia_sentido_html.text[9:index_referencia]
         bairro = enchente.tr.td.text.strip()
         hora_inicio = local_hora_html.text[3:8]
         hora_fim = local_hora_html.text[11:16]

         # execoes para enchentes ativos
         intransitavel = enchente.tr.find_next_sibling('tr').td.div.ul.findAll('li',{'class':'ativo-intransitavel'})

         if intransitavel:
          hora_fim = 'sem hora fim'
          local = local_hora_html.text[11:]
          print(local)
#          enchentes.append({
#           'data':data,
#           'local':local.lower(),
#           'referencia':referencia.lower(),
#           'sentido':sentido.lower(),
#           'bairro':bairro.lower(),
#           'hora_inicio':hora_inicio,
#           'hora_fim':hora_fim,
#           'geocode_address':'',
#           'latlgd':''
#           })

# correcoes = [
#     ('av. prof. ', 'avenida professor '),
#     ('av. prof ', 'avenida professor '),
#     ('av prof ', 'avenida professor '),
#     ('av. gal. ', 'avenida general '),
#     ('av. gal ', 'avenida general '),
#     ('av gal ', 'avenida general '),
#     ('av. eng. ', 'avenida engenheiro '),
#     ('av. eng ', 'avenida engenheiro '),
#     ('av eng ', 'avenida engenheiro '),
#     ('av. cel. ', 'avenida coronel '),
#     ('av. cel ', 'avenida coronel '),
#     ('av cel ', 'avenida coronel '),
#     ('av. dr. ', 'avenida doutor '),
#     ('av. dr ', 'avenida doutor '),
#     ('av dr ', 'avenida doutor '),
#     ('av. ', 'avenida '),
#     ('av ', 'avenida '),

#     ('vd. gal. ', 'viaduto general '),
#     ('vd. gal ', 'viaduto general '),
#     ('vd gal ', 'viaduto general '),
#     ('vd. eng. ', 'viaduto engenheiro '),
#     ('vd. eng ', 'viaduto engenheiro '),
#     ('vd eng ', 'viaduto engenheiro '),
#     ('vd. dr. ', 'viaduto doutor '),
#     ('vd. dr ', 'viaduto doutor '),
#     ('vd dr ', 'viaduto doutor '),
#     ('vd. ', 'viaduto '),
#     ('vd ', 'viaduto '),

#     ('pte. ', 'ponte '),
#     ('pte ', 'ponte '),

#     ('lgo. ', 'largo '),
#     ('lgo ', 'largo '),
#     ('lg. ', 'largo '),
#     ('lg ', 'largo '),

#     ('pca. ', 'praça '),
#     ('pca ', 'praça '),
#     ('pc. ', 'praça '),
#     ('pc ', 'praça '),

#     ('rua prof. ', 'rua professor '),
#     ('rua prof ', 'rua professor '),    
#     ('rua gal. ', 'rua general '),
#     ('rua gal ', 'rua general '),
#     ('rua eng. ', 'rua engenheiro '),
#     ('rua eng ', 'rua engenheiro '),
#     ('rua dr. ', 'rua doutor '),
#     ('rua dr ', 'rua doutor '),
#     ('r. dr. ', 'rua doutor '),
#     ('r. cel. ', 'rua coronel '),
#     ('r cel ', 'rua coronel '),
#     ('r. ', 'rua ')
#     # ('r ', 'rua ') # da pau com todas as palavras terminas em 'r ' 
# ]

# for s in enchentes:

#     if len(s) > 1:

#         for r in correcoes:
#             if s['local'].find(r[0]) > -1:  # se precisa corrigir local
#                 local_corrigido = s['local'].replace(r[0], r[1]).lower()
#                 s['local'] = local_corrigido

#             if s['referencia'].find(r[0]) > -1:  # se precisa corrigir referencia
#                 referencia_corrigida = s['referencia'].replace(r[0], r[1]).lower()
#                 s['referencia'] = referencia_corrigida

#             else:
#                 s['local'] = s['local'].lower()
#                 s['referencia'] = s['referencia'].lower()
#                 s['sentido'] = s['sentido'].lower()

#         if s['referencia'].isdigit():
#             s['geocode_address'] = s['local'] + ', ' + s['referencia'] + ', ' + s['bairro'] + ', São Paulo - SP, Brazil'
#             s['latlgd'] = geocoder.google(s['geocode_address']).latlng

#         elif not s['referencia'].isdigit(): # se nao ha numero 
#             s['geocode_address'] = s['local'] + ' AND '+ s['referencia'] + ', São Paulo - SP, Brazil'

#             if s['referencia'].find(' - ') != -1: #remover - '50 metro apos', '100 metro antes' e outros comentarios que antecedem o endereco 
#                 index = s['referencia'].find(' - ')
#                 s['referencia'] = s['referencia'][0:index]
#                 s['geocode_address'] = s['local'] + ' AND ' + s['referencia'] + ', São Paulo - SP, Brazil'

#             elif s['local'][0:5] == 'ponte':
#                 s['geocode_address'] = s['local'] +', ' +s['bairro'] + ', São Paulo - SP, Brazil' 

#             elif s['referencia'][0:5] == 'ponte':
#                 s['geocode_address'] = s['referencia'] +', ' +s['bairro'] + ', São Paulo - SP, Brazil' 

#             elif s['local'][0:5] == 'praça':
#                 s['geocode_addrss'] = s['local'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'

#             elif s['referencia'][0:5] == 'praça':
#                 s['geocode_addrss'] = s['referencia'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'

#             s['latlgd'] = geocoder.google(s['geocode_address']).latlng

#             if geocoder.google(s['geocode_address']).ok == False:
#               if s['local'][0:7] == 'viaduto':
#                 s['geocode_addrss'] = s['local'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'
#               if s['referencia'][0:7] == 'viaduto':
#                 s['geocode_addrss'] = s['referencia'] +', '+s['bairro'] + ', São Paulo - SP, Brazil'

#               print('nao-localizados: ' + s['geocode_address'])
#               failed_geocoding.append(s)

#         # if not s['latlgd']:
#         #   print('nao-localizados: ' + s['geocode_address'])
#         #   failed_geocoding.append(s)

# if enchentes!=0:
#     nome_do_arquivo = 'enchentes_de_'+str(start_date.year)+'-'+str(start_date.month)+'-'+str(start_date.day)+'_a_'+str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day)+'.js'
#     arquivo_js = open(nome_do_arquivo,'w')
#     content = json.dumps(enchentes, indent=4, sort_keys=True,ensure_ascii=False)
#     arquivo_js.write(content)
#     arquivo_js.close()

# if failed_geocoding!=0:
#     nome_do_arquivo = 'enchentes_de_'+str(start_date.year)+'-'+str(start_date.month)+'-'+str(start_date.day)+'_a_'+str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day)+'_failed.js'          
#     arquivo_js = open(nome_do_arquivo,'w')
#     content = json.dumps(failed_geocoding, indent=4, sort_keys=True,ensure_ascii=False)
#     arquivo_js.write(content)
#     arquivo_js.close()

# else:
#     print('nao alagou neste periodo')

# print('localizados: ', len(enchentes))
# print('nao-localizados: ', len(failed_geocoding))


# not: marginal tiete AND ponte velha fepasa, São Paulo - SP, Brazil
# not: avenida prestes maia AND passarela das noivas, São Paulo - SP, Brazil
# not: viaduto antartica AND praça luiz carlos mesquita, São Paulo - SP, Brazil
# not: avenida eusebio matoso AND praça jorge de lima  50m antes, São Paulo - SP, Brazil
# not: viaduto leste-oeste AND viaduto do glicerio, São Paulo - SP, Brazil
# not: rua john harrison AND praça rene barreto, São Paulo - SP, Brazil
# not: marginal pinheiros AND ponte eusebio matoso, São Paulo - SP, Brazil
# not: avenida aricanduva AND rua afonso sampaio e souza, São Paulo - SP, Brazil
# not: ponte bernardo goldfarb AND no inicio e fim da mesma, São Paulo - SP, Brazil
# not: avenida eusebio matoso AND praça antonio sabino, São Paulo - SP, Brazil
# not: rua prof. martim damy AND avenida conde de frontin, São Paulo - SP, Brazil
# not: viaduto bresser AND rua coronelantonio marcelo, São Paulo - SP, Brazil
# not: avenida conde de frontin AND rua joaquim marra, São Paulo - SP, Brazil
# not: avenida paes de barros AND avenida professor luiz ignacio anhaia mello, São Paulo - SP, Brazil
# not: avenida vinte e tres de maio AND viaduto gal euclides figueiredo, São Paulo - SP, Brazil
# not: avenida inajar de souza AND avenida gen. penha brasil, São Paulo - SP, Brazil
# not: avenida conde de frontin AND acesso  para o elevado aricanduva, São Paulo - SP, Brazil
# not: avenida cruzeiro do sul AND rua darzan / avenida gal ataliba leonel, São Paulo - SP, Brazil
# not: avenida paulo freire educador AND acesso marg. tietê, São Paulo - SP, Brazil
# not: rua john harrison AND praça rene barreto, São Paulo - SP, Brazil
# not: marginal pinheiros AND viaduto republica da armenia, São Paulo - SP, Brazil
# not: ponte aricanduva AND no incio da mesma, São Paulo - SP, Brazil
# not: avenida ragueb chohfi AND tobogã, São Paulo - SP, Brazil
# not: rua costa barros AND rua sao raimundo, São Paulo - SP, Brazil
# not: marginal tiete AND saída  da alça  ponte cruzeiro do sul, São Paulo - SP, Brazil
# not: praça jorge de lima AND avenida vital brasil, São Paulo - SP, Brazil