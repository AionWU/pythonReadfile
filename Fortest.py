import pandas as pd

DOC_PATH = './data/docx/'
FILE_NAME = '资产管理计划资产管理合同-样例'

COL1NUM = ['（一', '（二', '（三', '（四', '（五', '（六', '（七', '（八', '（九', '（十']
COL2NUM = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '0.']
COL3NUM = ['（1', '（2', '（3', '（4', '（5', '（6', '（7', '（8', '（9']


def sepNum(list):
    # （一）1.（1）。（①②③不划分）
    col_num = [0, 0, 0]
    newlist = []
    title_flag = 0
    for line in list:
        for index in range(len(COL1NUM)):
            if line.find(COL1NUM[index]) == 0:
                col_num[0] += 1
                col_num[1] = 0
                col_num[2] = 0
                title_flag = 1
        for index in range(len(COL2NUM)):
            if 0 <= line.find(COL2NUM[index]) <= 2:  # <=2时最多到三位数：111.
                col_num[1] += 1
                col_num[2] = 0
        for index in range(len(COL3NUM)):
            if line.find(COL3NUM[index]) == 0:
                col_num[2] += 1
        if title_flag == 1 or line == '':
            title_flag = 0  # 是一级标题的话，跳过;或是空行
        else:
            newlist.append([col_num[0], col_num[1], col_num[2], line])
    print(col_num)
    return newlist


def list2Dateframe(list):
    list = list[1:-1]  # 掐头去尾
    col_name = ['t1', 't2', 't3', 'context']
    strlist = sepNum(list)
    dataframe = pd.DataFrame(columns=col_name, data=strlist)
    return dataframe


f = open(DOC_PATH + FILE_NAME + '.txt', encoding='gbk')
txt = []
start = 0
end = 0
for line in f:
    if line.strip().find('第十一节') != -1:
        start += 1
        end = 0
    if start > 1:
        txt.append(line.strip())
        if line.strip().find('第十二节') != -1:
            end = 1
    if end == 1:
        start = 0
# print(txt)

txtDateFrame = list2Dateframe(txt)
print(txtDateFrame)
txtDateFrame.to_csv('./data/temp.csv', index=False)  # 不保存序号
