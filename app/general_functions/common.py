# general functions for all python activity
from datetime import datetime as dt
from time import sleep, time

def _sleep(n):
    sleep(n)
    
def _get_time():
    return time()

def _get_datetime():
    return dt.now()
    
def _get_sdatetime(insteadofspace=None):
    return str(dt.now()).replace(' ','T' if insteadofspace == None else insteadofspace)


