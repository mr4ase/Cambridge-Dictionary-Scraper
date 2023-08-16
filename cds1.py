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

def get_text_with_spaces(element):
    """Extract text from an element and its children, adding spaces between them."""
    text = " ".join(element.stripped_strings)
    text = re.sub(r'\s([?.!,";:])', r'\1', text)
    return text


def main(vocaFileName,outputFileName):
    try :
        vocaFile = open(vocaFileName, 'r')
        outFile = open(outputFileName,'w', encoding='utf-8')
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
            divs_ddef_h = soup.find_all('div', class_='ddef_h')
            transcription_span = soup.find('span', class_='ipa dipa lpr-2 lpl-1')
            if transcription_span:
                transcription = transcription_span.get_text(strip=True)
            # print(divs_ddef_h)
            outFile.write(f"=============\n{voca}\n")
            outFile.write(f"/{transcription}/\n\n")



            parsed_data = []

            for div in divs_ddef_h:
                description = get_text_with_spaces(div)
                
                # Find the associated examples div for the current description
                examples_div = div.find_next_sibling('div', class_='def-body ddef_b')
                examples = []
                if examples_div:
                    examples = [get_text_with_spaces(examp) for examp in examples_div.find_all('span', class_='eg deg')]
    
                parsed_data.append((description, examples))

            # Write to a .txt file
            print(transcription)
            # outFile.write(transcription)
            # outFile.write(f" {transcription_span} \n")
            for description, examples in parsed_data:
                outFile.write(f"---\n{description}\n---\n\n\n\n\n")
                for example in examples:
                    outFile.write(f"- {example}\n")
                outFile.write("\n")

            print("Data has been written to parsed_data.txt")

        except :
            break
    vocaFile.close()
    outFile.close()



if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    main(sys.argv[1], sys.argv[2])
