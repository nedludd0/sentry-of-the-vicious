"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
from os import environ
WITH_DATA = environ.get('WITH_DATA')

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
## My Database (SqlAlchemy)
from sentry.database.sqlalchemy.client import SqlAlchemyClientClass
from sentry.database.sqlalchemy import models
from sentry.database.sqlalchemy import models_crud

"""""""""""""""""""""""""""""""""""""""""""""""""""
INIT : "main" to create tables & to load data
"""""""""""""""""""""""""""""""""""""""""""""""""""
def create_tables_command():
    
    ## Instance My SqlAlchemyClient OBJS
    SqlAlchemyEngine = SqlAlchemyClientClass().get_engine()
    SqlAlchemyBase = SqlAlchemyClientClass().get_base()
    
    ## Drop ALL tables
    print('\n')
    SqlAlchemyBase.metadata.drop_all(SqlAlchemyEngine)
    print('Drop All --> OK')

    ## Create ALL tables
    print('\n')    
    SqlAlchemyBase.metadata.create_all(SqlAlchemyEngine)
    print('Create All --> OK')

def load_data_command():
    
    ## Load Datas
    _outputs = load_data_all()
    print('Load Data: ')
    for _output in _outputs:
        print(_output)


if WITH_DATA == 'y':

    create_tables_command()
    print('\n')    
    load_data_command()
    print('\n')
    print('>> INITIALIZED THE DATABASE - WITH START DATA <<')
    print('\n')     

elif WITH_DATA == 'n':

    create_tables_command()
    print('\n')
    print('>> INITIALIZED THE DATABASE - NO START DATA <<')
    print('\n')  

else:
    print(f"Input {WITH_DATA} error")

"""""""""""""""""""""""""""""""""
FUNCTIONS : load datas
"""""""""""""""""""""""""""""""""

# Load start data into database  
def load_data_all():
    
    # Prepare
    _msg_final = []

    """ Start SQLALCHEMY Session """ 
    _sqlalchemy_session_working = SqlAlchemyClientClass().get_session_normal_started()

    """ DATA_SAMPLE - USERS, MESSAGES """
    _output = None
    _output = load_data_4sample(_sqlalchemy_session_working)       
    if _output[0] == 'NOK':
        SqlAlchemyClientClass().close_sqlalchemy(_session_normal = _sqlalchemy_session_working)        
        return _output[1]
    else:
        _msg_final.append(_output[1])

    """ Close SQLALCHEMY Session """
    SqlAlchemyClientClass().close_sqlalchemy(_session_normal = _sqlalchemy_session_working)

    return _msg_final


""" LOAD DATA SAMPLE Users, Messages""" 
# Users > AppTraders
# Messages > AppTgMsgs
def load_data_4sample(_sqlalchemy_session_working ):

    ## PREPARE
    _output = None
    _response_tuple = None
    _msg_ok = '- 4SAMPLE: Users --> OK'

    ## AppTraders
    
    _app_user_fk = 1
    _toc_fk = 1
    _trader_name = 'trader2'
    _trader_project = 'Giusto una prova di progetto'
    _tg_group_ckeck = '@followseciriesci'
    
    _insert_obj = models.AppTraders( app_user_fk = _app_user_fk, toc_fk = _toc_fk, trader_name = _trader_name, trader_project = _trader_project, tg_group_ckeck  = _tg_group_ckeck )
    _output = models_crud.my_insert_general(_insert_obj, _sqlalchemy_session_working)                                          
    if _output[0] == 'NOK':
        _response_tuple = ('NOK', _output[1])
        return _response_tuple

        
    ## AppTgMsgs
    
    """
    _app_tg_msg_type_fk = 1
    _applied = False
    
    _author_id = 1
    _title = 'Phasellus at elementum odio'
    _body = 'Phasellus at elementum odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. '\
            'Vestibulum id ante finibus, mollis orci eu, rhoncus sem. Vivamus in sodales neque. Praesent blandit lorem non risus pellentesque faucibus. '\
            'Suspendisse eget metus vel nulla viverra vestibulum quis ut elit. Ut blandit sem aliquam urna elementum egestas'
    
    _insert_obj = models.AppTgMsgs( app_user_fk = _author_id, app_tg_msg_type_fk =_app_tg_msg_type_fk, title =_title, body = _body , applied = _applied )
    _output = models_crud.my_insert_general(_insert_obj, _create_date = False, _sqlalchemy_session_working)
    if _output[0] == 'NOK':
        _response_tuple = ('NOK', _output[1])
        return _response_tuple
        
        
    _author_id = 2
    _title = 'Nunc nec fermentum tortor, eget convallis magna'
    _body = 'Nunc nec fermentum tortor, eget convallis magna. Cras quis lacus et nunc consectetur accumsan. Aliquam justo est, imperdiet sed magna quis, '\
            'elementum blandit nisl. Ut lorem sapien, interdum quis interdum ut, semper pretium purus. Phasellus sapien turpis, consectetur sit amet placerat quis, '\
            'imperdiet sit amet dui. Morbi bibendum porttitor porttitor. Phasellus eget tortor feugiat, aliquet nibh volutpat, imperdiet turpis.'
    
    _insert_obj = models.AppTgMsgs( app_user_fk = _author_id, app_tg_msg_type_fk =_app_tg_msg_type_fk, title =_title, body = _body, applied = _applied )
    _output = models_crud.my_insert_general(_insert_obj, _create_date = False, _sqlalchemy_session_working)
    if _output[0] == 'NOK':
        _response_tuple = ('NOK', _output[1])
        return _response_tuple

    """
    
    _response_tuple = ('OK', _msg_ok)
    
    return _response_tuple
