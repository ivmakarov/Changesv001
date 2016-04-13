# -*- coding: utf-8 -*-
#
# "CHANGES" library - Medical Unit
#
#  brings chinese philosophy to life
#
# (C) Ivan Makarov, Oleksandr Golovchansky 2015-2016
# Email: ivmakarov@yahoo.com
#
from ElementsT1 import *
from ChangesT1_StemsBranches import *
from termcolor import colored, cprint

# for Linux and  Mac Os X :
PatientsDataDirectory =  homedir+libdir+'/p'
PTimagesDirectory = homedir+libdir+'/p/timg/'
# for Windows :
#PatientsDataDirectory = r"C:\Changesv001\p"
#PTimagesDirectory = r"C:\Changesv001\p\timg"


class med_unit(Elements):
    
    def add_Pinfo(self, Name, Pname, Pbirthday, Pdiagnosis):
        """adds patient info to element Name - Patient name, birthday, diagnosis"""
        self.elements[Name].add_pinfo(Pname, Pbirthday, Pdiagnosis)
        
        
    def add_Pinfo_to_all(self, Pname, Pbirthday, Pdiagnosis):
        """adds patient info to all elements in working group - Patient name, birthday YYYY-MM-DD, diagnosis"""
        for e in self.elements :
            self.elements[e].add_pinfo(Pname, Pbirthday, Pdiagnosis)
            

    def add_comment(self, Name, Pcomment):
        """adds a comment to hexagram Name"""
        self.elements[Name].Pcomment = Pcomment
        
    def add_channels(self, Name, channels):
        """adds channels info to element Name"""
        self.elements[Name].channels = channels
        
    def set_tag(self, Name, tag):
        """sets a tag W -for working, R -for resulting , T -for treatment """
        self.elements[Name].tag = tag
    
    def minvert(self, Name, InvName, hset):
        """invertes hexagram, adds info from hset, and patient data from original hexagram""" 
        self.invert(Name, InvName)  
        self.find_in_set(InvName, InvName, hset)
        self.copy_Pinfo(InvName,self.elements[Name])
        
        print self.__call__(InvName)
        
    def mnuclear(self, Name, InvName, hset):
        """creates nuclear hexagram, adds info from hset, and patient data from original hexagram""" 
        self.nuclear(Name, InvName)  
        self.find_in_set(InvName, InvName, hset)
        self.copy_Pinfo(InvName,self.elements[Name])
        
        print self.__call__(InvName)
        
        
    def minv_keep_float(self, Name, InvName, hset):
        """invertes hexagram but keeps floating, adds info from hset, and patient data from original hexagram"""
        self.inv_keep_float(Name, InvName)
        self.find_in_set(InvName, InvName, hset)
        self.copy_Pinfo(InvName,self.elements[Name])
        
        print self.__call__(InvName)
    
    
    def mchange_yao(self,Name,CGName,hset,Yao,Yao2=None, Yao3=None, Yao4=None, Yao5=None, Yao6=None):
        """changes yao(s),  adds info from hset, and patient data from original hexagram """ 
        self.change_yaos(Name, CGName, Yao, Yao2, Yao3, Yao4, Yao5, Yao6)
        self.find_in_set(CGName, CGName, hset)
        self.copy_Pinfo(CGName,self.elements[Name]) 
        
        print self.__call__(CGName)
        
    def mchange_float(self,Name,CGName,hset):  
        """changes floating yaos,  adds info from hset, and patient data from original hexagram """ 
        self.change_float_yaos(Name, CGName)
        self.find_in_set(CGName, CGName, hset)
        self.copy_Pinfo(CGName,self.elements[Name]) 
        
        #print self.__call__(CGName)
        
    def madd_float_and_change(self,Name,hset,Yao,Yao2=None, Yao3=None, Yao4=None, Yao5=None, Yao6=None):
        """adds floating yaos,changes it, set working tag  adds info from hset, and patient data from original hexagram """
        DelName = None
        for e in self.elements :
            if self.elements[e].tag == 'W':
                DelName = self.elements[e].Name
                #print DelName
        if DelName is not None:
            self.del_W_float(DelName)
            #print 'deleted'
        CGName = 'CY'+Name
        self.set_tag(Name, 'W')
        self.del_float_yao(Name)
        if Yao is not None :
            self.add_float_yao(Name, Yao, Yao2, Yao3, Yao4, Yao5, Yao6)
            print 'WORKING hexagram : \n'
            print self.__call__(Name)
            print 'CHANGED YAOS hexagram : \n'
            self.mchange_float(Name, CGName, hset)
            self.set_tag(CGName, 'R')
            print self.__call__(CGName)
        else :
            print 'WORKING hexagram : \n'
            print self.__call__(Name)
            print 'Result hexagram is the same. \n'
            
            
            

    def madd_float_and_change_col(self,Name,hset,Yao,Yao2=None, Yao3=None, Yao4=None, Yao5=None, Yao6=None):
        """(colored output!)adds floating yaos,changes it, set working tag  adds info from hset, and patient data from original hexagram """
        
        DelName = None
        for e in self.elements :
            if self.elements[e].tag == 'W':
                DelName = self.elements[e].Name
        #print DelName
        if DelName is not None:
                self.del_W_float(DelName)
        #print 'deleted'
        CGName = 'CY'+Name
        self.set_tag(Name, 'W')
        self.del_float_yao(Name)
        self.add_float_yao(Name, Yao, Yao2, Yao3, Yao4, Yao5, Yao6)
        print colored("WORKING hexagram : \n", 'green',attrs=['bold'])
        #print 'WORKING hexagram : \n'
        print self.__call__(Name)
        print colored("CHANGED YAOS hexagram : \n", 'green',attrs=['bold'])
        #print 'CHANGED YAOS hexagram : \n'
        self.mchange_float(Name, CGName, hset)
        self.set_tag(CGName, 'R')
        print self.__call__(CGName)


    def del_W_float(self,Name):
        """deleting W tag and floating yaos and resulting hexagram"""
        self.del_tag(Name) 
        self.del_float_yao(Name)
        CGName = 'CY'+Name
        self.delete(CGName)
    
    def ptransform(self, Name,LG,MG,UG,bset,hset):
        """p transformation from lower gua, middle gua, upper gua - 
        added under Name"""
        
               
        temp = Elements()
        temp.basic_copy(LG, bset.elements[LG])
        temp.basic_copy(MG, bset.elements[MG])
        temp.basic_copy(UG, bset.elements[UG])
        
        self.add(Name, temp.elements[LG].Y1, temp.elements[MG].Y1, temp.elements[UG].Y1, temp.elements[LG].Y3, temp.elements[MG].Y3, temp.elements[UG].Y3)
        

    def pulse_hex(self,Name,RU,RM,RL,LU,LM,LL,bset,hset):
        """building hexagrams from pulse first dex then sin, gua names: Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui"""
        #l = ["Qian","Zhen","Kan","Gen","Kun","Xun","Li","Dui"]
        
        #forming hexagrams from puls and nuclear
        
        self.add_from_gua(Name+"P_SIN", LL, LU, bset)
        self.add_from_gua(Name+"P_DEX", RL, RU, bset)
        self.nuclear(Name+"P_SIN", Name+"P_SIN_NUC")
        self.nuclear(Name+"P_DEX", Name+"P_DEX_NUC")
        
        # forming p transformed hexagrams and nuclear
        
        self.ptransform(Name+"PTRANS_SIN", LL, LM, LU, bset, hset)
        self.ptransform(Name+"PTRANS_DEX", RL, RM, RU, bset, hset)
        self.nuclear(Name+"PTRANS_SIN", Name+"PTRANS_SIN_NUC")
        self.nuclear(Name+"PTRANS_DEX", Name+"PTRANS_DEX_NUC")
        
        # add information from hexagram set
        
        self.all_add_info_from_set(hset)
        
        # print them
        
        print"PULSE hexagrams : \n"
        
        print self.__call__(Name+'P_DEX')
        print self.__call__(Name+'P_SIN')
        
        print "PULSE NUCLEAR hexagrams : \n"
        
        print self.__call__(Name+"P_DEX_NUC")
        print self.__call__(Name+"P_SIN_NUC")
        
        print "P TRANSFORMED hexagrams : \n"
        
        print self.__call__(Name+"PTRANS_DEX")
        print self.__call__(Name+"PTRANS_SIN")
        
        print "NUCLEAR P TRANSFORMED hexagrams : \n"
        
        print self.__call__(Name+"PTRANS_DEX_NUC")
        print self.__call__(Name+"PTRANS_SIN_NUC")
        
        print "MIDDLE GUA DEX :"
        
        print bset.__call__(bset.elements[RM].Name)
        
        print "MIDDLE GUA SIN :"
        
        print bset.__call__(bset.elements[LM].Name)
    
    def pulse_hexS(self,Name,RU,RM,RL,LU,LM,LL,bset,hset):
        """building hexagrams from pulse and adding to ordered set first dex then sin, gua names: Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui"""
        #l = ["Qian","Zhen","Kan","Gen","Kun","Xun","Li","Dui"]
        
        #forming hexagrams from puls and nuclear
        
        S = '------------------------------------------------------------------------------------------\n'
        
        self.add_from_gua("2_"+Name+"P_SIN", LL, LU, bset)
        self.add_from_gua("1_"+Name+"P_DEX", RL, RU, bset)
        self.nuclear("2_"+Name+"P_SIN", "4_"+Name+"P_SIN_NUC")
        self.nuclear("1_"+Name+"P_DEX", "3_"+Name+"P_DEX_NUC")
        
        # forming p transformed hexagrams and nuclear
        
        self.ptransform("6_"+Name+"PTRANS_SIN", LL, LM, LU, bset, hset)
        self.ptransform("5_"+Name+"PTRANS_DEX", RL, RM, RU, bset, hset)
        self.nuclear("6_"+Name+"PTRANS_SIN", "8_"+Name+"PTRANS_SIN_NUC")
        self.nuclear("5_"+Name+"PTRANS_DEX", "7_"+Name+"PTRANS_DEX_NUC")
        
        
        
        # add information from hexagram set
        
        self.all_add_info_from_set(hset)
        
        e = Element("9_M_GUA_DEX",bset.elements[RM].Y1,bset.elements[RM].Y2,bset.elements[RM].Y3)
        self.elements["9_M_GUA_DEX"] = e
        e = Element("9_M_GUA_SIN",bset.elements[LM].Y1,bset.elements[LM].Y2,bset.elements[LM].Y3)
        self.elements["9_M_GUA_SIN"] = e
        
        
        self.find_in_set("9_M_GUA_DEX","9_M_GUA_DEX",bset)
        self.find_in_set("9_M_GUA_SIN","9_M_GUA_SIN",bset)
        
        
        dt = datetime.datetime.now()
        self.add_Elcrdatetime("1_"+Name+'P_DEX', dt)
        self.add_Elcrdatetime("2_"+Name+'P_SIN', dt)
        self.add_Elcrdatetime("3_"+Name+"P_DEX_NUC", dt)
        self.add_Elcrdatetime("4_"+Name+"P_SIN_NUC", dt)
        self.add_Elcrdatetime("5_"+Name+"PTRANS_DEX", dt)
        self.add_Elcrdatetime("6_"+Name+"PTRANS_SIN", dt)
        self.add_Elcrdatetime("7_"+Name+"PTRANS_DEX_NUC", dt)
        self.add_Elcrdatetime("8_"+Name+"PTRANS_SIN_NUC", dt)
        
        
        
        
        # print them
        
        S+= "PULSE hexagrams : \n"
        
        
        S+=  self.getstrE("1_"+Name+'P_DEX')
        
        S+=  self.getstrE("2_"+Name+'P_SIN')
        
        S+= '----------------------------------------------------------------------------------------\n'

        
        S+=  "PULSE NUCLEAR hexagrams : \n"
        
        
        S+=  self.getstrE("3_"+Name+"P_DEX_NUC")
        
        S+=  self.getstrE("4_"+Name+"P_SIN_NUC")
        
        S+= '----------------------------------------------------------------------------------------\n'

        
        S+=  "P TRANSFORMED hexagrams : \n"
        
        
        S+=  self.getstrE("5_"+Name+"PTRANS_DEX")
        
        S+=  self.getstrE("6_"+Name+"PTRANS_SIN")
        
        S+= '----------------------------------------------------------------------------------------\n'

        
        S+=  "NUCLEAR P TRANSFORMED hexagrams : \n"
        
        
        S+=  self.getstrE("7_"+Name+"PTRANS_DEX_NUC")
        
        S+=  self.getstrE("8_"+Name+"PTRANS_SIN_NUC")
        
        S+= '----------------------------------------------------------------------------------------\n'

        
        S+=  "MIDDLE GUA DEX :"
        
        
        S+=  bset.getstrE(bset.elements[RM].Name)
        
        
        S+=  "MIDDLE GUA SIN :"
        
        
        S+=  bset.getstrE(bset.elements[LM].Name)
        
        return S
    
    def pulse_hex_col(self,Name,RU,RM,RL,LU,LM,LL,bset,hset):
        """(colored output!) building hexagrams from pulse first dex then sin, gua names: Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui, colored output version"""
        #l = ["Qian","Zhen","Kan","Gen","Kun","Xun","Li","Dui"]
        
        #forming hexagrams from puls and nuclear
        
        
        
        self.add_from_gua(Name+"P_SIN", LL, LU, bset)
        self.add_from_gua(Name+"P_DEX", RL, RU, bset)
        self.nuclear(Name+"P_SIN", Name+"P_SIN_NUC")
        self.nuclear(Name+"P_DEX", Name+"P_DEX_NUC")
        
        # forming p transformed hexagrams and nuclear
        
        self.ptransform(Name+"PTRANS_SIN", LL, LM, LU, bset, hset)
        self.ptransform(Name+"PTRANS_DEX", RL, RM, RU, bset, hset)
        self.nuclear(Name+"PTRANS_SIN", Name+"PTRANS_SIN_NUC")
        self.nuclear(Name+"PTRANS_DEX", Name+"PTRANS_DEX_NUC")
        
        # add information from hexagram set
        
        self.all_add_info_from_set(hset)
        
        # print them
        
        print colored("PULSE hexagrams : \n", 'green',attrs=['bold'])

        
        print self.__call__(Name+'P_DEX')
        print self.__call__(Name+'P_SIN')
        
        print colored("PULSE NUCLEAR hexagrams : \n", 'green',attrs=['bold'])
        
        print self.__call__(Name+"P_DEX_NUC")
        print self.__call__(Name+"P_SIN_NUC")
        
        print colored("P TRANSFORMED hexagrams : \n", 'green',attrs=['bold'])
        
        print self.__call__(Name+"PTRANS_DEX")
        print self.__call__(Name+"PTRANS_SIN")
        
        print colored("NUCLEAR P TRANSFORMED hexagrams : \n", 'green',attrs=['bold'])
        
        print self.__call__(Name+"PTRANS_DEX_NUC")
        print self.__call__(Name+"PTRANS_SIN_NUC")
        
        print colored("MIDDLE GUA DEX :", 'green',attrs=['bold'])
        
        print bset.__call__(bset.elements[RM].Name)
        
        print colored("MIDDLE GUA SIN :", 'green',attrs=['bold'])
        
        print bset.__call__(bset.elements[LM].Name)
    
        
    def mchange_gua(self,Name,CGName,cname,bset): 
        """performs change of gua defined by cname - heaven, heavenman, hsiao, hsi, earthman, earth, heavenearth, man, threepowers """   
        if cname == 'heaven':
            self.change_gua_heaven(Name, CGName, bset)
        elif cname == 'heavenman':
            self.change_gua_heavenmen(Name, CGName, bset)
        elif cname == 'hsiao':
            self.change_gua_hsiao(Name, CGName, bset)
        elif cname == 'hsi':
            self.change_gua_hsi(Name, CGName, bset)
        elif cname == 'earthman':
            self.change_gua_earthman(Name, CGName, bset)
        elif cname == 'earth':
            self.change_gua_earth(Name, CGName, bset)
        elif cname == 'heavenearth':
            self.change_gua_heavenearth(Name, CGName, bset)
        elif cname == 'man':
            self.change_gua_man(Name, CGName, bset)
        elif cname == 'threepowers':
            self.change_gua_threepowers(Name, CGName, bset)
            
    def mvitalitymov(self,branch,subhour):
        """returns channel and transf. corresponding to brunch and subhour"""
        if branch == 'Zi' or branch == 'Wu' or branch == 'Mao' or branch == 'You':
            if subhour == '1':
                s = 'Ht earthman threepowers'
            elif subhour == '2':
                s = 'SI earth threepowers'
            elif subhour == '3':
                s = 'BL heaven heavenearth'
            elif subhour == '4':
                s = 'KID heavenman heavenearth'
        if branch == 'Chou' or branch == 'Wei' or branch == 'Chen' or branch == 'Xu':
            if subhour == '1':
                s = 'HG hsiao man'
            elif subhour == '2':
                s = 'TB hsi man'
            elif subhour == '3':
                s = 'GB earthman threepowers'
            elif subhour == '4':
                s = 'LIV earth threepowers'
        if branch == 'Yin' or branch == 'Shen' or branch == 'Si' or branch == 'Hai':
            if subhour == '1':
                s = 'LU heaven heavenearth'
            elif subhour == '2':
                s = 'LI heavenman heavenearth'
            elif subhour == '3':
                s = 'ST hsiao man'
            elif subhour == '4':
                s = 'Sp hsi man'
        return s
    
    def pain_trtfr(self, Channel, LT, bset,SK = None,dt = None):
        """performs pain treatment- Channel in french notation- channel, LT - limbs or trunk, channel names: VB,V,GI,E,TR,IG,R,F,P,Rp,C,MC , and SK = 1 - sunrize/sunset correction, 0 - no correction, dt -moment of time """
        ch  = self.channeleng(Channel)
        self.pain_trt(ch, LT, bset,SK,dt)
    
    def pain_trt(self, Channel, LT, bset,SK = None,dt = None):
        """performs pain treatment- Channel - channel, LT - limbs or trunk, channel names: GB, BL, LI, ST, TB, SI, KID, LIV, LU, Sp, Ht, HG,   and SK = 1 - sunrize/sunset correction, 0 - no correction, dt -moment of time """
        #print 'Initial channel : '+str(Channel)
        Gua = self.guabychannel(Channel)
        #self.eighttrigrambalance(Gua, LT, bset)
        if dt == None:
            dt = datetime.datetime.now()
        st = stemsbranches()
        #print dt
        #print '------------------------------------------------------------------------------------------'

        if SK is None:
            SK = 0
        if SK == 1:
            st.init_solar12shichen(dt)
            print 'Sunrise/Sunset correction applied!'
        else:
            st.init_12shichen(dt)
        #st.init_12shichen(dt)
        br = st.hour_branch(dt)
        
        for i in range(1,15) :
            if st.hstart[i] < dt and dt < st.hend[i] :
                brst = st.hstart[i]
                brend = st.hend[i]
                
        d1 = brend - brst
        dlt = divtd(d1,4)
        #dlt = datetime.timedelta(minutes=30)
        dt1 = dt + dlt
        #print '------------------------------------------------------------------------------------------'

        print 'Time : '+str(dt.time()).split(':')[0]+' h '+str(dt.time()).split(':')[1]+' min \n'
        #print 'Hour Branch : '+ str(br)+ '\n'
        channelfr = self.channelfr(Channel)
        
        print 'Pain location in Channel : '+str(channelfr)+'  ('+str(Channel)+')'
        print 'Limbs/trunk : '+str(LT)+'\n'
        self.copy_El('initialGua', bset.elements[Gua])
        self.find_in_set('initialGua', 'initialGua', bset)
        #print 'Initial Gua: \n'
        #print self.__call__(self.elements['initialGua'].Name)
        
        deltah = st.diff_sub_hour(dt)
        print 'This '+str(deltah).split(':')[1]+' min '
        br = st.hour_branch(dt)
        print 'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt)
        #print sha
        sh = sha.split(' ')[0]
        vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        print 'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        print t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min'
        c = vchannel.split(' ')[0]
        cfr = self.channelfr(c)
        oppc = self.oppchannel(c)
        lo = self.channello(oppc)
        oppfr = self.channelfr(oppc)
        print 'Channel : '+ str(cfr)+ '  ('+str(c)+')'
        print 'to influence Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+')'
        if LT == 'limbs':
            move = vchannel.split(' ')[1]
        elif LT == 'trunk':
            move = vchannel.split(' ')[2]
        #print 'Limbs/trunk : '+str(LT) 
        #print 'Transformation : '+str(move)+'\n'
        
        self.mchange_gua('initialGua', 'resultGua', move, bset)
        #print 'Result : \n'
        #print self.__call__(self.elements['resultGua'].Name)
        ch1 = self.channelbygua(self.elements['resultGua'].EngName)
        sp = ' '
        if sp in ch1:
            ch10 = ch1.split(' ')[0]
            ch11 = ch1.split(' ')[1]
            ch10fr = self.channelfr(ch10)
            ch11fr = self.channelfr(ch11)
            print "to treat pain Channels : "+str(ch10fr)+' '+str(ch11fr)+'  ('+str(ch10)+' '+str(ch11)+')\n'
        else:    
            ch1fr = self.channelfr(ch1)
            print "to treat pain Channel : "+str(ch1fr)+'  ('+str(ch1)+')\n'
        
        
        deltah = st.delta_sub_hour(dt1)
        print 'Next '+str(deltah).split(':')[1]+' min '
        #print 'Next 30 min '
        
        if SK == 1:
            st.init_solar12shichen(dt1)
        else:
            st.init_12shichen(dt1)
        #st.init_12shichen(dt1)
        
        br = st.hour_branch(dt1)
        print 'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt1)
        #print sha
        sh = sha.split(' ')[0]
        vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        print 'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        print t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min'
        #print str(sha.split(' ')[1]) +' to '+str(sha.split(' ')[2])
        c = vchannel.split(' ')[0]
        cfr = self.channelfr(c)
        oppc = self.oppchannel(c)
        oppfr = self.channelfr(oppc)
        lo = self.channello(oppc)
        print 'Channel : '+ str(cfr)+ '  ('+str(c)+')'
        print 'to influence Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+')'
        
        if LT == 'limbs':
            move = vchannel.split(' ')[1]
        elif LT == 'trunk':
            move = vchannel.split(' ')[2]
        #print 'Limbs/trunk : '+str(LT) 
        #print 'Transformation : '+str(move)+'\n'
        
        self.mchange_gua('initialGua', 'nextSHGua', move, bset)
        #print 'Result for next 30 min : \n'
        #print self.__call__(self.elements['nextSHGua'].Name)
        ch1 = self.channelbygua(self.elements['nextSHGua'].EngName)
        sp = ' '
        if sp in ch1:
            ch10 = ch1.split(' ')[0]
            ch11 = ch1.split(' ')[1]
            ch10fr = self.channelfr(ch10)
            ch11fr = self.channelfr(ch11)
            print "to treat pain Channels : "+str(ch10fr)+' '+str(ch11fr)+'  ('+str(ch10)+' '+str(ch11)+')\n'
        else:    
            ch1fr = self.channelfr(ch1)
            print "to treat pain Channel : "+str(ch1fr)+'  ('+str(ch1)+')\n'
        
        #print '------------------------------------------------------------------------------------------'
        
    def pain_trtS(self, Channel, LT, bset,SK = None,dt = None):
        """performs pain treatment- Channel - channel, LT - limbs or trunk, channel names: GB, BL, LI, ST, TB, SI, KID, LIV, LU, Sp, Ht, HG,   and SK = 1 - sunrize/sunset correction, 0 - no correction, dt -moment of time, srting output """
        #print 'Initial channel : '+str(Channel)
        S = '------------------------------------------------------------------------------------------\n'
        Gua = self.guabychannel(Channel)
        #self.eighttrigrambalance(Gua, LT, bset)
        if dt == None:
            dt = datetime.datetime.now()
        st = stemsbranches()
        #print dt
        if SK is None:
            SK = 0
        if SK == 1:
            st.init_solar12shichen(dt)
            S+= 'Sunrise/Sunset correction applied! \n'
        else:
            st.init_12shichen(dt)
        #st.init_12shichen(dt)
        br = st.hour_branch(dt)
        
        for i in range(1,15) :
            if st.hstart[i] < dt and dt < st.hend[i] :
                brst = st.hstart[i]
                brend = st.hend[i]
                
        d1 = brend - brst
        dlt = divtd(d1,4)
        #dlt = datetime.timedelta(minutes=30)
        dt1 = dt + dlt
        
        S+=  'Time : '+str(dt.time()).split(':')[0]+' h '+str(dt.time()).split(':')[1]+' min \n'
        #print 'Hour Branch : '+ str(br)+ '\n'
        channelfr = self.channelfr(Channel)
        
        S+=  'Pain location in Channel : '+str(channelfr)+'  ('+str(Channel)+') \n'
        S+=  'Limbs/trunk : '+str(LT)+'\n'
        S+= '\n'
        self.copy_El('initialGua', bset.elements[Gua])
        self.find_in_set('initialGua', 'initialGua', bset)
        #print 'Initial Gua: \n'
        #print self.__call__(self.elements['initialGua'].Name)
        
        deltah = st.diff_sub_hour(dt)
        S+=  'This '+str(deltah).split(':')[1]+' min \n'
        br = st.hour_branch(dt)
        #S+=  'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt)
        #print sha
        sh = sha.split(' ')[0]
        vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        S+=  'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        S+=  t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min \n'
        c = vchannel.split(' ')[0]
        cfr = self.channelfr(c)
        oppc = self.oppchannel(c)
        lo = self.channello(oppc)
        oppfr = self.channelfr(oppc)
        S+=  'Channel : '+ str(cfr)+ '  ('+str(c)+') \n'
        S+=  'to influence Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+') \n'
        if LT == 'limbs':
            move = vchannel.split(' ')[1]
        elif LT == 'trunk':
            move = vchannel.split(' ')[2]
        #print 'Limbs/trunk : '+str(LT) 
        #print 'Transformation : '+str(move)+'\n'
        
        self.mchange_gua('initialGua', 'resultGua', move, bset)
        #print 'Result : \n'
        #print self.__call__(self.elements['resultGua'].Name)
        ch1 = self.channelbygua(self.elements['resultGua'].EngName)
        sp = ' '
        if sp in ch1:
            ch10 = ch1.split(' ')[0]
            ch11 = ch1.split(' ')[1]
            ch10fr = self.channelfr(ch10)
            ch11fr = self.channelfr(ch11)
            S+=  "to treat pain Channels : "+str(ch10fr)+' '+str(ch11fr)+'  ('+str(ch10)+' '+str(ch11)+') \n'
        else:    
            ch1fr = self.channelfr(ch1)
            S+=  "to treat pain Channel : "+str(ch1fr)+'  ('+str(ch1)+') \n'
        
        S+= '\n'
        deltah = st.delta_sub_hour(dt1)
        S+=  'Next '+str(deltah).split(':')[1]+' min \n'
        #print 'Next 30 min '
        
        if SK == 1:
            st.init_solar12shichen(dt1)
        else:
            st.init_12shichen(dt1)
        #st.init_12shichen(dt1)
        
        br = st.hour_branch(dt1)
        #S+=  'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt1)
        #print sha
        sh = sha.split(' ')[0]
        vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        S+=  'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        S+=  t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min \n'
        #print str(sha.split(' ')[1]) +' to '+str(sha.split(' ')[2])
        c = vchannel.split(' ')[0]
        cfr = self.channelfr(c)
        oppc = self.oppchannel(c)
        oppfr = self.channelfr(oppc)
        lo = self.channello(oppc)
        S+=  'Channel : '+ str(cfr)+ '  ('+str(c)+') \n'
        S+=  'to influence Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+') \n'
        
        if LT == 'limbs':
            move = vchannel.split(' ')[1]
        elif LT == 'trunk':
            move = vchannel.split(' ')[2]
        #print 'Limbs/trunk : '+str(LT) 
        #print 'Transformation : '+str(move)+'\n'
        
        self.mchange_gua('initialGua', 'nextSHGua', move, bset)
        #print 'Result for next 30 min : \n'
        #print self.__call__(self.elements['nextSHGua'].Name)
        ch1 = self.channelbygua(self.elements['nextSHGua'].EngName)
        sp = ' '
        if sp in ch1:
            ch10 = ch1.split(' ')[0]
            ch11 = ch1.split(' ')[1]
            ch10fr = self.channelfr(ch10)
            ch11fr = self.channelfr(ch11)
            S+=  "to treat pain Channels : "+str(ch10fr)+' '+str(ch11fr)+'  ('+str(ch10)+' '+str(ch11)+') \n'
        else:    
            ch1fr = self.channelfr(ch1)
            S+=  "to treat pain Channel : "+str(ch1fr)+'  ('+str(ch1)+') \n'
        return S
            
    def firstIntEndS(self, Channel, LT, bset,SK = None,dt = None):
        """finds first int end- Channel - channel, LT - limbs or trunk, channel names: GB, BL, LI, ST, TB, SI, KID, LIV, LU, Sp, Ht, HG,   and SK = 1 - sunrize/sunset correction, 0 - no correction, dt -moment of time, srting output """
        #print 'Initial channel : '+str(Channel)
        S = ''
        #Gua = self.guabychannel(Channel)
        #self.eighttrigrambalance(Gua, LT, bset)
        if dt == None:
            dt = datetime.datetime.now()
        st = stemsbranches()
        #print dt
        if SK is None:
            SK = 0
        if SK == 1:
            st.init_solar12shichen(dt)
            #S+= 'Sunrise/Sunset correction applied! \n'
        else:
            st.init_12shichen(dt)
        #st.init_12shichen(dt)
        br = st.hour_branch(dt)
        
        for i in range(1,15) :
            if st.hstart[i] < dt and dt < st.hend[i] :
                brst = st.hstart[i]
                brend = st.hend[i]
                
        d1 = brend - brst
        dlt = divtd(d1,4)
        #dlt = datetime.timedelta(minutes=30)
        dt1 = dt + dlt
        
        #S+=  'Time : '+str(dt.time()).split(':')[0]+' h '+str(dt.time()).split(':')[1]+' min \n'
        #print 'Hour Branch : '+ str(br)+ '\n'
        #channelfr = self.channelfr(Channel)
        
        #S+=  'Pain location in Channel : '+str(channelfr)+'  ('+str(Channel)+') \n'
        #S+=  'Limbs/trunk : '+str(LT)+'\n'
        #self.copy_El('initialGua', bset.elements[Gua])
        #self.find_in_set('initialGua', 'initialGua', bset)
        #print 'Initial Gua: \n'
        #print self.__call__(self.elements['initialGua'].Name)
        
        deltah = st.diff_sub_hour(dt)
        #S+=  'This '+str(deltah).split(':')[1]+' min \n'
        br = st.hour_branch(dt)
        #S+=  'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt)
        #print sha
        sh = sha.split(' ')[0]
        #vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        #S+=  'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        S = t2
        return S
    
    def secondIntEndS(self, Channel, LT, bset,SK = None,dt = None):
        """performs pain treatment- Channel - channel, LT - limbs or trunk, channel names: GB, BL, LI, ST, TB, SI, KID, LIV, LU, Sp, Ht, HG,   and SK = 1 - sunrize/sunset correction, 0 - no correction, dt -moment of time, srting output """
        #print 'Initial channel : '+str(Channel)
        S = ''
        #Gua = self.guabychannel(Channel)
        #self.eighttrigrambalance(Gua, LT, bset)
        if dt == None:
            dt = datetime.datetime.now()
        st = stemsbranches()
        #print dt
        if SK is None:
            SK = 0
        if SK == 1:
            st.init_solar12shichen(dt)
            #S+= 'Sunrise/Sunset correction applied! \n'
        else:
            st.init_12shichen(dt)
        #st.init_12shichen(dt)
        br = st.hour_branch(dt)
        
        for i in range(1,15) :
            if st.hstart[i] < dt and dt < st.hend[i] :
                brst = st.hstart[i]
                brend = st.hend[i]
                
        d1 = brend - brst
        dlt = divtd(d1,4)
        #dlt = datetime.timedelta(minutes=30)
        dt1 = dt + dlt
        
        #S+=  'Time : '+str(dt.time()).split(':')[0]+' h '+str(dt.time()).split(':')[1]+' min \n'
        #print 'Hour Branch : '+ str(br)+ '\n'
        #channelfr = self.channelfr(Channel)
        
        #S+=  'Pain location in Channel : '+str(channelfr)+'  ('+str(Channel)+') \n'
        #S+=  'Limbs/trunk : '+str(LT)+'\n'
        #self.copy_El('initialGua', bset.elements[Gua])
        #self.find_in_set('initialGua', 'initialGua', bset)
        #print 'Initial Gua: \n'
        #print self.__call__(self.elements['initialGua'].Name)
        
        deltah = st.diff_sub_hour(dt)
        #S+=  'This '+str(deltah).split(':')[1]+' min \n'
        #br = st.hour_branch(dt)
        #S+=  'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt)
        #print sha
        sh = sha.split(' ')[0]
        #vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        #S+=  'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        #S+=  t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min \n'
        #c = vchannel.split(' ')[0]
        #cfr = self.channelfr(c)
        #oppc = self.oppchannel(c)
        #lo = self.channello(oppc)
        #oppfr = self.channelfr(oppc)
        #S+=  'Channel : '+ str(cfr)+ '  ('+str(c)+') \n'
        #S+=  'to influence Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+') \n'
        #if LT == 'limbs':
        #    move = vchannel.split(' ')[1]
        #elif LT == 'trunk':
        #    move = vchannel.split(' ')[2]
        #print 'Limbs/trunk : '+str(LT) 
        #print 'Transformation : '+str(move)+'\n'
        
        #self.mchange_gua('initialGua', 'resultGua', move, bset)
        #print 'Result : \n'
        #print self.__call__(self.elements['resultGua'].Name)
        #ch1 = self.channelbygua(self.elements['resultGua'].EngName)
        #sp = ' '
        #if sp in ch1:
        #    ch10 = ch1.split(' ')[0]
        #    ch11 = ch1.split(' ')[1]
        #   ch10fr = self.channelfr(ch10)
        #    ch11fr = self.channelfr(ch11)
        #    S+=  "to treat pain Channels : "+str(ch10fr)+' '+str(ch11fr)+'  ('+str(ch10)+' '+str(ch11)+') \n'
        #else:    
        #    ch1fr = self.channelfr(ch1)
        #    S+=  "to treat pain Channel : "+str(ch1fr)+'  ('+str(ch1)+') \n'
        
        
        deltah = st.delta_sub_hour(dt1)
        #S+=  'Next '+str(deltah).split(':')[1]+' min \n'
        #print 'Next 30 min '
        
        if SK == 1:
            st.init_solar12shichen(dt1)
        else:
            st.init_12shichen(dt1)
        #st.init_12shichen(dt1)
        
        #br = st.hour_branch(dt1)
        #S+=  'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt1)
        #print sha
        sh = sha.split(' ')[0]
        #vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        #S+=  'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        S = t2
        
        return S
    
    
    def eighttrigrambalance(self, Gua, LT, bset, SK = None, dt = None):
        """performs corresponding balance of eight trigrams. Gua- corr.to channel, LT - limbs or trunk, bset- bagua set,SK = 1 - sunrize/sunset correction, 0 - no correction, dt -moment of time  gua names: Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui """
        if dt == None:
            dt = datetime.datetime.now()
        st = stemsbranches()
        #print dt
        if SK is None:
            SK = 0
        if SK == 1:
            st.init_solar12shichen(dt)
            print 'Sunrise/Sunset correction applied!'
        else:
            st.init_12shichen(dt)
            
        for i in range(1,15) :
            if st.hstart[i] < dt and dt < st.hend[i] :
                brst = st.hstart[i]
                brend = st.hend[i]
                
        d1 = brend - brst
        dlt = divtd(d1,4)
        #dlt = datetime.timedelta(minutes=30)
        dt1 = dt + dlt
        
        print 'Time : '+str(dt.time()).split(':')[0]+' h '+str(dt.time()).split(':')[1]+' min \n'
        
        self.copy_El('initialGua', bset.elements[Gua])
        self.find_in_set('initialGua', 'initialGua', bset)
        print 'Initial Gua: \n'
        print self.__call__(self.elements['initialGua'].Name)
        
        deltah = st.diff_sub_hour(dt)
        print 'This '+str(deltah).split(':')[1]+' min '
        br = st.hour_branch(dt)
        
        print 'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt)
        #print sha
        sh = sha.split(' ')[0]
        vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        print 'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        print t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min'
        #print str(sha.split(' ')[1]) +' to '+str(sha.split(' ')[2])
        c = vchannel.split(' ')[0]
        cfr = self.channelfr(c)
        oppc = self.oppchannel(c)
        oppfr = self.channelfr(oppc)
        lo = self.channello(oppc)
        print 'Channel : '+ str(cfr)+ '  ('+str(c)+')'
        print 'Opposite Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+')'
        if LT == 'limbs':
            move = vchannel.split(' ')[1]
        elif LT == 'trunk':
            move = vchannel.split(' ')[2]
        print 'Limbs/trunk : '+str(LT) 
        print 'Transformation : '+str(move)+'\n'
        
        self.mchange_gua('initialGua', 'resultGua', move, bset)
        print 'Result : \n'
        print self.__call__(self.elements['resultGua'].Name)
        
        
        deltah = st.delta_sub_hour(dt1)
        print 'Next '+str(deltah).split(':')[1]+' min '
        #print 'Next 30 min \n'
        
        if SK == 1:
            st.init_solar12shichen(dt1)
        else:
            st.init_12shichen(dt1)
        
        #st.init_12shichen(dt1)
        
        br = st.hour_branch(dt1)
        print 'Hour Branch : '+ str(br)+ '\n'
        sha = st.sub_hour(dt1)
        #print sha
        sh = sha.split(' ')[0]
        vchannel = self.mvitalitymov(br, sh)
        #print vchannel
        print 'Vitality and Blood movement : \n'
        t1 = sha.split(' ')[1]
        t2 = sha.split(' ')[2]
        print t1.split(':')[0]+' h '+t1.split(':')[1]+' min' +' to '+t2.split(':')[0]+' h '+t2.split(':')[1]+' min'
        #print str(sha.split(' ')[1]) +' to '+str(sha.split(' ')[2])
        c = vchannel.split(' ')[0]
        cfr = self.channelfr(c)
        oppc = self.oppchannel(c)
        oppfr = self.channelfr(oppc)
        lo = self.channello(oppc)
        print 'Channel : '+ str(cfr)+ '  ('+str(c)+')'
        print 'Opposite Channel : '+ str(oppfr)+' '+str(lo)+ '  ('+str(oppc)+' '+str(lo)+')'
        #print 'Opposite Channel : '+ str(oppfr)+ '  ('+str(oppc)+')'
        if LT == 'limbs':
            move = vchannel.split(' ')[1]
        elif LT == 'trunk':
            move = vchannel.split(' ')[2]
        print 'Limbs/trunk : '+str(LT) 
        print 'Transformation : '+str(move)+'\n'
        
        self.mchange_gua('initialGua', 'nextSHGua', move, bset)
        print 'Result for next '+str(deltah).split(':')[1]+' min : \n'
        print self.__call__(self.elements['nextSHGua'].Name)
        
        
    def guabychannel(self,Channel):
        """prints gua that corresponds to channel"""
        chgua  = {'GB':'Qian','BL':'Qian','LI':'Zhen','ST':'Kan','TB':'Gen','SI':'Gen','KID':'Kun', 'LIV':'Kun','LU':'Xun','Sp':'Li','Ht':'Dui','HG':'Dui'} 
        s = chgua[Channel]
        #print bset.__call__(bset.elements[s].Name)
        return s
    
    def channelbygua(self,Gua):
        """gives channel that corresponds to gua """
        guach  = {'Qian':'GB BL','Zhen':'LI','Kan':'ST','Gen':'TB SI','Kun':'KID LIV','Xun':'LU','Li':'Sp','Dui':'Ht HG'} 
        s = guach[Gua]
        #print bset.__call__(bset.elements[s].Name)
        return s
        
    def channelfr(self,Channel):  
        """returnes french notation for channel """  
        chfr  = {'GB':'VB','BL':'V','LI':'GI','ST':'E','TB':'TR','SI':'IG','KID':'R', 'LIV':'F','LU':'P','Sp':'Rp','Ht':'C','HG':'MC'}
        s = chfr[Channel]
        return s
    
    def channeleng(self,Channel):  
        """returnes english notation for channel """  
        cheng  = {'VB':'GB','V':'BL','GI':'LI','E':'ST','TR':'TB','IG':'SI','R':'KID', 'F':'LIV','P':'LU','Rp':'Sp','C':'Ht','MC':'HG'}
        s = cheng[Channel]
        return s

    def oppchannel(self,Channel):  
        """returns channel opposite to vilality channel"""  
        oppch  = {'GB':'Ht','BL':'LU','LI':'KID','ST':'HG','TB':'Sp','SI':'LIV','KID':'LI', 'LIV':'SI','LU':'BL','Sp':'TB','Ht':'GB','HG':'ST'} 
        s = oppch[Channel]
        return s

    def channellofr(self,Channel):
        """returnes lo point for channel """
        chlo  = {'VB':'37','V':'58','GI':'6','E':'40','TR':'5','IG':'7','R':'4', 'F':'5','P':'7','Rp':'4','C':'5','MC':'6'}
        s = chlo[Channel]
        return s

    def channello(self,Channel):
        """returnes french notation for channel """
        chfr  = {'GB':'37','BL':'58','LI':'6','ST':'40','TB':'5','SI':'7','KID':'4', 'LIV':'5','LU':'7','Sp':'4','Ht':'5','HG':'6'}
        s = chfr[Channel]
        return s





            
            
        
        
        
        
            
        
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
    
