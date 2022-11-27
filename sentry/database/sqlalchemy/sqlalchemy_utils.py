"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
## Log
import traceback
import inspect
## Database (SqlAlchemy)
from sqlalchemy import func, Table
from sqlalchemy import inspect as sqlalchemy_inspect # per evitare di sovrascrivere la inspect della standard lib python

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
## General
from mymoney.common import utility
## SQLALCHEMY CLIENT
from mymoney.common.database.sqlalchemy.client import SqlAlchemyClientClass

# Count ottimizzata --> https://gist.github.com/hest/8798884
# FUNZIONA SOLO SE NELLA _query ci sono filtri, altrimenti da sempre e solo 1 come risultato
def utility_get_optimized_count(_query):
    
    _count_q = _query.statement.with_only_columns([func.count()]).order_by(None)
    _count = _query.session.execute(_count_q).scalar()
    
    return _count

# Count Generica - with ORM
def utility_get_simple_count_orm(p_table_model_name, p_session = None):
    
    # Prepare
    _count = 0

    # Choose Session
    _session_working = None
    if not utility.is_filled(p_session):
        _session_working = SqlAlchemyClientClass().get_session_normal_started()
    else:
        _session_working = p_session

    # Work
    _count = _session_working.query(func.count(p_table_model_name.id)).scalar() 

    # Close Session
    if not utility.is_filled(p_session):
        SqlAlchemyClientClass().close_session_normal_started_input(_session_working)

    return _count

# Count Generica - no ORM
def utility_get_simple_count_no_orm(p_table_name, p_session = None):
    
    # Prepare
    _count = 0
    _query = f"SELECT COUNT(*) FROM {p_table_name}"
    
    # Work
    _count = utility_exec_sql_raw(  _sql_statement = _query, 
                                    _option_scalar = True, 
                                    p_session = p_session )
    # Return
    return _count

# Execution Sql Raw
def utility_exec_sql_raw(_sql_statement, _option_scalar = False, p_session = None):

    # Choose Session
    _session_working = None
    if not utility.is_filled(p_session):
        _session_working = SqlAlchemyClientClass().get_session_normal_started()
    else:
        _session_working = p_session
    
    # Work
    if _option_scalar:
        _output = _session_working.execute(_sql_statement).scalar()
    else:
        _output = _session_working.execute(_sql_statement)

    # Close Session
    if not utility.is_filled(p_session):
        SqlAlchemyClientClass().close_session_normal_started_input(_session_working)
    
    return _output

# Generic Table Obj
def utility_get_table_obj_from_table_name(p_table_model_name, p_session = None):

    # Prepare
    _table_obj = None

    # Choose Session
    _session_working = None
    if not utility.is_filled(p_session):
        _session_working = SqlAlchemyClientClass().get_session_normal_started()
    else:
        _session_working = p_session
    
    # Work    
    _table_obj = _session_working.query(p_table_model_name).all()

    # Close Session
    if not utility.is_filled(p_session):
        SqlAlchemyClientClass().close_session_normal_started_input(_session_working)

    return _table_obj

# List all tables of a database - no model use
def utility_list_all_tables_name_no_model(p_sqlalchemyengine):

    # Prepare
    _inputs = None
    _module_name = __name__
    _func_name = inspect.currentframe().f_code.co_name      
    _response_tuple = None
    _msg = None

    # Work
    try:
        
        # Inspect Obj
        _insp = sqlalchemy_inspect(p_sqlalchemyengine) 
        
        # Table List
        _table_list = _insp.get_table_names()
        
        # Response
        _response_tuple = ('OK', _table_list)
        
    except Exception:
        
        _msg = traceback.format_exc(2)
        _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")   

    # Return
    return _response_tuple

# Add or Remove a table on Metadata
def utility_manage_table_on_metadata(p_what, p_table_name):
    
    # p_what: add or remove
    
    # Prepare
    _inputs = f"{p_what}|{p_table_name}"
    _module_name = __name__
    _func_name = inspect.currentframe().f_code.co_name      
    _response_tuple = None
    _msg = None

    ## Instance My SqlAlchemyClient OBJS
    SqlAlchemyBaseMetadata = SqlAlchemyClientClass().get_base_metadata()

    # Work
    try:
        
        if p_what == 'add':

            ## Instance My SqlAlchemyClient OBJS
            SqlAlchemyEngine = SqlAlchemyClientClass().get_engine()

            # Add Table to Metadata
            _table_obj = Table( p_table_name,
                                SqlAlchemyBaseMetadata, 
                                autoload_with = SqlAlchemyEngine  )

            # Response
            _response_tuple = ('OK', _table_obj)                                

        elif p_what == 'remove':
            
            # Remove Table from Metadata
            SqlAlchemyBaseMetadata.remove(p_table_name)
        
            # Response
            _response_tuple = ('OK', 'OK')
        
    except Exception:
        
        _msg = traceback.format_exc(2)
        _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")   

    
    # Return
    return _response_tuple

