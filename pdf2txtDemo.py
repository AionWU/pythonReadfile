# -*- coding:utf-8 -*-
# 来源：https://blog.csdn.net/xc_zhou/article/details/81009809
import os,re
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

'''
pip install pdfminer3k
pip install pdfminer.six 安装这个引入的内容不会报错
'''

#将一个pdf转换成txt
def pdfTotxt(filepath,outpath):
    try:
        fp = open(filepath, 'rb')
        outfp=open(outpath,'w')
        #创建一个PDF资源管理器对象来存储共享资源,caching = False不缓存
        rsrcmgr = PDFResourceManager(caching = False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)
        #创建一个PDF解析器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        #关闭输入流
        fp.close()
        #关闭输出流
        device.close()
        outfp.flush()
        outfp.close()
    except Exception as e:
         print("Exception:%s",e)

#一个文件夹下的所有pdf文档转换成txt
def fileTotxt(fileDir):
    files=os.listdir(fileDir)
    tarDir=fileDir+'txt'
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)
    replace=re.compile(r'\.pdf',re.I)
    for file in files:
        filePath=fileDir+'\\'+file
        outPath=tarDir+'\\'+re.sub(replace,'',file)+'.txt'
        pdfTotxt(filePath,outPath)
        print("Saved "+outPath)


if __name__ == '__main__':
    #pdfTotxt('000.pdf', 'test.txt')
    fileTotxt('./data/pdf/')
