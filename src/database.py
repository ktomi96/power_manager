from datetime import datetime
import pytz
import os

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Boolean, Float, text, select, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import pandas
import dotenv

env_path = ("./env/")
env_file = f"{env_path}.env"
dotenv.find_dotenv(env_file, raise_error_if_not_found=True)
dotenv.load_dotenv(env_file)
time_zone = os.getenv("TIME_ZONE")
db_url = f"{os.getenv('DB')}{os.getenv('DB_PATH')}"

Base = declarative_base()


class AC_LOG(Base):
    __tablename__ = "ac_logs"
    id = Column(Integer, primary_key=True)
    running = Column("running", Boolean)
    indoor_temperature = Column("indoor_temperature", Float)
    out_door_temperature = Column("out_door_temperature", Float)
    date_time = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"{self.running}, {self.indoor_temperature}, {self.out_door_temperature}, {self.date_time}"

    # def __dict__(self):
    #    return {"running": self.running, "indoor_temperature": self.indoor_temperature, "out_door_temperature": self.out_door_temperature, "date_time": self.date_time}


class SOLAR_LOG(Base):
    __tablename__ = "solar_logs"
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, default=func.now())
    power_generated = Column("power_generated", Float)
    production_time = Column("production_time", Float)
    daytime = Column("daytime", Float)
    efficeny = Column("efficeny", Float)

    def __repr__(self):
        return f"{self.date_time}, {self.power_generated}, {self.production_time}, {self.daytime}, {self.efficeny}"


def get_date():
    return datetime.now(pytz.timezone(time_zone))


def append_to_db(obj_list: list, db_url):
    engine = create_engine(db_url, echo=False, future=True)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        session.add_all(obj_list)
        session.commit()


def query(db_url, obj):
    engine = create_engine(db_url, echo=False, future=False)

    with Session(engine) as session:
        '''
        sqlalchemy 2.0 brakes pandas, cant use execute
        return session.execute(select(obj)).all()
        '''
        return session.query(obj)


def query_last_row(db_url, obj):
    engine = create_engine(db_url, echo=False, future=False)

    with Session(engine) as session:
        '''
        sqlalchemy 2.0 brakes pandas, cant use execute
        return session.execute(select(obj)).all()
        '''
        return session.query(obj).order_by(obj.id.desc()).first()


def query_to_df(db_url, obj, date_from: str, date_to: str):
    engine = create_engine(db_url, echo=False, future=False)
    with Session(engine) as session:
        query_data = session.query(obj).filter(
            obj.date_time.between(date_from, date_to)).order_by(obj.date_time.asc())

    df = pandas.read_sql_query(
        sql=query_data.statement.compile(engine), con=engine)
    df["date_time"] = df["date_time"].dt.tz_localize('UTC')
    df["date_time"] = df["date_time"].dt.tz_convert(time_zone)
    return df


if __name__ == '__main__':
    ac_log = AC_LOG()
    db_url = "sqlite:///./database/power_manager.db"
    from datetime import date
    b = AC_LOG(running=True, indoor_temperature=22.0,
               out_door_temperature=10.0, date_time="2023-01-04 17:38:38.370094")
    asd = {"running": True, "indoor_temperature": 22.0,
           "out_door_temperature": 10.0}
    a = AC_LOG(**asd)
    # append_to_db([a], db_url)
    today = date.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    print(now)
    df = query_to_df(db_url, AC_LOG,
                     today, now)

    print(df.tail())
