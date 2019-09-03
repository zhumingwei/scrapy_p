from scrapy.cmdline import execute
import numpy as py
import sys
import os
import shutil

oxpath = "%s/ooxx"%os.path.dirname(os.path.realpath(__file__))
os.chdir(oxpath)

sys.path.insert(0,"%s/ooxx/spiders"%oxpath)

#删除output目录
if (os.path.exists("output")):
    shutil.rmtree("output") 

execute(['scrapy','crawl','ooxx','-a' ,'search=java.lang.OutOfMemoryError'])
