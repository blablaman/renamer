# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QWidget,QTableView,QAbstractItemView,QVBoxLayout,QHeaderView,QStyleOptionButton,QStyle,QPushButton,QHBoxLayout,QFileDialog,QStyledItemDelegate,QComboBox,QStyleOptionComboBox,QItemDelegate,QStatusBar
from PyQt5.QtCore import QAbstractTableModel,Qt,QVariant
import sys, os, operator, requests
from lxml import html
import pickle
import greq

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, owner):
        super(ComboBoxDelegate, self).__init__(owner)
        #self.items = items
    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
	print index.data(Qt.EditRole)
        self.editor.addItems(index.model().data(index,Qt.EditRole))
        return self.editor
    #def paint(self, painter, option, index):
    #    value = index.model().data(index,QtCore.Qt.DisplayRole)
    #    style = QApplication.style()
    #    opt = QStyleOptionComboBox()
    #    opt.text = str(value)
    #    opt.rect = option.rect
    #    style.drawComplexControl(QStyle.CC_ComboBox, opt, painter)
    #    QItemDelegate.paint(self, painter, option, index)
    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        #num = self.items.index(value)
	if len(value):
		eindex = index.model().index(index.row(),4) 
		editor.setCurrentIndex(eindex.data(Qt.DisplayRole))
		editor.showPopup()
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index.model().index(index.row(),4), editor.currentIndex(), Qt.EditRole)
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class CheckBoxHeader(QHeaderView):
    clicked=QtCore.pyqtSignal(bool)

    def __init__(self,orientation=QtCore.Qt.Horizontal,parent=None):
        super(CheckBoxHeader,self).__init__(orientation,parent)
	self.setStretchLastSection(False)
        #self.setSectionResizeMode(QHeaderView.Interactive)
	#self.resizeSection(2,100)
	self.setSectionsClickable(True)
        self.isChecked=False

    def paintSection(self,painter,rect,logicalIndex):
        painter.save()
        super(CheckBoxHeader,self).paintSection(painter,rect,logicalIndex)
        painter.restore()
        if logicalIndex==0:
            option=QStyleOptionButton()
            option.rect= QtCore.QRect(3,1,20,20)  #may have to be adapt
            option.state=QStyle.State_Enabled | QStyle.State_Active
            if self.isChecked:
                option.state|=QStyle.State_On
            else:
                option.state|=QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox,option,painter)

    def mousePressEvent(self,event):
	index = self.logicalIndexAt(event.pos())
	if index == 0:
		if 6 < event.pos().x() < 21:
			alldata = self.parent().model().arraydata
			if self.isChecked:
			    self.isChecked=False
			    for el in alldata:
				el[0] = False
			    self.parent().model().layoutChanged.emit()
			else:
			    self.isChecked=True
			    for el in alldata:
				el[0] = True
			    self.parent().model().layoutChanged.emit()
			self.clicked.emit(self.isChecked)
			self.viewport().update()
		else:
			super(CheckBoxHeader,self).mousePressEvent(event)
	else:
		super(CheckBoxHeader,self).mousePressEvent(event)

