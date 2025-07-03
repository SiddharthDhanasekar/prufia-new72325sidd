from datetime import datetime
from app.services.db.mysql import db_connection

def getTime(timestamp):
    timestamp_ms = int(timestamp)
    timestamp_sec = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_sec)
    formatted_date = dt.strftime('%B %d, %Y %H:%M:%S')
    return formatted_date