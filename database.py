import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())    


def get_connection():
    conn = psycopg2.connect(host=os.getenv("DB_HOST"), database=os.getenv("DB_DATABASE"),user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"))
    return conn

def get_user_events(registered_email, conn) -> list:
    curr = conn.cursor()
    curr.execute(f'SELECT event_id FROM {os.getenv("USER_EVENTS")} where user_id=\'{registered_email}\';')
    result = curr.fetchall()
    events = []
    if result:
        for event in result:
            events.append(event[0])
    else:
        return []
    curr.close()

    return events

def close(conn):
    conn.close()
