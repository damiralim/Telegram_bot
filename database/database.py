import psycopg2 as ps2
from config import PostgreSQL
from loguru import logger
from typing import Union, List

''' Проверка подключения к БД '''

def test_bot_db_conn() -> ps2.extensions.connection:
    try:
        shelter_db_conn = ps2.connect(user="postgres",
                                    password=PostgreSQL,
                                    host="127.0.0.1",
                                    port="5432",
                                    database='shelter_bot_db')
        logger.info(f"Подключение к базе данных shelter_bot_db прошло успешно")
        return shelter_db_conn

    except ps2.Error as err:
        logger.exception(f'При подключении к базе данных shelter_bot_db возникла ошибка: {err}')

''' Создание таблицы в БД '''

def create_table() -> None:
    try:
        shelter_db_conn = test_bot_db_conn()
        with shelter_db_conn.cursor() as cursor:
            create_data_table = """CREATE TABLE IF NOT EXISTS shelter_tbl (
              session_id SERIAL PRIMARY KEY,
              user_id INTEGER NOT NULL,
              command VARCHAR(9) NOT NULL,
              datetime TIMESTAMP NOT NULL, 
              city VARCHAR(50) NOT NULL,
              location_id INTEGER NOT NULL,
              photo VARCHAR(3) NOT NULL, 
              hotels JSON NOT NULL
              );"""
            cursor.execute(create_data_table)
            shelter_db_conn.commit()

        logger.info("Создание таблицы с данными shelter прошло успешно")

    except ps2.Error as err:
        logger.exception(f'При создании таблицы с данными shelter возникла ошибка: {err}')

''' Подключение к дефолтному соединению и создание в нем БД бота '''

def connect_database() -> None:
    try:
        base_connection = ps2.connect(user="postgres",
                                     password=PostgreSQL,
                                     host="127.0.0.1",
                                     port="5432",
                                     database="postgres")

        ''' Проверка наличия БД в списке уже созданных баз '''

        with base_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_database WHERE datistemplate IS FALSE "
                           "AND datallowconn IS TRUE AND datname!='postgres';")
            for entry in cursor.fetchall():
                if 'shelter_bot_db' in entry:
                    logger.info(f"Повторное подключение к базе данных shelter_bot_db")
                    break
            else:
                base_connection.set_isolation_level(ps2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # установка уровня изоляции
                cursor.execute("CREATE DATABASE shelter_bot_db")
                logger.info("Создание базы данных shelter_bot_db прошло успешно")
                create_table()
                base_connection.commit()

    except ps2.Error as err:
        logger.exception(f'При работе с базой данных postgres возникла ошибка: {err}')

''' Вставка значений в БД '''

def insert_values(data_tup) -> None:
    try:
        shelter_db_conn = test_bot_db_conn()

        val_quantity: str = ", ".join(["%s"] * len(data_tup)) # подстановочная строка для вставки значений в БД
        with shelter_db_conn.cursor() as cursor:
            querystring = f"INSERT INTO shelter_tbl (user_id, command, datetime, city, location_id, photo, hotels) " \
                          f"VALUES ({val_quantity})"
            cursor.execute(querystring, data_tup)
            shelter_db_conn.commit()

        logger.info("Вставка значений в таблицу shelter_tbl прошла успешно")

    except ps2.Error as err:
        logger.exception(f'При вставке значений в таблицу shelter возникла ошибка: {err}')

''' Вывод истории из БД по user_id '''

def show_history(user_id) -> Union[str, list]:
    try:
        shelter_db_conn = test_bot_db_conn()

        with shelter_db_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM shelter_tbl WHERE user_id = {user_id}")
            db_history: List[str, int, dict] = cursor.fetchall()
            if db_history:
                return db_history
            return 'К сожалению, у вас пока нет истории поиска'

        logger.info("Запрос значений из таблицы shelter_tbl прошел успешно")

    except ps2.Error as err:
        logger.exception(f'При запросе значений из таблицы shelter возникла ошибка: {err}')



