import snowflake.connector
from decouple import config


def load_file_snowflake(file_path, table):
    # Snowflake connection
    conn = snowflake.connector.connect(
        user=str(config('SNOW_USER')),
        password=str(config('SNOW_PWD')),
        account=str(config('SNOW_ACCOUNT')),
        warehouse=str(config('SNOW_WAREHOUSE')),
        database=str(config('SNOW_DB')),
        schema=str(config('SNOW_SCHEMA'))
    )

    try:
        # Create a cursor to execute SQL commands
        cur = conn.cursor()

        # Upload the file to the Snowflake stage
        cur.execute(f"PUT file:///{file_path} @{str(config('SNOW_STAGE'))} AUTO_COMPRESS=TRUE OVERWRITE=TRUE;")
        print(f"{file_path.split('/')[-1]} file uploaded to Stage '{str(config('SNOW_STAGE'))}'.")

        # Truncate the table
        cur.execute(f"""
            TRUNCATE TABLE {table};
        """)

        # Upload the data from the CSV file to the table
        copy_command = f"""
            COPY INTO {table}
            FROM @{str(config('SNOW_STAGE'))}/{file_path.split('/')[-1]}
            FILE_FORMAT = (TYPE = 'CSV' skip_header = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"')
        """
        cur.execute(copy_command)
        print(f"Data loaded into the {table} table successfully\n")

    except Exception as e:
        print(f"Error loading data: {e}\n")

    finally:
        # Close the connection
        cur.close()
        conn.close()
