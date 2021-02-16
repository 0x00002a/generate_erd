#!/usr/bin/env python3

"""
generate_erd.py 

Written by Natasha England-Elbro MIT License

Usage: generate_erd.py <sqlite database path>

It will print output to stdout in the dot format. This can be run through
graphviz to generate an ERD.

"""

import sqlite3 as sql
import sys
from dataclasses import dataclass
import re
import datetime
import argparse as ap


@dataclass
class DBCol:
    name: str
    dtype: str


@dataclass
class DBTable:
    name: str
    cols: [DBCol]
    create_sql: str
    links = []  # This is [DBLink]


@dataclass
class DBLink:
    src_tbl: DBTable
    dest_tbl: DBTable
    src_col: DBCol
    dest_col: DBCol


def find_tables(conn: sql.Connection) -> [DBTable]:
    c = conn.cursor()
    c.execute("""
            SELECT
                name, sql
            FROM
                sqlite_master
            WHERE
                type = 'table'
                AND
                name NOT LIKE 'sqlite_%'
            """)
    return [DBTable(name=x[0], cols=fetch_column_data(conn, x[0]),
                    create_sql=x[1]) for x in c.fetchall()]


def find_if(src, fn):
    return [x for x in src if fn(x)][0]


def find_links(tbls: [DBTable]) -> [DBLink]:
    out = []
    fkey_reg = re.compile(
        r"FOREIGN KEY\s*\((\w+)\)\s*REFERENCES\s*(\w+)\((\w+)\)")

    for tbl in tbls:
        sql = tbl.create_sql
        matches = fkey_reg.finditer(sql)
        for m in matches:
            key_col = m.group(1)
            target_tbl = m.group(2)
            target_col = m.group(3)
            def cond(t): return t.name == target_tbl
            dest_tbl = find_if(tbls, cond)
            out.append(DBLink(src_tbl=tbl, dest_col=[x for x in dest_tbl.cols if
                                                     x.name == target_col][0],
                              src_col=[x for x in tbl.cols if
                                       x.name == key_col][0],
                              dest_tbl=dest_tbl,),)
    return out


def fetch_column_data(conn: sql.Connection, name: str) -> [DBCol]:
    c = conn.cursor()
    # Yes this is vulnerable to SQL injection
    c.execute("pragma table_info({0});".format(name))
    return [DBCol(name=x[1], dtype=x[2]) for x in c.fetchall()]


def load_formatter(path: str):
    return __import__(path).format_erd


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('-f', type=str, required=True, dest='formatter')
    args = parser.parse_args()

    conn = sql.connect(args.infile)
    tbls = find_tables(conn)

    load_formatter(args.formatter)(tbls, find_links(tbls), print)
