# ELT Process - Oracle, Snowflake and DBT

This project is an ELT process on Windows.

## Prerequisites
The following list is what is needed to use the software.

* Python
* Oracle
* Snowflake
* Apache Airflow

### Installation

To install the software mentioned above, the following steps must be performed. The following steps are to install the required software in a windows environment.

#### Python

To install Python, you must download the executable file from the following link:

https://www.python.org/downloads/release/python-3119/

When executing the file, in the same process it indicates that if you want to save the Python variable in the environment variables, so it is no longer necessary to add them when finishing the installation.

A cmd terminal is opened and validated, execute the next command

```
python --version
```

Python has a library with which you can install plugins on the command line called pip. Copy the script from the following link into a notepad

https://bootstrap.pypa.io/get-pip.py

Save the copied script as get-pip.py file and open a cmd terminal in the path where you saved the file and executed the following command

```
python get-pip.py
```

The following environment variable must be created:

PIP_HOME = C:\Users\<user_sesion>\AppData\Local\Programs\Python\Python311

The %PIP_HOME%\Scripts variable is added to the Path variable.

> [!NOTE]
> The session user must be changed to that of the current Windows session.

#### Oracle

You must have an Oracle Database installed, preferably a version greater than or equal to Oracle 11. If you do not have it installed, you must install it by downloading the executable file from the following link:

https://www.oracle.com/database/technologies/xe-prior-release-downloads.html

Once Oracle is installed, you must have a user who can have the necessary permissions to generate, load and read the tables that will be used for loading to Snowflake. The tables will be created with the following script found in the **database** folder. 

Data_Model_Oracle.sql

Additionally, here are the steps to generate a user, in case a user does not exist for the new tables. In the script you must enter what the user's name and password will be, as well as validate in which tablespace the tables of this new user should be generated. If it is in the Users tablespace, the script already points to that tablespace.

#### Snowflake

You must have a Snowfalke account, if you do not have an account, you must create a Snowflake account with a Standard type Database and preferably it must be mounted on AWS. In the following link you can register a Snowflake account with a 30-day trial period.

https://www.snowflake.com/en/data-cloud/platform/

Once the account is activated, in a new Workshhet, the Database called SNOWFLAKE and the scheme called CORE are selected.

Once the Database and the corresponding Schema have been selected, the following script located in the **database** folder must be executed to create a new Role, Store, User and Database, as well as the necessary permissions to be able to manipulate the Database, the corresponding Scheme and created objects.

Setup_Snowflake.sql

> [!NOTE]
> In the script you must add the username and password that you want for the user who will be executing the DBT processes.

Once the previous script has been executed correctly, the following script must be executed to create tables and stage them in the Snowflake RAW schema.

Raw_Snowflake.sql

##### Snowflake CLI

Snowflake CLI is an open-source command-line tool explicitly designed for developer-centric workloads in addition to SQL operations. It is a flexible and extensible tool that can accommodate modern development practices and technologies. In the following link are the steps to do the installation:

https://docs.snowflake.com/developer-guide/snowflake-cli/installation/installation?_fsi=A5dElN68&_fsi=A5dElN68#label-snowcli-install-windows-installer


#### Airflow

To install Airflow, the WSL tool must be used to configure a Linux (Ubuntu) operating system on Windows. This is because Airflow cannot be installed on Windows. In the following link are the steps to do the installation:

https://documentation.ubuntu.com/wsl/en/latest/guides/install-ubuntu-wsl2/

Once it has been installed, run the following commands:

```
sudo apt update
sudo apt install python3.11
sudo apt install python3-pip 
cd ~
pip install virtualenv
sudo apt install python3-virtualenv
virtualenv airflow_env
source airflow_env/bin/activate
mkdir airflow
```

Once the previous commands have been executed, open the .bashrc file with the vi editor, with the following command:

```
vi ~/.bashrc
```

The following variable must be added, preferably after the initial comments of the file:

AIRFLOW_HOME=~/airflow

Once the file with the new variable has been saved, the following command is executed so that the changes in the .bashrc file are recognized:

```
source ~/.bashrc
```

Next, the following commands must be executed to continue with the installation of Airflow:

```
cd $AIRFLOW_HOME
pip install apache-airflow
airflow version
airflow db init
airflow users create --username <user> --password <password> --firstname <name> --lastname <lastname> --role Admin --email <email>
airflow users list
mkdir dags
```

> [!NOTE]
> For the airflow users create command, the first name, last name and email do not have to be real, since the data is saved in the Airflow Database. The **username** and **password** will be the credentials used to enter the Airflow console.

By default, Airflow has some DAG examples. If you do not want to see the example DAGs in the Airflow console, you must open the airflow.fcg file with the vi editor, with the following command:

```
vi ~/airflow/airflow.cfg
```

On the load_examples line, True must be changed to False, as follows:

load_examples = False

Once the file has been saved, two new Ubuntu windows should open. In the first window the following commands are executed:

