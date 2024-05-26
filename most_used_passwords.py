#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:29:38 2024

@author: egon
"""


def main(min_count=100):

    
    with open("passwords.txt", "r") as f:
        for line in f:
             
            line = line.strip()
            if not line: continue

            try:
                k,v = line.split(", ")
            except:
                continue
             
            v = int(v)
            if v>=min_count:
                print(k, v)
             
if __name__ == "__main__": 

    main(1000)
