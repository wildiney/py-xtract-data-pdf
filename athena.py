import time
import datetime
from classes.xtract_nf_data import XtractData

while True:
  time.sleep(0.1)
  print(datetime.datetime.now())
  XtractData("./pdfs", "athena")
  time.sleep(60*60)