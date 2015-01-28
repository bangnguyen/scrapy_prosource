import random
import time
import traceback
from selenium import webdriver
phantom_js_path_linux = "./phantomjs"
driver = None
import pdb
from scrapy import FormRequest, Request, Selector

class Keyword:
    def __init__(self, value=None,meta=None,popularity=None,competition=None,price=None):
        self.value=value
        self.meta=meta
        self.popularity=popularity
        self.competition = competition
        self.price = price

    def to_string(self):
        return "value %s, popularity %s "%(self.value,self.popularity)
   

def screen():
    print "save screenshot page.png"
    driver.save_screenshot('page.png')

def html():
    print "save file page.html"
    f=open('page.html','wb')
    f.write(driver.page_source.encode('utf-8'))
    f.close()
def save():
    time.sleep(2)
    screen()
    html()


def init():

    global driver
    #driver = webdriver.PhantomJS(phantom_js_path_linux)
    driver = webdriver.Chrome("./chromedriver")
    print "Init : successful"



def find(id=None, name=None,xpath=None, retries=5,is_display=True):
    time.sleep(1)
    while retries:
        try:
            element = None
            target = None
            if id:
                target = id 
                element = driver.find_element_by_id(id)
            elif name:
                target = name 
                element = driver.find_element_by_name(name)
            elif xpath:
                target = xpath
                element = driver.find_element_by_xpath(xpath)       
            if is_display and element.is_displayed():
                print "Found element target %s "%(target)
        
                return element
            else:
                return element
        except:
            traceback.print_exc()
            pass
        retries = retries - 1
        time.sleep(2)

def sleep(default=2):
    time.sleep(default)

def login():
    driver.get("https://adwords.google.com/")
    if find(xpath="//a[contains(.,'Sign in')]",retries=10):
        find(xpath="//a[contains(.,'Sign in')]").click()
    find(id='Email').send_keys('tathu.nguyen1')
    find(id='Passwd').send_keys('xxx')
    find(id='signIn').click()
    sleep()
    """
    find(xpath="//td[@id='gwt-uid-397']//div[contains(.,'Tools')]").click()
    find(xpath="//a[contains(.,'Keyword Planner')]").click()
    """ 
    print "Login : successful"

def get_data():
    selector = Selector(text=driver.page_source.encode('utf-8'))
    data=selector.xpath("//div[@id='gwt-debug-table']//tr")
    for tr in data:
        tds=tr.xpath('./td')
        if len(tds) == 7:
	    value = tds[0].xpath('.//a/text()').extract()[0]
	    meta = tds[1].xpath('.//text()').extract()[0]
            popularity = tds[2].xpath('.//text()').extract()[0]
            competition = tds[3].xpath('.//text()').extract()[0]
            price = tds[4].xpath('.//text()').extract()[0]
	    kw = Keyword(value=value,meta=meta,popularity=popularity,competition=competition,price=price)
	    print kw.to_string()
        elif len(tds) ==6:
            value = tds[0].xpath('.//text()').extract()[0]
            popularity = tds[1].xpath('.//text()').extract()[0]
            competition = tds[2].xpath('.//text()').extract()[0]
            price = tds[3].xpath('.//text()').extract()[0]
            kw = Keyword(value=value,meta=meta,popularity=popularity,competition=competition,price=price)
	    print kw.to_string()
        
        
        
            
     
    

def action():
    driver.get("https://adwords.google.com/ko/KeywordPlanner/Home?__c=1323728368&__u=8436691768&authuser=0&__o=cues#start")
    sleep()
    find(xpath="//div[contains(.//div/text(),'Search for new keyword')]").click()
    sleep()
    find(xpath="//div[@id='gwt-debug-splash-panel-form']//textarea[@id='gwt-debug-keywords-text-area']").send_keys("ngoc trinh")
    sleep()
    find(xpath="//div[@id='gwt-debug-splash-panel-form']//span[@id='gwt-debug-search-button-content']").click()
    sleep()
    find(id="gwt-debug-grouping-toggle-KEYWORD_IDEAS").click()
    sleep()
    save()
    pdb.set_trace()
    get_data()
    
    #find(id="gwt-debug-search-button-content",is_display=False).click()


def display(driver):
    try:
        elms = driver.find_elements_by_xpath("//div[@class='umISB']")
        for elm in elms:
            print elm.text
    except:
        traceback.print_exc()


if __name__ == "__main__":
    try:
        init()
        login()
        action()
    except:
        traceback.print_exc()
        pdb.set_trace()
        driver.close()




#driver.find_element_by_id("gwt-debug-campaign-page-keywords-drawer")
#driver.find_element_by_xpath("//div[@id='gwt-debug-keywords-editor-keyword-table']//span[contains(.,'More like this')]")

"""
try:
    for i in range(1):
        time.sleep(random.randint(1, 4))
        d = driver.find_element_by_xpath(
            "//div[@id='gwt-debug-keywords-editor-keyword-table']//span[contains(.,'More like this')]")
        if d:
            d.click()
            display(driver)
except:
    traceback.print_exc()
"""



