import datetime
from pathlib import Path
from extractFiles import extract_files


# Path variables
script_path = Path(__file__).resolve()
parent_dir = script_path.parent.parent
formatted_path = str(parent_dir).replace('\\', '/')
tmp_dir = "/tmp/"
tmp_path = formatted_path + tmp_dir

# File variables
hosts_file = "hosts.csv"
file_path_hosts = tmp_path + hosts_file
listings_file = "listings.csv"
file_path_listings = tmp_path + listings_file

# DB variables
hosts_table = "hosts"
listings_table = "listings"

# Start the process
now = datetime.datetime.now()
start_date = now.strftime("%d/%m/%Y")
start_time = now.strftime("%H:%M:%S")
print(f"Start the process on {start_date} at {start_time}\n")

# Extract hosts file
# Extract hosts file
print(f"Extract data from {hosts_table}\n")
extract_files(hosts_table, file_path_hosts)

# Extract listings file
print(f"Extract data from {listings_table}\n")
extract_files(listings_table, file_path_listings)

# End the process
now = datetime.datetime.now()
end_date = now.strftime("%d/%m/%Y")
end_time = now.strftime("%H:%M:%S")
print(f"\nEnd the process on {end_date} at {end_time}")
