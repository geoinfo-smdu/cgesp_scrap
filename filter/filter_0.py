#!/usr/bin/python
# coding: utf8
import ast
import json
cf_original = open("com_falhas.js", "r", encoding="utf-8")
com_falhas = cf_original.read()
com_falhas_list = ast.literal_eval(com_falhas)

corretor_original = open('corretor_2017-7-13__2016-12-13.js','r')
corretor = corretor_original.read()
corretor_list = ast.literal_eval(corretor)

corrigidos = []

for failed in com_falhas_list:
    for correctus in corretor_list:
        if len(correctus)>1:
            if not failed['latlgd']:
                if correctus['geocode_address'] == failed['geocode_address']:
                   coords_corrigido  = correctus['latlgd']
        else:
            coords_corrigido = failed['latlgd']

    corrigidos.append({
    "bairro":failed['bairro'],
    "data": failed['data'],
    "geocode_address": failed['geocode_address'],
    "hora_fim": failed['hora_fim'],
    "hora_inicio": failed['hora_inicio'],
    "latlgd":coords_corrigido,
    "local": failed["local"],
    "referencia": failed["referencia"],
    "sentido": failed["sentido"]
    })
    coords_corrigido = []

file = open('corrigidos.js','w')
content = json.dumps(corrigidos, indent=4, sort_keys=True,ensure_ascii=False)
file.write(content)

file.close()
cf_original.close()
corretor_original.close()

print('originais: ',len(com_falhas_list))
print('corrigidos: ',len(corrigidos))