```
cd ~
source airflow_env/bin/activate
cd airflow
airflow scheduler
```

In the second window, execute the following commands:

```
cd ~
source airflow_env/bin/activate
cd airflow
airflow webserver
```

After executing each of the commands, you can now open the console from the following link in a browser:

http://localhost:8080/home

## Architecture

The process is divided into three parts, as can be seen in the following diagram.

![Architecture](https://github.com/ArmandoAv/elt_oracle_snowflake_dbt/blob/main/architecture/ELT%20process.png)

Below, you will see the steps to execute the process.

### Usage

To run this project, you first need to make a copy of the files and directories, this can be done with the following command in a cmd terminal

```
git clone https://github.com/ArmandoAv/elt_oracle_snowflake_dbt
```

Once you have all the files locally, you should check the following folders:

* load_oracle
* elt_snowflake
* dbt_snowflake
* airflow_dags

Each of the folders will be seen as independent processes.

### load_oracle

In this folder there are the scripts and files to load the Oracle tables that were previously generated. This folder has the following structure:

```
load_oracle
├── bads 
├── ctl 
├── data 
└── logs
```

#### bads

This folder saves records that cannot be loaded into Oracle tables due to some error.

#### ctl

This folder contains the control files that define how SQL Loader should interpret and load data into the Oracle table.

#### data

This folder contains the files with the data that must be loaded into the Oracle tables.

#### logs

This folder saves files that contain detailed information about the upload process, including statistics on the number of logs uploaded, errors and warnings.

#### Execution

To load the information into the Oracle tables, the following commands must be executed in a terminal in the load_oracle folder path:

```
sqlldr <User>/<Password>@//localhost:1521/xe control=ctl/hosts.ctl log=logs/hosts.log data=data/hosts.csv bad=bads/hosts.bad
sqlldr <User>/<Password>@//localhost:1521/xe control=ctl/listings.ctl log=logs/listings.log data=data/listings.csv bad=bads/listings.bad
```

> [!NOTE]
> In the commands you must enter the username and password that was created with the help of the Data_Model_Oracle.sql script.
> This execution is unique as it helps load the data into the tables of the source system which is Oracle.

Once the commands have been executed, validate that the Oracle tables have been loaded with the following commands in a terminal:

```
sqlplus <User>/<Password>@//localhost:1521/xe
SET LINESIZE 1000
SET HEADING ON

select *
from   hosts
where  rownum <= 2;

select count(*)
from   hosts;

select *
from   listings
where  rownum <= 2;

select count(*)
from   listings;

quit
```

> [!NOTE]
> In the commands you must enter the username and password that was created with the help of the Data_Model_Oracle.sql script.

### elt_snowflake

In this folder are the scripts and files to load the Snowflake tables that were previously generated. This folder has the following structure:

```
etl_snowflake
├── src
└── tmp
```

#### src

In this folder are the Python scripts that extract the information from the Oracle tables and the AWS bucket and load it into the Snowflake tables.

#### tmp

In this folder, temporary files are created with the information from the Oracle tables, for later loading into the Snowflake tables. Once the files have been loaded into the Snowflake tables, the files are deleted.

#### Execution

To load the information into the Snowflake tables, the following commands must be executed in a terminal in the path of the etl_snowflake folder:

```
python -m venv vnenv
venv\Scripts\activate
pip install -r requirements.txt
```

A file must be created in the same path of the etl_snowflake folder called .env, with the following content:

```
# Oracle connection
DB_HOST = <IP_WSL>
DB_SERVICENAME = XE
DB_USR = <User>
DB_PWD = <Password>
DB_PORT = 1521

# Snowflake connection
SNOW_ACCOUNT = <Account>
SNOW_DB = airbnb
SNOW_WAREHOUSE = COMPUTE_WH
SNOW_SCHEMA = RAW
SNOW_USER = <User>
SNOW_PWD = <Password>
SNOW_STAGE = RAW_FILES
```

> [!NOTE]
> In the Oracle part, you must enter the username and password that was created with the help of the Data_Model_Oracle.sql script. For the IP, you must enter the IP that comes out of the **ipconfig** command in the Ethernet adapter vEthernet ( WSL): section; the IPv4 Address value.
> In the Snowflake part, you must enter the account, username and password to enter the Snowflake console.

Once the .env file has been created, the following commands must be executed to execute the Snowflake tables loading process:

```
cd src
python extract.py
python load.py
```

### dbt_snowflake

In this folder are the scripts and files to load the Snowflake tables with DBT. This folder has the following structure:

```
dbt_snowflake
└── dbtsnowflake
```

#### dbtsnowflake

In this folder is the DBT project with all the necessary files and scripts. This folder has the following structure:

```
dbtsnowflake
├── analyses 
├── assets 
├── hooks 
├── macros 
├── models 
├── seeds 
├── snapshot 
└── tests
```

##### analyses

This folder is used to store ad-hoc analysis and SQL queries that are not part of the regular DBT transformation logic.

##### assets

This folder is used to store files that are not part of the data transformations, but are useful for the project.

##### hooks

In this folder you can define custom hooks that are executed at specific times in the DBT lifecycle.

##### macros

This folder contains macros, which are reusable functions written in Jinja (the templating engine used by DBT).

##### models

This is one of the most important folders in a DBT project, as it contains the data models that define how the data is transformed.

##### seeds

This folder is used to store CSV files that can be loaded directly into the database as tables.

##### snapshot

This folder defines snapshots, which are a way to capture the state of the data at a given time.

##### test

This folder is used to store data quality tests.

#### Execution

To load the information into the Snowflake tables with DBT, the following commands must be executed in a terminal in the path of the dbt_snowflake folder:

```
python -m venv vnenv
venv\Scripts\activate
pip install -r requirements.txt
```

Once the commands have been executed, we proceed with the installation of DBT. Running the following commands in the same terminal and path:

```
mkdir %userprofile%\.dbt
```

In a Windows file explorer, you should go to the following path:

C:\Users\<user_name>\.dbt

> [!NOTE]
> The user name must be changed to that of the current Windows session.

Once in the path, you must open the profiles.yml file with a notepad and add the following to the file:

```
dbtsnowflake:
  outputs:
    dev:
      account: <Account>
      database: AIRBNB
      password: <Password>
      role: TRANSFORM
      schema: DEV
      threads: 1
      type: snowflake
      user: <User>
      warehouse: COMPUTE_WH
  target: dev

```

> [!NOTE]
> You must change the account with which you log in to the Snowflake console. Additionally, the username and password must be the same as those with which the Setup_Snowflake.sql script was executed.

Once the profiles.yml file has been saved with the changes, the following commands must be executed again in the terminal:

```
cd dbtsnowflake
dbt deps
dbt debug
```

Once the commands have been executed, the following commands must be executed to execute the Snowflake tables loading process with DBT:

```
dbt snapshot
dbt run
```

### airflow_dags

In the previous section, the ELT process was executed through a terminal. So now we will see how to execute the process with an orchestration tool, in this case with Airflow.

In this folder are the scripts used to run the DAGs in Airlfow. This folder has the following structure:

airflow_dags
└── dags

#### dags

In this folder are the Python scripts that are the Ariflow DAGs.

#### Execution

To run the Airflow DAGs, you must open an Ubuntu terminal, executing the following commands:

```
cd ~
source airflow_env/bin/activate
pip install dbt-snowflake==1.7.1
pip install snowflake-connector-python
pip install cx_Oracle
pip install python-decouple
pip install python-dotenv
pip install pandas
deactivate
```

Once the commands have been executed, the Snowflake client must be installed. The following commands are executed:

```
cd ~
wget https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.3/linux_x86_64/snowsql-1.3.1-linux_x86_64.bash
bash snowsql-1.3.1-linux_x86_64.bash
y
```

Once the commands have been executed, the DAGs must be copied from the project's dags folder to the dags folder in WSL. The following commands are executed:

```
cd ~/airflow/dags
cp /mnt/c/<path_ariflow_dags>/dags/ETL_Snowflake.py .
cp /mnt/c/<path_ariflow_dags>/dags/DBT_Snowflake.py .
```

> [!NOTE]
> You must change the path where you have the airflow_dags folder in Windows.


Once the commands have been executed, to execute the DAGs in Airflow, the following steps must be completed:

Open two Ubuntu terminals.

The following commands are executed in the first terminal:

```
cd ~
source airflow_env/bin/activate
airflow scheduler
```

The following commands are executed in the second terminal:

```
cd ~
source airflow_env/bin/activate
airflow webserver
```

After executing each of the commands, you can now open the console from the following link in a browser:

http://localhost:8080/home

Once the Airflow console has been opened, in the same console the following variables must be created with their respective values:

```
dbt_snowflake_path		/mnt/c/<path_dbt_snowflake>/dbtsnowflake/
extract_snowflake_script	/mnt/c/<path_elt_snowflake>/src/extract.py
load_snowflake_script		/mnt/c/<path_elt_snowflake>/src/load.py

```

Once the variables have been created and the DAGs are visible in the Airflow console, they must be executed in the following order:

1. elt_snowflake_dag
1. dbt_snowflake_dag

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
1. Adding your changes in the staging area (`git add -A`)
1. Commit your changes with your comments (`git commit -m 'Add some AmazingFeature'`)
1. Push to the branch (`git push origin feature/AmazingFeature`)
1. Open a Pull Request

## Contact

You can contact me in my LinkedIn profile

Armando Avila - [@Armando Avila](https://www.linkedin.com/in/armando-avila-419a8623/)

Project Link: [https://github.com/ArmandoAv/elt_oracle_snowflake_dbt](https://github.com/ArmandoAv/elt_oracle_snowflake_dbt)
