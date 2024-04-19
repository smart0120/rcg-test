import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime, MetaData, Table, exc
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Constants
API_KEY = os.getenv('API_KEY')
TIMEZONE_LIST_URL = 'http://api.timezonedb.com/v2.1/list-time-zone'
TIMEZONE_URL = 'http://api.timezonedb.com/v2.1/get-time-zone'
DATABASE_URI = os.getenv('DATABASE_URI')

# Database setup
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Table definitions
tzdb_timezones = Table('tzdb_timezones', metadata,
                       Column('countrycode', String(2)),
                       Column('countryname', String(100)),
                       Column('zonename', String(100), primary_key=True),
                       Column('gmtoffset', Integer),
                       Column('import_date', DateTime))

tzdb_zone_details = Table('tzdb_zone_details', metadata,
                          Column('countrycode', String(2)),
                          Column('countryname', String(100)),
                          Column('zonename', String(100), primary_key=True),
                          Column('gmtoffset', Integer),
                          Column('dst', Integer),
                          Column('zonestart', Integer),
                          Column('zoneend', Integer),
                          Column('import_date', DateTime))

tzdb_error_log = Table('tzdb_error_log', metadata,
                       Column('error_date', DateTime, primary_key=True),
                       Column('error_message', String(1000)))

metadata.create_all(engine)

# API interaction functions
def get_api_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log_error(str(e))
        return None

# Database operation functions
def log_error(message):
    with engine.begin() as conn:
        conn.execute(tzdb_error_log.insert().values(error_date=datetime.now(), error_message=message))

def clear_and_populate_timezones(data):
    db_data = []
    import_date = datetime.now()
    for item in data['zones']:
        db_data.append({
            'countrycode': item['countryCode'],
            'countryname': item['countryName'],
            'zonename': item['zoneName'],
            'gmtoffset': item['gmtOffset'],
            'import_date': import_date,
        })
    with engine.begin() as conn:
        conn.execute(tzdb_timezones.delete())
        conn.execute(tzdb_timezones.insert(), db_data)

def populate_zone_details(zone_name):
    with engine.begin() as conn:
        existing = conn.execute(tzdb_zone_details.select().where(tzdb_zone_details.c.zonename == zone_name)).fetchone()
        if not existing:
            data = get_api_data(TIMEZONE_URL, {'key': API_KEY, 'by': 'zone', 'zone': zone_name})
            if data:
                conn.execute(tzdb_zone_details.insert().values(
                    countrycode=data['countryCode'],
                    countryname=data['countryName'],
                    zonename=data['zoneName'],
                    gmtoffset=data['gmtOffset'],
                    dst=data['dst'],
                    zonestart=data['zoneStart'],
                    zoneend=data['zoneEnd'],
                    import_date=datetime.now()
                ))

# Main execution
if __name__ == '__main__':
    # Populate TZDB_TIMEZONES
    timezone_data = get_api_data(TIMEZONE_LIST_URL, {'key': API_KEY, 'format': 'json'})
    if timezone_data:
        clear_and_populate_timezones(timezone_data)
    
        for zone in timezone_data['zones']:
            # Add codes to sleep for API limit call
            populate_zone_details(zone['zoneName'])
