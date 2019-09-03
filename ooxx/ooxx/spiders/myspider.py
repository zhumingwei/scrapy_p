import scrapy
import os
import myconfig
import sys
import util
from scrapy import signals

class xxoo(scrapy.Spider):
    
    name = "ooxx" # 定义蜘蛛名
    

    def input_url(self,version,search,urls):
        if (search):
            search_p = "&search=%s" % search
        else:
            search_p = ""

        if (version):
            version_p = "&version=%s" % version
        else :
            version_p = ""

        urls.append("https://bugly.qq.com/v2/issueList?start=0&searchType=errorType&exceptionTypeList=Crash&pid=1&platformId=1&sortOrder=desc%s&rows=50&sortField=crashCount&appId=24be824147&fsn=a37bd6a3-7a5f-466b-9193-b35cb976215d%s" % (search_p, version_p))

    def spider_closed():
        print('the end')

    def start_requests(self): # 由此方法通过下面链接爬取页面

        search = getattr(self, 'search', None)
        self.search = search
        if (not os.path.isdir(myconfig.output_file)):
            os.mkdir(myconfig.output_file)
        
        # 定义爬取的链接
        
        urls = []
        for v in myconfig.versions:
            self.input_url(v,search,urls)
            self.input_url(v,None,urls)

        for url in urls:
            print("url=%s"%url)
            yield scrapy.Request(url=url, callback=self.parse,headers= myconfig.header,errback=self.errback) #爬取到的页面如何处理？提交给parse方法处理

  
    
    def parse(self, response):
        
        '''
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        就是这么个流程，似不似很简单呀？
        '''

        qu = util.getQuery(response.url)
        qu.setdefault(None)
        if(qu.get('version')):
            version = qu['version'][0]
        else:
            version = None
        
        if (qu.get('search')):
            search = qu['search'][0]
            page = "%s-%s-%s-%s" % (version,qu['start'][0],qu['rows'][0],qu['search'][0])
        else:
            page = "%s-%s-%s" % (version,qu['start'][0],qu['rows'][0])
            search = None
        save_file_name = "%s/%s.json" % (myconfig.output_file, page)
        util.savefile(self,save_file_name,response.body)

     
        #解析json有用的数据
        json_response = util.parse_json(response.body)
        numFoud = json_response["ret"]["numFound"]

        with open("%s/result"%myconfig.output_file,"a") as f:
            f.write("%s-%s-%s\n"%(version,search,numFoud))
        # page = response.url.split("/")[-2]     #根据上面的链接提取分页,如：/page/1/，提取到的就是：1
        # filename = '%s/mingyan-%s.json' % (myconfig.output_file,page)    #拼接文件名，如果是第一页，最终文件名便是：mingyan-1.html
        
                
        # with open(filename, 'wb') as f:        #python文件操作，不多说了；
        #     f.write(response.body)             #刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        # self.log('保存文件: %s' % filename)      # 打个日志

        

    def errback(self, failure):
        print("#error###############")
        print(failure)
        pass

    
    