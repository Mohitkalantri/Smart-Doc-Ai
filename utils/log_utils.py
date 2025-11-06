import datetime

def log_info(tag, message):
    print(f"[{datetime.datetime.now()}][INFO][{tag}] {message}")

def log_error(tag, error):
    print(f"[{datetime.datetime.now()}][ERROR][{tag}] {error}")
