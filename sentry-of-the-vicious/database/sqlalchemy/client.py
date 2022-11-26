"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
## Log
import traceback
import inspect
## Sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
## General
from mymoney import config
from mymoney.common import utility


# Borg pattern singleton
class SqlAlchemyClientClass:

    # Database&User Url
    __sqlalchemy_url = config.SQLALCHEMY_URL
    
    # Options Engine & SessionFactory
    __option_engine_pool_size = 20
    __option_engine_pool_recycle = 7200 # 120 minutes ; 2 hr
    __option_session_autocommit = False
    __option_session_autoflush = True
    __option_session_expire_on_commit = False
    
    # Prepare Borg
    __base_builded_response = None
    __engine_builded_response = None
    __session_factory_builded_response = None
    
    # Prepare OnDemand     
    __session_normal_started_response = None
    __session_scoped_started_response= None    
    __session_normal_started = None
    __session_scoped_started = None

    # Init with BORG Singleton: base, engine and session factory
    __state = {}
    def __init__(self):
        self.__dict__ = self.__state
        if not hasattr(self, 'borg_base'):
            self.__base_builded_response = self.__build_base()
            if self.check_base_build_ok():
                self.borg_base = self.__base_builded_response[1] 
        if not hasattr(self, 'borg_engine'):
            self.__engine_builded_response = self.__build_engine()
            if self.check_engine_build_ok():
                self.borg_engine = self.__engine_builded_response[1] 
        if not hasattr(self, 'borg_session_factory'):
            self.__session_factory_builded_response = self.__build_session_factory()
            if self.check_session_factory_build_ok():
                self.borg_session_factory = self.__session_factory_builded_response[1]
                 
    """"""""""""
    """ BORG """
    """"""""""""

    """ DECLARATIVE CLASS DEFINITIONS """
    
    # Build
    def __build_base(self):
    
        # Prepare
        _inputs = None
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None
        _declarative_base_obj = None
        
        try:
            
            # Get
            _declarative_base_obj = declarative_base()
            
            # Response
            _response_tuple = ('OK',_declarative_base_obj)
        
        except:
            _msg = traceback.format_exc(2)
            _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
                  
        return(_response_tuple)

    # Check if build was successful
    def check_base_build_ok(self):
        if self.__base_builded_response[0] == 'OK':
            return True
        else:
            return False

    # Return error when the build went wrong 
    def get_base_msg_nok(self):
        return self.__base_builded_response[1]

    # Return builded Base
    def get_base(self):
        return self.borg_base

    # Return builded Base Metadata
    def get_base_metadata(self):
        return self.borg_base.metadata

    """ ENGINE """
    
    # Build
    def __build_engine(self):
    
        # Prepare
        _inputs = f"{self.__sqlalchemy_url}|{self.__option_engine_pool_size}|{self.__option_engine_pool_recycle}"
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None
        _engine_obj = None
        
        try:
            
            # Get
            _engine_obj = create_engine(    self.__sqlalchemy_url, 
                                            pool_size = self.__option_engine_pool_size, 
                                            pool_recycle = self.__option_engine_pool_recycle   )
            
            # Response
            _response_tuple = ('OK',_engine_obj)
            
        except Exception:
            _msg = traceback.format_exc(2)
            _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
                  
        return(_response_tuple)

    # Check if build was successful
    def check_engine_build_ok(self):
        if self.__engine_builded_response[0] == 'OK':
            return True
        else:
            return False

    # Return error when the build went wrong 
    def get_engine_msg_nok(self):
        return self.__engine_builded_response[1]

    # Return builded 
    def get_engine(self):
        return self.borg_engine


    """ SESSION FACTORY """
    
    # Build
    def __build_session_factory(self):
    
        # Prepare
        _inputs = f"{self.__option_session_autocommit}|{self.__option_session_autoflush}|{self.__option_session_expire_on_commit}"
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None
        _engine_obj = None
        _session_factory = None

        try:
            
            # Get Engine
            _engine_obj = self.borg_engine
            
            # Build Session Factory
            _session_factory = sessionmaker(    autocommit = self.__option_session_autocommit,
                                                autoflush = self.__option_session_autoflush,
                                                expire_on_commit = self.__option_session_expire_on_commit,
                                                bind = _engine_obj  )
           
           # Response
            _response_tuple = ('OK',_session_factory)
            
        except Exception:
            _msg = traceback.format_exc(2)
            _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
                  
        return(_response_tuple)

    # Check if build was successful
    def check_session_factory_build_ok(self):
        if self.__session_factory_builded_response[0] == 'OK':
            return True
        else:
            return False

    # Return error when the build went wrong 
    def get_session_factory_msg_nok(self):
        return self.__session_factory_builded_response[1]

    # Return builded 
    def get_session_factory(self):
        return self.borg_session_factory


    """"""""""""""""""
    """  ON DEMAND """
    """"""""""""""""""


    """ SESSION NORMAL """

    # Start
    def __start_session_normal(self):
    
        # Prepare
        _inputs = None
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None
        _session_factory = None
        _session_started_obj = None

        try:
            
            # Get Session Factory
            _session_factory = self.borg_session_factory
            
            # Start Session with ()
            _session_started_obj = _session_factory()
            
            # Response
            _response_tuple = ('OK',_session_started_obj)
            
        except Exception:
            _msg = traceback.format_exc(2)
            _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
                  
        return(_response_tuple)

    # Check if start was successful
    def check_session_normal_started_ok(self):
        if self.__session_normal_started_response[0] == 'OK':
            return True
        else:
            return False

    # Return error when the start went wrong 
    def get_session_normal_started_msg_nok(self):
        return self.__session_normal_started_response[1]

    # Return started 
    def get_session_normal_started(self):
        
        self.__session_normal_started_response = self.__start_session_normal()
        if self.check_session_normal_started_ok():
            self.__session_normal_started = self.__session_normal_started_response[1]        
        
        return self.__session_normal_started

    # Stop - Close
    def close_session_normal_started_input(self, p_session):
    
        # Prepare
        _inputs = None
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None

        if utility.is_filled(p_session):
            try:
                p_session.close()
                _response_tuple = ('OK', True)
            except Exception:
                _msg = traceback.format_exc(2)
                _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
        else:
            _response_tuple = ('OK', False)
            
        return _response_tuple


    """ SESSION SCOPED """

    # Start
    def __start_session_scoped(self, _scopefunc):
    
        # Prepare
        _inputs = f"{_scopefunc}"
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None
        _session_factory_obj = None
        _session_started_obj = None

        try:
            
            # Get Session Factory
            _session_factory_obj = self.borg_session_factory
            
            # Start Session Scoped
            _session_started_obj = scoped_session(_session_factory_obj, scopefunc = _scopefunc)
            
            # Response
            _response_tuple = ('OK',_session_started_obj)
            
        except Exception:
            _msg = traceback.format_exc(2)
            _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
                  
        return(_response_tuple)

    # Check if start was successful
    def check_session_scoped_started_ok(self):
        if self.__session_scoped_started_response[0] == 'OK':
            return True
        else:
            return False

    # Return error when the start went wrong 
    def get_session_scoped_started_msg_nok(self):
        return self.__session_scoped_started_response[1]

    # Return started 
    def get_session_scoped_started(self, _scopefunc):
        
        self.__session_scoped_started_response = self.__start_session_scoped(_scopefunc)
        if self.check_session_scoped_started_ok():
            self.__session_scoped_started = self.__session_scoped_started_response[1]        
        
        return self.__session_scoped_started

    # Stop - Remove
    def close_session_scope_started_input(self, p_session):
    
        # Prepare
        _inputs = None
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None
        
        if utility.is_filled(p_session):
            try:
                p_session.remove()
                _response_tuple = ('OK', True)
            except Exception:
                _msg = traceback.format_exc(2)
                _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
        else:
            _response_tuple = ('OK', False)
        
        return _response_tuple


    """ COMMON """
    def close_sqlalchemy(self, _session_normal = None, _session_scoped = None):
    
        # Prepare
        _inputs = None
        _module_name = __name__
        _func_name = inspect.currentframe().f_code.co_name      
        _response_tuple = None
        _msg = None

        try:
            if utility.is_filled(_session_normal):
                self.close_session_normal_started_input(_session_normal)
            if utility.is_filled(_session_scoped):
                self.close_session_scope_started_input(_session_scoped)                
            Session.close_all()
            self.borg_engine.dispose()
            _response_tuple = ('OK', True)
        except Exception:
            _msg = traceback.format_exc(2)
            _response_tuple = ('NOK', f"{ utility.my_log('Exception',_module_name,_func_name,inspect.currentframe().f_lineno,_inputs,_msg)}")        
                  
        return(_response_tuple)
