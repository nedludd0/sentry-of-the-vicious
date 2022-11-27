"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
### Time
from datetime import datetime
from datetime import timedelta
from pytz import timezone

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
## Common
from sentry import config


"""""""""
GENERAL
"""""""""

# Check if input is filled or no
def is_filled(data):
    if data is None:
      return False
    if data == '':
      return False
    if data == []:
      return False
    if data == {}:
      return False
    if data == ():
      return False
    if hasattr(data, '__iter__'):
        if not all(data): # for data = [None] or (None, None) or {None} 
            return False
    return True
    
# Find What In String_data
def find_what_in_string_data(what, string_data):
    _find = -1
    _find = string_data.find(what)
    if _find == -1: #--> cioè NON l'ha trovati (if it’s not found then FIND returns -1)
        return False
    else:
        return True


"""""""""
NETWORK
"""""""""
def get_current_public_ip():
    
    import requests
    
    _ip = '0.0.0.0'
    _external_service = 'https://checkip.amazonaws.com'
    
    _response = requests.get(_external_service)
    if _response.status_code in (200, 201):
         _ip = _response.text.strip()
    
    return _ip

"""""""""
ARITHMETICS
"""""""""
def get_remainder_of_division(dividend, divider):
    
    # dividend  -->  primo termine dell'operazione di divisione.
    # divider   -->  secondo termine dell'operazione di divisione.
    
    _remainder = dividend % divider
    
    return _remainder

"""""""""
TIME
"""""""""
# My Default Timezone
def default_timezone():
    return timezone(config.TIMEZONE)
    
# Now Time with Formatter or not
def my_time_now(_what_format):
    _my_timezone = default_timezone()
    if _what_format == 'no-format':
        _now = datetime.now(_my_timezone)
    elif _what_format == 'format-extended':
        _now = datetime.now(_my_timezone).strftime("%Y-%m-%d %H:%M:%S")
    elif _what_format == 'format-compact':
        _now = datetime.now(_my_timezone).strftime("%Y%m%d.%H%M")        
    return _now

"""
timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

1 millisecond = 1000 microseconds
1 second = 1000 millisecond
1 minute = 60 seconds

--> mezzo secondo (0,5) = 500 millisecondi

"""

# in how many seconds ? --> fra quanti secondi?
def in_how_many_seconds(_what):
    _when = my_time_now('no-format') + timedelta(seconds=_what)
    return(_when)
    
# in how many milliseconds ? --> fra quanti millisecondi?
def in_how_many_milliseconds(_what):
    _when = my_time_now('no-format') + timedelta(milliseconds=_what)
    return(_when)

# TimeStamp milliseconds Formatter
def timestamp_formatter(_date):
    _my_timezone = default_timezone()
    _my_date = datetime.fromtimestamp(_date/1000, _my_timezone).strftime('%Y-%m-%d %H:%M:%S')
    return(_my_date)

# TimeStamp milliseconds Formatter
def timestamp_formatter_only_date(_date):
    _my_timezone = default_timezone()
    _my_date = datetime.fromtimestamp(_date/1000, _my_timezone).strftime('%Y-%m-%d')
    return(_my_date)

# Convert seconds to hh:mm:ss
def convert_seconds_to_hhmmss(_seconds):
    _readable_time  = None
    _readable_time  = str(timedelta(seconds=_seconds))
    return(_readable_time)

# Formatter only YYYY-MM-DD
def yyyy_mm_dd_formatter(_date):
    _my_date = _date.strftime('%Y-%m-%d')
    return(_my_date)

"""""""""
STRING
"""""""""
def split_string_into_list(txt, separator):
    
    # Prepare
    _list = []
    _slices = None
    
    _slices = txt.split(separator)
    for _slice in _slices:
        if bool(_slice):
            if _slice == 'None':
                _slice = None
            _list.append(_slice)
            
    return(_list)


"""""""""
LOG
"""""""""
def my_log(_type, _module, _func_name, _func_line, _inputs ,_msg,_clean=True):

    # Logger
    from followstrategy.common.logging import my_logger_main

    # Prepare
    _msg_error_complete = None
    _msg_return = None
    _response_split = None
    _where = f"{_module}.{_func_name}"
    
    # Build Error Msg
    if _inputs is not None:    
        _msg_error_complete = f"{_type} on {_where}, line {_func_line} with inputs {_inputs} -- MESSAGE: {my_time_now('format-extended')} - {_type.upper()} - {_msg}"
    else:
        _msg_error_complete = f"{_type} on {_where}, line {_func_line} -- MESSAGE: {my_time_now('format-extended')} - {_type.upper()} - {_msg}"
        
    # Complete Msg for Logger
    my_logger_main.error(_msg_error_complete)
    
    # Return Nice Msg for Users or Not
    if _clean:
        _response_split = split_string_into_list(_msg_error_complete,'MESSAGE: ')
        if _response_split:
            _msg_return = _response_split[-1]
        else:
            _msg_return = _msg_error_complete
    else:
        _msg_return = _msg_error_complete
        
    return _msg_return
    
    
