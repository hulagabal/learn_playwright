from datetime import datetime

def get_datestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

