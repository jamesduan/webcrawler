# encoding:utf8


class UrlQueue:

    def __init__(self):
        #已访问的url集合
        self.visted=[]
        #待访问的url集合
        self.unVisited=[]

    #获取访问过的url队列
    def getVisitedUrl(self):
        return self.visted

    #获取未访问的url队列
    def getUnvisitedUrl(self):
        return self.unVisited

    #添加到访问过得url队列中
    def addVisitedUrl(self,url):
        self.visted.append(url)

    #移除访问过得url
    def removeVisitedUrl(self,url):
        self.visted.remove(url)

    #未访问过得url出队列
    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None

    #保证每个url只被访问一次 添加未被访问的url到unVisitedUrl 队列中
    def addUnvisitedUrl(self,url):
        if url!="" and url != None and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0,url)

    #获得已访问的url数目
    def getVisitedUrlCount(self):
        return len(self.visted)

    #获得未访问的url数目
    def getUnvistedUrlCount(self):
        return len(self.unVisited)

    #判断未访问的url队列是否为空
    def unVisitedUrlsEmpty(self):
        return len(self.unVisited)==0


