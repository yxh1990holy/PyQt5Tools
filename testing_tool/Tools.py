import sys, openpyxl, ToolIco
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidgetItem, QStyleFactory, QFileDialog, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QBrush, QColor, QIcon
from ToolsUI import Ui_MainWindow
from MyTableWidget import MyTableWidget
from DataBaseQuery import DataBaseQuery
from MyRequest import HTTPThread
from ToolsQSS import qss
from Logger import logger
from PyQt5 import QtWidgets, QtCore


class Tools(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Tools, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.initSignalAndSlot()
        self.currentRowNum = -1     # 设置当前点击表格的行初始值

    def initUI(self):
        logger.info('初始化UI')
        self.setWindowIcon(QIcon(':tool.ico'))
        screenRect = QApplication.desktop().screenGeometry()
        self.resize(3 * screenRect.width() / 5, 3 * screenRect.height() / 5)
        # 添加自定义tableWidget，支持拖拽
        self.dataTraceTableWidget = MyTableWidget(self.uploadFileGroupBox)
        self.dataTraceTableWidget.setObjectName("dataTraceTableWidget")
        self.dataTraceTableWidget.setColumnCount(0)
        self.dataTraceTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.dataTraceTableWidget)
        self.initXiaoYiAssistantUI()
        # self.orderStatusLabel.setVisible(False)

    def initXiaoYiAssistantUI(self):
        logger.info('开始隐藏小易助手中不显示部分')
        self.toConsultOrderNoLabel.setVisible(False)
        self.toConsultOrderLineEdit.setVisible(False)
        self.hide_widget(self.horizontalLayout_12)
        self.hide_widget(self.horizontalLayout_13)
        self.hide_widget(self.horizontalLayout_15)
        self.hide_widget(self.horizontalLayout_16)
        self.hide_widget(self.horizontalLayout_17)

    def initSignalAndSlot(self):
        self.dataTraceTableWidget.updateTableSignal.connect(self.updateTableWidget)
        self.uploadFileBtn.clicked.connect(self.uploadFile)
        self.dataTraceTableWidget.itemClicked.connect(self.assembleSQLAndQuery)
        self.queryBtn.clicked.connect(self.queryData)
        # self.payBtn.clicked.connect(self.pay)
        # self.getOrderNoBtn.clicked.connect(self.getLatestOrderNo)
        self.sendBtn.clicked.connect(self.xiaoYiAssistantTool)
        self.assistantTypeComboBox.currentTextChanged.connect(self.updateAssistantToolUi)
        self.tabWidget.currentChanged.connect(self.initTabUI)

    def initTabUI(self):
        print(self.tabWidget)
        if self.tabWidget.currentIndex() == 1:
            self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.PayToolTab)
            self.horizontalLayout_9.setObjectName("horizontalLayout_9")
            self.verticalLayout_6 = QtWidgets.QVBoxLayout()
            self.verticalLayout_6.setObjectName("verticalLayout_6")
            self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_7.setObjectName("horizontalLayout_7")
            self.orderNoLabel = QtWidgets.QLabel(self.PayToolTab)
            self.orderNoLabel.setObjectName("orderNoLabel")
            self.horizontalLayout_7.addWidget(self.orderNoLabel)
            self.orderNoLineEdit = QtWidgets.QLineEdit(self.PayToolTab)
            self.orderNoLineEdit.setObjectName("orderNoLineEdit")
            self.horizontalLayout_7.addWidget(self.orderNoLineEdit)
            self.orderStatusLabel = QtWidgets.QLabel(self.PayToolTab)
            self.orderStatusLabel.setEnabled(True)
            self.orderStatusLabel.setObjectName("orderStatusLabel")
            self.horizontalLayout_7.addWidget(self.orderStatusLabel)
            spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout_7.addItem(spacerItem1)
            self.getOrderNoBtn = QtWidgets.QPushButton(self.PayToolTab)
            self.getOrderNoBtn.setObjectName("getOrderNoBtn")
            self.horizontalLayout_7.addWidget(self.getOrderNoBtn)
            self.horizontalLayout_7.setStretch(0, 1)
            self.horizontalLayout_7.setStretch(1, 2)
            self.horizontalLayout_7.setStretch(2, 2)
            self.horizontalLayout_7.setStretch(3, 4)
            self.horizontalLayout_7.setStretch(4, 1)
            self.verticalLayout_6.addLayout(self.horizontalLayout_7)
            self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_8.setObjectName("horizontalLayout_8")
            self.label_4 = QtWidgets.QLabel(self.PayToolTab)
            self.label_4.setObjectName("label_4")
            self.horizontalLayout_8.addWidget(self.label_4)
            self.paidAmountLineEdit = QtWidgets.QLineEdit(self.PayToolTab)
            self.paidAmountLineEdit.setObjectName("paidAmountLineEdit")
            self.horizontalLayout_8.addWidget(self.paidAmountLineEdit)
            self.label_5 = QtWidgets.QLabel(self.PayToolTab)
            self.label_5.setObjectName("label_5")
            self.horizontalLayout_8.addWidget(self.label_5)
            self.horizontalLayout_8.setStretch(0, 1)
            self.horizontalLayout_8.setStretch(1, 2)
            self.horizontalLayout_8.setStretch(2, 7)
            self.verticalLayout_6.addLayout(self.horizontalLayout_8)
            self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_6.setObjectName("horizontalLayout_6")
            self.payBtn = QtWidgets.QPushButton(self.PayToolTab)
            self.payBtn.setObjectName("payBtn")
            self.horizontalLayout_6.addWidget(self.payBtn)
            spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout_6.addItem(spacerItem2)
            self.horizontalLayout_6.setStretch(0, 1)
            self.horizontalLayout_6.setStretch(1, 9)
            self.verticalLayout_6.addLayout(self.horizontalLayout_6)
            self.resultTextBrowser = QtWidgets.QTextBrowser(self.PayToolTab)
            self.resultTextBrowser.setObjectName("resultTextBrowser")
            self.verticalLayout_6.addWidget(self.resultTextBrowser)
            self.verticalLayout_6.setStretch(0, 1)
            self.verticalLayout_6.setStretch(1, 1)
            self.verticalLayout_6.setStretch(2, 1)
            self.verticalLayout_6.setStretch(3, 7)
            self.horizontalLayout_9.addLayout(self.verticalLayout_6)
            _translate = QtCore.QCoreApplication.translate
            self.orderNoLabel.setText(_translate("MainWindow", "订单号："))
            self.orderStatusLabel.setText(_translate("MainWindow", "当前订单状态："))
            self.getOrderNoBtn.setText(_translate("MainWindow", "获取最新订单号"))
            self.label_4.setText(_translate("MainWindow", "金额："))
            self.label_5.setText(_translate("MainWindow", "金额以分为单位，其他单位需要自己转成分"))
            self.payBtn.setText(_translate("MainWindow", "支付"))
            self.orderStatusLabel.setVisible(False)

            self.payBtn.clicked.connect(self.pay)
            self.getOrderNoBtn.clicked.connect(self.getLatestOrderNo)

    # 上传数据后更新tableWidget
    def updateTableWidget(self, file_path):
        # 读取表格，转换表格
        if len(file_path) > 0:
            wb =  openpyxl.load_workbook(file_path)
            ws = wb.active
            # 获取行数和列数
            rows = ws.max_row
            cols = ws.max_column
            # tablewidget设置行数和列数
            self.dataTraceTableWidget.setRowCount(rows-1)    # 注意行数要减掉表头
            self.dataTraceTableWidget.setColumnCount(cols+1) # 注意列数要加上左侧增加的1列
            # 获取表头数据
            table_data = []
            for row in ws.iter_rows(min_row=1, max_col=cols, max_row=rows, values_only=True):
                table_data.append(list(row))
            table_head_data = table_data[0]
            table_head_data.insert(0, "测试结果")
            self.dataTraceTableWidget.setHorizontalHeaderLabels(table_head_data)
            for column_num in range(cols+1):
                head_item = self.dataTraceTableWidget.horizontalHeaderItem(column_num)
                head_item.setFont(QFont("宋体", 12, QFont.Bold))
                head_item.setBackground(QBrush(QColor(192, 192, 192)))
                # 设置字体颜色为白色
                head_item.setForeground(QBrush(QColor(255, 255, 255)))
            # 遍历表格每个元素，同时添加到tablewidget中
            for i in range(0, rows-1):
                comBox = QComboBox()
                comBox.addItems(['成功', '失败'])
                comBox.setCurrentIndex(-1)
                self.dataTraceTableWidget.setCellWidget(i, 0, comBox)
                for j in range(0, cols):
                    # 将遍历的元素添加到tablewidget中并显示
                    newItem = QTableWidgetItem('' if table_data[i+1][j] is None else str(table_data[i+1][j]))
                    newItem.setFlags(Qt.ItemIsEnabled)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.dataTraceTableWidget.setItem(i, j+1, newItem)
            # 获取上传表格中的page_key和action_key的列数
            self.pageKeyLineEdit.setText(str(table_head_data.index("page_key")))
            self.actionKeyLineEdit.setText(str(table_head_data.index("action_key")))

    def uploadFile(self):
        # 获取路径
        file_names = QFileDialog.getOpenFileName(None, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        # 获取路径
        file_path = file_names[0]
        if len(file_path) > 0:
            self.updateTableWidget(file_path)

    def assembleSQLAndQuery(self, item=None):
        if item is None:
            logger.info('item为空')
            return
        else:
            if self.currentRowNum != -1:
                for i in range(1, self.dataTraceTableWidget.columnCount()):
                    self.dataTraceTableWidget.item(self.currentRowNum,i).setBackground(QColor(255,255,255))
            # 获取被点击的行数
            rowNum = item.row()
            # 设置点击所在行的背景色
            for i in range(1, self.dataTraceTableWidget.columnCount()):
                self.dataTraceTableWidget.item(rowNum,i).setBackground(QColor(240,255,255))
            user_id = self.userIdLineEdit.text().strip().replace('，',',')
            action_key = self.dataTraceTableWidget.item(rowNum, int(self.actionKeyLineEdit.text().strip())).text()
            page_key = self.dataTraceTableWidget.item(rowNum, int(self.pageKeyLineEdit.text().strip())).text()
            sql_text = 'SELECT * FROM data_trace.t_action_info WHERE  1'
            if user_id is not '':
                sql_text += '\nAND user_id in ("%s")' %user_id
            sql_text = sql_text + '\nAND page_key = "%s" \nAND action_key = "%s"' %(page_key, action_key)
            sql_text += '\nAND DATE_FORMAT(action_time,"%y-%M-%d") = DATE_FORMAT(now(),"%y-%M-%d")\nORDER BY action_time DESC limit 10;'
            self.sqlTextEdit.setText(sql_text)
            self.currentRowNum = rowNum
            self.queryData()

    def queryData(self):
        # print('开始查询数据')
        sql_text = self.sqlTextEdit.toPlainText()
        # 线程类实例化时变量是 self.thread_1 一定要加上self，
        # 如果不加，thread_1就是一个局部变量，当其所在方法运行结束的时候，它的生命周期也都结束了，
        # 但是这个线程里的程序很有可能还没有运行完！可能会报错：QThread ：Destroyed while thread is still running！
        self.dataBaseQuery = DataBaseQuery(sql_text)
        self.dataBaseQuery.sqlResultSignal.connect(self.updateResultTableWidget)
        self.dataBaseQuery.exceptionSignal.connect(self.show_message)
        self.dataBaseQuery.start()

    def updateResultTableWidget(self, tableData, tablHeader):
        self.statusbar.showMessage("共查询到%d条埋点数据" %(len(tableData)))
        tablHeaderData= [item[0] for item in tablHeader]
        # tablewidget设置行数和列数
        self.resultTableWidget.setRowCount(len(tableData))
        self.resultTableWidget.setColumnCount(len(tablHeaderData))
        # 设置表头
        self.resultTableWidget.setHorizontalHeaderLabels(tablHeaderData)
        # 表头颜色设置
        for column_num in range(len(tablHeaderData)):
            head_item = self.resultTableWidget.horizontalHeaderItem(column_num)
            head_item.setFont(QFont("宋体", 12, QFont.Bold))
            head_item.setBackground(QBrush(QColor(192, 192, 192)))
            # 设置字体颜色为白色
            head_item.setForeground(QBrush(QColor(255, 255, 255)))
        # 设置表格数据
        for row in range(len(tableData)):
            for column in range(len(tablHeaderData)):
                newItem = QTableWidgetItem(str(tableData[row][column]))
                newItem.setFlags(Qt.ItemIsEnabled)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.resultTableWidget.setItem(row, column , newItem)

    def pay(self):
        logger.info('订单号：%s；订单金额：%s' %(self.orderNoLineEdit.text().strip(),self.paidAmountLineEdit.text().strip()))
        if len(self.orderNoLineEdit.text().strip())==0 or len(self.paidAmountLineEdit.text().strip())==0:
            self.show_message(False, '订单号和订单金额不能为空')
            return
        url = 'http://mall-gateway-test.dayustudy.com/order_api/pay/manual/notify/order'
        method = 'post'
        data = {
            'orderNo': self.orderNoLineEdit.text().strip(),
            'paidAmount': int(self.paidAmountLineEdit.text().strip())
        }
        header = {
            'content-type': 'application/json;charset=UTF-8'
        }
        self.httpthread = HTTPThread(url=url, method=method, data=data, headers=header)
        self.httpthread.respSignal.connect(self.updateHttpResult)
        self.httpthread.start()

    def updateHttpResult(self, resp):
        self.resultTextBrowser.append('响应信息：')
        self.resultTextBrowser.append(resp)
        # 查询结果并更新订单状态
        orderNo = self.orderNoLineEdit.text().strip()
        logger.info('支付订单号为：%s' % orderNo)
        self.dataBaseQuery = DataBaseQuery(
            'select order_status from sd_minimall.sd_order where order_no="%s" order by create_time desc limit 1;' % orderNo)
        self.dataBaseQuery.sqlResultSignal.connect(self.updateOrderStatus)
        self.dataBaseQuery.exceptionSignal.connect(self.show_message)
        self.dataBaseQuery.start()

    def updateOrderStatus(self, tableData, tableHeader):
        if len(tableData) == 0:
            logger.info("查询结果为空")
            self.exceptionSignal.emit(False, "查询结果为空")
            return
        order_status = tableData[0][0]
        logger.info('订单状态为：%s' % str(order_status))
        if str(order_status) == 'COMPLETE':
            self.orderStatusLabel.setText('<b>当前订单状态：<font color="green">' + str(order_status) + '</font></b>')
        elif str(order_status) == 'UNPAID':
            self.orderStatusLabel.setText('<b>当前订单状态：<font color="red">' + str(order_status) + '</font></b>')
        else:
            self.orderStatusLabel.setText('<b>当前订单状态：<font color="yellow">' + str(order_status) + '</font></b>')
        self.orderStatusLabel.setVisible(True)

    def getLatestOrderNo(self):
        # 这里不知道为什么要加self，不加self就无法使用
        self.dataBaseQuery = DataBaseQuery(
            'select order_no,receivable_amount,order_status from sd_minimall.sd_order where order_status="UNPAID" order by create_time desc limit 1;')
        self.dataBaseQuery.sqlResultSignal.connect(self.updateOrderNoLineEdit)
        self.dataBaseQuery.exceptionSignal.connect(self.show_message)
        self.dataBaseQuery.start()

    # 获取订单后更新订单号输入框
    def updateOrderNoLineEdit(self, tableData, tableHeader):
        if len(tableData) == 0:
            logger.info("查询结果为空")
            self.show_message(False, '不存在未支付的订单，请重新查询')
            return
        orderNo = tableData[0][0]
        receivableAmount = str(int(tableData[0][1]*100))
        order_status = tableData[0][2]
        self.orderNoLineEdit.setText(orderNo)
        self.paidAmountLineEdit.setText(receivableAmount)
        self.orderStatusLabel.setText('<b>当前订单状态：<font color="red">'+str(order_status)+'</font></b>')
        self.orderStatusLabel.setVisible(True)

    def updateAssistantToolUi(self):
        if self.assistantTypeComboBox.currentIndex() == 0:
            self.couponIdLabel.setVisible(True)
            self.couponIdLineEdit.setVisible(True)
            self.toConsultOrderNoLabel.setVisible(False)
            self.toConsultOrderLineEdit.setVisible(False)
            self.initXiaoYiAssistantUI()
        elif self.assistantTypeComboBox.currentIndex() == 1:
            self.couponIdLabel.setVisible(False)
            self.couponIdLineEdit.setVisible(False)
            self.hide_widget(self.horizontalLayout_12)
            self.hide_widget(self.horizontalLayout_13)
            self.hide_widget(self.horizontalLayout_15)
            self.hide_widget(self.horizontalLayout_16)
            self.hide_widget(self.horizontalLayout_17)
        elif self.assistantTypeComboBox.currentIndex() == 2:
            self.couponIdLabel.setVisible(False)
            self.couponIdLineEdit.setVisible(False)
            self.show_widget(self.horizontalLayout_12)
            self.show_widget(self.horizontalLayout_13)
            self.show_widget(self.horizontalLayout_15)
            self.show_widget(self.horizontalLayout_16)
            self.show_widget(self.horizontalLayout_17)
        elif self.assistantTypeComboBox.currentIndex() == 3:
            self.couponIdLabel.setVisible(False)
            self.couponIdLineEdit.setVisible(False)
            self.show_widget(self.horizontalLayout_12)
            self.show_widget(self.horizontalLayout_13)
            self.show_widget(self.horizontalLayout_15)
            self.show_widget(self.horizontalLayout_16)
            self.show_widget(self.horizontalLayout_17)
        elif self.assistantTypeComboBox.currentIndex() == 4:
            self.couponIdLabel.setVisible(False)
            self.couponIdLineEdit.setVisible(False)
            self.show_widget(self.horizontalLayout_12)
            self.show_widget(self.horizontalLayout_13)
            self.show_widget(self.horizontalLayout_15)
            self.show_widget(self.horizontalLayout_16)
            self.show_widget(self.horizontalLayout_17)
        elif self.assistantTypeComboBox.currentIndex() == 5:
            self.couponIdLabel.setVisible(False)
            self.couponIdLineEdit.setVisible(False)
            self.toConsultOrderNoLabel.setVisible(True)
            self.toConsultOrderLineEdit.setVisible(True)
            self.hide_widget(self.horizontalLayout_12)
            self.hide_widget(self.horizontalLayout_13)
            self.hide_widget(self.horizontalLayout_15)
            self.hide_widget(self.horizontalLayout_16)
            self.hide_widget(self.horizontalLayout_17)

    # 显示布局下所有组件
    def show_widget(self, layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(True)

    # 隐藏布局下所有组件
    def hide_widget(self, layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(False)

    def xiaoYiAssistantTool(self):
        url = 'http://mall-gateway-test.dayustudy.com'
        method = 'post'
        header = {
            'content-type': 'application/json;charset=UTF-8'
        }
        if self.assistantTypeComboBox.currentIndex() == 0:
            url += '/miniMallFreeStudy/userOperate/sendCoupon'
            data = {
                "appId": "wxf0dfe3125ef9a4fd",
                "brandId": 22,
                "couponId": self.couponIdLineEdit.text().strip(),
                "operator": "yuanxihui",
                "assistUserId": 800106383,
                "userIdList": self.toUserIdListLineEdit.text().strip().replace('，',',').split(',')
            }
        elif self.assistantTypeComboBox.currentIndex() == 1:
            url += '/miniMallFreeStudy/consultClient/sendEvaluateCardByUserList'
            data = {
                "brandId": 22,
                "userIdList": self.toUserIdListLineEdit.text().strip().replace('，',',').split(',')
            }
        elif self.assistantTypeComboBox.currentIndex() == 2:
            url += '/tencentApi/imUserMsg/sendCustomerMsg'
            data = {
                "brandId": 22,
                "fromUserId": 800106383,
                "toUserIdList": [int(self.toUserIdListLineEdit.text().strip())],
                "templateCode": "custom.all",
                "param": {
                    "type": "act_01",
                    "actTitle": "福利中心！！！你敢充，我敢送，首次充值，超值特惠！每人仅限一次机会",
                    "actPic": "https://sfs-public.shangdejigou.cn/sunlands_back_freestudy/c9790906abff47aeae61fbed7ce4781c.png",
                    "actButtonText": "点击进入查看详情>>",
                    "directCode": "inner",
                    "innerPageH5Path": "/WelfareCenterPage",
                    # // 福利中心：/WelfareCenterPage;
                    # // 直播间：/VoiceRoomPage?liveId=1212;
                    # // 咨询师主页：/ConsultInfoPage?userId=800105506;
                    # // 易云课堂：/YYClassroomPage;
                    # // 签到活动：/SignInPage
                    # // 帖子详情：/PostDetailPage?taskId=1777510&isVideoPost=false；isVideoPost=true视频贴  isVideoPost=false文本帖子
                    # // /PostDetailPage?taskId=1777514&isVideoPost=true
                    "innerPageAppPath": "/WelfareCenterPage",
                    "innerPageMiniAppPath": "/pages/welfare/index"
                }
            }
        elif self.assistantTypeComboBox.currentIndex() == 3:
            pass
        elif self.assistantTypeComboBox.currentIndex() == 4:
            url += '/tencentApi/imUserMsg/sendCustomerMsg'
            data = {
                "brandId": 22,
                "fromUserId": 800106383,
                "toUserIdList": self.toUserIdListLineEdit.text().strip().replace('，',',').split(','),
                "templateCode": "custom.all",
                "param": {
                    "type": "toWechat",
                    "actTitle": "添加小助手微信",
                    "actSubTitle": "为你提供真人1对1定制服务",
                    "actPic": "https://sfs-public.shangdejigou.cn/sunlands_back_freestudy/8df9bcd3ba124772aa32431c3f7e4cb9.png",
                    "actButtonText": "立即添加",
                    "secChannelCode": "IM_WECHAT_API"
                }
            }
        elif self.assistantTypeComboBox.currentIndex() == 5 :
            url += '/miniMallFreeStudy/consultOrder/allotConsult'
            data = {
                "orderNo": self.toConsultOrderLineEdit.text().strip(),
                "consultUserId": int(self.toUserIdListLineEdit.text().strip())
            }
        self.httpthread = HTTPThread(url=url, method=method, data=data, headers=header)
        self.httpthread.respSignal.connect(self.updateResult)
        self.httpthread.start()

    def updateResult(self, resp):
        self.textBrowser_2.append('响应信息：')
        self.textBrowser_2.append(resp)

    def show_message(self, flag=None, message=None):
        if flag:
            QMessageBox.information(None, "成功", message)
        else:
            QMessageBox.critical(None, "失败", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":tool.ico"))
    app.setStyleSheet(qss)
    main = Tools()
    main.show()
    # 设置程序运行样式为融合风格，不然表头背景色不会生效
    app.setStyle(QStyleFactory.create('fusion'))
    sys.exit(app.exec_())
