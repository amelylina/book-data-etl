# Book Data ETL

*A data-engineering exercise, cleaned up and documented as a portfolio piece.*

A small ETL pipeline that ingests a semi-structured data file into a relational
database and runs an in-database transformation to produce a yearly summary of
book publications.

## What it does

1. **Extract & Load** - Reads a raw data file and loads each record into a
   SQLite `books` table.
2. **Transform** - Runs a SQL query *inside the database* that aggregates books
   by publication year and computes a summary table.

The input file looks like JSON but is actually a serialized array of Ruby
hashes (`:key=>value` syntax), so it can't be parsed by a standard JSON reader
without preprocessing.

## The summary table

| Field           | Description                                                      |
|-----------------|------------------------------------------------------------------|
| `year`          | Publication year                                                 |
| `book_count`    | Number of books published that year                             |
| `average_price` | Average price of those books in USD, rounded to cents           |

Prices in the source data are a mix of USD (`$`) and EUR (`€`). EUR values are
converted to USD at a fixed rate of **€1 = $1.20** during transformation.

## Design decisions

- **Python `re` over Ruby `eval` for parsing.** The data is valid Ruby hash
  syntax, so `eval` in Ruby would parse it in one line - but `eval` executes
  *any* code in the file, which is unsafe for input I don't fully control. I
  used a small regex to rewrite the Ruby hash syntax into valid JSON instead.
- **SQLite.** Lightweight, zero-setup, and bundled with Python's standard
  library - a good fit for a self-contained exercise.
- **IDs stored as `TEXT`.** Some IDs exceed the 64-bit integer limit, so they're
  kept as strings to avoid overflow.
- **Transformation lives in SQL, not Python.** The currency conversion and
  aggregation happen entirely inside the database (per the task constraint that
  transformation should be in the RDBMS).

## Running it

```bash
# 1. Load the raw data into SQLite (creates books table in book-data.db)
python src/load.py

# 2. Build the summary table
sqlite3 book-data.db < src/transform.sql

# 3. Inspect the result
sqlite3 book-data.db "SELECT * FROM summary ORDER BY year;"
```

Requires Python 3.x (standard library only) and the `sqlite3` CLI.

## Project structure

```
.
├── notes/
│   └── rejected_ruby_eval.rb  # how i would parse it, if i trusted the raw file
├── data/
│   └── books_raw.json         # raw input (Ruby-hash format)
├── src/
│   ├── load.py                # extract + load into SQLite
│   └── transform.sql          # in-database aggregation
└── README.md
```