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

FOLDERS = "folders.data"
HOSTS = "hosts.data"
NAMES = "names.data"
PASSWORDS = "passwords.data"

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

def read_passwords(file, hosts, names, passwords_file):
    
    with open(file, "r") as f:
        
        for line in f.readlines():
            
            line = line.strip()
            
            name, password = line.split(":")
            host, name = name.split("@")
            
            idx_name = get_val(name, names)
            idx_host = get_val(host, hosts)
            
            with open(passwords_file, "a") as f_pass:
                f_pass.write(str(idx_name)
                             +"@"+str(idx_host)+":"+password+"\n")
                
            
def get_val(string, dic):
    
    if string not in dic:
        dic[string] = len(dic)+1
    
    return dic[string]

def as_dict(a_list):
    
    return {element : idx+1 for idx,element in enumerate(a_list)}
def main():
    
    files = glob("../**/*.txt")
    folders = set(read_file(FOLDERS))
    hosts = as_dict(read_file(HOSTS))
    names = as_dict(read_file(NAMES))
            
    for file in files:
        
        print(".", end="")
        path_, file_ = path.split(file)
        if path_ in folders: continue
        folders.add(path_)
        
        read_passwords(file, hosts, names, PASSWORDS)
        
        
    save_file(FOLDERS, folders)  
    
if __name__ == "__main__": 
    
    main()