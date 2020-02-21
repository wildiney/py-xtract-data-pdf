#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from classes.Xtractdata import Xtractdata

now = datetime.datetime.now()

Xtractdata(
    r"C:\\INDRA\\{0}\\Traduções\\Orçamentos".format(now.year), "athena",
    r"C:\\INDRA\\{0}\\Traduções\\relatorio.csv".format(now.year), False
)
