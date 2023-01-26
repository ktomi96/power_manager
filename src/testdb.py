from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Boolean, Float, text
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas
from sqlalchemy.orm import Session


Base = declarative_base()


class AC_LOG(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    running = Column("running", Boolean)
    indoor_temperature = Column("indoor_temperature", Float)
    out_door_temperature = Column("out_door_temperature", Float)

    def __init__(self):
        self.engine = create_engine(
            "sqlite:///./database/power_manager.db", echo=False)
        Base.metadata.create_all(bind=self.engine)

    def __repr__(self):
        return f"{self.running}, {self.indoor_temperature}, {self.out_door_temperature}, {self.date_time}"

    def append_to_db(self, temp):
        self.running = 1
        self.indoor_temperature = temp
        self.out_door_temperature = 1

        with Session(self.engine) as session:
            session.add(self)
            session.commit()

    def query_all(self):
        with Session(self.engine) as session:
            return session.query(AC_LOG)

    def query_to_df(self):
        query_data = self.query_all()
        return pandas.read_sql_query(sql=query_data.statement.compile(self.engine), con=self.engine)


if __name__ == '__main__':
    solar = AC_LOG()
    for a in [1, 2, 3, 4, 5]:
        solar.append_to_db(a)

    print(solar.query_all())
