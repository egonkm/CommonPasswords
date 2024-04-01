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
from sys import stderr, getsizeof
import psutil
import sqlite3

FOLDERS = "folders.data"


def create_tables(conn):
    
    conn.execute("drop table names")
    conn.execute("drop table hosts")
    conn.execute("drop table passwords")
    conn.execute("create table names (id integer primary key autoincrement, name text)")
    conn.execute("create table hosts ( id integer primary key autoincrement, host text)")
    conn.execute("create table passwords (host integer, name integer, password text, primary key (host, name))")
    
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
            print("Separator not found in name:", line, file=stderr)                   
            host=name
            
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
            
            for ignore in ["РІР‚ВР Р"]:
                
                if ignore in line:
                    skip = True
                    break
            
            if skip: continue
            
            name, host, password = split_line(line)
            
            if name is None: continue
        
            
            idx_name = conn.execute("")
            idx_host = 
            
       
 
    return True

            
def get_val(string, dic):
    
    if string not in dic:
        dic[string] = len(dic)+1
    
    return dic[string]

def as_dict(a_list):
    
    return {element : idx+1 for idx,element in enumerate(a_list)}

K = 1024
M = K*K
MIN_RAM = 512*M

def main():
    
    conn = sqlite3.connect("emails.db")
    folders = read_file()(FOLDERS)
    files = glob("../**/*.txt")
    print("FILES:", len(files))

    count = 1
    
    for file in files:
    
        if psutil.virtual_memory().free<MIN_RAM:
            print("Running out of ram!")
            break
        
        print(count,"/", len(files), file,              
              psutil.virtual_memory().free//M)
        
        count += 1
        
        path_, file_ = path.split(file)
        if path_ in folders: continue
        
        try:
            if not read_passwords(file, conn):
                continue
            folders.add(path_)
        except Exception as e:
            print("***Error reading file", file=stderr)
            print(str(e), file=stderr)
        
    save_file(FOLDERS, folders)  
    conn.close() 
        
if __name__ == "__main__": 
    pass 
    # main()