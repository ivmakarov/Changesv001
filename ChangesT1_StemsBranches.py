# -*- coding: utf-8 -*-
#
# "CHANGES" library - Celestial Stems and Terrestrial Branches calculation
#
#  brings chinese philosophy to life
#
# (C) Ivan Makarov, 2015-2016
# Email: ivmakarov@yahoo.com
#
from __future__ import division
import datetime
import ephem
import lunardate
from PyQt4 import QtCore
#from params import *


LAT = '50:27'   # '36:02'
LON = '30:31'   # '103:48'   
DUTC = 2        # 8              use for places with no DST, for DST places use DUTC = difUTC()
PLACE = 'Kiev'  # 'LANZHOU'

divtdi = datetime.timedelta.__div__

def divtd(td1, td2):
    """div time"""
    if isinstance(td2, (int, long)):
        return divtdi(td1, td2)
    us1 = td1.microseconds + 1000000 * (td1.seconds + 86400 * td1.days)
    us2 = td2.microseconds + 1000000 * (td2.seconds + 86400 * td2.days)
    return us1 / us2 

def difUTC():
    """returns UTC / local time difference in hours"""
    utc = datetime.datetime.utcnow()
    local = datetime.datetime.now()
    dt = local - utc
    h = int(dt.seconds/3600)
    Qdt = QtCore.QDateTime.currentDateTime()
    Udt = QtCore.QDateTime.currentDateTimeUtc()
    dt2 = Qdt.toPyDateTime() - Udt.toPyDateTime()
    h2 = int(dt.seconds/3600)
    if h == h2:
        return h
    else :
        print 'Time Init Error'
        return h2

    
