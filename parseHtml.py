# coding:utf-8

import requests
import bs4
import io
import os
import re
import json

kBaseUrl = 'http://baidu.com'

# http://www.runoob.com/python3

# 解析二级页面视频播放地址
def parsePlayData(videoType,url):


    path = '/Users/wang/Desktop/data/' + videoType

    if not os.path.exists(path):
        # 不存在文件
        os.mkdir(path)
    fullpath = '%s/%s.txt' % (path, videoType)

    f = open(fullpath,'w')

    # 获取子菜单HTML
    req = requests.get(kBaseUrl + url)
    data = req.text.encode(resp.encoding).decode('utf-8')

    dataSoup = bs4.BeautifulSoup(data, 'html.parser')
    # 打印子菜单详情信息
    # print(dataSoup.find('div', class_='content bord mtop'))

    contentSoup = bs4.BeautifulSoup(data, 'html.parser')

    # 子菜单下内容列表
    tt = contentSoup.find('div', class_='content bord mtop').find('ul').find_all('li')
    print('-----------------------content--------------------------')

    # 遍历菜单list
    for t in tt:
        # 获取子菜单第一个元素内容
        # t = tt[0]
        # print(t.text)
        # print(t.a['href'])

        # 加载子菜单内容列表下内容详情
        detailReq = requests.get(kBaseUrl + t.a['href'])
        detailData = detailReq.text.encode(resp.encoding).decode('utf-8')
        # print(detailData)
        detailSoup = bs4.BeautifulSoup(detailData, 'html.parser')
        # playData = detailSoup.find('div', class_='left1')

        # 获取视频源播放地址
        hlsurl = detailSoup.find(text=re.compile('var vHLSurl'))

        # print(hlsurl)

        # 解析hlsurl

        hlsEle = (hlsurl.replace(";", "")).split("=")

        lastEle = hlsEle[len(hlsEle) - 1]
        # print(lastEle)

        newArr = lastEle.split('+')

        newArrLastObj = ((newArr[len(newArr) - 1]).split('\r\n'))[0]
        # print(newArrLastObj)

        # 获取js代码 随机选择的host
        jsReq = requests.get(kBaseUrl + '/js/sp.js')
        jsData = jsReq.text.encode(resp.encoding).decode('utf-8')
        # print(jsData)

        # 检查host在js中的下标
        index = jsData.find(newArr[1], 0, len(jsData))
        # print('index = %s' % index)
        indexStr = jsData[index - 40:index - 5]
        # print(indexStr)
        if indexStr.__contains__('"'):
            # 获取下标
            lIndex = indexStr.find('"')
            rIndex = indexStr.rfind('"')
            # print(lIndex, rIndex)
            # 截取host地址
            hostCon = indexStr[lIndex + 1:rIndex] + ':8011'
            # print(hostCon)

            totalUrl = newArr[0] + hostCon + newArrLastObj
            totalUrl = totalUrl.replace('"', '')
            print(videoType + '/' + t.text + totalUrl)

            # 写入数据
            f.write(t.text + totalUrl + '\n')

    f.close()

# 获取首页菜单数据
def getHomeMenu(menu):

    menuList = []

    print(len(menu))

    for div in menu:


        values = ''.join(str(v) for v in div)

        # print(values)
        # continue
        soup2 = bs4.BeautifulSoup(values, 'html.parser')
        soup2 = soup2.ul
        for i in range(1, len(soup2.contents) - 1):

            if soup2.contents[i].string != '\n':
                print('content = ' + soup2.contents[i].string)
                # 菜单title
                if soup2.contents[i].a['href'] == '/':
                    content = '\n\n%s' % soup2.contents[i].string
                else:

                    # 菜单下的内容
                    content = '%s : %s%s' % (soup2.contents[i].string, url, soup2.contents[i].a['href'])

                    if soup2.contents[1].string == '视频区':
                        parsePlayData(soup2.contents[i].string, soup2.contents[i].a['href'])

                        print('-----------------------content--------------------------')

                # print(content)
                menuList.append(content)
            else:
                title = '%s' % soup2.contents[i].string
                menuList.append(title)

    writeDataToFile('/data', menuList)





# 写入数据
def writeDataToFile(fileName, data):

    path = '/Users/wang/Desktop' + fileName

    if not os.path.exists(path):
        # 不存在文件
        os.mkdir(path)
    fullpath = '%s%s.txt' % (path, fileName)

    if os.path.exists(fullpath):
        return
    print(fullpath)
    f = open(fullpath, 'w')

    for str in data:
        f.write(str)

    f.close()


if __name__ == '__main__':
    print('解析HTML')

    resp = requests.get(kBaseUrl)
    # data = resp.text.encode(resp.encoding).decode('gbk')
    data = resp.text.encode(resp.encoding).decode('utf-8')

    # print(data)

    soup = bs4.BeautifulSoup(data, 'html.parser')

    menu = soup.find_all('div', class_='menu')
    # print(menu)
    print('-----------------\n------------------')
    getHomeMenu(menu)








