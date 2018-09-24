import os
import PyPDF2
import re
import pprint
import json
import csv


class XtractData:
    def __init__(self, pdfs_directory, company):
        self.pdfs_directory = pdfs_directory
        self.company = company
        self.batchFiles()
        pass

    def convert2text(self, file):
        file = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(file)
        pageObj = pdfReader.getPage(0)
        text = self.cleanText(pageObj.extractText())
        file.close()
        return text

    def cleanText(self, text):
        text = text.replace('\n', '')
        text = re.sub("\s\s+", " ", text)
        text = text.strip()
        return text

    def athena_data(self, text):
        words = text.split(' ')
        laudas = 0
        lauda = 0.0
        subtotal = 0.0

        for idx, word in enumerate(words):
            indice = idx+1
            if word == "Proposta:":
                proposta = int(words[indice])
            if word == "Solicitante:":
                solicitante = words[indice]
            if word == "Data:":
                dataProposta = words[indice]
            if word == "Laudas:":
                laudas = int(words[indice])
            if word == "Lauda:":
                indice = idx+2
                lauda = float(words[indice].replace(",", '.'))
            if word == "tradução:":
                indice = idx+2
                total = float(words[indice].replace(",", '.'))
        if(laudas != 0 and lauda != 0):
            subtotal = float(laudas)*float(lauda)

        data = {}
        data['Fornecedor'] = self.company.upper()
        data['Proposta'] = proposta
        data['Solicitante'] = solicitante
        data['Data'] = dataProposta
        data['Laudas'] = laudas
        data['Valor_Lauda'] = lauda
        data['Subtotal'] = subtotal
        data['Total'] = total

        return data

    def batchFiles(self):
        files = os.listdir(self.pdfs_directory)
        data = {}
        for file in files:
            text = self.convert2text(self.pdfs_directory+"/"+file)
            if self.company == "athena":
                data = self.athena_data(text)
                print(data)
            #os.remove(self.pdfs_directory+"/"+file)

            with open("orcamentos.csv", 'a', newline='') as f:
                w = csv.DictWriter(f, data.keys())
                w.writerow(data)
