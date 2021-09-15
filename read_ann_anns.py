

filename = 'F:\doc\项目\数据\公司提供\基金合同样本\南方全球精选配置证券投资基金招募说明书（更新）.docx.anns'
# 从文件读入
with open(filename, 'r', encoding='utf-8') as f:
    text = f.read()
# 选出各类
textlist = text.split('\n')
for itemtext in textlist:
    starti = itemtext.find('S-')
    if starti != -1:
        print(itemtext[starti + 2:])
