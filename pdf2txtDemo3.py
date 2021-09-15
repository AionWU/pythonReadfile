import pdfplumber

PDF_PATH = './data/pdf/'
FILE_NAME = '招商招福宝货币市场基金基金合同'
END_FLAG = ['。', '；', ' ']

path = PDF_PATH + FILE_NAME + '.pdf'
pdf = pdfplumber.open(path)
f = open(PDF_PATH + FILE_NAME + '.txt', 'w', encoding='utf-8')
finfo = open(PDF_PATH + FILE_NAME + 'raw' + '.txt', 'w', encoding='utf-8')

l_header = ['', '']  # 页眉
for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    words_list = page.extract_words()

    pageinfo = str(page) + ',width:' + str(page.width) + ',height:' + str(page.height)
    finfo.write(str(words_list) + '\n' + pageinfo + '\n')

    # 去除页眉
    has_header = False
    t_header = [words_list[0]['text'], words_list[1]['text']]
    if l_header == ['', '']:
        l_header = t_header
    elif t_header == l_header:
        has_header = True
    if has_header:
        last_word = words_list[2]
        start_i = 3
    else:
        last_word = words_list[0]
        start_i = 1

    pagetext = last_word['text']
    minx0 = words_list[0]['x0']
    lastline_minx0 = words_list[0]['x0']  # 上一行最小起始位置
    for i in range(start_i, len(words_list) - 1):  # 最后一个是页码
        t_word = words_list[i]
        if t_word['top'] == last_word['top']:
            # 是同一行
            pagetext += t_word['text']
        else:
            # 不是同一行。判断缩进关系
            if t_word['x0'] == lastline_minx0:
                # 同一起始，需判断是否是换行的。
                if t_word['x0'] <= minx0:
                    pagetext += t_word['text']
                    minx0 = t_word['x0']
                else:
                    pagetext += '\n' + t_word['text']
            elif 0 < lastline_minx0 - t_word['x0'] <= 30:
                pagetext += t_word['text']
            else:
                pagetext += '\n' + t_word['text']
            lastline_minx0 = t_word['x0']  # 记录刚换行时的x0
        last_word = t_word

    f.write(pagetext + '\n')

pdf.close()
f.close()
finfo.close()
