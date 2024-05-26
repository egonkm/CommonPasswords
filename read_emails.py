#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:29:38 2024

@author: egon
"""

# read email from .txt files, separate in names, hosts, andd passwords
# passwords file: #name@#host:password

from glob import glob
from os import path 
from sys import stderr
import psutil
import sqlite3

FILES_READ = "files_read.data"
DB = "/home/egon/emails/e-mails.db"

def connect_db(file, create=False):
    
    create = create or not path.exists(file)
    
    conn = sqlite3.connect(file)
    
    if create:
        conn.execute("drop table if exists passwords")
        conn.execute("create table passwords (host text, name text, password text, primary key (host, name))")
    return conn


def read_file(file):
    
    if not path .exists(file):
        return []
    
    with open(file, "r") as f:
        while line := f.readline():
            yield line.strip()
    
def save_file(file, content):
    
    with open(file, "w") as f:
        for item in content:
            f.write(item)
            f.write("\n")

def add_to_file(file, item):
    
    with open(file, "a") as f:
            f.write(item)
            f.write("\n")
            
def find_separator(separators, line):
    
    for separator in separators:
        if separator in line:
            return separator
    
    return False  
    
def split_line(line):
    
    if not (sep := find_separator([":", ";"], line)):
        print("Separator not found:", line, file=stderr)               
        return None, None, None
    
    try:
        idx = line.index(sep)
        name, password = line[0:idx].strip(), line[idx+1:].strip()
        
        if not name:
            print("Incomplete line: ", line, file=stderr)
            return 0,0,0
        
        if sep := find_separator(["@",","," "], name):

            name, host = name.split(sep)
        else:
            # print("Separator not found in name:", line, file=stderr)                   
            host="unknown"
            
    except Exception as e:
        print("\nERROR: ", str(e), file=stderr)
        print("Line:", line, file=stderr)
        return None, None, None
    
    return name, host, password
            
            
def read_passwords(file, conn):
    
    with open(file, "r") as f:
        
        
        for line in f:
            
            line = line.strip()
            
            if not line: continue
            
            skip = False
            
            for ignore in ["РІР‚ВР"]:
                
                if ignore in line:
                    skip = True
                    break
            
            if skip: continue
            
            name, host, password = split_line(line)
            
            if name is None: continue    
            
            try:
                
                if conn.execute(
                    "Select host,name from passwords where host=? and name=? ",
                    (host, name)
                    ).fetchone(): continue
                
                conn.execute(
                    "insert into passwords values (?,?,?)",
                    (host, name, password))
                
            except sqlite3.DatabaseError as e:
                print("Error inserting data:", line, str(e))
                
    
            
    return True

            
def get_val(conn, table, field, val):
    
    result = conn.execute(
        "select * from %s where %s=?" % (table, field),
        (val,)
    ).fetchone() 

    if result is None:
        
        conn.execute(
            "insert into %s values (NULL, ?)" % table,
            (val,)
        )          
        result = conn.execute(
            "select * from %s where %s=?" % (table, field),
            (val,)
        ).fetchone()
        
        if result is None:
            print("DOuble none")
            return None  
        
    return result[0]
    

def as_dict(a_list):
    
    return {element : idx+1 for idx,element in enumerate(a_list)}

K = 1024
M = K*K
MIN_RAM = 300*M

def main():
    
    files_read = set(read_file(FILES_READ))
    files = glob("../**/*.txt")
    #print("FILES:", len(files))
    count = 1

    with connect_db(DB) as conn:

    
        for file in files:
        
            if psutil.virtual_memory().free<MIN_RAM:
                print("Running out of ram!")
                #break
                
            if file in files_read:
            	continue
            	
            files_read.add(file)
            add_to_file(FILES_READ, file)
            
            print(count,"/", #len(files),
             file, path.getsize(file)/M,           
                  psutil.virtual_memory().free//M)
            
            count += 1
            
            path_, file_ = path.split(file)
                   
            try:
                if not read_passwords(file, conn):
                    continue
                
            except Exception as e:
                print("***Error reading file", file=stderr)
                print(str(e), file=stderr)
        
          
 
        
if __name__ == "__main__": 
    pass 
    main()
