import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from setting import Base
from setting import ENGINE

class User(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'hantei'
    id = Column('id', Integer, primary_key = True)
    A = Column('magari', String(50))
    B = Column('sakibutori', String(50))
    C = Column('seijyo', String(50))

def main(args):
    """
    メイン関数
    """

    #Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)
