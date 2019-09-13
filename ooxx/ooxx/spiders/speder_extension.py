import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
import myconfig
logger = logging.getLogger(__name__)
import util
class SpiderOpenCloseLogging(object):

    def __init__(self, item_count):
        self.item_count = item_count
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

        # instantiate the extension object
        ext = cls(item_count)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s", spider.name)

    def spider_closed(self, spider):
        logger.info("closed spider %s", spider.name)
        self.makeResult()
            
    def makeResult(self):
        p="%s/result"%myconfig.output_file
        lines = None
        with open(p,"r") as f:
            lines = f.readlines()
        if(lines):
            data = {}
            for l in lines:
                ss = l.strip('\n').split("-")#分号隔开 version, search ,start ,pagetotal
                version,search,start,pagetotal = ss[0],ss[1],int(ss[2]),int(ss[3])

                if(data.get(version)):
                    lasttotal = data[version].get(search)
                    if (lasttotal):
                        newtotal = lasttotal + pagetotal
                    else:
                        newtotal = pagetotal
                    data[version][search]=newtotal
                else:
                    data[version]={search:pagetotal}
                        
            self.save_analysis("%s\t\t%s\t\t%s\t\t%s\n"%("version","all","oom","ratio"))
            for v in myconfig.versions:
                
                aNum = util.string2int(data[v].get("None"))
                sNum = util.string2int(data[v].get(myconfig.keyword))
                try:
                    print ("%s-%s-%s-%s"%(v,aNum,sNum,sNum/aNum))
                    self.save_analysis("%s\t\t%s\t\t%s\t\t%s\n"%(v,aNum,sNum,sNum/aNum))
                except ZeroDivisionError:
                    print ("%s-%s-%s"%(v,aNum,sNum))
                    self.save_analysis("%s\t\t%s\t\t%s\n"%(v,aNum,sNum))
                else:
                    pass
                
    def save_analysis(self,mstr):
        with open("%s/analysis_result"%myconfig.output_file,"a") as f:
            f.write(mstr)

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        if self.items_scraped % self.item_count == 0:
            logger.info("scraped %d items", self.items_scraped)

if __name__ == "__main__":
        import sys
        import os
        print(1)
        print(os.path.dirname(os.path.realpath(__file__)))
        sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
        os.chdir("%s/../.."%os.path.dirname(os.path.realpath(__file__)))
        print(1)
        print(os.getcwd())
        s = SpiderOpenCloseLogging(1)
        s.makeResult()