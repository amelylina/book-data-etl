import re
from typing import Dict, List
from pathlib import Path
import json
import sqlite3 as sql
import logging

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
INPUT_PATH = PROJECT_ROOT / 'raw_data' / 'task1_d.json'
DB_PATH = PROJECT_ROOT/ 'task1.db'

# helper-parser function
def convert_ruby_hash_to_dict(ruby_hash)-> List[Dict]:
    new_str = re.sub(":(\w+)=>", r'"\1" :', ruby_hash)
    return json.loads(new_str)


if __name__ == "__main__" :

    log.info("Reading raw data file")

    with open(INPUT_PATH, 'r') as f:
        ruby_hash = f.read()

    parsed_list = convert_ruby_hash_to_dict(ruby_hash)
    log.info(f"Parsed {len(parsed_list)} books")

    # sqlite has issues with very big numbers
    for book in parsed_list:
        book['id'] = str(book['id'])

    # create the db
    log.info(f"Connecting to db")
    con = sql.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            publisher TEXT NOT NULL,
            year INTEGER NOT NULL,
            price TEXT NOT NULL
            )
            """
        )

        cur.executemany("""INSERT INTO books (id, title, author, genre, publisher, year, price) 
                        VALUES(:id, :title, :author, :genre, :publisher, :year, :price);
                        """, parsed_list)
        con.commit()

        log.info("Successfully created/inserted data into db")

    except Exception as e:
        con.rollback()
        log.warning(f"Couldn't load data: {e}")

    finally:
        con.close()
