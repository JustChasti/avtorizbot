import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create(user, passs, name):
    connection = psycopg2.connect(user=user, password=passs)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = cursor.execute("create database " + name)
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create("postgres", "qm7hFSIW", "test")
