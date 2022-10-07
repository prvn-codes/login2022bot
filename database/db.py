import psycopg2
import os
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())    


def get_connection():
    conn = psycopg2.connect(host=os.getenv("DB_HOST"), database=os.environ["DB_DATABASE"],user=os.environ["DB_USER"], password=os.environ["DB_PASS"])
    return conn

def get_user_events(registered_email, conn) -> list:
    curr = conn.cursor()
    curr.execute(f'SELECT event_id FROM {os.environ["USER_EVENTS"]} where user_id=\'{registered_email}\';')
    result = curr.fetchall()
    curr.close()
    events = []
    if result:
        for event in result:
            events.append(event[0])
    else:
        return []
    return events

def get_user_name(registered_email, conn) -> str:
    curr = conn.cursor()
    curr.execute(f'SELECT name FROM {os.environ["USER_TABLE"]} where email=\'{registered_email}\';')
    result = curr.fetchall()
    curr.close()
    if result:
        for event in result:
            return event[0]
    return "UserNameNotFound"


def get_alumni(registered_email, conn) -> str:
    curr = conn.cursor()
    curr.execute(f'SELECT name FROM {os.environ["ALUMNI_TABLE"]} where email=\'{registered_email}\';')
    result = curr.fetchall()
    curr.close()
    if result:
        for event in result:
            return event[0]
    return "UserNameNotFound"

def close(conn):
    conn.close()
