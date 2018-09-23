import os
import PyPDF2
import re
import pprint
import json
import csv


def convert2text(file):
    file = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    pageObj = pdfReader.getPage(0)
    return cleanText(pageObj.extractText())


def cleanText(text):
    text = text.replace('\n', '')
    text = re.sub("\s\s+", " ", text)
    text = text.strip()
    return text


def saveData2File(text):
    words = text.split(' ')
    data = {}

    for idx, word in enumerate(words):
        indice = idx+1
        if word == "Proposta:":
            data['proposta'] = words[indice]
        if word == "Solicitante:":
            data['solicitante'] = words[indice]
        if word == "Data:":
            data['data'] = words[indice]
        if word == "Laudas:":
            data['laudas'] = words[indice]
        if word == "Lauda:":
            indice = idx+2
            data['lauda'] = float(words[indice].replace(",", '.'))
        if word == "tradução:":
            indice = idx+2
            data['total'] = float(words[indice].replace(",", '.'))

    data['subtotal'] = float(data['laudas'])*float(data['lauda'])

    return data


def batchFiles():
    files = os.listdir('pdfs')
    data = {}
    for file in files:
        text = convert2text('pdfs/'+file)
        data = saveData2File(text)
        print(data)
        with open("orcamentos.csv", 'a') as f:
            w = csv.DictWriter(f, data.keys())
            w.writerow(data)


batchFiles()
