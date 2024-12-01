import datetime
from pathlib import Path
from loadFileSnowflake import load_file_snowflake
from loadBucketSnowflake import load_bucket_snowflake


# Path variables
script_path = Path(__file__).resolve()
parent_dir = script_path.parent.parent
formatted_path = str(parent_dir).replace('\\', '/')
tmp_dir = "/tmp/"
tmp_path = formatted_path + tmp_dir

# File variables
hosts_file = "hosts.csv"
file_path_hosts = formatted_path + tmp_dir + hosts_file
listings_file = "listings.csv"
file_path_listings = formatted_path + tmp_dir + listings_file

# Bucket variable
reviews_bucket = "s3://dbtlearn/reviews.csv"

# DB variables
hosts_table = 'raw_hosts'
listings_table = 'raw_listings'
reviews_table = 'raw_reviews'

# Delete temporary files
def delete_files(path):
    # Create a path object for the folder
    p = Path(path)
    
    # Iterate over files and delete them
    for files in p.iterdir():
        if files.is_file():
            # Delete file
            files.unlink()

# Start the process
now = datetime.datetime.now()
start_date = now.strftime("%d/%m/%Y")
start_time = now.strftime("%H:%M:%S")
print(f"Start the process on {start_date} at {start_time}\n")

# Load hosts file
print(f"Load data from {hosts_file} file to {hosts_table} table\n")
load_file_snowflake(file_path_hosts, hosts_table)

# Load listings file
print(f"Load data from {listings_file} file to {listings_table}\n")
load_file_snowflake(file_path_listings, listings_table)

# Load reviews bucket file
print(f"Load data from S3 bucket file to {reviews_table}\n")
load_bucket_snowflake(reviews_bucket, reviews_table)

# Delete csv files
print("Delete temporary files")
#delete_files(tmp_path)

# End the process
now = datetime.datetime.now()
end_date = now.strftime("%d/%m/%Y")
end_time = now.strftime("%H:%M:%S")
print(f"\nEnd the process on {end_date} at {end_time}")
