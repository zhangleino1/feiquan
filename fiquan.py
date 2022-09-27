#!/usr/bin/python3
import requests
import threading
import json
from bs4 import BeautifulSoup
# pip install beautifulsoup4
# pip install  requests
colIndex = [0,4,5,6,8,9]
professions = [{"mc":"金融","dm":"0251"},{"mc":"应用统计","dm":"0252"},{"mc":"税务","dm":"0253"},{"mc":"国际商务","dm":"0254"},{"mc":"保险","dm":"0255"},{"mc":"资产评估","dm":"0256"},{"mc":"审计","dm":"0257"},
{"mc":"法律","dm":"0351"},{"mc":"社会工作","dm":"0352"},{"mc":"警务","dm":"0353"},{"mc":"教育","dm":"0451"},{"mc":"体育","dm":"0452"},{"mc":"汉语国际教育","dm":"0453"},{"mc":"应用心理","dm":"0454"},{"mc":"翻译","dm":"0551"}
,{"mc":"新闻与传播","dm":"0552"},{"mc":"出版","dm":"0553"},{"mc":"文物与博物馆","dm":"0651"},{"mc":"建筑学","dm":"0851"},{"mc":"城市规划","dm":"0853"},{"mc":"电子信息","dm":"0854"},{"mc":"机械","dm":"0855"},{"mc":"材料与化工","dm":"0856"}
,{"mc":"资源与环境","dm":"0857"},{"mc":"能源动力","dm":"0858"},{"mc":"土木水利","dm":"0859"},{"mc":"生物与医药","dm":"0860"},{"mc":"交通运输","dm":"0861"},{"mc":"农业","dm":"0951"},{"mc":"兽医","dm":"0952"},{"mc":"风景园林","dm":"0953"}
,{"mc":"林业","dm":"0954"},{"mc":"临床医学","dm":"1051"},{"mc":"口腔医学","dm":"1052"},{"mc":"公共卫生","dm":"1053"},{"mc":"护理","dm":"1054"},{"mc":"药学","dm":"1055"},{"mc":"中药学","dm":"1056"},{"mc":"中医","dm":"1057"}
,{"mc":"军事","dm":"1151"},{"mc":"工商管理","dm":"1251"},{"mc":"公共管理","dm":"1252"},{"mc":"会计","dm":"1253"},{"mc":"旅游管理","dm":"1254"},{"mc":"图书情报","dm":"1255"},{"mc":"工程管理","dm":"1256"},{"mc":"艺术","dm":"1351"}]
cities = requests.post('https://yz.chsi.com.cn/zsml/pages/getSs.jsp')


     




class myThread (threading.Thread):
    def __init__(self, dm,mc):
        threading.Thread.__init__(self)
        self.dm = dm
        self.mc = mc
        self.fo = open("d:/2023/2023"+mc+"非全日制招生学校和专业清单.md", "w",encoding='utf-8')
    def run(self):
        for city in json.loads(cities.text):
            self.fo.writelines('# '+ city['mc']+'\n' )
            self.getSchool(city['dm'],self.dm)
        self.fo.close()

    def getSchool(self,ssdm,dm):
        # ssdm 省市代码 yjxkdm 学科代码  zymc 专业名称 xxfs 学习方式
        r = requests.post('https://yz.chsi.com.cn/zsml/queryAction.do', params={'ssdm': ssdm, 'yjxkdm': dm,'xxfs':2})
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.select(".ch-table a"):
            self.fo.writelines('## '+ item.string+'\n' )
            self.fo.writelines('| 院系所   |  专业  |  研究方向  |   考试范围 |  \n' )
            self.fo.writelines('| - | - | - |  - |   \n' )
            
            self.getProfession(item.attrs['href'])
  
    def getProfession(self,url):
        professionHtml = requests.post(' https://yz.chsi.com.cn'+url)
        professionHtml.encoding = 'utf-8'
        professionSoup = BeautifulSoup(professionHtml.text, 'html.parser')
        trs = professionSoup.select(".more-content tr")
        for trItem in trs:
            self.handleTd(trItem)
  
    def handleTd(self,trItem):
        for  index, tdItem in enumerate(trItem.select("td")):
            if index in colIndex:
                continue
            if index == 7:
                self.fo.writelines('| '+ '[详情](https://yz.chsi.com.cn'+tdItem.select('a')[0].attrs['href']+')' )
                self.fo.writelines(' |\n')      
                continue
            value = tdItem.string if tdItem.string!=None else ' '
            self.fo.writelines(' | '+value)



threadList = []




for profession in professions:
  print(profession['dm']+"ss"+profession['mc'])
  dms = profession['dm']
  mcs = profession['mc']
   
  threadList.append( myThread(dms, mcs))
for threado in threadList:
  threado.start()
  threado.join() 


