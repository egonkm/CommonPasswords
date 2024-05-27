#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:29:38 2024

@author: egon
"""


def main(min_count=100):

    
    with open("passwords.txt", "r") as f:
        for line in f:
             
            vals = line = line.strip().split(", ")
            if len(vals) != 2: continue
            k, v = vals
            if int(v)>=min_count:
                print(k, v)
             
if __name__ == "__main__": 

    main(10000)
