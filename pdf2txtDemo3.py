import pdfplumber

PDF_PATH = './data/pdf/'
FILE_NAME = '1591144640909-dongfanghonghuobishichangjijinjijinhetong'
END_FLAG = ['。', '；', ' ']

path = PDF_PATH + FILE_NAME + '.pdf'
pdf = pdfplumber.open(path)
f = open(PDF_PATH + FILE_NAME + '.txt', 'w', encoding='utf-8')
finfo = open(PDF_PATH + FILE_NAME + 'raw' + '.txt', 'w', encoding='utf-8')

l_header = ['', '']  # 页眉
page_last_word = dict()
for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    words_list = page.extract_words()

    pageinfo = str(page) + ',width:' + str(page.width) + ',height:' + str(page.height)
    finfo.write(str(words_list) + '\n' + pageinfo + '\n')

    # 去除页眉
    has_header = False
    has_header_one = False
    t_header = [words_list[0]['text'], words_list[1]['text']]
    if l_header == ['', '']:
        l_header = t_header
    elif t_header == l_header:
        has_header = True  # 有两个页眉（左，右）
    elif t_header[0] == l_header[0]:
        has_header_one = True  # 有一个页眉

    if has_header:
        # last_word = words_list[2]
        last_word = page_last_word
        pagetext = words_list[2]['text']
        start_i = 3
    elif has_header_one:
        last_word = page_last_word
        pagetext = words_list[1]['text']
        start_i = 2
    else:
        last_word = words_list[0]
        pagetext = last_word['text']
        start_i = 1
        minx0 = words_list[0]['x0']  # 全文最小x0

    lastline_minx0 = words_list[0]['x0']  # 上一行最小起始位置
    for i in range(start_i, len(words_list) - 1):  # 最后一个是页码
        t_word = words_list[i]
        if t_word['top'] - last_word['top'] <= 8:
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
    page_last_word = words_list[len(words_list) - 2]
    # print(page_last_word)
    f.write(pagetext)

pdf.close()
f.close()
finfo.close()
