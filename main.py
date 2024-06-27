import bitcoin_api as bt
import pandas as pd
import db_connection as db
import json

def main():
    with open('api_key.json', 'r') as file:
        config = json.load(file)
        api_key = config["api_key"]

    total_cryptocurrencies = 5  #quantidade total de criptomoedas a extrair
    batch_size = 5 #quantidade de criptomoedas a extrair a cada chamada de api

    df_coins = bt.get_data_coins(total_cryptocurrencies, batch_size, api_key)#extraindo os dados financeiros das moedas
    conn = db.connect_database()
    cursor = conn.cursor()
    db.create_table_coins(conn, cursor, df_coins)#colocando os dados no bd

    df_coins_id_list = df_coins["id"].to_list()
    if not db.check_table_exists(conn, cursor, "coins_names"):
        #se a tabela de meta dados das moedas ainda não existe então pesquise os metadados
        #sobre todas as moedas extraidas, utilizando o id
        df_names = bt.get_data_names(df_coins_id_list, api_key)
        db.create_table_names(conn, cursor, df_names)
    else:
        #se a tabela de meta dados já existe então pesquise meta dados somente sobre as moedas
        #que ainda não conheço
        ids = db.get_ids_names(conn, cursor)
        ids = [item[0] for item in ids]
        subtracted = [item for item in df_coins_id_list if item not in ids]
        df_names = bt.get_data_names(subtracted, api_key)
        db.create_table_names(conn, cursor, df_names)

    #imprimindo o estado final das duas tabelas
    db.print_names(cursor)
    db.print_values(cursor)


    cursor.close()
    conn.close()    

if __name__ == "__main__":
    main()