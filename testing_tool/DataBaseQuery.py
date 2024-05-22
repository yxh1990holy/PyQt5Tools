from PyQt5.QtCore import QThread, pyqtSignal
import pymysql
from pymysql.err import OperationalError
from Logger import logger

class DataBaseQuery(QThread):
    '''
    数据库操作类
    '''
    sqlResultSignal = pyqtSignal(tuple, tuple)
    exceptionSignal = pyqtSignal(bool, str)
    def __init__(self, sql=None):
        super(DataBaseQuery, self).__init__()
        self.sql = sql
        logger.info(self.sql)

    def run(self):
        ip = 'bj-cdb-4kqb4cis.sql.tencentcdb.com'
        username = 'xd_dev_mysql'
        password = 'Ycc3lgu1rjc4q8qe'
        database_name = 'data_trace'
        port = 61292
        try:
            conn = pymysql.connect(host=ip, user=username, password=password, database=database_name, port=port, read_timeout=5)
            cursor = conn.cursor()
            cursor.execute(self.sql)
            data = cursor.fetchall()
            desc = cursor.description
            # if len(data) == 0:
            #     logger.info("查询结果为空")
            #     self.exceptionSignal.emit(False, "查询结果为空")
            # else:
            #     self.sqlResultSignal.emit(data, desc)
            self.sqlResultSignal.emit(data, desc)
            conn.close()
            return
        except AttributeError as ae:
            self.exceptionSignal.emit(False, str(ae))
            # print(str(ae))
            logger.info(str(ae))
        except OperationalError as oe:
            # print(str(oe))
            self.exceptionSignal.emit(False, '查询超时')
            logger.info(str(oe))
        except Exception as e:
            self.exceptionSignal.emit(False, str(e))
            # print(str(e))
            logger.info(str(e))
            return