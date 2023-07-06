import psycopg2
import datetime


def init_connection(database: str, user: str, password: str, host: str,
                    port: int) -> psycopg2.extensions.connection | None:
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, host=host,
                                port=port)
        return conn
    except:
        return None


def add_table(conn: psycopg2.extensions.connection, table_name: str, columns: str) -> bool:
    # columns contains all [name  type ] seperated by comma
    cur = conn.cursor()
    try:
        query = "CREATE TABLE IF NOT EXISTS {} (id serial PRIMARY KEY, {});".format(table_name, columns)
        cur.execute(query)
        cur.close()
        conn.commit()
        return True
    except:
        return False


def run_and_store(fun, conn, table_name , time):
    # Call the function and retrieve the return value
    return_value = fun()
    # Get the current timestamp
    cursor = conn.cursor()
    insert_query = "INSERT INTO {} (value, datetime) VALUES (%s, %s);".format(table_name)
    cursor.execute(insert_query, (return_value, time))
    conn.commit()
    # Close the cursor
    cursor.close()
    return return_value
