# cgesp_scrap
Extração de endereços dos pontos de alagamentos da página https://www.cgesp.org/v3/alagamentos.jsp e subsequente conversão dos pontos em coordenadas.

## Objetivo
Extrair dados de pontos de alagamentos de hoje até 2005.

### Pré-requisitos
- Python 3.6.X([Instruções](https://www.python.org/downloads/))

### Setup
Instalar as seguintes bibliotecas python
```
virtualenv env # criar o ambiente virtual
env\Scripts\activate # ativar o ambiente virtual
pip install -r requirements.txt # instalar as dependencias de python
```


## Para extrair os dados
Abrir o arquivo 'script.py'. 

Alterar os parâmetros "start_date" e "end_date"
```
start_date = date(2015, 4, 13)
end_date = date(2015, 4, 15)
```

abrir o terminal ou prompt e digitar:
```
python scrap.py
```
