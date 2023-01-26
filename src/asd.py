import asyncio
import csv
from sqlalchemy import create_engine

async def migrate_csv_to_sqlalchemy(file_path, table_name, db_url):
    # create a sqlalchemy engine
    engine = create_engine(db_url)

    # read the csv file
    async with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # create a list to store the rows
        rows = []

        # iterate through the rows in the csv
        async for row in reader:
            rows.append(row)

        # insert the rows into the table
        engine.execute(f"INSERT INTO {table_name} ({', '.join(rows[0].keys())}) VALUES {', '.join(['?' for _ in rows[0].keys()])}", *[tuple(row.values()) for row in rows])