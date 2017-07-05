import sys
import datetime
import time

PrintLevel = {
    'DEBUG':'DEBUG',
    'ERROR': 'ERROR',
    'NOTICE': '!',
    'PROGRESS': '*',
    'STATUS': '+',
    'QUESTION': '?'
}

#disabled by default
DEBUG = False

def EnableDebug(enable = True):
    global DEBUG
    
    DEBUG = enable
    
    return DEBUG

def GetTimeStamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def Message(level, message, endline = '\n'):
    global DEBUG
    
    level = level.upper()
    
    if endline == None:
        endline = ''
    
    if level == 'DEBUG' and not DEBUG:
        return #nothing to print - we don't have debug enabled
    
    if level in PrintLevel:
        if level == 'ERROR':
            sys.stderr.write('[{0}] {1} | {2}{3}'.format(PrintLevel[level], GetTimeStamp(),message, endline))
            sys.stderr.flush()
        else:
            sys.stdout.write('[{0}] {1} | {2}{3}'.format(PrintLevel[level], GetTimeStamp(),message, endline))
            sys.stdout.flush()
    else:
        sys.stdout.write('[{0}] {1} | {2}{3}'.format(level, GetTimeStamp(), message,endline))
        sys.stdout.flush()
        
if __name__ == '__main__':
    Message('ERROR', 'logging.py is used as utility - not for direct execution')