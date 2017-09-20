# cgesp_scrap
Extração de endereços dos pontos de alagamentos da página https://www.cgesp.org/v3/alagamentos.jsp e subsequente conversão dos pontos em coordenadas.

## Objetivo
Extrair dados de pontos de alagamentos de hoje até 2005.

### Pré-requisitos
- Python ([Instruções](https://www.python.org/downloads/))

### Setup
Instalar as seguintes bibliotecas python
- datetime 
- urllib.request
- bs4
- json
- geocoder

- Para instalar os recursos, digitar no terminal ou prompt:
```
pip install nomedabiblioteca
```

## Para extrair os dados

Feito o setup, alterar os parâmetros (para testes recomendamos não que 10 dias):
```
start_date = date(2015, 4, 13)
end_date = date(2015, 4, 15)
```

baixar o arquivo 'script.py' abrir o terminal ou prompt e digitar:
```
python script.py
```