class MainWindow(QWidget):
	def __init__(self, parent=None):
	    super(MainWindow, self).__init__(parent)

	    self.openBtn = QPushButton("&Open")
	    self.searchBtn = QPushButton("KP Search")
	    self.renameBtn = QPushButton("Rename")
	    self.statusBar = QStatusBar()
	    # create table
	    self.get_table_data()
	    self.table = self.createTable() 

	    # layout
	    hbox = QHBoxLayout()
	    hbox.addStretch(1)
	    hbox.addWidget(self.openBtn)
	    hbox.addWidget(self.searchBtn)
	    hbox.addWidget(self.renameBtn)
	    layout = QVBoxLayout()
	    layout.addLayout(hbox)
	    layout.addWidget(self.table) 
	    layout.addWidget(self.statusBar)
	    self.setLayout(layout) 
	    self.searchBtn.clicked.connect(self.buttonClicked)
	    self.openBtn.clicked.connect(self.buttonClicked)
	    self.renameBtn.clicked.connect(self.buttonClicked)
	    self.statusBar.showMessage("hello")

	def get_table_data(self):
	    #stdouterr = os.popen("ls /Users/").read()
	    #lines = stdouterr.splitlines()
	    #lines = lines[5:]
	    #lines = lines[:-2]
	    #self.tabledata = [re.split(r"\s+", line, 4)
	#		 for line in lines]
	    self.tabledata = []#[[False,'','',[],0]] #[[True,'2','3',[],0],[True,'b','c',['','dfd','4','e'],0],[True,'b','c',['2','3'],0],[True,'b','c',['hi','mi','la','bu','mu'],0]]

	def createTable(self):
	    # create the view
	    tv = QTableView()

	    # set the table model
	    header = ['', 'Файл', 'rename to', 'kinopoisk search', 'filename', 'is_already_renamed']
	    tm = MyTableModel(self.tabledata, header, self) 
	    tv.setModel(tm)
	    tv.setItemDelegateForColumn(3, ComboBoxDelegate(self))
	    # set the minimum size
	    tv.setMinimumSize(800, 600)

	    # hide grid
	    tv.setShowGrid(False)

	    tv.setSelectionBehavior(QAbstractItemView.SelectRows)
	    # set the font

	    # hide vertical header
	    vh = tv.verticalHeader()
	    vh.setVisible(False)

	    # set horizontal header properties
	    #hh = tv.horizontalHeader()
	    hh = CheckBoxHeader(parent=tv)
	    tv.setHorizontalHeader(hh)
	    tv.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
	    #tv.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
	    #tv.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
	    tv.horizontalHeader().setStretchLastSection(True)
	    header = tv.horizontalHeader()
	    #for column in range(header.count()):
		#header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
		#width = header.sectionSize(column)
		#header.setSectionResizeMode(column, QHeaderView.Interactive)
		#header.resizeSection(column, width)
	    header.setSectionResizeMode(1, QHeaderView.Interactive)
	    header.resizeSection(1, (tv.width() - header.sectionSize(0))/3)
	    header.setSectionResizeMode(2, QHeaderView.Interactive)
            header.resizeSection(2, (tv.width() - header.sectionSize(0))/3)
	    # popup comboboxes on single click
	    tv.setEditTriggers(QAbstractItemView.AllEditTriggers)
	    # set column width to fit contents
	    #`tv.resizeColumnToContents(3)

	    # set row height
	    nrows = len(self.tabledata)
	    for row in range(nrows):
		tv.setRowHeight(row, 18)

	    # enable sorting
	    tv.setSortingEnabled(True)
	    tv.setColumnHidden(4,True)
	    tv.setColumnHidden(5,True)

	    return tv
	    self.setWindowTitle("Finance")
	
	def buttonClicked(self):
	    if self.sender().text() == "&Open":
		#self.fileDlg.setOptions(QtGui.QFileDialog.DontUseNativeDialog)
		oDir = QFileDialog.getExistingDirectory(self, "Select Directory","/Volumes/Multimedia",QFileDialog.DontUseNativeDialog).encode('utf-8')
		print oDir
		if oDir:
			self.table.model().update(oDir)	
	    if self.sender().text() == "KP Search":
		self.table.model().kpUpdate()
	    if self.sender().text() == "Rename":
		self.table.model().rename()
		
	def closeEvent(self, event):
		print 'closed'
		f = open('filmlist.dat','wb')
                pickle.dump(self.table.model().arraydata,f)
                f.close()
		event.accept()
		
		

class MyTableModel(QAbstractTableModel): 
	def __init__(self, datain, headerdata, parent=None, *args): 
	    """ datain: a list of lists
		headerdata: a list of strings
	    """
	    QAbstractTableModel.__init__(self, parent, *args) 

	    if os.path.isfile('filmlist.dat'):
	    	f = open('filmlist.dat','rb')
		self.arraydata = pickle.load(f)
		f.close()
	    else:
		self.arraydata = []

	    self.arraydata = []
	    self.headerdata = headerdata

	def rowCount(self, parent): 
	    return len(self.arraydata) 

	def columnCount(self, parent): 
	    if len(self.arraydata):
	    	return len(self.arraydata[0]) 
	    else:
		return 6

	def data(self, index, role): 
	    row = index.row()
	    column = index.column()
	    if not index.isValid(): 
		return QVariant() 
	    if role == Qt.CheckStateRole:
		if index.column() == 0:
			if self.arraydata[index.row()][index.column()]:
				return QVariant(Qt.Checked)
			else:
				return QVariant(Qt.Unchecked)
