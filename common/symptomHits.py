import re
import MySQLdb
import mysql.connector
import MySQLdb.cursors
import sys
import json
sys.path.append('..')

from dataScripts.kb.webpage import IKBPage


class SymptomHits:
    def __init__(self):

        global cnx
        cnx = mysql.connector.connect(user='root',password='vmware', database='unified')

        global cursor
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
    
    def topHits(self):
        sql = 'select kbnumber,  sum(hits) as total from symptom_hits group by kbnumber ORDER by total DESC'
        cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
        for row in data:
          # print row
           ret.append({'kbnumber':row[0], 'hits':row[1]})
        return ret

    def hit(self, kbnumber):
        sql = 'INSERT INTO `symptom_hits`(`kbnumber`, `hits` ) VALUES (%d, 1)' % ( kbnumber)
        print sql
        cursor.execute(sql)
        cnx.commit()

    def getHits(self, kbnumber):
        sql = 'select sum(hits) from symptom_hits where kbnumber = %d' % kbnumber
        cursor.execute(sql)
        data = cursor.fetchall()
          # print row
        return data[0][0]
  
    def topHitsFull(self):
        kbs = self.topHits()
        jret = []
        
        for kb in kbs:
            try:
                page = IKBPage('/data/data/kbraw/data/%s' % kb['kbnumber'])
                j = dict()
                j['url'] = 'http://kb.vmware.com/kb/%d' % kb['kbnumber']
                j['title'] = page.get_title()
                j['text'] = page.get_text()[0:300] + '...'
                #j['text'] = 'aaaaaa'
                j['hits'] = str(kb['hits']) + ' hits'
        
                jret.append(j)
            except:
                pass
        jret = jret[0:10]
        return jret
        #print j







if __name__ == "__main__":
    s = SymptomHits()
    s.hit(1009484)
    s.hit(1031636)
    s.hit(1005266)   
    s.hit(2101938)   
    s.hit(2101938)   
    print s.topHits()

    print s.topHitsFull()
    print json.dumps(s.topHitsFull())
        