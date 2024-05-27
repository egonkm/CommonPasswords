#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:29:38 2024

@author: egon
"""

import sqlite3

DB = "e-mails.db"

        # conn.execute("create table passwords (host text, name text, password text, primary key (host, name))")
  

def main(min_count):


    with sqlite3.connect(DB) as conn:   
    
        cursor = conn.cursor()
        query = f"SELECT password, count(password) FROM passwords GROUP BY password HAVING count(password)>{min_count}"
        cursor.execute(query)

        with open("most_used2.txt", "w") as f:
            for record in cursor:
                f.write(record[0]+", "+str(record[1])+"\n")
        
        

if __name__ == "__main__": 

    main(10000)
