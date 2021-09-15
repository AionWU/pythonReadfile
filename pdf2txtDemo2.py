import pdfplumber
import tqdm

PDF_PATH = './data/pdf/'
FILE_NAME = '华安宝利配置证券投资基金基金合同'
END_FLAG = ['。', '；',' ']

path = PDF_PATH + FILE_NAME + '.pdf'
pdf = pdfplumber.open(path)
f = open(PDF_PATH + FILE_NAME + '.txt', 'w', encoding='utf-8')

for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    text = page.extract_text()
    # str = str[:str.rfind('\n')]  # 去除页码（最后一行）
    # str = str.replace('\n', '')
    # str = str.replace('。', '。\n')
    # print(str)
    newtext = ''
    strlist = text.split('\n')
    for value in strlist:
        print(page,value[len(value)-1])
        if value[len(value) - 1] in END_FLAG:
            newtext += value + '\n'
        else:
            newtext += value
    f.write(newtext)
    # for table in page.extract_tables():
    #     # print(table)
    #     for row in table:
    #         print(row)
    #     print('---------- 分割线 ----------')

pdf.close()
f.close()
