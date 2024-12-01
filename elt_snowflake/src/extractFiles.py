import cx_Oracle
import pandas as pd
from decouple import config


def extract_files(table, file):

    # Connection to the Oracle database
    dsn = cx_Oracle.makedsn(str(config('DB_HOST')), str(config('DB_PORT')), service_name = str(config('DB_SERVICENAME')))
    conn = cx_Oracle.connect(user = str(config('DB_USR')), password = str(config('DB_PWD')), dsn = dsn)

    # Get file name
    file_name = file.split("/")[-1]

    try:
        # Create a DataFrame from a SQL query
        sql_query = f"SELECT * FROM {table}"
        df = pd.read_sql(sql_query, con=conn)

        # Export the DataFrame to a CSV file
        df.to_csv(file, index=False)
        print(f"Data exported to {file_name} file successfully.\n")

    except cx_Oracle.DatabaseError as e:
        conn.rollback()
        print("Database error:", e)

    finally:
        # Close the connection
        conn.close()
