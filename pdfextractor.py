from pdf_parser import data_extractor_numbers, data_extractor_alphanumeric, data_extractor_string
import re
import pdfplumber
import psycopg2
import os ,shutil
import sys
from datetime import datetime

import glob
#start time
x = datetime.now()
print("start_time=",x.strftime("%I : %M : %S : %f %p"))

data_dict={}
l={'(',')','.','/','-',',','%',"'"}


path=r"C:\Users\MICROSOFT\OneDrive\Desktop\automation\New folder"
print(os.listdir((path)))
file_list=os.listdir(path)
##print(path_list)

def extract_all(path):
#text of the file
    with pdfplumber.open(path) as pdf:
        pages=pdf.pages
        text = ' '
        for i in range(0,len(pages)):
            page=pages[i]
            text1=page.extract_text(x_tolerance=3,y_tolerance=3)
            text = text + text1
        print(text,"\n")

    #line item
    data3=re.search(r'(?s)Description\sof.*?Total',text).group()

    line_item=re.findall(r'\d+\s+\d+\s+\D+[0-9\,\.]+',data3)
    print("line item=",line_item)


    line_item=re.findall(r'\d+\s\d+\s\D+[0-9\.]\D+[0-9\,\.]',data3)
    print(line_item)
    for i in line_item:
        line=i.split()
        print(line)
        data_dict['HSN']=line[0]
        data_dict['qty']=line[1]
        data_dict['rate']=line[-3]
        data_dict['total']=line[-1]
    data_extractor_alphanumeric(text,"ITEM",1,data_dict,"ROUND","ITEM CODE",l,r"\d{10}",0)#item code
    data_extractor_alphanumeric(text,'Estate',1,data_dict,'\n','Invoice_date',l,'[0-9]+\-\w+\-\d+',0)#invoice date
    data_extractor_alphanumeric(text,'Buyer’s Order No. Dated',1,data_dict,'Lohia','Po_date',l,'[0-9]+\-\w+\-\d+',0)#po date
    data_extractor_alphanumeric(text,'PAN/IT No  :',1,data_dict,'BY','PAN',l,'A+CL2470J$',0)  #pan id
    data_extractor_alphanumeric(text,'Buyer’s Order No. Dated',1,data_dict,'Lohia','Po_no',l,'[0-9]+',0)#po no
    data_extractor_alphanumeric(text,'(ORIGINAL FOR RECIPIENT)',1,data_dict,'Invoice No.','Vendor Nane',l,'A[a-z]\w+\s[a-zA-Z]+\s+[a-zA-Z]+',0)#vendor name
    data_extractor_alphanumeric(text,'Terms of Payment',1,data_dict,'60 DAYS','GSTIN_CL',l,'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9][A-Z][0-9]',0)#gst client
    data_extractor_alphanumeric(text,'Estate  Kanpur',1,data_dict,'Despatched','GSTIN_lo',l,'\d\dAAA[a-zA-Z]+\d+[a-zA-Z]+\d[a-zA-Z]+',0) #gst lohia
    data_extractor_alphanumeric(text,'Total',1,data_dict,'Amount Chargeable','Grand total',l,'\d{1},\d{3}.\d{2}',0)#grand total 
    
    print(data_dict,"\n")
    

#file names:
    parent_dir = r"C:\Users\MICROSOFT\OneDrive\Desktop\automation"
    for pdf_file in glob.glob('*.pdf'):
        print (pdf_file)
  
     
#extract_all(r"C:\Users\MICROSOFT\OneDrive\Desktop\automation\20.pdf")

##New=pd.data_dict.from_dict(data_dict,orient='index').T
##print(New)

#end time

x = datetime.now()
print("end_time=",x.strftime("%I : %M : %S : %f %p"))

for file_name in file_list:
        file_path=os.path.join(path,file_name)
        print(file_path)
        extract_all(file_path)
