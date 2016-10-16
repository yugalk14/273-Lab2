import logging
import re
import datetime
import collections
import string
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, srpc, ServiceBase, \
    Integer, Unicode
import requests
import request
import json
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

class crime(ServiceBase):
    @srpc(float, float, float, _returns=Unicode)
    def checkcrime(lat,lon,radius):
        URL="https://api.spotcrime.com/crimes.json"
        values={'lat':lat,'lon':lon,'radius':radius,'key':'.'}
        result=requests.get(URL,params=values)
        #yield result.json()
        data=result.json()
        #----------------------Total number crimes-----------------------
        #yield "Total Number of crimes : %s" % len(data["crimes"])

        ####
        totalCrimes=len(data["crimes"])
        #----------------------Most dangerous streets-----------------------
        '''dictionary={}
        for n in range(len(data["crimes"])):
            Type = data["crimes"][n]["address"]
            add = Type.split(" BLOCK ")[-1]
            if not dictionary.has_key(add):
            
                dictionary[Type]=1
            else:
                dictionary[Type]+=1
        #yield dictionary
        #yield sorted(dictionary.values())
        yield "Most Dangerous Streets"
        yield sorted(dictionary,key=dictionary.__getitem__,reverse=True)#[:3]
        '''
        dictionary={}
        for n in data["crimes"]:
            Type = n["address"]
            add = Type.split(" BLOCK ")[-1]
            add=add.split("BLOCK ")[-1]
            add=add.split(" OF ")[-1]
            add=add.split("OF ")[-1]
            if not dictionary.has_key(add):
                dictionary[add]=1
            else:
                dictionary[add]+=1
        #yield dictionary
        #yield sorted(dictionary.values())
        #
        #yield "Most Dangerous Streets"
        #yield sorted(dictionary,key=dictionary.__getitem__,reverse=True)[:3]

        ####
        dangerousStreets=sorted(dictionary,key=dictionary.__getitem__,reverse=True)[:3]
        #yield dangerous
         #----------------------crime types-----------------------
        dictionary={}
        for n in range(len(data["crimes"])):
            Type = (data["crimes"][n]["type"])
            if not dictionary.has_key(Type):
                dictionary[Type]=1
            else:
                dictionary[Type]+=1
        #yield dictionary

        #####
        crimeType=dictionary
        #yield crimeType
        #----------------------crime times-----------------------
        time1=time2=time3=time4=time5=time6=time7=time8=0 #initialising time counters

        date1=datetime.datetime.strptime("12:00 AM","%I:%M %p").time()
        date2=datetime.datetime.strptime("03:00 AM","%I:%M %p").time()
        date3=datetime.datetime.strptime("06:00 AM","%I:%M %p").time()
        date4=datetime.datetime.strptime("09:00 AM","%I:%M %p").time()
        date5=datetime.datetime.strptime("12:00 PM","%I:%M %p").time()
        date6=datetime.datetime.strptime("03:00 PM","%I:%M %p").time()
        date7=datetime.datetime.strptime("06:00 PM","%I:%M %p").time()
        date8=datetime.datetime.strptime("09:00 PM","%I:%M %p").time()
        
        for n in range(len(data["crimes"])):
            dateString=data["crimes"][n]["date"]
            date0=datetime.datetime.strptime(dateString,"%m/%d/%y %I:%M %p").time()
            if date1 < date0 <= date2:
                time1 +=1
            elif date2<date0<=date3:
                time2 +=1
            elif date3<date0<=date4:
                time3 +=1
            elif date4<date0<=date5:
                time4 +=1
            elif date5<date0<=date6:
                time5 +=1
            elif date6<date0<=date7:
                time6 +=1
            elif date7<date0<=date8:
                time7 +=1
            else:
                time8 +=1
        dictionaryTime={"12:01am-3am":time1,"3:01am-6am":time2,"6:01am-9am":time3,"9:01am-12noon":time4,"12:01pm-3pm":time5,"3:01pm-6pm":time6,"6:01pm-9pm":time7,"9:01pm-12midnight":time8}
        #yield dictionaryTime

        dictionaryOutpout={"Total Number of Crimes":totalCrimes,
                            "Most Dangerous Streets":dangerousStreets,
                            "Crime type Count":crimeType,
                            "Event Time Count":dictionaryTime}
        yield dictionaryOutpout
        ''' yield "12:01am-3am",time1
        yield "3:01am-6am",time2
        yield "6:01am-9am",time3
        yield "9:01am-12noon",time4
        yield "12:01pm-3pm",time5
        yield "3:01pm-6pm",time6
        yield "6:01pm-9pm",time7
        yield "9:01pm-12midnight",time8
        '''
        '''
        dictionaryTime={}
        for n in range(len(data["crimes"])):
            dateString=data["crimes"][n]["date"]
            date0=datetime.datetime.strptime(dateString,"%m/%d/%y %I:%M %p").time()
            if date1 < date0 <= date2:
                dictionaryTime[time1] +=1
            elif date2<date0<=date3:
                dictionaryTime[time2] +=1
            elif date3<date0<=date4:
                dictionaryTime[time3] +=1
            elif date4<date0<=date5:
                dictionaryTime[time4] +=1
            elif date5<date0<=date6:
                dictionaryTime[time5] +=1
            elif date6<date0<=date7:
                dictionaryTime[time6] +=1
            elif date7<date0<=date8:
                dictionaryTime[time7] +=1
            else:
                dictionaryTime[time8] +=1
        yield dictionaryTime

        '''
        
        '''
        #yield data["crimes"][1]["cdid"]
        #yield data["crimes"][1]["date"]
       
        arrestCount=0
        burglaryCount=0
        theftCount=0
        robberyCount=0
        assaultCount=0
        othersCount=0

        for n in range(len(data["crimes"])):
            if data["crimes"][n]["type"]=="Assault":
                assaultCount+=1
            elif data["crimes"][n]["type"]=="Arrest":
                arrestCount+=1
            elif data["crimes"][n]["type"]=="Burglary":
                burglaryCount+=1
            elif data["crimes"][n]["type"]=="Robbery":
                robberyCount+=1
            elif data["crimes"][n]["type"]=="Theft":
                theftCount+=1
            elif data["crimes"][n]["type"]=="Other":
                othersCount+=1
        
        yield "Total Number of crimes : %s" % len(data["crimes"])
        yield "Crime type counts :"
        yield "Assualt : %s" % assaultCount
        yield "Arrest : %s" % arrestCount
        yield "Burglary : %s" % burglaryCount
        yield "Robbery : %s" % robberyCount
        yield "Theft : %s" % theftCount
        yield "Other : %s" % othersCount

        cnt=collections.Counter()
        for n in range(len(data["crimes"])):
            for word in (data["crimes"][n]["type"]):
                cnt[word] += 1
        yield cnt
        pattern = '11:00 AM'
        ct = 0
        #n=0
        for n in range(len(data["crimes"])):
            for match in re.findall(pattern,str(data["crimes"][n]["date"])):
                ct += 1              
        yield ct'''


application = Application([crime],
    tns='spyne.google',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=JsonDocument()
)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 5000, wsgi_app)
    server.serve_forever()