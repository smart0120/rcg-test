# TimezoneDB Interaction Project

This Python project queries the TimezoneDB API to populate a database with timezone information. The project is structured to populate two main tables: `TZDB_TIMEZONES` and `TZDB_ZONE_DETAILS`, and to log any errors into `TZDB_ERROR_LOG`.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3.x.
* You have a `<Your_Database>` database set up and accessible.
* You have obtained an API key from [TimezoneDB](https://timezonedb.com).

## Installing TimezoneDB Interaction Project

To install the TimezoneDB Interaction Project, follow these steps:

1. Clone the repo:
```bash
git clone https://github.com/smart0120/rcg-test.git
cd timezonedb_interaction_project
```

2. Setup a Virtual Environment:
```bash
python -m venv venv

# Activate the virtual environment
# On Windows
source venv/Scripts/activate
# On MacOS/Linux
source venv/bin/activate
```

4. Install required Python packages:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables by renaming `.env.example` to `.env` and replacing the placeholder values with your actual API key and database URI.

## Using TimezoneDB Interaction Project
Run the main script:
```bash
python main.py
```
