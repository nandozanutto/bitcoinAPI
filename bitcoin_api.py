import requests
import pandas as pd
from datetime import datetime

def convert_to_mysql_format(iso_date):
    datetime_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

def get_cryptocurrency_data(start, api_key, limit=10):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': start,
        'limit': limit,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()

def get_cryptocurrency_names(id_list, api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    parameters = {
        'id': id_list
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()

def get_data_coins(total_cryptocurrencies, batch_size, api_key):
    #esta função consulta os dados da api com paginação, para lidar com limitações da api
    lista = []
    for start in range(1, total_cryptocurrencies + 1, batch_size):
        data = get_cryptocurrency_data(start, api_key, batch_size)
        if 'data' in data:
            for currency in data['data']:
                new_row = [currency['id'], currency['quote']['USD']['market_cap'], currency['quote']['USD']['price'], currency['quote']['USD']['last_updated']]
                lista.append(new_row)#adiciona os dados em uma lista para depois juntá-los em um dataframe
        else:
            print(f"Erro na requisição para start={start}: {data['status']['error_message']}")
    df_coins = pd.DataFrame(lista, columns = ['id', 'market_cap', 'price', 'last_updated'])
    df_coins["last_updated"] = df_coins["last_updated"].apply(convert_to_mysql_format)

    return df_coins

def get_data_names(lista_ids, api_key):
    """
    esta função utiliza uma lista de ids como entrada para extrair da api o nome de moedas.
    Para lidar com limitações da api chunks é uma variável que salva a lista de ids em 'pedaços',
    ou seja, em uma lista de listas. Por exemplo se a lista de ids é [1,2,3,4,5,6,7,8,9,10] chunks
    será [[1,2,3,4,5],[6,7,8,9,10]]
    """
    batch_size = 5
    #lista_ids = ids_to_search.to_list()
    chunks = [lista_ids[x:x+batch_size] for x in range(0, len(lista_ids), batch_size)]
    lista = []
    for chunk in chunks:
        string_ids = ','.join(str(x) for x in chunk)
        info_data = get_cryptocurrency_names(string_ids, api_key)
        for id in chunk:
            if 'data' in info_data and str(id) in info_data['data']:
                info = info_data['data'][str(id)]
                new_row = [id, info['name'], info['symbol'], info['logo'], info['category'], info['description'], info['urls']['website'][0]]
                lista.append(new_row)
            else:
                print(f"Erro: {info_data['status']['error_message']}")


    df_metaData = pd.DataFrame(lista, columns = ['id','name', 'symbol', 'logo', 'category', 'description', 'website'])
    return df_metaData
