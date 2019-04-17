import os
import re
import PyPDF2
import csv


class XtractData:
    def __init__(self, pdfs_directory, company, save_as, delete=False, repeat=False):
        self.pdfs_directory = pdfs_directory
        self.company = company
        self.save_as = save_as
        self.delete = delete
        self.repeat = repeat
        self.batch_files()

    def convert2text(self, file):
        file = open(file, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(file)
        page_obj = pdf_reader.getPage(0)
        text = self.clean_text(page_obj.extractText())
        file.close()
        return text

    @staticmethod
    def clean_text(text):
        text = text.replace('\n', ' ')
        text = re.sub(r"\s\s+", " ", text)
        text = text.strip()
        return text

    def athena_data(self, text):
        words = text.split(' ')
        descritivo = ''
        solicitante = ''
        laudas = 0
        lauda = 0.0
        subtotal = 0.0
        total = ''
        proposta = ''
        data_proposta = ''
        print(" ")
        print("=========================================================")
        for idx, word in enumerate(words):
            indice = idx + 1
            if word == "Proposta":
                for i in range(10):
                    if words[indice + i] != "Empresa":
                        proposta = proposta + words[indice + i]
                        proposta = proposta.replace(".", "")
                        proposta = proposta.replace(":", "")
                        proposta = proposta[:5]
                        proposta = proposta.strip()
                    else:
                        break
                print("proposta", proposta)
            if word == "Solicitante:" or word == "Solicitante":
                for i in range(10):
                    if words[indice + i] == "Data" or words[indice + i] == "Data:" or words[indice + i] == "Empresa" or \
                            words[indice + i] == "Empresa:":
                        break
                    else:
                        solicitante = solicitante + " " + words[indice + i]
                        solicitante = solicitante.replace(":", "")
                        solicitante = solicitante.strip()
                print("Solicitante", solicitante)
            if word == "Data:" or word == "Data":
                for i in range(10):
                    if words[indice + i] == "Descritivo" or words[indice + i] == "Descritivo:":
                        break
                    else:
                        data_proposta = data_proposta + " " + words[indice + i]
                        data_proposta = data_proposta.replace(":", "")
                        data_proposta = data_proposta.replace(" ", "")
                        data_proposta = data_proposta.strip()
                print("Data da Proposta", data_proposta)

            if word == "Descritivo:" or word == "Descritivo":
                for i in range(10):
                    if words[indice + i] == "Tipo" or words[indice + i] == "Tipo:":
                        break
                    else:
                        descritivo = descritivo + " " + words[indice + i]
                        descritivo = descritivo.replace(":", "")
                        descritivo = descritivo.replace(" ", "")
                        descritivo = descritivo.strip()
                print("Descritivo", descritivo)

            if word == "Laudas:" or word == "Laudas":
                laudas = int(words[indice])
                print("Laudas", laudas)

            if word == "Lauda:":
                indice = idx + 2
                words[indice] = words[indice].replace(".", '')
                words[indice] = words[indice].replace(",", '.')
                lauda = "{:.2f}".format(float(words[indice]))

            if word == "Projeto:" or word == "Projeto":
                for i in range(10):
                    if words[indice + i] == "Prazo":
                        break
                    else:
                        total = total + " " + words[indice + i]
                        total = total.replace(":", "")
                        total = total.replace(" ", "")
                        total = total.replace("(", "")
                        total = total.replace("Fechado", "")
                        total = total.replace(")", "")
                        total = total.replace("R$", "")
                        total = total.strip()
                print("Total", total)

            if word == "Tradução:":
                if words[indice - 2] == "a" and words[indice - 3] == "d":
                    for i in range(10):
                        if words[indice + i] == "Prazo":
                            break
                        else:
                            total = total + " " + words[indice + i]
                            total = total.replace(":", "")
                            total = total.replace(" ", "")
                            total = total.replace("(", "")
                            total = total.replace("Fechado", "")
                            total = total.replace(")", "")
                            total = total.replace("R$", "")
                            total = total.strip()
                print("Total", total)

        if laudas != 0 and lauda != 0.0:
            subtotal = "{:.2f}".format(float(laudas) * float(lauda))

        if (laudas != 0 and lauda != 0.0) and (subtotal != total):
            warning = "CHECK THIS!"
        else:
            warning = ''

        print("=========================================================")
        print(" ")

        data = dict()
        data['Fornecedor'] = self.company.upper()
        data['Proposta'] = proposta
        data['Solicitante'] = solicitante
        data['Data'] = data_proposta
        data['Descritivo'] = descritivo
        data['Laudas'] = laudas
        data['Valor_Lauda'] = str(lauda).replace(".", ",")
        data['Subtotal'] = str(subtotal).replace(".", ",")
        data['Total'] = str(total).replace(".", ",")
        data['Observacoes'] = warning

        return data

    def batch_files(self):
        files = os.listdir(self.pdfs_directory)
        data = {}
        for file in files:
            text = self.convert2text(self.pdfs_directory + "/" + file)
            if self.company == "athena":
                data = self.athena_data(text)
                # print(data)
            if self.delete is True:
                os.remove(self.pdfs_directory + "/" + file)

            with open(self.save_as, 'a', newline='') as f:
                w = csv.DictWriter(f, delimiter=';', fieldnames=data.keys())
                w.writerow(data)
