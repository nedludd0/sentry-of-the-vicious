"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
## SqlAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, BigInteger, Float, Interval
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
## Common
from sentry.common import utility
## Database (SqlAlchemy)
from sentry.database.sqlalchemy.client import SqlAlchemyClientClass

"""""""""""""""""""""""""""""""""
INSTANCE My SqlAlchemyClient OBJS
"""""""""""""""""""""""""""""""""
Base = SqlAlchemyClientClass().get_base()


"""""""""""""""""""""""""""
 Abstract to extend - 4 
"""""""""""""""""""""""""""

class MyBase(Base):
    
    # Property
    __abstract__ = True

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False, default=utility.my_time_now('no-format'))
    updated = Column(DateTime)

class MyCatalog(MyBase):

    # Property
    __abstract__ = True

    # Columns
    name = Column(String(50), unique=True, nullable=False)
    label = Column(String(100))
    description = Column(String(200))
    enabled = Column(Boolean, nullable=False, default=False)

class MyType(MyCatalog):

    # Property
    __abstract__ = True

    # Columns
    group = Column(String(50), nullable=False)

class MyLogs(MyBase):

    # Property
    __abstract__ = True

    # Columns
    result_short = Column(String(20), index=True, nullable=False)
    result_full = Column(String(600), nullable=False)

"""""""""""""""""""""""""""
 DATA Area - 6 
"""""""""""""""""""""""""""

# Anag
class ViciousData(MyBase):

    # Property
    __tablename__ = 'vicious_data'

    # Columns
    qta = Column(Integer, unique=True, nullable=False)
    vicious_data_category_fk = Column(Integer, ForeignKey('vicious_data_category.id'))  
    
    vicious_data_category = relationship("ViciousDataCategory")
    
class ViciousDataCategory(MyCatalog):

    # Property
    __tablename__ = 'vicious_data_category'
