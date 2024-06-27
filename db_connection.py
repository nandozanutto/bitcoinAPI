import mysql.connector
from mysql.connector import Error
import configparser
import pandas as pd
from tabulate import tabulate


def read_db_config(filename='db_config.ini', section='mysql'):
    parser = configparser.ConfigParser()
    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db_config


def connect_database():
    try:
        config = read_db_config()
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
        else:
            return -1
    except Error as e:
        print("Erro ao conectar ao MySQL", e)

def create_table_coins(connection, cursor, df_coins):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS coins_prices (
        id INT,
        market_cap DECIMAL(38, 2),
        price DECIMAL(20, 8),
        last_updated DATETIME
    )
    """
    try:
        cursor.execute(create_table_query)
        for index, row in df_coins.iterrows():
            insert_query = """
            INSERT INTO coins_prices (id, market_cap, price, last_updated) VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))
        
        connection.commit()
    except Error as e:
        print("Erro ao criar a tabela de coins", e)

def check_table_exists(connection, cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

def create_table_names(connection, cursor, df_names):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS coins_names (
        id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        symbol VARCHAR(10) NOT NULL,
        logo VARCHAR(255),
        category VARCHAR(50),
        description TEXT,
        website VARCHAR(255),
        PRIMARY KEY (id)
    )
    """
    try:
        cursor.execute(create_table_query)
        for index, row in df_names.iterrows():
            insert_query = """
            INSERT INTO coins_names (id, name, symbol, logo, category, description, website) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))
        
        connection.commit()
    except Error as e:
        print("Erro ao criar a tabela de names", e)

def get_ids_names(connection, cursor):
    #essa função retorna os ids das moedas que já existem na tabela coins_names
    cursor.execute("SELECT id FROM coins_names")
    records = cursor.fetchall()
    return records

def print_names(cursor):
    #não imprimi todas as informações pq fica dificil de visualizar
    query = "SELECT id, name, symbol, category FROM coins_names"
    cursor.execute(query)
    results = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(results, columns=columns)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def print_values(cursor):
    query = "SELECT * FROM coins_prices"
    cursor.execute(query)
    results = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(results, columns=columns)
    print(tabulate(df, headers='keys', tablefmt='psql'))