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

FOLDERS = "folders.data"
HOSTS = "hosts.data"
NAMES = "names.data"
PASSWORDS = "passwords.data"
ERRORS = "errors.data"

def read_file(file):
    
    if not path.exists(file):
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

    print("Separator not found:", line, file=stderr)
    
    return False  
    
def read_passwords(file, hosts, names, passwords_file):
    
    with open(file, "r") as f:
        
        with open(passwords_file, "a") as f_pass:
            
            for line in f.readlines():
                
                line = line.strip()
                
                if not line: continue
                
                skip = False
                
                for ignore in ["РІР‚ВР Р"]:
                    
                    if ignore in line:
                        skip = True
                        break
                
                if skip: continue
                
                if not (sep := find_separator([":", ";"], line)):
                    return False
                
                try:
                    idx = line.index(sep)
                    name, password = line[0:idx].strip(), line[idx+1:].strip()
                    
                    if not name:
                        print("Incomplete line: ", line, file=stderr)
                        continue
                    
                    if sep := find_separator(["@",","," "], name):
        
                        name, host = name.split(sep)
                    else:
                        host=name
                        
                except Exception as e:
                    print("\nERROR: ", str(e), file=stderr)
                    print("Line:", line, file=stderr)
                    continue
                
                idx_name = get_val(name, names)
                idx_host = get_val(host, hosts)
                
           
                f_pass.write(str(idx_name)
                             +"@"+str(idx_host)+":"+password+"\n")
     
    return True

            
def get_val(string, dic):
    
    if string not in dic:
        dic[string] = len(dic)+1
    
    return dic[string]

def as_dict(a_list):
    
    return {element : idx+1 for idx,element in enumerate(a_list)}

K = 1024
M = K*K

def main():
    
    files = glob("../**/*.txt")
    print("FILES:", len(files))
    
    folders = set(read_file(FOLDERS))
    hosts = as_dict(read_file(HOSTS))
    names = as_dict(read_file(NAMES))
    errors = []
            
    for file in files:
        
        print(file, getsizeof(hosts)//M, getsizeof(names)//M)
        path_, file_ = path.split(file)
        if path_ in folders: continue
        
        try:
            if not read_passwords(file, hosts, names, PASSWORDS):
                errors.append(file)
                continue
            folders.add(path_)
        except Exception as e:
            print("***Error reading file")
            print(str(e))
        
        
        save_file(FOLDERS, folders)  
        save_file(HOSTS, hosts.keys())
        save_file(NAMES, names.keys())
        save_file(ERRORS, errors)
        
if __name__ == "__main__": 
    
    main()