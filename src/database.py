from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Boolean, Float, text
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas


Base = declarative_base()


class AC_LOG(Base):
    __tablename__ = "ac_logs"
    id = Column(Integer, primary_key=True)
    running = Column("running", Boolean)
    indoor_temperature = Column("indoor_temperature", Float)
    out_door_temperature = Column("out_door_temperature", Float)
    date_time = Column("date_time", String)

    def __init__(self):

        self.engine = create_engine(
            "sqlite:///./database/power_manager.db", echo=False, future=True)
        Base.metadata.create_all(bind=self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __repr__(self):
        return f"{self.running}, {self.indoor_temperature}, {self.out_door_temperature}, {self.date_time}"

    def append_to_db(self, **status):
        self.running = status["running"]
        self.indoor_temperature = status["indoor_temperature"]
        self.out_door_temperature = status["out_door_temperature"]
        self.date_time = status["date_time"]

        self.session.add(self)
        self.session.commit()

    def query_all(self):
        return self.session.query(AC_LOG)

    def query_to_df(self):
        query_data = self.query_all()
        return pandas.read_sql_query(sql=query_data.statement.compile(self.engine), con=self.engine)


class SOLAR_LOG(Base):
    __tablename__ = "solar_logs"
    id = Column(Integer, primary_key=True)
    date_time = Column("date_time", String)
    power_generated = Column("power_generated", Float)
    production_time = Column("production_time", Float)
    daytime = Column("daytime", Float)
    efficeny = Column("efficeny", Float)

    def __init__(self):
        self.engine = create_engine(
            "sqlite:///./database/power_manager.db", echo=False, future=True)
        Base.metadata.create_all(bind=self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __repr__(self):
        return f"{self.date_time}, {self.power_generated}, {self.production_time}, {self.daytime}, {self.efficeny}"

    def append_to_db(self, **status):
        self.date_time = status["date_time"]
        self.power_generated = status["power_generated"]
        self.production_time = status["production_time"]
        self.daytime = status["daytime"]
        self.efficeny = status["efficeny"]

        self.session.add(self)
        self.session.commit()

    def query_all(self):
        return self.session.query(SOLAR_LOG)

    def query_to_df(self):
        query_data = self.query_all()
        return pandas.read_sql_query(sql=query_data.statement.compile(self.engine), con=self.engine)


if __name__ == '__main__':
    solar = AC_LOG()
    print(solar.query_all())