# Drop a table - no model use
def utility_drop_table_no_model(p_table_name, p_sqlalchemybasemetadata, p_sqlalchemyengine):

    # Prepare
    _inputs = f"{p_table_name}"
    _module_name = __name__
    _func_name = inspect.currentframe().f_code.co_name      
    _response_tuple = None
    _msg = None

    # Work
    try:
        
        # Add Table to Metadata
        _table_obj = Table( p_table_name,
                            p_sqlalchemybasemetadata, 
                            autoload_with = p_sqlalchemyengine  )
        
        # Remove Table from Database
        _table_obj.drop(p_sqlalchemyengine)
        
        # Remove Table from Metadata
        p_sqlalchemybasemetadata.remove(_table_obj)
        
        # Response
        _response_tuple = ('OK', 'OK')
        
    except Exception:
        
        _msg = traceback.format_exc(2)
        _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")   

    
    # Return
    return _response_tuple

# Bulk Insert ORM
def utility_bulk_insert_mappings_yes_orm(p_table_model_name, p_list_of_dicts, p_session = None):

    """
    EXAMPLE inputs

    p_table_model_name = models.MoneyloverLoadStep1Typed
    
    p_list_of_dicts = [ {'id_ml': 1, 'note': 'blablabla', 'amount': 3.4, 'category': 'CATEGGG1', 'date': '03/03/2022', 'event': 0}, 
                        {'id_ml': 2, 'note': 'blablabla', 'amount': -1.4, 'category': 'CATEGGG2', 'date': '04/03/2022', 'event': 1}, 
                        {'id_ml': 3, 'note': 'blablabla', 'amount': 7.4, 'category': 'CATEGGG3', 'date': '05/03/2022', 'event': 0}   ]        
    """

    # Prepare
    _inputs = f"{p_table_model_name}"
    _module_name = __name__
    _func_name = inspect.currentframe().f_code.co_name      
    _response_tuple = None
    _msg = None

    # Choose Session
    _session_working = None
    if not utility.is_filled(p_session):
        _session_working = SqlAlchemyClientClass().get_session_normal_started()
    else:
        _session_working = p_session

    # Work
    try:
        
        # Insert
        _session_working.bulk_insert_mappings(  mapper = p_table_model_name,
                                                mappings = p_list_of_dicts  )
    
        # Commit
        _session_working.commit()

        # Response
        _response_tuple = ('OK', 'OK')

    except Exception:
        
        _msg = traceback.format_exc(2)
        _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")   


    # Close Session
    if not utility.is_filled(p_session):
        SqlAlchemyClientClass().close_session_normal_started_input(_session_working)

    # Return
    return _response_tuple

# Truncate a table - orm workaround
def utility_truncate_table_orm(p_table_model_name):

    # Prepare
    _inputs = f"{p_table_model_name}"
    _module_name = __name__
    _func_name = inspect.currentframe().f_code.co_name      
    _response_tuple = None
    _msg = None

    ## Instance My SqlAlchemyClient OBJS
    SqlAlchemyEngine = SqlAlchemyClientClass().get_engine()
    SqlAlchemyBaseMetadata = SqlAlchemyClientClass().get_base_metadata()

    # Work
    try:
        
        """
        As there is no truncate() operation, a simple workaround in sqlalchemy for deleting all entries from a table 
        and resetting the autoincrement count is to drop and recreate the table like this
        """
        SqlAlchemyBaseMetadata.drop_all(SqlAlchemyEngine, tables=[p_table_model_name.__table__])
        SqlAlchemyBaseMetadata.create_all(SqlAlchemyEngine, tables=[p_table_model_name.__table__])
        
        # Response
        _response_tuple = ('OK', 'OK')
        
    except Exception:
        
        _msg = traceback.format_exc(2)
        _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")   

    
    # Return
    return _response_tuple
