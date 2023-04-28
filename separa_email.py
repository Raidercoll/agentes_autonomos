import  jpype     
import  asposecells     
jpype.startJVM() 
from asposecells.api import Workbook

workbook = Workbook("files/emails.xlsx")
workbook.save("Output.txt")
jpype.shutdownJVM()