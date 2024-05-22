from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import pyqtSignal

class MyTableWidget(QTableWidget):
    '''
    自定义tableWidget类，使其支持拖拽到表格内上传数据
    '''
    # 更新表格控件信号，当拖拽到表格并释放鼠标后触发该信号，参数为文件路径名
    updateTableSignal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)
        self.setAcceptDrops(True)
    # 设置拖拽文件到该表格，触发该方法
    def dragEnterEvent(self, event):
        self.file_path = event.mimeData().text()
        if '.xls' in self.file_path or ('.xlsx' in self.file_path):
            event.accept()
            # print(self.file_path.replace('file:///', '').replace("/", "\\"))
            self.file_path = self.file_path.replace('file:///', '').replace("/", "\\")
        else:
            event.ignore()
            # print('文件非excel文件')

    def dragMoveEvent(self, event):
        # print("dragMoveEvent")
        event.accept()

    # 注意此方法必须在dragMoveEvent接受后触发
    # 用户释放鼠标按钮时，这个方法会被触发，用于处理拖拽事件
    def dropEvent(self, event):
        # print('释放后触发')
        self.updateTableSignal.emit(self.file_path)