import listmysqldatabase
import mysqldumpreturn
import time
import logging
from logging.handlers import RotatingFileHandler


import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
#handler = RotatingFileHandler('sqlbak.log', maxBytes=10*1024*1024,backupCount=5)
handler = logging.FileHandler("sqlbak.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
handler.setFormatter(formatter)
 
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
 
logger.addHandler(handler)
logger.addHandler(console)



'''
Rthandler = RotatingFileHandler('sqlbak.log', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
#logger.addHandler(handler)
#logger.addHandler(console)
'''


if __name__ == '__main__':
    logger.info('app start...')
    host = "10.88.23.199"
    user = "it"
    passwd = "007"
    port = 3306
    db_name = "mysql"

    obj = listmysqldatabase.Mysql(host, user, passwd, port, db_name)
    all_db_list = obj.get_all_db()
    user_power = obj.get_user_power()

    #print("all_db_list",all_db_list)
    #print("user_power",user_power)
    fp = open("dblist.txt","r")
    dblist = fp.readlines()
    for dbname in dblist: 
        dbname = dbname.strip()   
        logger.info(dbname)

        ret = mysqldumpreturn.creatdumpsql(host,user,passwd,dbname,dbname)
        time.sleep(5)
        if ret.returncode == 0:
            logger.info("dump success." )
        else:
            logger.info("dump error:" + dbname)
            logger.info(ret.stderr)
            logger.info(ret.stdout)