class stemsbranches(object):
    
    def __init__(self):
        self.stems = {1:'Jia', 2:'Yi', 3:'Bing', 4:'Ding', 5:'Wu', 6:'Ji', 7:'Geng', 8:'Xin', 9:'Ren', 10:'Gui'}
        self.cstems = {1:'甲',2:'乙',3:'丙',4:'丁',5:'戊',6:'己',7:'庚',8:'辛',9:'壬',10:'癸'}
        self.monthes = { 1:'Yin', 2:'Mao', 3:'Chen', 4:'Si', 5:'Wu', 6:'Wei', 7:'Shen', 8:'You', 9:'Xu', 10:'Hai', 11:'Zi', 12:'Chou'}
        self.branches = {1:'Zi', 2:'Chou', 3:'Yin', 4:'Mao', 5:'Chen', 6:'Si', 7:'Wu', 8:'Wei', 9:'Shen', 10:'You', 11:'Xu', 12:'Hai', 13:'Zi',14:'Chou'}
        self.cbranches = {1:'子', 2:'丑', 3:'寅', 4:'卯',5:'辰',6:'巳',7:'午',8:'未',9:'申',10:'酉',11:'戌',12:'亥',13:'子',14:'丑'}
        self.zodiac ={1:'Rat',2:'Ox',3:'Tiger',4:'Rabbit',5:'Dragon',6:'Snake',7:'Horse',8:'Goat',9:'Monkey',10:'Rooster',11:'Dog',12:'Pig',13:'Rat',14:'Ox'}
        self.sixty = {1:'Jia-Zi', 2:'Yi-Chou', 3:'Bing-Yin', 4:'Ding-Mao', 5:'Wu-Chen', 6:'Ji-Si', 7:'Geng-Wu', 8:'Xin-Wei', 9:'Ren-Shen', 10:'Gui-You',
             11:'Jia-Xu', 12:'Yi-Hai', 13:'Bing-Zi', 14:'Ding-Chou', 15:'Wu-Yin', 16:'Ji-Mao', 17:'Geng-Chen', 18:'Xin-Si', 19:'Ren-Wu', 20:'Gui-Wei',
             21:'Jia-Shen', 22:'Yi-You', 23:'Bing-Xu', 24:'Ding-Hai', 25:'Wu-Zi', 26:'Ji-Chou', 27:'Geng-Yin', 28:'Xin-Mao', 29:'Ren-Chen', 30:'Gui-Si',
             31:'Jia-Wu', 32:'Yi-Wei', 33:'Bing-Shen', 34:'Ding-You', 35:'Wu-Xu', 36:'Ji-Hai', 37:'Geng-Zi', 38:'Xin-Chou', 39:'Ren-Yin', 40:'Gui-Mao',
             41:'Jia-Chen', 42:'Yi-Si', 43:'Bing-Wu', 44:'Ding-Wei', 45:'Wu-Shen', 46:'Ji-You', 47:'Geng-Xu', 48:'Xin-Hai', 49:'Ren-Zi', 50:'Gui-Chou',
             51:'Jia-Yin', 52:'Yi-Mao', 53:'Bing-Chen', 54:'Ding-Si', 55:'Wu-Wu', 56:'Ji-Wei', 57:'Geng-Shen', 58:'Xin-You', 59:'Ren-Xu', 60:'Gui-Hai'}
        self.twelweshichen = {1:'Zi hour', 2:'Chou hour', 3:'Yin hour', 4:'Mao hour', 5:'Chen hour', 6:'Si hour', 7:'Wu hour', 8:'Wei hour', 9:'Shen hour', 10:'You hour', 11:'Xu hour', 12:'Hai hour',13:'Zi hour',14:'Chou hour'}
        self.hchannel = {1:'GB', 2:'LIV', 3:'LU', 4:'LI', 5:'ST', 6:'Sp', 7:'Ht', 8:'SI', 9:'BL', 10:'KID', 11:'HG', 12:'TB',13:'GB',14:'LIV'}
        self.hstart = {}    #start moment for hour
        self.hend = {}      #end moment foe hour
        self.solarterms = {0:'vernal equinox',15:'clear and bright',30:'grain rain',45:'summer commences',60:'grain full',75:'grain in ear',90:'summer solstice',105:'moderate heat',120:'great heat',135:'autumn commences',150:'end of heat',165:'white dew',180:'autumnal equinox',195:'cold dew',210:'frost',225:'winter commences',240:'light snow',255:'heavy snow',270:'winter solstice',285:'moderate cold',300:'severe cold',315:'spring commences',330:'spring showers',345:'insects waken'}
        self.solartermsch = {0:'春分',15:'清明',30:'穀雨 (谷雨)',45:'立夏',60:'小滿 (小满)',75:'芒種 (芒种)',90:'夏至',105:'小暑',120:'大暑',135:'立秋',150:'處暑 (处暑)',165:'白露',180:'秋分',195:'寒露',210:'霜降',225:'立冬',240:'小雪',255:'大雪',270:'冬至',285:'小寒',300:'大寒',315:'立春',330:'雨水',345:'驚蟄 (惊蛰)'}
        self.solartermsdt = {}
        self.lat = None
        self.lon = None
        self.tdiffUTC = None
        self.place = None
        self.solnoon = None
        self.solrising = None
        self.solsetting = None
        self.moonrising = None
        self.moontransit = None
        self.moonsetting = None
    
    
    
    #@staticmethod
    def year_stembranch(self, year): 
        """returnes stem-branch for year from 1901
        no correcton for  11th 12 lunar month"""
        
       
        rr = (year-3)%60
        if int(rr) == 0 :
            rr = 60
        s = self.sixty[int(rr)]
        return s
    
    #@staticmethod
    def year_dt_stembranch(self, dt): 
        """returnes stem-branch for year dt - datetime object from 1901 to 2050"""
        day = dt.timetuple().tm_mday
        
        month = dt.timetuple().tm_mon
        
        year = dt.timetuple().tm_year
        
        if month == 1 or month == 2:
            ld = lunardate.LunarDate.fromSolarDate(year, month, day)
            #print ld
            lmonth = ld.month
            if lmonth == 11 or lmonth == 12 :
                year = year -1
        rr = (year-3)%60
        if int(rr) == 0 :
            rr = 60
        s = self.sixty[int(rr)]
        return s
    
    #@staticmethod
    def month_branch(self, year, month, day):
        """returnes branch of the month for given date"""

        ld = lunardate.LunarDate.fromSolarDate(year, month, day)
        #print ld
        month = ld.month
        #print month
        #if ld.isLeapMonth :
        #    month = month -1
        s = self.monthes[month]
        return s
    
    #@staticmethod    
    def month_stem(self, year_stem, month_branch):
        """returnes month stem """
        if year_stem == 'Jia' or  year_stem == 'Ji' :
            if month_branch == 'Yin' :
                s = 'Bing'
            if month_branch == 'Mao' :
                s = 'Ding'
            if month_branch == 'Chen' :
                s = 'Wu'
            if month_branch == 'Si' :
                s = 'Ji'
            if month_branch == 'Wu' :
                s = 'Geng'
            if month_branch == 'Wei' :
                s = 'Xin'
            if month_branch == 'Shen' :
                s = 'Ren'
            if month_branch == 'You' :
                s = 'Gui'
            if month_branch == 'Xu' :
                s = 'Jia'
            if month_branch == 'Hai' :
                s = 'Yi'
            if month_branch == 'Zi' :
                s = 'Bing'
            if month_branch == 'Chou' :
                s = 'Ding'
        
        if year_stem == 'Yi' or  year_stem == 'Geng' :
            if month_branch == 'Yin' :
                s = 'Wu'
            if month_branch == 'Mao' :
                s = 'Ji'
            if month_branch == 'Chen' :
                s = 'Geng'
            if month_branch == 'Si' :
                s = 'Xin'
            if month_branch == 'Wu' :
                s = 'Ren'
            if month_branch == 'Wei' :
                s = 'Gui'
            if month_branch == 'Shen' :
                s = 'Jia'
            if month_branch == 'You' :
                s = 'Yi'
            if month_branch == 'Xu' :
                s = 'Bing'
            if month_branch == 'Hai' :
                s = 'Ding'
            if month_branch == 'Zi' :
                s = 'Wu'
            if month_branch == 'Chou' :
                s = 'Ji'
                
        if year_stem == 'Bing' or  year_stem == 'Xin' :
            if month_branch == 'Yin' :
                s = 'Geng'
            if month_branch == 'Mao' :
                s = 'Xin'
            if month_branch == 'Chen' :
                s = 'Ren'
            if month_branch == 'Si' :
                s = 'Gui'
            if month_branch == 'Wu' :
                s = 'Jia'
            if month_branch == 'Wei' :
                s = 'Yi'
            if month_branch == 'Shen' :
                s = 'Bing'
            if month_branch == 'You' :
                s = 'Ding'
            if month_branch == 'Xu' :
                s = 'Wu'
            if month_branch == 'Hai' :
                s = 'Ji'
            if month_branch == 'Zi' :
                s = 'Geng'
            if month_branch == 'Chou' :
                s = 'Xin'
                
        if year_stem == 'Ding' or  year_stem == 'Ren' :
            if month_branch == 'Yin' :
                s = 'Ren'
            if month_branch == 'Mao' :
                s = 'Gui'
            if month_branch == 'Chen' :
                s = 'Jia'
            if month_branch == 'Si' :
                s = 'Yi'
            if month_branch == 'Wu' :
                s = 'Bing'
            if month_branch == 'Wei' :
                s = 'Ding'
            if month_branch == 'Shen' :
                s = 'Wu'
            if month_branch == 'You' :
                s = 'Ji'
            if month_branch == 'Xu' :
                s = 'Geng'
            if month_branch == 'Hai' :
                s = 'Xin'
            if month_branch == 'Zi' :
                s = 'Ren'
            if month_branch == 'Chou' :
                s = 'Gui'
                
        if year_stem == 'Wu' or  year_stem == 'Gui' :
            if month_branch == 'Yin' :
                s = 'Jia'
            if month_branch == 'Mao' :
                s = 'Yi'
            if month_branch == 'Chen' :
                s = 'Bing'
            if month_branch == 'Si' :
                s = 'Ding'
            if month_branch == 'Wu' :
                s = 'Wu'
            if month_branch == 'Wei' :
                s = 'Ji'
            if month_branch == 'Shen' :
                s = 'Geng'
            if month_branch == 'You' :
                s = 'Xin'
            if month_branch == 'Xu' :
                s = 'Ren'
            if month_branch == 'Hai' :
                s = 'Gui'
            if month_branch == 'Zi' :
                s = 'Jia'
            if month_branch == 'Chou' :
                s = 'Yi'
            
        return s  
    
    #@staticmethod
    def month_dt_stembranch(self, dt):
        """returnes stem and branch of the month dt - datetime object"""
        year = dt.timetuple().tm_year
        #print year
        month = dt.timetuple().tm_mon
        #print month
    
        day = dt.timetuple().tm_mday
        #print day
        br = self.month_branch(year, month, day)
        ys  = self.year_dt_stembranch(dt).split('-')[0]
        #print ys
        st = self.month_stem(ys, br)
        s = st +'-'+br
        return s
        
        
        
        
      
   
    #@staticmethod 
    def day_dt_stembranch(self, dt):
        """returnes stem and branch of the day dt - datetime object""" 
        
        day_of_year = dt.timetuple().tm_yday

        year = dt.timetuple().tm_year

        y = year%100
        
        if year//1000 == 2 :
            rr = (5*(100+y-1)+(100+y-1)/4 +15 +day_of_year)%60
            if int(rr) == 0 :
                rr = 60
            s = self.sixty[int(rr)]
            
        else :
            rr = (5*(y-1)+(y-1)/4 +15 +day_of_year)%60
            if int(rr) == 0 :
                rr = 60
            s = self.sixty[int(rr)]
        return s

    def init_hours(self,dt):
        """init 12 shichen - start -end"""
        year = dt.timetuple().tm_year
        #print year
        month = dt.timetuple().tm_mon
        #print month
    
        day = dt.timetuple().tm_mday
        self.hstart[1] = datetime.datetime(year,month,day,0,0)-datetime.timedelta(hours=1)
        #print self.hstart[1]
        self.hend[1] = datetime.datetime(year,month,day,1,0)
        #print self.hend[1]
        h=2
        for i in range(1,22,2) :
            self.hstart[h] = datetime.datetime(year,month,day,i,0)
            #print self.hstart[h]
            self.hend[h] = datetime.datetime(year,month,day,i+2,0)
            #print self.hend[h]
            h= h+1
        self.hstart[13] = datetime.datetime(year,month,day,23,0)
        #print self.hstart[13]
        self.hend[13] = datetime.datetime(year,month,day,23,0)+datetime.timedelta(hours=2)
        #print self.hend[13]
        self.hstart[14] = datetime.datetime(year,month,day,23,0)+datetime.timedelta(hours=2)
        #print self.hstart[13]
        self.hend[14] = datetime.datetime(year,month,day,23,0)+datetime.timedelta(hours=4)
        #print self.hend[13]
    
    def init_coords(self,lat,lon,dtUTC,place = None):
        """init latitude '50:27' longitude '30:31' and timezone 2 for Kiev"""
        self.lat = lat
        self.lon = lon
        self.tdiffUTC = dtUTC
        self.place = place
        
    def print_coords(self):
        """ prints current latitude and longitude and timezone for place"""
        print 'Latitude : '+str(self.lat)
        print 'Longitude : '+str(self.lon)
        print 'Timezone (diff to UTC) : '+ str(self.tdiffUTC)
        if self.place is not None :
            print 'Location : '+ str(self.place)
        
            
    def find_solar_noon(self,dt):
        """(obsolete!!!)finds solar noon for dt date"""
        year = dt.timetuple().tm_year
        #print year
        month = dt.timetuple().tm_mon
        #print month
    
        day = dt.timetuple().tm_mday 
        
        sitka = ephem.Observer()
        
        date = str(year)+'/'+str(month)+'/'+str(day)
        #print date

        sitka.date = date

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Sun()

        noon = sitka.next_transit(m)
        
        ntime = str(noon).split(' ')[1]
        
        h = ntime.split(':')[0]
        m = ntime.split(':')[1]
        s = ntime.split(':')[2]
        
        snoon = datetime.datetime(year,month,day,int(h),int(m),int(s))
        
        snoon += datetime.timedelta(hours=self.tdiffUTC)
        
        self.solnoon = snoon
        
        return snoon

    
    
    def find_solar_risingC(self,dt):
        """finds solar rising for dt date """
        
        d = ephem.Date(dt.date())
        
        
        sitka = ephem.Observer()
        
      
        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Sun()

        ri = sitka.next_rising(m)
      
        sri = ri.datetime()
        sri += datetime.timedelta(hours=self.tdiffUTC)
        
        
        if dt.date() < sri.date() :
            dt = dt - datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Sun()

            ri = sitka.next_rising(m)
            #print ri
        
            sri = ri.datetime()
            sri += datetime.timedelta(hours=self.tdiffUTC)
            #print sri
        elif dt.date() > sri.date() :
            dt = dt + datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Sun()

            ri = sitka.next_rising(m)
            #print ri
        
            sri = ri.datetime()
            sri += datetime.timedelta(hours=self.tdiffUTC)
            #print sri
        
        
        self.solrising = sri
        
        return sri

    def find_solar_settingC(self,dt):
        """finds solar setting for dt date """
        
        d = ephem.Date(dt.date())
        
            
        
        sitka = ephem.Observer()
        
       

        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Sun()

        ss = sitka.next_setting(m)
        
        sss = ss.datetime()
        sss += datetime.timedelta(hours=self.tdiffUTC)
        #print sss
        
        if dt.date() < sss.date() :
            dt = dt - datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Sun()

            ss = sitka.next_setting(m)
            #print ss
        
            sss = ss.datetime()
            sss += datetime.timedelta(hours=self.tdiffUTC)
            #print sss
        elif dt.date() > sss.date() :
            dt = dt + datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Sun()

            ss = sitka.next_setting(m)
            #print ss
        
            sss = ss.datetime()
            sss += datetime.timedelta(hours=self.tdiffUTC)
            #print sss
        
        
        self.solsetting = sss
        
        return sss

    def find_solar_noonC(self,dt):
        """finds solar setting for dt date """
        
        d = ephem.Date(dt.date())
       
            
        
        sitka = ephem.Observer()
        

        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Sun()

        sn = sitka.next_transit(m)
        
        snoon = sn.datetime()
        snoon += datetime.timedelta(hours=self.tdiffUTC)
        #print snoon
        
        if dt.date() < snoon.date() :
            dt = dt - datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Sun()

            sn = sitka.next_transit(m)
            #print sn
        
            snoon = sn.datetime()
            snoon += datetime.timedelta(hours=self.tdiffUTC)
            #print snoon
        elif dt.date() > snoon.date() :
            dt = dt + datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Sun()

            sn = sitka.next_transit(m)
            #print sn
        
            snoon = sn.datetime()
            snoon += datetime.timedelta(hours=self.tdiffUTC)
            #print snoon
        
        
        self.solnoon = snoon
        
        return snoon

    def find_moon_risingC(self,dt):
        """finds moon rising for dt date """
        
        d = ephem.Date(dt.date())
        
            
        
        sitka = ephem.Observer()
        
        

        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Moon(d)

        ri = sitka.next_rising(m)
       
        sri = ri.datetime()
        sri += datetime.timedelta(hours=self.tdiffUTC)
        #print sri
        if dt.date() < sri.date() :
            dt = dt - datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Moon(d)

            ri = sitka.next_rising(m)
            #print ri
        
            sri = ri.datetime()
            sri += datetime.timedelta(hours=self.tdiffUTC)
            #print sri
        elif dt.date() > sri.date() :
            dt = dt + datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Moon(d)

            ri = sitka.next_rising(m)
            #print ri
        
            sri = ri.datetime()
            sri += datetime.timedelta(hours=self.tdiffUTC)
        
        self.moonrising = sri
        
        return sri
    
    def find_moon_transitC(self,dt):
        """finds moon transit for dt date """
        
        d = ephem.Date(dt.date())
        
            
        
        sitka = ephem.Observer()
        
        

        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Moon(d)

        ri = sitka.next_transit(m)
       
        sri = ri.datetime()
        sri += datetime.timedelta(hours=self.tdiffUTC)
        #print sri
        if dt.date() < sri.date() :
            dt = dt - datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Moon(d)

            ri = sitka.next_transit(m)
            #print ri
        
            sri = ri.datetime()
            sri += datetime.timedelta(hours=self.tdiffUTC)
            #print sri
        elif dt.date() > sri.date() :
            dt = dt + datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Moon(d)

            ri = sitka.next_transit(m)
            #print ri
        
            sri = ri.datetime()
            sri += datetime.timedelta(hours=self.tdiffUTC)
        
        self.moontransit = sri
        
        return sri
    
    def find_moon_settingC(self,dt):
        """finds solar setting for dt date """
        
        d = ephem.Date(dt.date())
       
            
        
        sitka = ephem.Observer()
        
        
        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Moon(d)

        ss = sitka.next_setting(m)
        
        sss = ss.datetime()
        sss += datetime.timedelta(hours=self.tdiffUTC)
        #print sss
        
        if dt.date() < sss.date() :
            dt = dt - datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Moon()

            ss = sitka.next_setting(m)
            #print ss
        
            sss = ss.datetime()
            sss += datetime.timedelta(hours=self.tdiffUTC)
            #print sss
        elif dt.date() > sss.date() :
            dt = dt + datetime.timedelta(hours=24)
        
            d = ephem.Date(dt.date())
            #print d
        
            sitka.date = d
            m = ephem.Moon()

            ss = sitka.next_setting(m)
            #print ss
        
            sss = ss.datetime()
            sss += datetime.timedelta(hours=self.tdiffUTC)
            #print sss
        
        
        self.moonsetting = sss
        
       
        
        return sss
    
    
    def find_moon_phase(self,dt):
        """finds Moon's phase """
        d = ephem.Date(dt.date())
        
        
        sitka = ephem.Observer()
        
       
        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Moon()
        
        m.compute(d)
        
        s = str(m.moon_phase)
        
        return s

    def find_moon_constell(self,dt):
        """finds Moon's  constellation """
        d = ephem.Date(dt.date())
        
        
        sitka = ephem.Observer()
        
       
        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Moon(d)
        
        s = ephem.constellation(m)[1]
        
        return s    
        
    def find_sun_constell(self,dt):
        """finds Sun's  constellation """
        d = ephem.Date(dt.date())
        
        
        sitka = ephem.Observer()
        
       
        sitka.date = d

        sitka.lat = self.lat

        sitka.lon = self.lon

        m = ephem.Sun(d)
        
        s = ephem.constellation(m)[1]
        
        return s    
        
    
    

    def corr_hours_soltime(self,dt):
        """ corrects  12 shichen -for solar noon -solar time""" 
        year = dt.timetuple().tm_year
        #print year
        month = dt.timetuple().tm_mon
        #print month
    
        day = dt.timetuple().tm_mday 
        
        n = datetime.datetime(year,month,day,12,0)
        
        sn = self.find_solar_noonC(dt)
        sr = self.find_solar_risingC(dt) #needed for init
        ss = self.find_solar_settingC(dt)
        
        delta = sn - n
        
        for i in range(1,15) :
            self.hstart[i] += delta
            #print self.hstart[i]
            self.hend[i] += delta
            #print self.hend[i]
            
    def solar_hours(self,dt,showparams = None):
        """init solar hours inc. sunrise/sunset correction"""
        sn = self.find_solar_noonC(dt)
        if showparams is not None:
            print 'Solar noon : '
            print sn
        sr = self.find_solar_risingC(dt)
        if showparams is not None:
            print 'Sun rising : '
            print sr
        ss = self.find_solar_settingC(dt)
        if showparams is not None:
            print 'Sun setting : '
            print ss
        day = ss - sr
        if showparams is not None:
            print 'Day :'
            print day
        dh = divtd(day,6)
        if showparams is not None:
            print 'Day hour :'
            print dh
        pddt = dt - datetime.timedelta(hours=24)
        pdss = self.find_solar_settingC(pddt)
        if showparams is not None:
            print 'Previous day setting :'
            print pdss
        pn = sr - pdss
        if showparams is not None:
            print 'Night :'
            print pn
        nh1 = divtd(pn,6)
        if showparams is not None:
            print 'Night hour 1 : '
            print nh1
        nddt = dt + datetime.timedelta(hours=24)
        ndsr = self.find_solar_risingC(nddt)
        if showparams is not None:
            print 'Next day rising :'
            print ndsr
        nn = ndsr - ss
        if showparams is not None:
            print 'Next night :'
            print nn
        nh2 = divtd(nn,6)
        if showparams is not None:
            print 'Night hour 2 : '
            print nh2
        total3 = day + divtd(pn,2) +divtd(nn,2)
        if showparams is not None:
            print 'Total day duration : '
            print total3
        sp = sn - datetime.timedelta(hours=12)
        self.hstart[1] = sp - divtd(nh1,2)
        self.hend[1] = self.hstart[1]+ nh1
        self.hstart[2] = self.hend[1]
        self.hend[2] = self.hstart[2] + nh1
        self.hstart[3] = self.hend[2]
        self.hend[3] = self.hstart[3] + nh1
        self.hstart[4] = self.hend[3]
        self.hend[4] = self.hstart[4] + divtd(nh1,2)+divtd(dh,2)
        for i in range(0,5):
            self.hstart[5+i] = self.hend[4+i]
            self.hend[5+i] = self.hstart[5+i] + dh
        self.hstart[10] = self.hend[9]
        self.hend[10] = self.hstart[10] + divtd(nh2,2)+divtd(dh,2)
        for i in range(0,5):
            self.hstart[11+i] = self.hend[10+i]
            self.hend[11+i] = self.hstart[11+i] + nh2
            
            
    def init_solar12shichen(self, dt):
        """inits 12 shichen for date dt and place Kiev for sunrise/sunset correction(3d parameter 3 in sommer, 2 in winter time """ 
        DUTC = difUTC()  # use if DST for no DST comment out 
        self.init_coords(LAT,LON,DUTC,PLACE)
        self.solar_hours(dt)
        self.calc_solar_terms(dt-datetime.timedelta(hours=27))
                
                
               
    def init_12shichen(self, dt):
        """inits 12 shichen for date dt and place Kiev(3d parameter 3 in summer, 2 in winter time """ 
        DUTC = difUTC()   # use if DST for no DST comment out 
        self.init_coords(LAT,LON,DUTC,PLACE)
        self.init_hours(dt)
        self.corr_hours_soltime(dt) 
        self.calc_solar_terms(dt-datetime.timedelta(hours=27))
        
    def print_12shichen(self,dt,duration = None): 
        """prints 12 shichen for date dt and place """ 
        chfr  = {'GB':'VB','BL':'V','LI':'GI','ST':'E','TB':'TR','SI':'IG','KID':'R', 'LIV':'F','LU':'P','Sp':'Rp','Ht':'C','HG':'MC'}
        
        #self.init_12shichen(dt)
        #if duration == 2:
        #    print '------------------------------------------------------------------------------------------'

        for i in range(1,15) :
            if i==13 :
                print('Next Day')
            t1 = self.hstart[i].time()
            t2 = self.hend[i].time()
                        
            print str(self.twelweshichen[i])+' = from '+str(t1).split(':')[0]+' h '+str(t1).split(':')[1]+' min'+' to '+str(t2).split(':')[0]+' h '+str(t2).split(':')[1]+' min'
            if duration == 1:
                delta = self.hend[i] -  self.hstart[i]
                hst = self.hstart[i]
                hen = self.hend[i]
                d= str(delta)
                print 'Duration : '+d.split(':')[0]+' h '+d.split(':')[1]+' min'
            elif duration == 2:
                ch = self.hchannel[i]
                cfr = chfr[ch]
                print 'Channel = '+str(cfr)+' ('+str(ch)+')'
                print ' Subhours :'
                delta = self.hend[i] -  self.hstart[i]
                hst = self.hstart[i]
                hen = self.hend[i]
                delta = divtd(delta, 4)
                t1s = hst
                t1e = hst + delta
                t2s = hst +delta
                t2e = hst + 2*delta
                t3s = hst + 2*delta
                t3e = hst + 3*delta
                t4s = hst + 3*delta
                t4e = hen
                branch = str(self.branches[i])
                #print branch
                ch1 = self.subhourch(branch, '1')
                ch1fr = chfr[ch1]
                print ' '+str(ch1fr)+' ('+str(ch1)+') = from '+str(t1s.time()).split(':')[0]+' h '+str(t1s.time()).split(':')[1]+' min'+' to '+str(t1e.time()).split(':')[0]+' h '+str(t1e.time()).split(':')[1]+' min'
                ch2 = self.subhourch(branch, '2')
                ch2fr = chfr[ch2]
                print ' '+str(ch2fr)+' ('+str(ch2)+') = from '+str(t2s.time()).split(':')[0]+' h '+str(t2s.time()).split(':')[1]+' min'+' to '+str(t2e.time()).split(':')[0]+' h '+str(t2e.time()).split(':')[1]+' min'
                ch3 = self.subhourch(branch, '3')
                ch3fr = chfr[ch3]
                print ' '+str(ch3fr)+' ('+str(ch3)+') = from '+str(t3s.time()).split(':')[0]+' h '+str(t3s.time()).split(':')[1]+' min'+' to '+str(t3e.time()).split(':')[0]+' h '+str(t3e.time()).split(':')[1]+' min'
                ch4 = self.subhourch(branch, '4')
                ch4fr = chfr[ch4]
                print ' '+str(ch4fr)+' ('+str(ch4)+') = from '+str(t4s.time()).split(':')[0]+' h '+str(t4s.time()).split(':')[1]+' min'+' to '+str(t4e.time()).split(':')[0]+' h '+str(t4e.time()).split(':')[1]+' min'
                print '\n'
                
                
    def subhourch(self,branch,subhour):
        """returns channel to brunch and subhour"""
        if branch == 'Zi' or branch == 'Wu' or branch == 'Mao' or branch == 'You':
            if subhour == '1':
                s = 'Ht'
            elif subhour == '2':
                s = 'SI'
            elif subhour == '3':
                s = 'BL'
            elif subhour == '4':
                s = 'KID'
        if branch == 'Chou' or branch == 'Wei' or branch == 'Chen' or branch == 'Xu':
            if subhour == '1':
                s = 'HG'
            elif subhour == '2':
                s = 'TB'
            elif subhour == '3':
                s = 'GB'
            elif subhour == '4':
                s = 'LIV'
        if branch == 'Yin' or branch == 'Shen' or branch == 'Si' or branch == 'Hai':
            if subhour == '1':
                s = 'LU'
            elif subhour == '2':
                s = 'LI'
            elif subhour == '3':
                s = 'ST'
            elif subhour == '4':
                s = 'Sp'
        return s
            
            
    def hour_branch(self, dt): 
        """ get hour branch for date dt """ 
        for i in range(1,15) :
            if self.hstart[i] < dt and dt < self.hend[i] :
                s = self.branches[i]
        return s
    
    def sub_hour(self, dt):
        """ get sub hour  for date dt, return str: 1-4 starttime endtime """ 
        for i in range(1,15) :
            if self.hstart[i] < dt and dt < self.hend[i] :
                #s = self.branches[i]
                hst = self.hstart[i]
                hen = self.hend[i]
        
        delta = divtd(hen-hst,4)
        #delta  = datetime.timedelta(minutes=30)
        t1s = hst
        t1e = hst + delta
        t2s = hst +delta
        t2e = hst + 2*delta
        t3s = hst + 2*delta
        t3e = hst + 3*delta
        t4s = hst + 3*delta
        t4e = hen
        if t1s < dt and dt <= t1e :
            s = str(1)+' '+str(t1s.time())+' '+str(t1e.time())
        if t2s < dt and dt <= t2e :
            s = str(2)+' '+str(t2s.time())+' '+str(t2e.time())
        if t3s < dt and dt <= t3e :
            s = str(3)+' '+str(t3s.time())+' '+str(t3e.time())
        if t4s < dt and dt <= t4e :
            s = str(4)+' '+str(t4s.time())+' '+str(t4e.time())
        return s
        
    def delta_sub_hour(self, dt):
        """ get sub hour duration for date dt """ 
        for i in range(1,15) :
            if self.hstart[i] < dt and dt < self.hend[i] :
                #s = self.branches[i]
                hst = self.hstart[i]
                hen = self.hend[i]
        
        delta = divtd(hen-hst,4)   
        
        return delta 
    
    def diff_sub_hour(self, dt):
        """ get time til sub hour end  for time dt """ 
        for i in range(1,15) :
            if self.hstart[i] < dt and dt < self.hend[i] :
                #s = self.branches[i]
                hst = self.hstart[i]
                hen = self.hend[i]
        
        delta = divtd(hen-hst,4)
        #delta  = datetime.timedelta(minutes=30)
        t1s = hst
        t1e = hst + delta
        t2s = hst +delta
        t2e = hst + 2*delta
        t3s = hst + 2*delta
        t3e = hst + 3*delta
        t4s = hst + 3*delta
        t4e = hen
        if t1s < dt and dt <= t1e :
            end = t1e
        if t2s < dt and dt <= t2e :
            end = t2e
        if t3s < dt and dt <= t3e :
            end = t3e
        if t4s < dt and dt <= t4e :
            end = t4e
           
        d = end - dt
        
        
        return d 
        
        
        
                
                
                
        
        
        
    def hour_stem(self, day_stem, hour_branch):
        """ get hour stem for date dt """ 
        if day_stem == 'Jia' or  day_stem == 'Ji' :
            if hour_branch == 'Zi' :
                s = 'Jia'
            if hour_branch == 'Chou' :
                s = 'Yi'
            if hour_branch == 'Yin' :
                s = 'Bing'
            if hour_branch == 'Mao' :
                s = 'Ding'
            if hour_branch == 'Chen' :
                s = 'Wu'
            if hour_branch == 'Si' :
                s = 'Ji'
            if hour_branch == 'Wu' :
                s = 'Geng'
            if hour_branch == 'Wei' :
                s = 'Xin'
            if hour_branch == 'Shen' :
                s = 'Ren'
            if hour_branch == 'You' :
                s = 'Gui'
            if hour_branch == 'Xu' :
                s = 'Jia'
            if hour_branch == 'Hai' :
                s = 'Yi'
             
        if day_stem == 'Yi' or  day_stem == 'Geng' :
            if hour_branch == 'Zi' :
                s = 'Bing'
            if hour_branch == 'Chou' :
                s = 'Ding'
            if hour_branch == 'Yin' :
                s = 'Wu'
            if hour_branch == 'Mao' :
                s = 'Ji'
            if hour_branch == 'Chen' :
                s = 'Geng'
            if hour_branch == 'Si' :
                s = 'Xin'
            if hour_branch == 'Wu' :
                s = 'Ren'
            if hour_branch == 'Wei' :
                s = 'Gui'
            if hour_branch == 'Shen' :
                s = 'Jia'
            if hour_branch == 'You' :
                s = 'Yi'
            if hour_branch == 'Xu' :
                s = 'Bing'
            if hour_branch == 'Hai' :
                s = 'Ding'
                
        if day_stem == 'Bing' or  day_stem == 'Xin' :
            if hour_branch == 'Zi' :
                s = 'Wu'
            if hour_branch == 'Chou' :
                s = 'Ji'
            if hour_branch == 'Yin' :
                s = 'Geng'
            if hour_branch == 'Mao' :
                s = 'Xin'
            if hour_branch == 'Chen' :
                s = 'Ren'
            if hour_branch == 'Si' :
                s = 'Gui'
            if hour_branch == 'Wu' :
                s = 'Jia'
            if hour_branch == 'Wei' :
                s = 'Yi'
            if hour_branch == 'Shen' :
                s = 'Bing'
            if hour_branch == 'You' :
                s = 'Ding'
            if hour_branch == 'Xu' :
                s = 'Wu'
            if hour_branch == 'Hai' :
                s = 'Ji'
                
        if day_stem == 'Ding' or  day_stem == 'Ren' :
            if hour_branch == 'Zi' :
                s = 'Geng'
            if hour_branch == 'Chou' :
                s = 'Xin'
            if hour_branch == 'Yin' :
                s = 'Ren'
            if hour_branch == 'Mao' :
                s = 'Gui'
            if hour_branch == 'Chen' :
                s = 'Jia'
            if hour_branch == 'Si' :
                s = 'Yi'
            if hour_branch == 'Wu' :
                s = 'Bing'
            if hour_branch == 'Wei' :
                s = 'Ding'
            if hour_branch == 'Shen' :
                s = 'Wu'
            if hour_branch == 'You' :
                s = 'Yi'
            if hour_branch == 'Xu' :
                s = 'Geng'
            if hour_branch == 'Hai' :
                s = 'Xin'
                
        if day_stem == 'Wu' or  day_stem == 'Gui' :
            if hour_branch == 'Zi' :
                s = 'Ren'
            if hour_branch == 'Chou' :
                s = 'Gui'
            if hour_branch == 'Yin' :
                s = 'Jia'
            if hour_branch == 'Mao' :
                s = 'Yi'
            if hour_branch == 'Chen' :
                s = 'Bing'
            if hour_branch == 'Si' :
                s = 'Ding'
            if hour_branch == 'Wu' :
                s = 'Wu'
            if hour_branch == 'Wei' :
                s = 'Ji'
            if hour_branch == 'Shen' :
                s = 'Geng'
            if hour_branch == 'You' :
                s = 'Xin'
            if hour_branch == 'Xu' :
                s = 'Ren'
            if hour_branch == 'Hai' :
                s = 'Gui'
                        
        return s             
           
    def hour_dt_stembranch(self, dt): 
        """ get hour stem and branch for date dt """
        br = self.hour_branch(dt)
        dstbr = self.day_dt_stembranch(dt)
        dst  = dstbr.split('-')[0]
        st = self.hour_stem(dst, br)
        s = st+'-'+br
        return s
        
    def get_chnames(self,s):
        """returns ch names for stem and branch"""
        st = s.split('-')[0]
        br = s.split('-')[1]
        for i in range(1,11) :
            #print i
            if self.stems[i]==st :
                cst = self.cstems[i]
        for i in range(1,14) :
            #print i
            if self.branches[i]==br :
                cbr = self.cbranches[i]
        cc = cst+cbr
        return cc
    
    def year_zodiac(self,year):
        """gets chinese zodiac for year"""
        sb = self.year_stembranch(year)
        br = sb.split('-')[1]
        for i in range(1,14) :
            #print i
            if self.branches[i]==br :
                cz = self.zodiac[i]
        return cz
        
    
    def print_stemsbranches(self, dt): 
        """prints stems and branches for defined location and time""" 
        print 'Year stem and branch :'
        s= self.year_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs
        
        print 'Month stem and branch :'
        s= self.month_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs

        print 'Day stem and branch :'
        s= self.day_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs
        
        print 'Hour stem and branch :'
        s = self.hour_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs
    
    def print_datetime(self,dt):
        """ prints date Gregorian and lunar and time local and solar """
        year = dt.timetuple().tm_year
        #print year
        month = dt.timetuple().tm_mon
        #print month
    
        day = dt.timetuple().tm_mday 
               
        hour = dt.timetuple().tm_hour
        
        min = dt.timetuple().tm_min
        
        ld = lunardate.LunarDate.fromSolarDate(year, month, day)
        #print ld
        lmonth = ld.month
        
        lyear = ld.year
        
        lday = ld.day
        #print month
        z = self.year_zodiac(lyear)
        
        print 'Gregorian :'
        
        print 'Year : '+str(year)
        print 'month : '+str(month)
        print 'day :'+str(day)
        
        print 'local time '+str(hour)+':'+str(min)
        
        
        print 'Lunar :'
        
        print 'Year : '+str(lyear)+' year of '+str(z)
        print 'month : '+str(lmonth)
        print 'day :'+str(lday)
        
        if ld.isLeapMonth :
            print 'Leap month'
        
        self.calc_solar_terms(dt-datetime.timedelta(hours=27))    
        start = 0 
        for i in range(24):
            if dt.date() == self.solartermsdt[start].date():
                print 'Solar term : '+str(self.solarterms[start])+' '+str(self.solartermsch[start])+' '
            start += 15
            
        n = datetime.datetime(year,month,day,12,0)
        
        sn = self.find_solar_noonC(dt)
        
        delta = sn - n
        
        st = dt - delta
        
        shour = st.timetuple().tm_hour
        
        smin = st.timetuple().tm_min
        
        print 'Solar time '+str(shour)+':'+str(smin)
        
        print 'Sun'
        dtr = self.solrising
        hour = dtr.timetuple().tm_hour
        
        min = dtr.timetuple().tm_min
        
        print 'Rising : '+ str(hour)+':'+str(min)
        dtr = self.solnoon
        hour = dtr.timetuple().tm_hour
        
        min = dtr.timetuple().tm_min
        
        print 'Noon : '+ str(hour)+':'+str(min)
        dtr = self.solsetting
        hour = dtr.timetuple().tm_hour
        
        min = dtr.timetuple().tm_min
        
        print 'Setting : ' + str(hour)+':'+str(min)
        
        sc = self.find_sun_constell(dt)
        
        print 'Constellation : '+ str(sc)

        
        print 'Moon'
        
        
        mp = self.find_moon_phase(dt)
        mc = self.find_moon_constell(dt)


        print 'Rising : '
        mr = self.find_moon_risingC(dt)
        
        year = mr.timetuple().tm_year
        #print year
        month = mr.timetuple().tm_mon
        #print month
    
        day = mr.timetuple().tm_mday 
        hour = mr.timetuple().tm_hour
        
        min = mr.timetuple().tm_min
       
        
        print str(day)+'/'+str(month)+ ' at '+ str(hour)+':'+str(min)
        
        print 'Transit : '
        mr = self.find_moon_transitC(dt)
        
        year = mr.timetuple().tm_year
        #print year
        month = mr.timetuple().tm_mon
        #print month
    
        day = mr.timetuple().tm_mday 
        hour = mr.timetuple().tm_hour
        
        min = mr.timetuple().tm_min
       
        
        print str(day)+'/'+str(month)+ ' at '+ str(hour)+':'+str(min)
        print 'Setting : '
        mr = self.find_moon_settingC(dt)
        
        year = mr.timetuple().tm_year
        #print year
        month = mr.timetuple().tm_mon
        #print month
    
        day = mr.timetuple().tm_mday 
        hour = mr.timetuple().tm_hour
        
        min = mr.timetuple().tm_min
       
        
        print str(day)+'/'+str(month)+ ' at '+ str(hour)+':'+str(min)
       
        
        print 'Phase : '+str(mp)
        print 'Constellation : '+ str(mc)
    
    def print_date_fc(self,dt):
        """ prints date Gregorian and lunar """
        year = dt.timetuple().tm_year
        #print year
        month = dt.timetuple().tm_mon
        #print month
    
        day = dt.timetuple().tm_mday 
               
        hour = dt.timetuple().tm_hour
        
        min = dt.timetuple().tm_min
        
        ld = lunardate.LunarDate.fromSolarDate(year, month, day)
        #print ld
        lmonth = ld.month
        
        lyear = ld.year
        
        lday = ld.day
        #print month
        z = self.year_zodiac(lyear)
        
        print 'Gregorian :'
        
        print 'Year : '+str(year)
        print 'month : '+str(month)
        print 'day :'+str(day)
        print '\n'
        
        #print 'local time '+str(hour)+':'+str(min)
        
        
        print 'Lunar :'
        
        print 'Year : '+str(lyear)+' year of '+str(z)
        print 'Stem and branch :'
        s= self.year_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs
        
        print 'Month : '+str(lmonth)
        if ld.isLeapMonth :
            print 'Leap month'
        print 'Stem and branch :'
        s= self.month_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs

        
        print 'Day :'+str(lday)
        print 'Stem and branch :'
        s= self.day_dt_stembranch(dt)
        print s
        cs = self.get_chnames(s)
        print cs
        
        #if ld.isLeapMonth :
        #    print 'Leap month'
        
        self.calc_solar_terms(dt-datetime.timedelta(hours=27))    
        start = 0 
        for i in range(24):
            if dt.date() == self.solartermsdt[start].date():
                print 'Solar term : '+str(self.solarterms[start])+' '+str(self.solartermsch[start])+' '
            
                
            start += 15
         
        print '\n'   
        n = datetime.datetime(year,month,day,12,0)
        
        sn = self.find_solar_noonC(dt)
        
        delta = sn - n
        
        st = dt - delta
        
        shour = st.timetuple().tm_hour
        
        smin = st.timetuple().tm_min
        
        #print 'Solar time '+str(shour)+':'+str(smin)
        
        print 'Sun'
        dtr = self.solrising
        hour = dtr.timetuple().tm_hour
        
        min = dtr.timetuple().tm_min
        
        print 'Rising : '+ str(hour)+':'+str(min)
        dtr = self.solnoon
        hour = dtr.timetuple().tm_hour
        
        min = dtr.timetuple().tm_min
        
        print 'Noon : '+ str(hour)+':'+str(min)
        dtr = self.solsetting
        hour = dtr.timetuple().tm_hour
        
        min = dtr.timetuple().tm_min
        
        print 'Setting : ' + str(hour)+':'+str(min)
        
        sc = self.find_sun_constell(dt)
        
        print 'Constellation : '+ str(sc)
        print '\n'

        
        print 'Moon'
        
        
        mp = self.find_moon_phase(dt)
        mc = self.find_moon_constell(dt)


        print 'Rising : '
        mr = self.find_moon_risingC(dt)
        
        year = mr.timetuple().tm_year
        #print year
        month = mr.timetuple().tm_mon
        #print month
    
        day = mr.timetuple().tm_mday 
        hour = mr.timetuple().tm_hour
        
        min = mr.timetuple().tm_min
       
        
        print str(day)+'/'+str(month)+ ' at '+ str(hour)+':'+str(min)
        
        print 'Transit : '
        mr = self.find_moon_transitC(dt)
        
        year = mr.timetuple().tm_year
        #print year
        month = mr.timetuple().tm_mon
        #print month
    
        day = mr.timetuple().tm_mday 
        hour = mr.timetuple().tm_hour
        
        min = mr.timetuple().tm_min
       
        
        print str(day)+'/'+str(month)+ ' at '+ str(hour)+':'+str(min)
        print 'Setting : '
        mr = self.find_moon_settingC(dt)
        
        year = mr.timetuple().tm_year
        #print year
        month = mr.timetuple().tm_mon
        #print month
    
        day = mr.timetuple().tm_mday 
        hour = mr.timetuple().tm_hour
        
        min = mr.timetuple().tm_min
       
        
        print str(day)+'/'+str(month)+ ' at '+ str(hour)+':'+str(min)
       
        
        print 'Phase : '+str(mp)
        print 'Constellation : '+ str(mc)
    

    
        
    def calc_solar_terms(self, dt):
        """solar terms calculation""" 
        from math import pi
        twopi = 2 * pi
         
        d = ephem.Date(dt.date())
        
        def when_is_sun_at_degrees_longitude(degrees):

            # Find out the sun's current longitude.

            sun = ephem.Sun(d)
            current_longitude = sun.hlong - pi
            #print 365.25*current_longitude/twopi

            # Find approximately the right time of year.

            target_longitude = degrees * ephem.degree
            difference = (target_longitude - current_longitude) % twopi
            t0 = d + 365.25 * difference / twopi

            # Zero in on the exact moment.

            def f(t):
                sun.compute(t)
                longitude = sun.hlong - pi
                return ephem.degrees(target_longitude - longitude).znorm

            return ephem.Date(ephem.newton(f, t0, t0 + ephem.minute))
  
        start = 0 
        for i in range(24):
            #print start
            ed = when_is_sun_at_degrees_longitude(start)
            cdt = ed.datetime()
            cdt += datetime.timedelta(hours=self.tdiffUTC)
            #print cdt
            self.solartermsdt[start] = cdt
                                      
            
            start += 15
    
    
            
    def print_solar_terms(self,dt):
        """prints solar terms for current solar year"""
        start = 0 
        for i in range(24):
            print str(start)+' '+str(self.solarterms[start])+' '+str(self.solartermsch[start])+' '+str(self.solartermsdt[start].date())
            start += 15
        
    def print_solar_terms_fc(self,dt):
        """prints solar terms for current month"""
        start = 0 
        for i in range(24):
            if dt.date().month == self.solartermsdt[start].date().month :
                print str(self.solartermsdt[start].date().day)+' '+str(self.solarterms[start])+' '+str(self.solartermsch[start])
            start += 15
                    
            
        
          
        
        
        
        
    
        
    
