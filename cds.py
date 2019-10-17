#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import urllib.request

from urllib.request import urlopen
from bs4 import BeautifulSoup

CAMBRIDGE_URL = "http://dictionary.cambridge.org/dictionary/english"


def usage():
    print("Usage: {name} 1.inputFileName 2.outputFileName 3.NumberOfDefines".format(name=sys.argv[0]))
    sys.exit(1)


def main(vocaFileName,outputFileName,defSize):
    try :
        vocaFile = open(vocaFileName,'r')
        outFile = open(outputFileName,'w')

        vocas =vocaFile.readlines()
    except :
        print("check your file name")
        exit()

    for voca in vocas :
        try :
            
            req = urllib.request.Request("/".join([CAMBRIDGE_URL, voca]), headers={'User-Agent': 'Mozilla/5.0'})
            camUrl = urlopen(req)
            soup = BeautifulSoup(camUrl, 'html.parser')
            defines = soup.findAll('div',class_='ddef_h')
        
            outFile.write(voca)
            
            print(voca)

            outFile.write("==")
            i = 0
            while  i<int(defSize) :
                try : 
                    outFile.write(defines[i].text+"\n")
                    i += 1
                except :
                    break
            outFile.write("@")
        except :
            break
    vocaFile.close()
    outFile.close()



if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
    main(sys.argv[1], sys.argv[2],sys.argv[3])
