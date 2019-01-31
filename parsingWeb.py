from selenium import webdriver
import time
import datetime
from bs4 import BeautifulSoup

def daumMapweb(query):

    try:
        startTime = datetime.datetime.now()

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome('chromedriver', chrome_options=options)

        # driver = webdriver.Chrome('chromedriver')

        driver.get('http://map.daum.net/')
        driver.find_element_by_id('search.keyword.query').send_keys(query)
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').click()

        resultArr = []
        try:
            for i in range(0,10):
                resultText = driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i+1) + ']/div/h6/a[1]').text
                resultArr.append(resultText)
        except:
            pass
        time.sleep(1)

        selectTarget = 1

        if len(resultArr) > 1:
            driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(selectTarget) + ']/div/div[2]/span[7]/a[2]/span[1]').click()
        else:
            driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li/div/div[2]/span[7]/a[2]/span[1]').click()

        time.sleep(3)
        last_tab = driver.window_handles[-1]
        driver.switch_to.window(window_name=last_tab)

        html = driver.page_source
        driver.close()


        soup = BeautifulSoup(html, 'html.parser')


        placeName = ''
        title = soup.select('title')
        for n in title:
            placeName = n.text.strip().replace(' | Daum 지도','')

        busStopList = []
        txt_busstop = soup.select('span[class=txt_busstop]') #.findall('txt_busstop')
        for n in txt_busstop:
            busStopList.append(n.text.strip())
            busNumList = []
        busDiv = 0
        stag = soup.find_all("ul", {"class": {"list_ride"}})

        busDistTempList = []
        stag = soup.find_all("span", {"class": {"txt_number"}})
        for tag in stag:
            for item in tag.find_all("span", {"class": {"screen_out"}}):
                if item.next_sibling != None and item.next_sibling != {}:
                    # print(item.next_sibling)
                    busDistText = item.next_sibling.replace('\n','').replace('(','').replace(') ','').replace('m','').strip()
                    busDistTempList.append(busDistText)


        busDistListA = []
        busDistListB = []
        for i in range(0,len(busDistTempList)):
            if i % 2 == 0 :
                busDistListA.append(busDistTempList[i])
            else:
                busDistListB.append(round(int(busDistTempList[i])/1000,3))

        busList = []
        for j in range(0,len(busStopList)):
            busList.append([ placeName, busStopList[j], busDistListA[j], busDistListB[j] ])

        selectFlag = 'y'

    # Needs bus number adding


        if len(busList) > 0:
            for a in busList:
                print(a)
            print('busStop start time : ', startTime)
            print('busStop end time   : ', datetime.datetime.now())
        else:
            print('No busStop')


    except:
        driver.close()
        busList = []

        selectFlag = 'c'

    return busList, selectFlag


# if __name__ == '__main__':
