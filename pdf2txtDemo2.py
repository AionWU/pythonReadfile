import pdfplumber

PDF_PATH = './data/pdf/'
FILE_NAME = '文件名'

path = PDF_PATH + FILE_NAME + '.pdf'
pdf = pdfplumber.open(path)
f = open(PDF_PATH + FILE_NAME + '.txt', 'w')

for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    str = page.extract_text()
    str = str[:str.rfind('\n')]  # 去除页码（最后一行）
    # str = str.replace('\n', '')
    # str = str.replace('。', '。\n')
    print(str)
    f.write(str + '\n')
    # for table in page.extract_tables():
    #     # print(table)
    #     for row in table:
    #         print(row)
    #     print('---------- 分割线 ----------')

pdf.close()
f.close()
