#!/usr/bin/python3
import requests
import threading
import json
from bs4 import BeautifulSoup
import time
import os
# pip install beautifulsoup4
# pip install  requests
colIndex = [0,4,5,6,8,9]
professions =[{"mc":"应用伦理","dm":"0151"},{"mc":"金融","dm":"0251"},{"mc":"应用统计","dm":"0252"},{"mc":"税务","dm":"0253"},{"mc":"国际商务","dm":"0254"},{"mc":"保险","dm":"0255"},{"mc":"资产评估","dm":"0256"},{"mc":"数字经济","dm":"0258"},{"mc":"","dm":"0259"},{"mc":"","dm":"0260"},{"mc":"法律","dm":"0351"},{"mc":"社会工作","dm":"0352"},{"mc":"警务","dm":"0353"},{"mc":"知识产权","dm":"0354"},{"mc":"国际事务","dm":"0355"},{"mc":"","dm":"0356"},{"mc":"教育","dm":"0451"},{"mc":"体育","dm":"0452"},{"mc":"国际中文教育","dm":"0453"},{"mc":"应用心理","dm":"0454"},{"mc":"","dm":"0455"},{"mc":"翻译","dm":"0551"},{"mc":"新闻与传播","dm":"0552"},{"mc":"出版","dm":"0553"},{"mc":"","dm":"0554"},{"mc":"博物馆","dm":"0651"},{"mc":"气象","dm":"0751"},{"mc":"建筑","dm":"0851"},{"mc":"城乡规划","dm":"0853"},{"mc":"电子信息","dm":"0854"},{"mc":"机械","dm":"0855"},{"mc":"材料与化工","dm":"0856"},{"mc":"资源与环境","dm":"0857"},{"mc":"能源动力","dm":"0858"},{"mc":"土木水利","dm":"0859"},{"mc":"生物与医药","dm":"0860"},{"mc":"交通运输","dm":"0861"},{"mc":"风景园林","dm":"0862"},{"mc":"","dm":"0863"},{"mc":"农业","dm":"0951"},{"mc":"兽医","dm":"0952"},{"mc":"林业","dm":"0954"},{"mc":"食品与营养","dm":"0955"},{"mc":"临床医学","dm":"1051"},{"mc":"口腔医学","dm":"1052"},{"mc":"公共卫生","dm":"1053"},{"mc":"护理","dm":"1054"},{"mc":"药学","dm":"1055"},{"mc":"中药","dm":"1056"},{"mc":"中医","dm":"1057"},{"mc":"医学技术","dm":"1058"},{"mc":"针灸","dm":"1059"},{"mc":"联合作战指挥","dm":"1152"},{"mc":"军兵种作战指挥","dm":"1153"},{"mc":"作战指挥保障","dm":"1154"},{"mc":"战时政治工作","dm":"1155"},{"mc":"后勤与装备保障","dm":"1156"},{"mc":"军事训练与管理","dm":"1157"},{"mc":"工商管理","dm":"1251"},{"mc":"公共管理","dm":"1252"},{"mc":"会计","dm":"1253"},{"mc":"旅游管理","dm":"1254"},{"mc":"图书情报","dm":"1255"},{"mc":"工程管理","dm":"1256"},{"mc":"审计","dm":"1257"},{"mc":"","dm":"1258"},{"mc":"","dm":"1259"},{"mc":"","dm":"1260"},{"mc":"音乐","dm":"1352"},{"mc":"舞蹈","dm":"1353"},{"mc":"戏剧与影视","dm":"1354"},{"mc":"戏曲与曲艺","dm":"1355"},{"mc":"美术与书法","dm":"1356"},{"mc":"设计","dm":"1357"},{"mc":"","dm":"1358"},{"mc":"文物","dm":"1451"},{"mc":"密码","dm":"1452"},{"mc":"","dm":"1453"}]

cities = requests.post('https://yz.chsi.com.cn/zsml/pages/getSs.jsp')


     




class myThread (threading.Thread):
    def __init__(self, dm,mc):
        threading.Thread.__init__(self)
        self.dm = dm
        self.mc = mc
        self.fo = open("D:/work/dream/feiquan/2024/2024"+mc+"非全日制招生学校和专业清单.md", "w",encoding='utf-8')
    def run(self):
        for city in json.loads(cities.text):
            time.sleep(3)
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
            time.sleep(3)
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

    if not os.path.exists("D:/work/dream/feiquan/2024/2024"+mcs+"非全日制招生学校和专业清单.md"):
        threadList.append( myThread(dms, mcs))
    else:
        print(mcs+"文件已存在")
for threado in threadList:
  time.sleep(3)
  threado.start()
  
  threado.join() 