#	    if role != Qt.DisplayRole: 
#	    	return QVariant() 
	    if role == Qt.DisplayRole and index.column() == 0:
		return QVariant()
	    if role == Qt.DisplayRole and index.column() == 1:
		return QVariant(self.arraydata[index.row()][index.column()].split('/')[-1:][0])
	    if role == Qt.DisplayRole and index.column() == 3:
		if len(self.arraydata[row][3]):
			return QVariant(self.arraydata[row][3][self.arraydata[row][4]])
		else:
			return QVariant([])
	    if role == Qt.DisplayRole:
		return QVariant(self.arraydata[index.row()][index.column()])
	    if role == Qt.EditRole: 
		if column == 3:
			return self.arraydata[row][column]
		else:
			return QVariant(self.arraydata[index.row()][index.column()])
	    return QVariant() 

	def headerData(self, col, orientation, role):
	    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
		return QVariant(self.headerdata[col])
	    return QVariant()

	def flags(self,index):
	    if self.arraydata[index.row()][5]:
		    if index.column() == 0:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
		    elif index.column() == 1:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable
		    else:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
	    else:
		    return Qt.ItemIsSelectable
	
	def setData(self, index, value, role=Qt.EditRole):
	    #if index.column() == 4 and 3:
		#self.arraydata[index.row()][index.column()] = value 
	    #else:
	    print 'setData'
	    print value
	    if index.column() == 0:
		if value:
			self.arraydata[index.row()][index.column()] = True
		else:
			self.arraydata[index.row()][index.column()] = False
	    else:
		    self.arraydata[index.row()][index.column()] = value
	    return True

	def sort(self, Ncol, order):
	    """Sort table by given column number.
	    """
	    self.layoutAboutToBeChanged.emit()
	    self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
	    if order == Qt.DescendingOrder:
		self.arraydata.reverse()
	    self.layoutChanged.emit()

	def kp_search(self, name):
		kp_names = list()
		kp_original_names = list()
		years = list()
		result = list()
		url = 'https://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s' % (name)
		r = requests.get(url)
		tree = html.fromstring(r.text)
		ps = tree.xpath('.//div[@class="info" and child::p/a/@data-type="film"]')
		if ps:
			for p in ps:
			    kp_names.append(p.xpath('./p/a[@data-type="film"]/text()')[0])
			    try:
				    years.append(p.xpath('.//span[@class="year"]/text()')[0])
			    except:
				    years.append('')
			    try:
				    n_t = p.xpath('./span[1]/text()')[0].split(',')[0]
			    except:
				    n_t = ''
			    if n_t.split(' ')[-1:][0] == u'мин':
				kp_original_names.append('')
			    else:
				kp_original_names.append(n_t)
		else:
			return []

		for i in range(len(ps)):
			result.append(unicode(i) +u'. '+ kp_names[i] +u' ['+ kp_original_names[i] +u'] ('+ years[i] +u')')
		return result


	def list_files(self, directory):
	    ext = ('mkv','avi','mp4')
	    r = []
	    subdirs = [x[0] for x in os.walk(directory)]
	    for subdir in subdirs:
		files = os.walk(subdir).next()[2]
		if (len(files) > 0):
		    for f in files:
			if f.split('.')[-1:][0] in ext:
				r.append(subdir + "/" + f)
	    return r
	
	def get_year(self, s):
		year = ''
		for i in range(len(s)):
			if s[i].isdigit():
				year = year + s[i]
			else:
				if len(year) < 4:
					year = ''
				else: #if len(year) == 4:
					if year[:2] == '19' or year[:2] == '20':
						return year
		return ''

	def normilize(self, file_name):
	        name = file_name.replace('.',' ').replace('_',' ')
		year = self.get_year(name)
		if year:
			name = name[:name.find(year)]
			name += ' (' + year + ')'	
		return name


	def update(self, directory):
	    #directory = ''
	    self.arraydata = []
	    filesList = self.list_files(directory)
	    for mediaFile in filesList:
		curName = mediaFile.split('/')[-1:][0]
		curRename = self.normilize(curName)
		kpList = []#self.kp_search(curName) #['1','2','3']
	   	self.arraydata.append([False, mediaFile, curRename, kpList, 0, True])
	    self.layoutChanged.emit()

        def rename(self):
		print 'Ren func'
                renameList = [el for el in self.arraydata if el[0]]
                for el in renameList:
			ext = '.' + os.path.basename(el[1]).split('.')[-1:][0]
			renameTo = os.path.join(os.path.dirname(el[1]),el[2])
			print renameTo
			if os.path.isfile(renameToi + ext):
				i = 0
				while os.path.exists(renameTo + ext):
					i+=1 
				os.rename(el[1],renameTo + ('-(%s)'%i if i else '') + ext)
				#os.rename(el[1],os.path.join(os.path.dirname(el[1]),el[2]))
			self.arraydata[self.arraydata.index(el)][5] = False
	
	def kpUpdate(self):
		if self.arraydata:
			searchList = [el for el in self.arraydata if el[0]]
			sLen = len(searchList)
			for i in range(sLen):
				searchList[i][3] = self.kp_search(searchList[i][2])
				if i != (sLen-1):
					self.parent().statusBar.showMessage("Films seaching: " +str(i+1) +"/"+str(sLen))
				else:
					self.parent().statusBar.showMessage("Films seaching: Done!", 2000)
				self.parent().statusBar.updateGeometry()
				QApplication.instance().processEvents()
				self.layoutChanged.emit()

if __name__ == '__main__':
	from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

helloPythonWidget = MainWindow()
helloPythonWidget.show()

sys.exit(app.exec_())
