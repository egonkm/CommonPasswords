#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:29:38 2024

@author: egon
"""

import sqlite3

DB = "e-mails.db"

        # conn.execute("create table passwords (host text, name text, password text, primary key (host, name))")
  

def main():

    passwords = dict()

    with sqlite3.connect(DB) as conn:   
    
        cursor = conn.cursor()
        query = "SELECT password FROM passwords"
        cursor.execute(query)

        for idx, record in enumerate(cursor):

            passwords[record[0]] = passwords.get(record[0], 0) + 1
            if idx%100000==0: 
                print(idx)
                

    with open("passwords.txt", "w") as f:
        for k,v in passwords.items():
            f.write(k+", "+str(v)+"\n")

if __name__ == "__main__": 

    main()
