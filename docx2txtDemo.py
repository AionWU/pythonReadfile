from docx import Document
from docx.shared import Inches

DOC_PATH = './data/doc/'
FILE_NAME = '资产管理计划资产管理合同-样例'
document = Document(DOC_PATH + FILE_NAME + '.docx')
f = open(DOC_PATH + FILE_NAME + '.txt', 'w')
i = 0
for paragraph in document.paragraphs:
    f.write(paragraph.text + '\n')
    print(i, paragraph.text)
    i += 1
f.close()
