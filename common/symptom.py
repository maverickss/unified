import re
import MySQLdb
import random
import mysql.connector
import MySQLdb.cursors



#global connection
cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
cursor = cnx.cursor(MySQLdb.cursors.DictCursor)

class Symptom:
    def __init__(self, kb):

        sql = 'SELECT * FROM `symptom` where kbnumber = ' +  str(kb)
        cursor.execute(sql)
        self.data = cursor.fetchall()

        #print self.data
        self.kbnumber = kb
        self.logs = []
        self.keywords = []
        if self.data:
            self.symptomscore = self.data[0][3]
            self.logcount = self.data[0][4]
            self.new = 0
            self.loadLog()
            self.loadKeyword()
        else:
            self.new = 1
            self.logcount = 0
            self.symptomscore = 0
    
    def loadLog(self):
        sql = 'SELECT * FROM `log_symptom2` where kbnumber = ' +  str(self.kbnumber)
        cursor.execute(sql)
        self.data = cursor.fetchall()
        for row in self.data:
          # print row
           self.logs.append({'log':row[1], 'score':float(row[2])})

    def loadKeyword(self):
        sql = 'SELECT * FROM `keyword2_symptom` where kbnumber = ' +  str(self.kbnumber)
        cursor.execute(sql)
        self.data = cursor.fetchall()
        for row in self.data:
          # print row
           self.keywords.append({'keyword':row[1], 'score':float(row[2])})



     
    def addLog(self, log):
        self.logcount = self.logcount + 1
        self.symptomscore = self.symptomscore + log['score']  
        #print log
        sql = 'INSERT INTO `log_symptom2`(`kbnumber`, `log`, `score` ) VALUES (%d, "%s" , %2.8f)' % ( self.kbnumber, log['log'], log['score'])
        print sql
        cursor.execute(sql)
        cnx.commit()
        self.save()

    def getKbnumber(self):
        return self.kbnumber

    def getScore(self):
        return self.score
 
    def getKeywords(self):
        return self.keywords


 
    def getLogs(self):
        return self.logs

    def getKeywordsDemo(self):
        ret = 'name,count\n'
        loop = 0 
        for keyword in self.getKeywords():
            loop = loop + 1
            if loop > 50:
                break
            #if log['score'] < 0.21:
            #    continue
         
            ret = ret + keyword['keyword'] + ',' + str(keyword['score'] * random.randint(1, 10) + 1) + '\n'
        return ret


    def getLogsDemo(self):
        ret = 'name,count\n'
        loop = 0 
        for log in self.getLogs():
            loop = loop + 1
            if loop > 50:
                break
            #if log['score'] < 0.21:
            #    continue
            l = re.sub('[^a-zA-Z _:-]', "", log['log'])
            l = l.strip()
            words = l.split(' ')
            lc = ""
            
            for w in words:
                lc = lc + w + ' '
                if len(lc) > 15:
                    break

                 
            lc.strip()
            if len(lc) > 20:
                lc = lc[0:16] + '...'
         
            ret = ret + lc + ',' + str(log['score'] *100) + '\n'

        return ret
    def hasLog(self,log):
        for l in self.logs:
            if log['log'] == l['log']:
                return True
        return False

    def updateIncreaseLog(self, log):
        for l in self.logs:
            if l['log'] == log['log']:
                l['score'] = l['score'] + log['score']
                self.updateLog(l)

    def updateDecreaseLog(self, log):
        for l in self.logs:
            if l['log'] == log['log']:
                l['score'] = l['score'] - log['score']
                self.updateLog(l)

    def updateLog(self, log):
        sql = 'UPDATE `log_symptom2` SET `score`= %2.8f WHERE kbnumber = "%s" and log = "%s"' % ( log['score'], self.kbnumber, log['log'])
        cursor.execute(sql)
        cnx.commit()
        self.save()
        
        


    def deleteLog(self, log):
   
        sql = 'delete from log_symptom2 where kbnumber = %d and log = "%s"' % ( self.kbnumber, log['log'])
        cursor.execute(sql)
        cnx.commit()
        self.save()
        self.logcount = self.logcount - 1
        self.symptomscore = self.symptomscore - log['score']  

        self.logcount = len(logs)
        self.save()

    def save(self):
        if self.new == 1:
            sql = 'INSERT INTO `symptom`(`kbnumber`, `symptomscore`, `logcount` ) VALUES (%d, %2.8f , %d)' % ( self.kbnumber, self.symptomscore, self.logcount)
        else:
            sql = 'UPDATE symptom SET `kbnumber`= "%d",`symptomscore`=%2.8f, `logcount` = %d WHERE `kbnumber`=%d ' % (self.kbnumber, self.symptomscore, self.logcount, self.kbnumber)
            
        #print sql
        cursor.execute(sql)
        cnx.commit()




if __name__ == "__main__":
    s = Symptom(1017910)

    #log1 = {'log':'test log', 'score':float(0.123)}
    #s.addLog(log1)
    #print s.getLogs()
    #log2 = {'log':'test log2', 'score':float(1.523)}
    #s.addLog(log2)
    #print s.getLogs()
        
    #log = {}
    #log['log'] = 'ToolsBackup: '
    #log['score'] = 0.3
    #print s.hasLog(log)
    #s.updateIncreaseLog(log)
    #print s.getLogs()
    print s.getKeywords()
    print s.getKeywordsDemo()
