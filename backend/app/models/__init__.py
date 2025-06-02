from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config, create_engine
from .base import Base
import logging

logger = logging.getLogger('db')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

DBSession = scoped_session(sessionmaker(
    expire_on_commit=False,
    autoflush=True,
    autocommit=False
))

def init_db(settings):
    try:
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False

from .category import Category
from .transaction import Transaction