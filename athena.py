#!/usr/bin/python 

import datetime
from classes.xtract_nf_data import XtractData

now = datetime.datetime.now()

XtractData(
    r"C:\\INDRA\\{0}\\Traduções\\Orçamentos".format(now.year),
    "athena",
    r"C:\\INDRA\\{0}\\Traduções\\relatorio.csv".format(now.year),
    True
    )
