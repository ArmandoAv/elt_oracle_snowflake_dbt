import snowflake.connector
from decouple import config


def load_bucket_snowflake(file_bucket, table):
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

        # Truncate the table
        cur.execute(f"""
            TRUNCATE TABLE {table};
        """)

        # Upload the data from the bucket to the table
        cur.execute(f"""
            COPY INTO {table} (listing_id,
                                   date,
            					   reviewer_name,
			            		   comments,
					               sentiment)
            FROM '{file_bucket}'
            FILE_FORMAT = (type = 'CSV' skip_header = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"');
        """)

        print(f"Data loaded into the {table} table successfully\n")
    
    except Exception as e:
        print(f"Error loading data: {e}\n")
    
    finally:
        # Close the connectionn
        cur.close()
        conn.close()
