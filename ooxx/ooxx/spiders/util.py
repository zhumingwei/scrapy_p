from urllib import parse
import json
def getQuery(url):
    return parse.parse_qs(parse.urlsplit(url).query)

def string2int(num):
    return int(num)

#可以是带路径的文件名
def savefile(self,filename,body):
    with open(filename, 'wb') as f:        #python文件操作，不多说了；
        f.write(body)             #刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        self.log('保存文件: %s' % filename)

def parse_json(s_json):
        return json.loads(s_json)
        
