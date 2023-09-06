from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QComboBox
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import pandas as pd
import numpy as np
import requests
import pymysql
from data_trace_tool_ui import Ui_MainWindow
from threading import Thread


class DataTraceTool(QMainWindow, Ui_MainWindow):
    signal = pyqtSignal(bool,str)

    def __init__(self):
        super().__init__()
        # self = uic.loadUi("ui//data_trace_tool.ui")
        # self = Ui_MainWindow()
        self.setupUi(self)
        # 充值窗口大小为屏幕的比例
        # 获取显示器分辨率
        self.screenRect = QtWidgets.QApplication.desktop().screenGeometry()
        self.resize(3 * self.screenRect.width() / 5, 3 * self.screenRect.height() / 5)
        self.user_id = None
        self.prevRow = -1
        self.action_key_num = 0
        self.page_key_num = 0

        self.ipLineEdit.setText("bj-cdb-4kqb4cis.sql.tencentcdb.com")
        self.portLineEdit.setText("61292")
        self.dataBaseNameLineEdit.setText("data_trace")
        self.userNameLineEdit.setText("xd_dev_mysql")
        self.dataBasePasswordLineEdit.setText("Ycc3lgu1rjc4q8qe")
        self.comboBox.currentIndexChanged.connect(self.handleSelectionChange)
        self.uploadFileButton.clicked.connect(self.openfile)
        self.uploadFileButton.clicked.connect(self.creat_table_show)
        self.tableWidget.itemClicked.connect(self.show_sql)
        self.getUserIdButton.clicked.connect(self.get_user_id)
        self.testConnectPushButton.clicked.connect(self.test_database_connect)
        self.SQLPushButton.clicked.connect(self.get_result)

    def show_message(self, flag=None, message=None):
        if flag:
            QMessageBox.information(None, "成功", message)
        else:
            QMessageBox.critical(None, "失败", message)

    def handleSelectionChange(self):
        self.userIdLineEdit.clear()
        self.user_id = None
        # self.passwordLineEdit.clear()
        if self.comboBox.currentText() == 'APP用户请输入user_id':
            self.getUserIdButton.setEnabled(False)
        else:
            self.getUserIdButton.setEnabled(True)

    def openfile(self):
        # 获取路径
        openfile_name = QFileDialog.getOpenFileName(None,'选择文件','','Excel files(*.xlsx , *.xls)')
        #print(openfile_name)
        global path_openfile_name
        # 获取路径
        path_openfile_name = openfile_name[0]

    def creat_table_show(self):
        # 读取表格，转换表格
        if len(path_openfile_name) > 0:
            input_table = pd.read_excel(path_openfile_name,keep_default_na=False)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]+1
            input_table_header = input_table.columns.values.tolist()
            # from openpyxl import load_workbook
            # wb = load_workbook(path_openfile_name,read_only=True)
            # ws = wb.sheet
            input_table_header.insert(0,"测试结果")
            # 获取上传表格中的page_key和action_key的列数
            self.page_key_num = input_table_header.index("page_key")
            self.action_key_num = input_table_header.index("action_key")
            self.actionKeyLineEdit.setText(str(self.action_key_num))
            self.pageKeyLineEdit.setText(str(self.page_key_num))
            # 给tablewidget设置行列表头
            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)
            for column_num in range(input_table_colunms):
                head_item = self.tableWidget.horizontalHeaderItem(column_num)
                head_item.setFont(QFont("宋体",12,QFont.Bold))
                head_item.setBackground(QBrush(QColor(192, 192, 192)))
                # 设置字体颜色为白色
                head_item.setForeground(QBrush(QColor(255,255,255)))
            # 遍历表格每个元素，同时添加到tablewidget中
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                comBox = QComboBox()
                comBox.addItems(['成功', '失败'])
                comBox.setCurrentIndex(-1)
                self.tableWidget.setCellWidget(i, 0, comBox)
                for j in range(1,input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j-1]
                    # 将遍历的元素添加到tablewidget中并显示
                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setFlags(Qt.ItemIsEnabled)
                    newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, newItem)

    def show_sql(self, Item=None):
        self.action_key_num = self.actionKeyLineEdit.text()
        self.page_key_num = self.pageKeyLineEdit.text()
        if self.comboBox.currentText() == 'APP用户请输入user_id':
            self.user_id = self.userIdLineEdit.text().strip()
        if (self.user_id is None) or (len(self.user_id)==0):
            QMessageBox.critical(None, '错误', '请先获取user_id')
            return
        else:
            if Item is None:
                return
            else:
                if self.prevRow != -1:
                    for i in range(1, self.tableWidget.columnCount()):
                        self.tableWidget.item(self.prevRow,i).setBackground(QColor(255,255,255))
                row = Item.row()
                for i in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(row,i).setBackground(QColor(240,255,255))
                self.sqlShowTextEdit.setText("SELECT * FROM data_trace.t_action_info WHERE  1 "
                                                    +"\n  AND user_id = '"+self.user_id
                                                    +"'\n  AND page_key = '"+self.tableWidget.item(row, int(self.page_key_num)).text()
                                                    +"'\n  AND action_key = '"+self.tableWidget.item(row, int(self.action_key_num)).text()
                                                    +"'\n  AND DATE_FORMAT(action_time,'%y-%M-%d') = DATE_FORMAT(now(),'%y-%M-%d') "
                                                    +"\nORDER BY action_time DESC limit 10;")
                self.prevRow = row
                self.get_result()

    def get_user_id(self):
        choice = self.comboBox.currentText().strip()
        user263 = self.userIdLineEdit.text().strip()
        web_header = {
            "Content-Type": "application/json;charset=UTF-8"            
        }
        web_url = "https://test_model-cloud-bf.dayustudy.com/inner/inner/getUserInfo"
        web_param = {
            "userName": user263,
            "systemType": 2
        }
        if len(user263) == 0:
            QMessageBox.critical(None, '错误', '请输入263点击获取user_id或直接输入APP中的user_id')
            return
        else:
            if choice=="大鱼或企微用户263":
                try:
                    resp = requests.get(url=web_url, params=web_param, headers=web_header)
                except Exception as e:
                    QMessageBox.critical(None, '请求异常', str(e))
                else:
                    self.user_id = str(resp.json().get("data").get("userId"))
            elif choice=="APP用户手机号":
                self.user_id = user263
            if self.user_id is not None:
                QMessageBox.information(None, '获取成功', 'user_id为'+self.user_id)
            else:
                QMessageBox.critical( None, '错误','user_id获取失败！')
                return

    def test_database_connect(self):
        ip = self.ipLineEdit.text()
        port = int(self.portLineEdit.text().strip())
        database_name = self.dataBaseNameLineEdit.text()
        username = self.userNameLineEdit.text()
        password = self.dataBasePasswordLineEdit.text()
        # 创建新的线程去执行测试链接数据库方法，
        # 服务器慢，只会在新线程中阻塞
        # 不影响主线程
        thread = Thread(target=self.test_connect_thread, args=(ip, username, password, database_name, port))
        thread.start()

    def test_connect_thread(self, ip, username, password, database_name, port):
        try:
            conn = pymysql.connect(host=ip, user=username, password=password, database=database_name, port=port)
            self.signal.emit(True, "数据库连接成功")
            conn.close()
            return
        except Exception as e:
            self.signal.emit(False, str(e))
            return

    def get_result(self):
        ip = self.ipLineEdit.text().strip()
        port = int(self.portLineEdit.text().strip())
        database_name = self.dataBaseNameLineEdit.text().strip()
        username = self.userNameLineEdit.text().strip()
        password = self.dataBasePasswordLineEdit.text().strip()
        sql = self.sqlShowTextEdit.toPlainText().strip()
        thread = Thread(target=self.get_result_thread, args=(ip, username, password, database_name, port, sql))
        thread.start()

    def get_result_thread(self, ip, username, password, database_name, port, sql):
        try:
            conn = pymysql.connect(host=ip, user=username, password=password, database=database_name, port=port)
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            desc = cursor.description
            table_header = [item[0] for item in desc]
            self.statusbar.showMessage("共查询到%d条埋点数据" %(len(data)))
            model = QStandardItemModel(len(data), len(desc))
            model.setHorizontalHeaderLabels(table_header)
            for column_num in range(len(desc)):
                head_item = model.horizontalHeaderItem(column_num)
                head_item.setFont(QFont("宋体",12,QFont.Bold))
                head_item.setBackground(QBrush(QColor(192, 192, 192)))
                # 设置字体颜色为黑色
                head_item.setForeground(QBrush(QColor(255,255,255)))
            for row in range(len(data)):
                for column in range(len(desc)):
                    item = QStandardItem(str(data[row][column]))
                    model.setItem(row, column, item)
            self.tableView.setModel(model)
            conn.close()
            return
        except AttributeError as ae:
            self.signal.emit(False,str(ae))
        except Exception as e:
            self.signal.emit(False, str(e))
            return

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("tool.ico"))
    # 读取样式表
    with open("data_trace_tool.qss", "r") as f:
        app.setStyleSheet(f.read())
    dataTraceTool = DataTraceTool()
    dataTraceTool.signal.connect(dataTraceTool.show_message)
    dataTraceTool.show()
    # 设置程序运行样式为融合风格，不然表头背景色不会生效
    app.setStyle(QtWidgets.QStyleFactory.create('fusion'))
    app.exec_()
