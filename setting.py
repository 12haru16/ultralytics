
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

# mysql��DB�̐ݒ�
DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    "root",
    "Choco12.16haru",
    "127.0.0.1",
    "kyuri",
)
ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True # True���Ǝ��s�̂��т�SQL���o�͂����
)

# Session�̍쐬
session = scoped_session(
  # ORM���s���̐ݒ�B�����R�~�b�g���邩�A�������f����ȂǁB
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

# model�Ŏg�p����
Base = declarative_base()
Base.query = session.query_property()
