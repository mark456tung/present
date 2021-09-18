# sleep5秒會被ban 
import twstock
import time
import pymongo
import datetime
print('Program start from {}'.format(datetime.datetime.now()))
stocktype = twstock.twse
# stocktype = twstock.tpex 
time.sleep(6)
month = [i for i in range(1,13)]
stockcodelist = []

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient.test
mydb = myclient.twse401toend  #1~100 [0:100] 101~200 [100:200] 201~300 [200:300] 
#mycol = mydb["twseetf"]

# 用來取得 上市/上櫃 且type為股票的股票代碼
def get_stockcodelist(stocktype):# stocktype=twstock.twse or twstock.tpex
    print('get stock code list') 
    for i in(stocktype):
        if(stocktype[i][0]=='股票'):
            stockcodelist.append(stocktype[i][1])
        
    return stockcodelist


def get_data(stockcode,stocktype):
    for stockcode in stockcodelist[584:]:
        print("----------股票代碼{}開始---------".format(stockcode))
        startyear = get_startyear(stocktype[stockcode])
        stock = twstock.Stock(stockcode)
        year = [i for i in range(int(startyear), 2022)]
        starttime = time.time()
        inserttodb(stock, year, month)
        endtime = time.time()
        print('------股票代碼:{}所花費時間------'.format(endtime-starttime))
        time.sleep(6)
        
# insert 到db 暫時只用print 還未和db連結
def inserttodb(stock, year, month):
    mycol = mydb[stock.sid]
    for yeari in year:
        for monthi in month:
            try:
                if(yeari == 2021 and monthi >= 9 ):
                    break
                insertdata(mycol, stock, yeari,monthi)
            except:
                print("xxxxxxxxxx股票代碼:{},{}年{}月發生錯誤".format(stock.sid,yeari,monthi))
                print('try again after 1 hour')
                for i in range(3650):
                    print('{}秒retry'.format(3649-i))
                    time.sleep(1)
                insertdata(mycol, stock, yeari,monthi)

        print("----------股票代碼{},{}年插入完畢".format(stock.sid, yeari))

# 用來判斷抓取開始年份 (twse的資料從民國99年開始即2010)
def get_startyear(stocktype):
    first_date = stocktype[4]
    second_date = "2010/01/01"
    formatted_date1 = time.strptime(first_date, "%Y/%m/%d")
    formatted_date2 = time.strptime(second_date, "%Y/%m/%d")
    if (formatted_date1<formatted_date2 ):
        return(time.strftime('%Y',formatted_date2))
    else:
        return(time.strftime('%Y',formatted_date1))

def transform_date(date):
        y, m, d = date.split('/')
        return str(int(y)+1911) + '-' + m  + '-' + d  #民國轉西元    

def insertdata(mycol,stock, yeari, monthi):
    time.sleep(6)
    stocklist = stock.fetch(yeari, monthi) #
    stockdays = len(stocklist)
    if(stockdays == 0):
        print('--------sotckcode:{} at {}year, {}month not exist'.format(stock.sid,yeari,monthi))
        
    else:
        for i in range(stockdays):
            insertList = stocklist[i]
            insert_dict = {"date":insertList[0],"capacity":insertList[1],"turnover":insertList[2],
                           "open":insertList[3],"high":insertList[4],"low":insertList[5],"close":insertList[6],
                           "change":insertList[7],"transaction":insertList[8]}
            x = mycol.insert_one(insert_dict) 
            print(x)
        print("----------股票代碼:{},{}年{}月插入完畢".format(stock.sid,yeari,monthi))
    
print("get sotck's codelist after 6 seconds")
time.sleep(6)

stockcodelist = get_stockcodelist(stocktype)
print(stockcodelist)
get_data(stockcodelist,stocktype)
print('Program end at {}'.format(datetime.datetime.now()))
   
