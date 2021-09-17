import pdfplumber

PDF_PATH = './data/pdf/'
FILE_NAME = '招商招福宝货币市场基金基金合同'

path = PDF_PATH + FILE_NAME + '.pdf'


def wordlist_to_linelist(words_list, line_list, minx_list):
    tp_line_l, tp_minx_l = [], []
    l_word = words_list[0]
    line = l_word['text']
    linex0 = l_word['x0']
    for i in range(1, len(words_list)):
        t_word = words_list[i]
        if -10 <= t_word['top'] - l_word['top'] <= 10:
            line += t_word['text']
            if t_word['x0'] < linex0:
                linex0 = t_word['x0']
        else:
            tp_line_l.append(line)
            tp_minx_l.append(linex0)
            line = t_word['text']
            linex0 = t_word['x0']
        l_word = t_word
    # 删去第一行页眉
    line_list.extend(tp_line_l[1:])
    minx_list.extend(tp_minx_l[1:])
    return line_list, minx_list


def main():
    pdf = pdfplumber.open(path)
    line_list, minx_list = [], []
    for page in pdf.pages:
        # 获取当前页面的全部文本信息，包括表格中的文字
        words_list = page.extract_words()

        line_list, minx_list = wordlist_to_linelist(words_list, line_list, minx_list)

    whole_minx = minx_list[0]
    text = line_list[0]
    for i in range(1, len(minx_list)):
        print(minx_list[i], whole_minx, line_list[i])
        if 60 < minx_list[i] <= whole_minx or abs(whole_minx - minx_list[i]) <= 10:  # 有的突出边界，有的边界不标准
            whole_minx = minx_list[i]
            text += line_list[i]
        else:
            text += '\n' + line_list[i]

    f = open(PDF_PATH + FILE_NAME + 'new' + '.txt', 'w', encoding='utf-8')
    f.write(text)
    f.close()


main()
