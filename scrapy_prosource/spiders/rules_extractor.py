from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
import os
import pdb
from selenium import webdriver
class ProsourceSpider(CrawlSpider):
    name = "dl"
    start_urls = ["http://prosource.edu.vn/"]
    rules = [
        Rule(lxml(allow=("http://prosource.*.html")),callback='add_url'),
        Rule(lxml(allow=("http://prosource",)), follow=True)
    ]
    html_path = "./html"
    images_path = "./images"
    cpt = 0
    all_urls= []
    chrome64_path = "lib/chrome/64/chromedriver"
    chrome32_path = "lib/chrome/32/chromedriver"
    phantom_js_path_linux = "lib/phantomjs-1.9.8-linux-x86_64/bin/phantomjs"
    phantom_js_path_macos = "lib/phantomjs-1.9.8-macosx/bin/phantomjs"

    #driver = webdriver.Chrome(chrome64_path)

    if not os.path.exists(html_path):
        os.makedirs(html_path)
    if not os.path.exists(images_path):
        os.makedirs(images_path)


    def add_url(self, response):
        self.all_urls.append(response.url)
        print response.url

    def closed(self, reason):
        global driver
        driver = webdriver.PhantomJS(self.phantom_js_path_linux)
        for url in self.all_urls:
            driver.get(url)
            self.store_data(url)
        driver.close()
        
        
        
    def store_data(self,url):
        print "saving %s"%(url)
        html_name = url.replace('http://','').replace('/','_')
        png_name = html_name.replace('.html','.png')
        driver.save_screenshot('%s/%s'%(self.images_path,png_name))
        f=open('%s/%s'%(self.html_path,html_name),'wb')
        f.write(driver.page_source.encode('utf-8'))
        f.close()









        
        
        


        #print "Total pages saved : %s"%(self.cpt)