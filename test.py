vocacc = 'traffic jam'
print(len(vocacc.split()))
if len(vocacc.split())>1:
    print(vocacc)
    vocacc = vocacc.replace(" ","-")
    print(vocacc)