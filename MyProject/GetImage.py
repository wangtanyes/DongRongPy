import PythonMagick;
from PyPDF2 import PdfFileReader;
import os

C_RESOURCE_FILE = r'D:';
C_PDFNAME = r'guokai.pdf';
C_JPGNAME = r'6p%s.jpg';

def getImage():
    input_stream = open(C_RESOURCE_FILE + '\\' + C_PDFNAME, 'rb');
    pdf_input = PdfFileReader(input_stream, strict=False);  # 错误1
    page_count = pdf_input.getNumPages();


    img = PythonMagick.Image()  # empty object first
    img.density('300');  # set the density for reading (DPI); must be as a string

    for i in range(page_count):
        try:
            print("====================================================", i)
            img.read(C_RESOURCE_FILE + '\\' + C_PDFNAME);  # 分页读取 PDF
            imgCustRes = PythonMagick.Image(img);  # make a copy
            imgCustRes.sample('x1600');
            imgCustRes.write(C_RESOURCE_FILE + '\\' + (C_JPGNAME % i));
        except Exception as e:
            print(e.__context__)
            pass;
if __name__ == '__main__':
    getImage()
