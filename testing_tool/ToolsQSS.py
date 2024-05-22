qss = '''
*{
    font-size:20px;
}
QGroupBox{
	font-size:24px;
}
QPushButton{
    display: inline-block;
    line-height: 1;
    white-space: nowrap;
    cursor: pointer;
    background-color: #409eff;
    border: 1px solid #409eff;
    color: #fff;
    box-sizing: border-box;
    font-weight: 250;
    padding: 12px 15px;
    border-radius: 5px;
}
QLineEdit{
    padding: 12px 15px;
    border: 1px solid black;
    border-radius: 5px;
}
QComboBox{
    padding: 12px 15px;
    border: 1px solid black;
    border-radius: 5px;
}
QComboBox QAbstractItemView::item{
    padding: 12px 15px;
}
/*设置TabWidget中QTabBar的样式*/
QTabBar::tab{
	backgroud-color: #fff;
	color:  #303133;                  /*设置tab中的文本的颜色*/
}
/*设置TabWidget中QTabBar的tab被选中时的样式*/
QTabBar::tab:selected{
    color: #409eff;
    backgroud-color: #fff;
}
/*设置TabWidget中鼠标悬浮在QTabBar的tab上，但未选中该Tab的样式*/
QTabBar::tab:hover:!selected {
    color: #409eff;
    backgroud-color: #fff;
}
'''

'''
QTabBar::tab:#DataTraceToolTab{
	backgroud-color: #ffa522;
	color:  #fff;                  /*设置tab中的文本的颜色 #2BFFA520*/
}
QTabBar#PayToolTab{
	backgroud-color: #2BFF5822;
	color:  #fff;                  /*设置tab中的文本的颜色*/
}
QTabBar#xiaoYiAssistantTab{
	backgroud-color: skyblue;
	color:  #fff;                  /*设置tab中的文本的颜色*/
}
'''



