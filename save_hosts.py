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

    hosts = set()

    with sqlite3.connect(DB) as conn:   
    
        cursor = conn.cursor()
        query = "SELECT host FROM passwords"
        cursor.execute(query)

        with open("hosts.txt", "w") as f: 
            for record in cursor:
                if record[0] in hosts: continue
                f.write(record[0]+"\n")
                hosts.add(record[0])
                if len(hosts) % 1000 == 0: print(".", end="")


        
            
        
if __name__ == "__main__": 

    main()
