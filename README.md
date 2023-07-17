# Polls API

# Introduction
This serves as an API for the Polls application. To get this app running, please check the following.

# Clone the repository
git clone this respository 

`cd poll-api`

# Prerequisites
We need to have python version >= 3.9.12. This can be installed from [here](https://www.python.org/downloads/release/python-3917/)

# Virtual Env
We will create a virtual env using the following commands. This will ensure that all the developers will work on the same environment. To begin with we have to install the virutalEnv package. You can do that using the following command.

Windows:
`py -m pip install --user virtualenv`

Unix/MacOS:
`python3 -m pip install --user virtualenv`

Learn more about virtual env [here](https://docs.python.org/3/library/venv.html).

## Create a virtual env
We will create a new env called .polls_env using the following command
`python -m venv ./.polls_env`

## Activate the virtual env
Once the environment is created, we have to activate it using the following command.

| Platform | Shell | Command to activate virtual environment |
|---|---|---|
| POSIX | bash/zsh |  `$ source <venv>/bin/activate` |
| | fish | `$ source <venv>/bin/activate.fish` |
| | csh/tcsh | `$ source <venv>/bin/activate.csh` |
| | PowerShell | `$ <venv>/bin/Activate.ps1` |
| Windows | cmd.exe | `C:\> <venv>\Scripts\activate.bat` |
| | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1` |

## Install the dependencies
Once the virtual env is activated, we will now install the dependencies. This will ensure that the dependencies are installed only inside the .polls_env environment. Install the dependencies using the following command

`pip install -r ./requirements.txt`

# Environment Variables
We need the following env variables to be set. But they are currently have sensistive details and hence the data is not checked into git. So create a file called `.env` under the `poll-api` folder. Remember to have a `.` infront of the file. Also, this `.env` is already included in our `.gitignore` and the file will not be checked into the repositoryt. 

`GOOGLE_PROJECT_ID="polls-by-gosu"`
`GOOGLE_PRIVATE_KEY_ID="[ask admin]"`
`GOOGLE_PRIVATE_KEY="[ask admin]"`
`GOOGLE_CLIENT_EMAIL="[ask admin]"`
`GOOGLE_CLIENT_ID="[ask admin]"`
`GOOGLE_CLIENT_X509_CERT_URL="[ask admin]"`

`COSMOSDB_HOST="[ask admin]"`
`COSMOSDB_MASTER_KEY="[ask admin]"`
`COSMOSDB_POLLS_DB_ID="polls-db"`
`COSMOSDB_USER_CONTAINER_ID="[ask admin]"`
`COSMOSDB_CWC_CONTAINER_ID="[ask admin]"`


# Run the API
Run the API using the following command

`python ./app/main.py `

# Test the Code
Note that we have use the port `3003` in our ./app/main.py. If this port is busy in your machine, you have to change it to an unused port.

Once the app is running, go to following 
## Home
URL: `http://localhost:3003/`

Output: `{"Polls":"Root"}`

## Fetching matches
URL: `http://localhost:3003/matches`

Output:
`{"data":[{"match_id":0,"date":20231005,"country1_id":3,"country2_id":6,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":0},{"match_id":1,"date":20231006,"country1_id":5,"country2_id":7,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":1},{"match_id":2,"date":20231007,"country1_id":0,"country2_id":2,"title":"","match_type_id":0,"match_time_id":0,"match_location_id":2},{"match_id":3,"date":20231007,"country1_id":8,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":3},{"match_id":4,"date":20231008,"country1_id":4,"country2_id":1,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":4},{"match_id":5,"date":20231009,"country1_id":5,"country2_id":6,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":1},{"match_id":6,"date":20231010,"country1_id":2,"country2_id":3,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":2},{"match_id":7,"date":20231011,"country1_id":4,"country2_id":0,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":3},{"match_id":8,"date":20231012,"country1_id":7,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":1},{"match_id":9,"date":20231013,"country1_id":1,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":5},{"match_id":10,"date":20231014,"country1_id":2,"country2_id":6,"title":"","match_type_id":0,"match_time_id":0,"match_location_id":4},{"match_id":11,"date":20231014,"country1_id":0,"country2_id":3,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":3},{"match_id":12,"date":20231015,"country1_id":4,"country2_id":7,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":0},{"match_id":13,"date":20231016,"country1_id":1,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":5},{"match_id":14,"date":20231017,"country1_id":5,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":2},{"match_id":15,"date":20231018,"country1_id":6,"country2_id":0,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":4},{"match_id":16,"date":20231019,"country1_id":4,"country2_id":2,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":6},{"match_id":17,"date":20231020,"country1_id":1,"country2_id":7,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":7},{"match_id":18,"date":20231021,"country1_id":5,"country2_id":9,"title":"","match_type_id":0,"match_time_id":0,"match_location_id":5},{"match_id":19,"date":20231021,"country1_id":3,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":8},{"match_id":20,"date":20231022,"country1_id":4,"country2_id":6,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":2},{"match_id":21,"date":20231023,"country1_id":0,"country2_id":7,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":4},{"match_id":22,"date":20231024,"country1_id":2,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":8},{"match_id":23,"date":20231025,"country1_id":1,"country2_id":5,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":3},{"match_id":24,"date":20231026,"country1_id":3,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":7},{"match_id":25,"date":20231027,"country1_id":7,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":4},{"match_id":26,"date":20231028,"country1_id":1,"country2_id":6,"title":"","match_type_id":0,"match_time_id":0,"match_location_id":2},{"match_id":27,"date":20231028,"country1_id":2,"country2_id":5,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":9},{"match_id":28,"date":20231029,"country1_id":4,"country2_id":3,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":5},{"match_id":29,"date":20231030,"country1_id":0,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":6},{"match_id":30,"date":20231031,"country1_id":2,"country2_id":7,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":9},{"match_id":31,"date":20231101,"country1_id":6,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":6},{"match_id":32,"date":20231102,"country1_id":4,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":8},{"match_id":33,"date":20231103,"country1_id":0,"country2_id":5,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":5},{"match_id":34,"date":20231104,"country1_id":6,"country2_id":7,"title":"","match_type_id":0,"match_time_id":0,"match_location_id":7},{"match_id":35,"date":20231104,"country1_id":1,"country2_id":3,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":0},{"match_id":36,"date":20231105,"country1_id":4,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":9},{"match_id":37,"date":20231106,"country1_id":2,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":3},{"match_id":38,"date":20231107,"country1_id":0,"country2_id":1,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":8},{"match_id":39,"date":20231108,"country1_id":3,"country2_id":5,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":6},{"match_id":40,"date":20231109,"country1_id":6,"country2_id":9,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":7},{"match_id":41,"date":20231110,"country1_id":0,"country2_id":8,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":0},{"match_id":42,"date":20231111,"country1_id":4,"country2_id":5,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":7},{"match_id":43,"date":20231112,"country1_id":1,"country2_id":2,"title":"","match_type_id":0,"match_time_id":0,"match_location_id":6},{"match_id":44,"date":20231112,"country1_id":3,"country2_id":7,"title":"","match_type_id":0,"match_time_id":1,"match_location_id":9},{"match_id":45,"date":20231115,"country1_id":"","country2_id":"","title":"","match_type_id":1,"match_time_id":1,"match_location_id":8},{"match_id":46,"date":20231116,"country1_id":"","country2_id":"","title":"","match_type_id":1,"match_time_id":1,"match_location_id":9},{"match_id":47,"date":20231119,"country1_id":"","country2_id":"","title":"","match_type_id":2,"match_time_id":1,"match_location_id":0}]}`

## Fetching countries
URL: `http://localhost:3003/countries`

Output: 
`{"data":[{"country_id":0,"name":"Afghanistan","short_code":"AFG","flag":""},{"country_id":1,"name":"Australia","short_code":"AUS","flag":""},{"country_id":2,"name":"Bangladesh","short_code":"BAN","flag":""},{"country_id":3,"name":"England","short_code":"ENG","flag":""},{"country_id":4,"name":"India","short_code":"IND","flag":""},{"country_id":5,"name":"Netherlands","short_code":"NED","flag":""},{"country_id":6,"name":"New Zealand","short_code":"NZL","flag":""},{"country_id":7,"name":"Pakistan","short_code":"PAK","flag":""},{"country_id":8,"name":"South Africa","short_code":"RSA","flag":""},{"country_id":9,"name":"Sri Lanka","short_code":"SRI","flag":""}]}`

