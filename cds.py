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
        # vocas = [line.rstrip('\n') for line in outFile]
        vocas =vocaFile.readlines()
        # print(vocas)
    except :
        print("check your file name")
        exit()

    for voca in vocas :
        try :
            voca = voca.rstrip()
            if len(voca.split())>1:
                voca = voca.replace(" ","-")
            req = urllib.request.Request("/".join([CAMBRIDGE_URL, voca]), headers={'User-Agent': 'Mozilla/5.0'})
            camUrl = urlopen(req)
            soup = BeautifulSoup(camUrl, 'html.parser')

            defines = soup.findAll('div', class_='ddef_h')
            examples = soup.findAll('div', class_='def-body ddef_b' )

            examples_d = []
            for div in examples:
                inner_div = div.find('div', class_='had daccord_b')
                inner_header = div.find('header', class_='ca_h')
                if inner_div:
                    # print(inner_div)
                    inner_div.extract()
                if inner_header:
                    # print(inner_header)
                    inner_header.extract()
                examples_d.append(div.text.strip())


            outFile.write(voca+'\n')

            print(examples_d)
            
            i = 0
            while  i<=int(defSize) :
                try : 
                    outFile.write(f"=======Definition {i  }:=======\n")
                    outFile.write(defines[i].text+"\n")
                    outFile.write(f"=======Examples of using {voca}:=======\n")
                    outFile.write(examples[i].text+"\n\n\n")
                    i += 1
                except :
                    break
            outFile.write("\n\n")
        except :
            break
    vocaFile.close()
    outFile.close()



if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
    main(sys.argv[1], sys.argv[2],sys.argv[3])
