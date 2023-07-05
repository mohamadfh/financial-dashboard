import psycopg2
import datetime

connection = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password"
)


def calc():
    return 1


def run_calc_and_store():
    # Call the calc function and retrieve the return value
    return_value = calc()

    # Get the current timestamp
    current_time = datetime.datetime.now()

    cursor = connection.cursor()
    insert_query = "INSERT INTO calc_results (value, timestamp) VALUES (%s, %s);"
    cursor.execute(insert_query, (return_value, current_time))
    connection.commit()

    # Close the cursor
    cursor.close()
