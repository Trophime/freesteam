#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from csv import writer
from ConfigParser import ConfigParser
from webbrowser import open_new_tab

from freesteam import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from numpy import meshgrid, zeros, arange, linspace, concatenate, max, min, transpose, logspace, log, arctan, pi
from scipy.optimize import fsolve

from images import images_rc
from units import unidades,  config
from units.UI import *


class Plot(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, dim=3):
        self.fig = pyplot.Figure(figsize=(width, height), dpi=dpi)
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        self.dim=dim
        
        if dim==2:
            self.axes2D = self.fig.add_subplot(111)
            self.axes2D.figure.subplots_adjust(left=0.09, right=0.98, bottom=0.08, top=0.98)
            self.lineDelta=self.axes2D.annotate("", xy=(0, 0), xycoords="data", xytext=(0, 0), textcoords="data", arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3"))

        else:
            self.axes3D = Axes3D(self.fig)

        FigureCanvasQTAgg.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


    def plot_sat(self, xsat, ysat, zsat=0):
        """Método que dibuja la línea de saturación"""
        if self.dim==3:
            self.satliq=self.axes3D.plot3D(xsat[0], ysat[0], zsat[0],'k-')
            self.satgas=self.axes3D.plot3D(xsat[1], ysat[1], zsat[1],'k-')
        else:
            self.satliq=self.axes2D.plot(xsat[0], ysat[0],'k-')
            self.satgas=self.axes2D.plot(xsat[1], ysat[1],'k-')

    def plot_3D(self, labels, xdata, ydata, zdata):
        """Método que dibuja la matriz de datos"""
        self.axes3D.clear()
        self.axes3D.plot_wireframe(xdata, ydata, zdata, rstride=1, cstride=1)
        self.axes3D.set_xlabel(labels[0])
        self.axes3D.set_ylabel(labels[1])
        self.axes3D.set_zlabel(labels[2])
        self.axes3D.mouse_init()
        
    def plot_2D(self, labels, bool):
        self.axes2D.clear()
        self.axes2D.grid(bool)        
        self.axes2D.axes.set_xlabel(labels[0], size='12')
        self.axes2D.axes.set_ylabel(labels[1], size='12')
        self.axes2D.add_artist(self.lineDelta)

        
    def plot_labels(self, tipo, x, y, label, angle=0, size="xx-small"):
        linea=[]
        for i in range(len(label)):
            linea.append(self.axes2D.axes.annotate(label[i], (x[i], y[i]), rotation=angle[i], size=size, horizontalalignment="center", verticalalignment="center"))
        if tipo =="T":
            self.Isoterma_label=linea
        elif tipo =="P":
            self.Isobara_label=linea
        elif tipo =="V":
            self.Isocora_label=linea
        elif tipo =="S":
            self.Isoentropica_label=linea
        elif tipo =="H":
            self.Isoentalpica_label=linea
        elif tipo =="X":
            self.IsoX_label=linea

    def plot_puntos(self, x, y, z=0):
        """Método que dibuja puntos individuales"""
        colores=config.colors(len(x))
        self.puntos=[]
        if self.dim==3:
            for i in range(len(x)):
                self.puntos.append(self.axes3D.plot3D([x[i]], [y[i]], [z[i]], color=colores[i], marker="o"))
        else:
            for i in range(len(x)):
                self.puntos.append(self.axes2D.plot([x[i]], [y[i]], color=colores[i], marker="o"))
            
    def plot_Isolinea(self, tipo, x, y, z=0, color="#000000", grosor=1, estilo=0):
        """Método que dibuja las isolineas"""
        if estilo==0:
            linestyle='-'
        elif estilo==1:
            linestyle='--'
        elif estilo==2:
            linestyle='-.'
        elif estilo==3:
            linestyle=':'
        
        linea=[]
        if self.dim==3:
            for i in range(len(x)):
                linea.append(self.axes3D.plot3D(x[i], y[i], z[i], color, lw=grosor, ls=linestyle))
        else:
            for i in range(len(x)):
                linea.append(self.axes2D.plot(x[i], y[i], color, lw=grosor, ls=linestyle))

        if tipo =="T":
            self.Isoterma=linea
        elif tipo =="P":
            self.Isobara=linea
        elif tipo =="V":
            self.Isocora=linea
        elif tipo =="S":
            self.Isoentropica=linea
        elif tipo =="H":
            self.Isoentalpica=linea
        elif tipo =="X":
            self.IsoX=linea

class DeltaWidget(QtGui.QWidget):
    def __init__(self, punto1=None, punto2=None, parent=None):
        self.punto1=None
        self.punto2=None
        self.parent=parent
        super(DeltaWidget, self).__init__(parent)
        layout=QtGui.QGridLayout(self)
        self.buttonDelete1=QtGui.QToolButton()
        self.buttonDelete1.clicked.connect(self.DeletePunto1)
        self.buttonDelete1.setIcon(QtGui.QIcon(QtGui.QPixmap(":/button/remove.png")))
        layout.addWidget(self.buttonDelete1,1,0,1,1)
        self.buttonDelete2=QtGui.QToolButton()
        self.buttonDelete2.clicked.connect(self.DeletePunto2)
        self.buttonDelete2.setIcon(QtGui.QIcon(QtGui.QPixmap(":/button/remove.png")))
        layout.addWidget(self.buttonDelete2,2,0,1,1)
        self.check1=QtGui.QRadioButton(QtGui.QApplication.translate("SteamTables", "Punto", None, QtGui.QApplication.UnicodeUTF8)+" 1:")
        layout.addWidget(self.check1,1,1,1,1)
        self.check2=QtGui.QRadioButton(QtGui.QApplication.translate("SteamTables", "Punto", None, QtGui.QApplication.UnicodeUTF8)+" 2:")
        self.check2.toggled.connect(self.setFoco)
        layout.addWidget(self.check2,2,1,1,1)
        self.labelPunto1=QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Hacer click en el dibujo o usar lista de puntos", None, QtGui.QApplication.UnicodeUTF8))
        layout.addWidget(self.labelPunto1,1,3,1,1)
        self.labelPunto2=QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Hacer click en el dibujo o usar lista de puntos", None, QtGui.QApplication.UnicodeUTF8))
        layout.addWidget(self.labelPunto2,2,3,1,1)
        layout.addItem(QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed), 1, 4, 2, 1)
        
        self.labelEntalpia=QtGui.QLabel(u"Δh")
        layout.addWidget(self.labelEntalpia,1,5,1,1)
        self.entalpia=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy", readOnly=True, boton=False, frame=False, width=70)
        layout.addWidget(self.entalpia,1,6,1,1)
        self.labelEntropia=QtGui.QLabel(u"Δs")
        layout.addWidget(self.labelEntropia,2,5,1,1)
        self.entropia=Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat", "Entropy", readOnly=True, boton=False, frame=False, width=70)
        layout.addWidget(self.entropia,2,6,1,1)
        
        self.labelGibbs=QtGui.QLabel(u"Δg")
        layout.addWidget(self.labelGibbs,1,8,1,1)
        self.gibbs=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy", readOnly=True, boton=False, frame=False, width=70)
        layout.addWidget(self.gibbs,1,9,1,1)
        self.labelEnergiaInterna=QtGui.QLabel(u"Δu")
        layout.addWidget(self.labelEnergiaInterna,2,8,1,1)
        self.energiaInterna=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy", readOnly=True, boton=False, frame=False, width=70)
        layout.addWidget(self.energiaInterna,2,9,1,1)
        if punto1:
            self.setPunto(0, punto1)
        else:
            self.buttonDelete1.setDisabled(True)
        if punto2:
            self.setPunto(1, punto2)
            self.setFoco(1)
        else:
            self.setFoco(0)
            self.buttonDelete2.setDisabled(True)
        if punto1 and punto2:
            self.set_visible(True)
        else:
            self.set_visible(False)
    
    def setFoco(self, i):
        self.foco=i
        if i:
            self.check2.setChecked(True)
        else:
            self.check1.setChecked(True)

    def addPunto(self, punto):
        if self.foco:
            self.setPunto(1, punto)
        else:
            self.setPunto(0, punto)
            
    def setPunto(self, i, punto):
        if i==0:
            self.punto1=punto
            self.labelPunto1.setText(config.representacion(unidades.Temperature(punto.T).config())+" "+config.Configuracion("Temperature").text()+", "+config.representacion(unidades.Pressure(punto.p).config())+" "+config.Configuracion("Pressure").text()+", x="+config.representacion(punto.x))
            self.buttonDelete1.setEnabled(True)
        else:
            self.punto2=punto
            self.labelPunto2.setText(config.representacion(unidades.Temperature(punto.T).config())+" "+config.Configuracion("Temperature").text()+", "+config.representacion(unidades.Pressure(punto.p).config())+" "+config.Configuracion("Pressure").text()+", x="+config.representacion(punto.x))
            self.buttonDelete2.setEnabled(True)
        self.calculo()
    
    def DeletePunto1(self):
        self.punto1=None
        self.labelPunto1.setText(QtGui.QApplication.translate("SteamTables", "Hacer click en el dibujo o usar lista de puntos", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDelete1.setEnabled(False)
        self.set_visible(False)
        
    def DeletePunto2(self):
        self.punto2=None
        self.labelPunto2.setText(QtGui.QApplication.translate("SteamTables", "Hacer click en el dibujo o usar lista de puntos", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDelete2.setEnabled(False)
        self.set_visible(False)
        
    def set_visible(self, bool):
        self.labelEntalpia.setVisible(bool)
        self.entalpia.setVisible(bool)
        self.labelEntropia.setVisible(bool)
        self.entropia.setVisible(bool)
        self.labelGibbs.setVisible(bool)
        self.gibbs.setVisible(bool)
        self.labelEnergiaInterna.setVisible(bool)
        self.energiaInterna.setVisible(bool)
        self.parent.diagrama2D.lineDelta.set_visible(bool)
        self.parent.diagrama2D.draw()

    def calculo(self):
        """Método que calcula los incrementos de propiedades y los muestra"""
        if self.punto1 and self.punto2:
            self.set_visible(True)
            self.entalpia.setValue(self.punto2.h-self.punto1.h)
            self.entropia.setValue(self.punto2.s-self.punto1.s)
            self.energiaInterna.setValue(self.punto2.u-self.punto1.u)
            self.gibbs.setValue((self.punto2.h-self.punto2.T*self.punto2.s)-(self.punto1.h-self.punto1.T*self.punto1.s))
        else:
            self.set_visible(False)
        
        
class Ventana_Lista_Puntos(QtGui.QDialog):
    """Dialogo que muestra la lísta de puntos especificados por el usuario así como sus propiedades"""
    def __init__(self, puntos, parent=None):
        super(Ventana_Lista_Puntos, self).__init__(parent)
        self.setFixedSize(500, self.minimumHeight())
        self.setWindowTitle(QtGui.QApplication.translate("SteamTables", "Puntos individuales", None, QtGui.QApplication.UnicodeUTF8))
        self.puntos=puntos
        self.gridLayout = QtGui.QGridLayout(self)
        self.listWidget = QtGui.QTableWidget(len(puntos), 3)
        self.listWidget.setHorizontalHeaderLabels([QtCore.QString(u"Δ1"), QtCore.QString(u"Δ2"), QtGui.QApplication.translate("SteamTables", "Definición", None, QtGui.QApplication.UnicodeUTF8)])
        self.listWidget.resizeColumnsToContents()
        self.listWidget.horizontalHeader().setStretchLastSection(True)
        self.listWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listWidget.setCornerButtonEnabled(False)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 3, 1)
        self.tablaPropiedades=QtGui.QTableWidget()
        self.tablaPropiedades.setVisible(False)
        self.tablaPropiedades.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablaPropiedades.setRowCount(16)
        self.tablaPropiedades.setVerticalHeaderItem(0, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Pressure").text()))
        self.tablaPropiedades.setVerticalHeaderItem(1, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Temperature").text()))
        self.tablaPropiedades.setVerticalHeaderItem(2, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Volumen", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificVolume").text()))
        self.tablaPropiedades.setVerticalHeaderItem(3, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Enthalpy").text()))
        self.tablaPropiedades.setVerticalHeaderItem(4, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificHeat", "Entropy").text()))
        self.tablaPropiedades.setVerticalHeaderItem(5, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", u"Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8)))
        self.tablaPropiedades.setVerticalHeaderItem(6, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Enthalpy").text()))
        self.tablaPropiedades.setVerticalHeaderItem(7, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Enthalpy").text()))
        self.tablaPropiedades.setVerticalHeaderItem(8, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Enthalpy").text()))
        self.tablaPropiedades.setVerticalHeaderItem(9, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Density").text()))
        self.tablaPropiedades.setVerticalHeaderItem(10, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificHeat").text()))
        self.tablaPropiedades.setVerticalHeaderItem(11, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificHeat").text()))
        self.tablaPropiedades.setVerticalHeaderItem(12, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Conductividad", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("ThermalConductivity").text()))
        self.tablaPropiedades.setVerticalHeaderItem(13, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Viscosity").text()))
        self.tablaPropiedades.setVerticalHeaderItem(14, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Speed").text()))
        self.tablaPropiedades.setVerticalHeaderItem(15, QtGui.QTableWidgetItem(QtGui.QApplication.translate("SteamTables", "Región", None, QtGui.QApplication.UnicodeUTF8)))
        self.gridLayout.addWidget(self.tablaPropiedades, 3, 0, 1, 2)
        self.botonBorrar = QtGui.QPushButton()
        self.botonBorrar.setText(QtGui.QApplication.translate("SteamTables", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.botonBorrar.clicked.connect(self.on_botonBorrar_clicked)
        self.gridLayout.addWidget(self.botonBorrar, 0, 1, 1, 1)
        self.botonPropiedades = QtGui.QPushButton()
        self.botonPropiedades.setCheckable(True)
        self.botonPropiedades.setText(QtGui.QApplication.translate("SteamTables", "Propiedades", None, QtGui.QApplication.UnicodeUTF8))
        self.botonPropiedades.toggled.connect(self.tablaPropiedades.setVisible)
        self.gridLayout.addWidget(self.botonPropiedades, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        
        self.colores=config.colors(len(self.puntos))
        self.rellenarLista()
        self.rellenarTabla()

    def rellenarLista(self):
#        self.listWidget.clearContents()
        self.listWidget.setRowCount(len(self.puntos))
        self.group1=QtGui.QButtonGroup()
        self.group2=QtGui.QButtonGroup()
        self.delta1=[]
        self.delta2=[]
        for i, punto in enumerate(self.puntos):
            self.listWidget.setItem(i, 2, QtGui.QTableWidgetItem(str(i+1)+" - "+config.representacion(unidades.Temperature(punto.T).config())+" "+config.Configuracion("Temperature").text()+", "+config.representacion(unidades.Pressure(punto.p).config())+" "+config.Configuracion("Pressure").text()+", x="+config.representacion(punto.x)))
            self.delta1.append(QtGui.QRadioButton(self))
            self.delta2.append(QtGui.QRadioButton(self))
            self.group1.addButton(self.delta1[-1])
            self.group2.addButton(self.delta2[-1])
            self.listWidget.setCellWidget(i, 0, self.delta1[-1])
            self.listWidget.setCellWidget(i, 1, self.delta2[-1])
            
            self.listWidget.setRowHeight(i, 20)
            self.listWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(""))
            pixmap=QtGui.QPixmap(10, 10)
            pixmap.fill(QtGui.QColor(self.colores[i]))
            self.listWidget.verticalHeaderItem(i).setIcon(QtGui.QIcon(pixmap))


    def rellenarTabla(self):
        if len(self.puntos)==0:
            self.tablaPropiedades.setFixedHeight(404)
        elif len(self.puntos)<5:
            self.tablaPropiedades.setFixedHeight(428)
        else:
            self.tablaPropiedades.setFixedHeight(444)
        self.tablaPropiedades.setColumnCount(len(self.puntos))
        for i in range(16):
            self.tablaPropiedades.setRowHeight(i,25)
        for i, punto in enumerate(self.puntos):
            pixmap=QtGui.QPixmap(10, 10)
            pixmap.fill(QtGui.QColor(self.colores[i]))
            self.tablaPropiedades.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(QtGui.QIcon(pixmap), str(i+1)))
            self.tablaPropiedades.setItem(0, i, QtGui.QTableWidgetItem(config.representacion(unidades.Pressure(punto.p).config())))
            self.tablaPropiedades.setItem(1, i, QtGui.QTableWidgetItem(config.representacion(unidades.Temperature(punto.T).config())))
            self.tablaPropiedades.setItem(2, i, QtGui.QTableWidgetItem(config.representacion(unidades.SpecificVolume(punto.v).config())))
            self.tablaPropiedades.setItem(3, i, QtGui.QTableWidgetItem(config.representacion(unidades.Enthalpy(punto.h).config())))
            self.tablaPropiedades.setItem(4, i, QtGui.QTableWidgetItem(config.representacion(unidades.SpecificHeat(punto.s).config("Entropy"))))
            self.tablaPropiedades.setItem(5, i, QtGui.QTableWidgetItem(config.representacion(punto.x)))
            self.tablaPropiedades.setItem(6, i, QtGui.QTableWidgetItem(config.representacion(unidades.Enthalpy(punto.u).config())))
            self.tablaPropiedades.setItem(7, i, QtGui.QTableWidgetItem(config.representacion(unidades.Enthalpy(punto.s).config())))
            self.tablaPropiedades.setItem(8, i, QtGui.QTableWidgetItem(config.representacion(unidades.Enthalpy(punto.s).config())))
            self.tablaPropiedades.setItem(9, i, QtGui.QTableWidgetItem(config.representacion(unidades.Density(punto.rho).config())))
            self.tablaPropiedades.setItem(10, i, QtGui.QTableWidgetItem(config.representacion(unidades.SpecificHeat(punto.cp).config())))
            self.tablaPropiedades.setItem(11, i, QtGui.QTableWidgetItem(config.representacion(unidades.SpecificHeat(punto.cv).config())))
            self.tablaPropiedades.setItem(12, i, QtGui.QTableWidgetItem(config.representacion(unidades.ThermalConductivity(punto.k).config())))
            self.tablaPropiedades.setItem(13, i, QtGui.QTableWidgetItem(config.representacion(unidades.Viscosity(punto.mu).config())))
            if punto.region !='\x04' and  punto.region !='\x03':
                self.tablaPropiedades.setItem(14, i, QtGui.QTableWidgetItem(config.representacion(unidades.Speed(punto.w).config())))
            else:
                self.tablaPropiedades.setItem(14, i, QtGui.QTableWidgetItem('nan'))
            if punto.region =='\x01':
                self.tablaPropiedades.setItem(15, i, QtGui.QTableWidgetItem('1'))
            elif punto.region =='\x02':
                self.tablaPropiedades.setItem(15, i, QtGui.QTableWidgetItem('2'))
            elif punto.region =='\x03':
                self.tablaPropiedades.setItem(15, i, QtGui.QTableWidgetItem('3'))
            elif punto.region =='\x04':
                self.tablaPropiedades.setItem(15, i, QtGui.QTableWidgetItem('4'))
            elif punto.region =='\x05':
                self.tablaPropiedades.setItem(15, i, QtGui.QTableWidgetItem('5'))
            for j in range(16):
                self.tablaPropiedades.item(j, i).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                
        self.tablaPropiedades.resizeColumnsToContents()

    def on_botonBorrar_clicked(self):
        """Borra el punto seleccionado de la lista"""
        if self.listWidget.currentRow()>=0:
            self.puntos.pop(self.listWidget.currentRow())
        self.rellenarLista()
        self.rellenarTabla()



class Ui_SteamTables(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_SteamTables, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/button/steamTables.png")))
        self.setWindowTitle(QtGui.QApplication.translate("SteamTables", "Tablas de Vapor", None, QtGui.QApplication.UnicodeUTF8))
        self.Config=ConfigParser()
        self.Config.read("UI_steamTablesrc")

        self.showMaximized()
        self.centralwidget = QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)
        
        #menus
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0,0,700,30))
        self.menuArchivo = QtGui.QMenu(QtGui.QApplication.translate("SteamTables", "Archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGrafico = QtGui.QMenu(QtGui.QApplication.translate("SteamTables", "Gráfico", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAyuda = QtGui.QMenu(QtGui.QApplication.translate("SteamTables", "Ayuda", None, QtGui.QApplication.UnicodeUTF8))
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar()
        self.setStatusBar(self.statusbar)
        self.progresbar=QtGui.QProgressBar()
        self.progresbar.setVisible(False)
        self.progresbar.setFixedSize(80, 15)
        self.statusbar.addPermanentWidget(self.progresbar)
        self.Preferencias = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(":/button/configure.png")), QtGui.QApplication.translate("SteamTables", "Preferencias", None, QtGui.QApplication.UnicodeUTF8), self)
        self.Preferencias.triggered.connect(self.preferencias)
        self.actionCSV = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(":/button/filesave.png")), QtGui.QApplication.translate("SteamTables", "Guardar", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionCSV.setShortcut("Ctrl+E")
        self.actionCSV.setEnabled(False)
        self.actionCSV.triggered.connect(self.exporttoCSV)
        self.actionSalir = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(":/button/exit.png")), QtGui.QApplication.translate("SteamTables", "Salir", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionSalir.setShortcut("Alt+F4")
        self.actionSalir.triggered.connect(self.close)
        self.actionTipoGrafico=QtGui.QActionGroup(self)
        self.action2D = QtGui.QAction(QtGui.QApplication.translate("SteamTables", "Gráfico 2D", None, QtGui.QApplication.UnicodeUTF8), self.actionTipoGrafico)
        self.action2D.setCheckable(True)
        self.action2D.setShortcut("Ctrl+2")
        self.action2D.toggled.connect(self.d2)
        self.action3D = QtGui.QAction(QtGui.QApplication.translate("SteamTables", "Gráfico 3D", None, QtGui.QApplication.UnicodeUTF8), self.actionTipoGrafico)
        self.action3D.setCheckable(True)
        self.action3D.setChecked(True)
        self.action3D.setShortcut("Ctrl+3")
        self.actionMostrarDelta = QtGui.QAction(QtGui.QApplication.translate("SteamTables", "Mostrar cambio de estado", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionMostrarDelta.setCheckable(True)
        self.actionMostrarDelta.setChecked(False)
        self.actionMostrarDelta.setShortcut("Ctrl+D")
        self.actionMostrarDelta.triggered.connect(self.mostrarDelta)
        self.actionMostrarBarra = QtGui.QAction(QtGui.QApplication.translate("SteamTables", "Mostrar barra de herramientas", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionMostrarBarra.setCheckable(True)
        self.actionMostrarBarra.setChecked(False)
        self.actionMostrarBarra.setShortcut("Ctrl+T")
        self.actionMostrarBarra.triggered.connect(self.mostrarBarra)
        self.actionDibujarSaturacion = QtGui.QAction(QtGui.QApplication.translate("SteamTables", "Dibujar línea de saturación", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionDibujarSaturacion.setCheckable(True)
        self.actionDibujarSaturacion.setChecked(True)
        self.actionDibujarSaturacion.setShortcut("Ctrl+S")
        self.actionDibujarSaturacion.triggered.connect(self.mostrarSaturacion)
        self.actionMostrarPuntos = QtGui.QAction(QtGui.QApplication.translate("SteamTables", "Mostrar puntos definidos por el usuario", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionMostrarPuntos.setCheckable(True)
        self.actionMostrarPuntos.setChecked(True)
        self.actionMostrarPuntos.setShortcut("Ctrl+P")
        self.actionMostrarPuntos.triggered.connect(self.mostrarPuntos)
        self.actionAyuda = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(":/button/help.png")), QtGui.QApplication.translate("SteamTables", "Ayuda", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionAyuda.setShortcut("F1")
        self.actionAyuda.triggered.connect(self.ayuda)
        self.actionAcerca_de = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(":/button/steamTables.png")), QtGui.QApplication.translate("SteamTables", "Acerca de freesteam", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionAcerca_de.triggered.connect(self.acerca)
        self.actionAcerca_deQt= QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(":/button/AboutQt.png")), QtGui.QApplication.translate("SteamTables", "Acerca de Qt", None, QtGui.QApplication.UnicodeUTF8), self)
        self.actionAcerca_deQt.triggered.connect(self.acercaQt)
        self.menuArchivo.addAction(self.Preferencias)
        self.menuArchivo.addAction(self.actionCSV)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionSalir)
        self.menuGrafico.addAction(self.action2D)
        self.menuGrafico.addAction(self.action3D)
        self.menuGrafico.addSeparator()
        self.menuGrafico.addAction(self.actionMostrarDelta)
        self.menuGrafico.addAction(self.actionMostrarBarra)
        self.menuGrafico.addAction(self.actionDibujarSaturacion)
        self.menuGrafico.addAction(self.actionMostrarPuntos)
        self.menuAyuda.addAction(self.actionAyuda)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menuAyuda.addAction(self.actionAcerca_deQt)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuGrafico.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
                
        #Ventana principal
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.toolBox = QtGui.QToolBox()
        self.page_1 = QtGui.QWidget()
        self.gridLayout_2 = QtGui.QGridLayout(self.page_1)
        self.tabla = QtGui.QTableWidget(self.page_1)
        self.gridLayout_2.addWidget(self.tabla,0, 0, 1, 1)
        self.toolBox.addItem(self.page_1,QtGui.QApplication.translate("SteamTables", "Tablas", None, QtGui.QApplication.UnicodeUTF8))

        self.page_Plot = QtGui.QWidget()
        self.gridLayout_3 = QtGui.QGridLayout(self.page_Plot)
        self.checkIsoTherm=QtGui.QCheckBox(self.page_Plot)
        self.checkIsoTherm.setText(QtGui.QApplication.translate("SteamTables", "Isotérmicas", None, QtGui.QApplication.UnicodeUTF8))
        self.checkIsoTherm.setStatusTip(QtGui.QApplication.translate("SteamTables", "Dibujar curvas isotérmicas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.checkIsoTherm,0,0,1,1)
        self.checkIsoBar=QtGui.QCheckBox(self.page_Plot)
        self.checkIsoBar.setText(QtGui.QApplication.translate("SteamTables", "Isobáricas", None, QtGui.QApplication.UnicodeUTF8))
        self.checkIsoBar.setStatusTip(QtGui.QApplication.translate("SteamTables", "Dibujar curvas isobáricas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.checkIsoBar,0,1,1,1)
        self.checkIsoEnth=QtGui.QCheckBox(self.page_Plot)
        self.checkIsoEnth.setText(QtGui.QApplication.translate("SteamTables", "Isoentálpicas", None, QtGui.QApplication.UnicodeUTF8))
        self.checkIsoEnth.setStatusTip(QtGui.QApplication.translate("SteamTables", "Dibujar curvas isoentálpicas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.checkIsoEnth,0,2,1,1)
        self.checkIsoEntr=QtGui.QCheckBox(self.page_Plot)
        self.checkIsoEntr.setText(QtGui.QApplication.translate("SteamTables", "Isoentrópicas", None, QtGui.QApplication.UnicodeUTF8))
        self.checkIsoEntr.setStatusTip(QtGui.QApplication.translate("SteamTables", "Dibujar curvas isoentrópicas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.checkIsoEntr,0,3,1,1)
        self.checkIsoVol=QtGui.QCheckBox(self.page_Plot)
        self.checkIsoVol.setText(QtGui.QApplication.translate("SteamTables", "Isocóricas", None, QtGui.QApplication.UnicodeUTF8))
        self.checkIsoVol.setStatusTip(QtGui.QApplication.translate("SteamTables", "Dibujar curvas isocóricas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.checkIsoVol,0,4,1,1)
        self.checkIsoX=QtGui.QCheckBox(self.page_Plot)
        self.checkIsoX.setText(QtGui.QApplication.translate("SteamTables", "Isocalidad", None, QtGui.QApplication.UnicodeUTF8))
        self.checkIsoX.setStatusTip(QtGui.QApplication.translate("SteamTables", "Dibujar curvas con igual fracción de vapor", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.checkIsoX,0,5,1,1)
        self.diagrama2D = Plot(self.page_Plot, dpi=self.Config.getfloat("General","Dpi"), dim=2)
        self.diagrama2D.fig.canvas.mpl_connect('button_press_event', self.click)
        self.gridLayout_3.addWidget(self.diagrama2D,1,0,1,6)
        self.diagrama3D = Plot(self.page_Plot, dpi=self.Config.getfloat("General","Dpi"), dim=3)
        self.diagrama3D.setStatusTip(QtGui.QApplication.translate("SteamTables", "Pinchar y arrastrar para mover la orientación del gráfico", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3.addWidget(self.diagrama3D,1,0,1,6)
        self.delta=DeltaWidget(parent=self)
        self.gridLayout_3.addWidget(self.delta,3,0,1,6)
        self.toolbar2D=NavigationToolbar2QT(self.diagrama2D, self.diagrama2D)
        self.gridLayout_3.addWidget(self.toolbar2D,4,0,1,6)
        self.toolbar3D=NavigationToolbar2QT(self.diagrama3D, self.diagrama3D)
        self.gridLayout_3.addWidget(self.toolbar3D,4,0,1,6)
        self.toolBox.addItem(self.page_Plot,QtGui.QApplication.translate("SteamTables", "Gráfico", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.toolBox,0,0,1,1)

        #Toolbox parámetros Tabla
        self.dockWidget_Tabla = QtGui.QDockWidget(QtGui.QApplication.translate("SteamTables", "Tabla", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_Tabla.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)

        self.dockWidgetContents = QtGui.QWidget()
        self.gridLayout_4 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_4.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Ejes", None, QtGui.QApplication.UnicodeUTF8)),0,0,1,1)
        self.ejesTabla = QtGui.QComboBox()
        self.ejesTabla.setFixedSize(QtCore.QSize(100,20))
        self.ejesTabla.setToolTip(QtGui.QApplication.translate("SteamTables", "p\tPresión\nT\tTemperatura\nh\tEntalpía\ns\tEntropía\nv\tVolumen específico\nx\tCalidad (cuando es vapor saturado)", None, QtGui.QApplication.UnicodeUTF8))
        self.ejesTabla.setStatusTip(QtGui.QApplication.translate("SteamTables", "Definir variables impuestas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_4.addWidget(self.ejesTabla,0,1,1,2)
        self.gridLayout_4.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Calcular", None, QtGui.QApplication.UnicodeUTF8)),1,0,1,1)
        self.variableTabla = QtGui.QComboBox()
        self.variableTabla.setFixedWidth(150)
        self.variableTabla.setStatusTip(QtGui.QApplication.translate("SteamTables", "Definir variables a calcular", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_4.addWidget(self.variableTabla,1,1,1,2)
        self.label_26 = QtGui.QLabel()
        self.label_26.setFixedHeight(30)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.gridLayout_4.addWidget(self.label_26,3,1,1,1)
        self.label_27 = QtGui.QLabel()
        self.label_27.setFixedHeight(30)
        self.label_27.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.gridLayout_4.addWidget(self.label_27,3,2,1,1)
        self.gridLayout_4.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Intervalo", None, QtGui.QApplication.UnicodeUTF8)),6,0,1,1)
        self.abscisaInicio = QtGui.QLineEdit()
        self.abscisaInicio.setMaximumSize(QtCore.QSize(80,16777215))
        self.abscisaInicio.setAlignment(QtCore.Qt.AlignRight)        
        self.gridLayout_4.addWidget(self.abscisaInicio,4,1,1,1)
        self.ordenadaInicio = QtGui.QLineEdit()
        self.ordenadaInicio.setMaximumSize(QtCore.QSize(80,16777215))
        self.ordenadaInicio.setAlignment(QtCore.Qt.AlignRight)        
        self.gridLayout_4.addWidget(self.ordenadaInicio,4,2,1,1)
        self.gridLayout_4.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Inicio", None, QtGui.QApplication.UnicodeUTF8)),4,0,1,1)
        self.gridLayout_4.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Fin", None, QtGui.QApplication.UnicodeUTF8)),5,0,1,1)
        self.abscisaFin = QtGui.QLineEdit()
        self.abscisaFin.setMaximumSize(QtCore.QSize(80,16777215))
        self.abscisaFin.setAlignment(QtCore.Qt.AlignRight)        
        self.gridLayout_4.addWidget(self.abscisaFin,5,1,1,1)
        self.ordenadaFin = QtGui.QLineEdit()
        self.ordenadaFin.setMaximumSize(QtCore.QSize(80,16777215))
        self.ordenadaFin.setAlignment(QtCore.Qt.AlignRight)        
        self.gridLayout_4.addWidget(self.ordenadaFin,5,2,1,1)
        self.abscisaIntervalo = QtGui.QLineEdit()
        self.abscisaIntervalo.setMaximumSize(QtCore.QSize(80,16777215))
        self.abscisaIntervalo.setAlignment(QtCore.Qt.AlignRight)        
        self.gridLayout_4.addWidget(self.abscisaIntervalo,6,1,1,1)
        self.ordenadaIntervalo = QtGui.QLineEdit()
        self.ordenadaIntervalo.setMaximumSize(QtCore.QSize(80,16777215))
        self.ordenadaIntervalo.setAlignment(QtCore.Qt.AlignRight)        
        self.gridLayout_4.addWidget(self.ordenadaIntervalo,6,2,1,1)
        self.botonCalcular = QtGui.QPushButton()
        self.botonCalcular.setText(QtGui.QApplication.translate("SteamTables", "Calcular", None, QtGui.QApplication.UnicodeUTF8))
        self.botonCalcular.setIcon(QtGui.QIcon(QtGui.QPixmap(":/button/calculate.png")))
        self.botonCalcular.clicked.connect(self.botonCalcular_clicked)
        self.botonCalcular.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.gridLayout_4.addWidget(self.botonCalcular,7,0,1,3)
        self.dockWidget_Tabla.setWidget(self.dockWidgetContents)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_Tabla)
        self.dockWidget_Tabla.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)


        #Toolbox graficos 2D
        self.dockWidget_2D = QtGui.QDockWidget(QtGui.QApplication.translate("SteamTables", "Gráfico 2D", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_2D.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.Dock_2D= QtGui.QWidget()
        self.gridLayout_13 = QtGui.QGridLayout(self.Dock_2D)
        self.gridLayout_13.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Eje X:", None, QtGui.QApplication.UnicodeUTF8)),0,0,1,1)
        self.ejeX = QtGui.QComboBox()
        self.ejeX.setFixedWidth(50)
        self.gridLayout_13.addWidget(self.ejeX,0,1,1,1)
        self.ejeX_escala=QtGui.QCheckBox()
        self.ejeX_escala.setText(QtGui.QApplication.translate("SteamTables", "Escala logarítmica", None, QtGui.QApplication.UnicodeUTF8))
        self.ejeX_escala.toggled.connect(self.ejeX_log)
        self.gridLayout_13.addWidget(self.ejeX_escala,0,2,1,2)
        self.gridLayout_13.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Mínimo", None, QtGui.QApplication.UnicodeUTF8)),1,1,1,1)
        self.ejeX_min=[Entrada_con_unidades(UI_pressure, unidades.Pressure, "Pressure"), Entrada_con_unidades(UI_temperature, unidades.Temperature, "Temperature"), Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat","Entropy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_specificVolume, unidades.SpecificVolume, "SpecificVolume")]
        for i in self.ejeX_min:
            i.valueChanged.connect(self.diagrama2D_ejeX)
            self.gridLayout_13.addWidget(i,1,2,1,2)
        
        self.gridLayout_13.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Máximo", None, QtGui.QApplication.UnicodeUTF8)),2,1,1,1)
        self.ejeX_max=[Entrada_con_unidades(UI_pressure, unidades.Pressure, "Pressure"), Entrada_con_unidades(UI_temperature, unidades.Temperature, "Temperature"), Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat","Entropy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_specificVolume, unidades.SpecificVolume, "SpecificVolume")]
        for i in self.ejeX_max:
            i.valueChanged.connect(self.diagrama2D_ejeX)
            self.gridLayout_13.addWidget(i,2,2,1,2)

        self.gridLayout_13.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Eje Y:", None, QtGui.QApplication.UnicodeUTF8)),3,0,1,1)
        self.ejeY = QtGui.QComboBox()
        self.ejeY.setFixedWidth(50)
        self.gridLayout_13.addWidget(self.ejeY,3,1,1,1)
        self.ejeY_escala=QtGui.QCheckBox()
        self.ejeY_escala.setText(QtGui.QApplication.translate("SteamTables", "Escala logarítmica", None, QtGui.QApplication.UnicodeUTF8))
        self.ejeY_escala.toggled.connect(self.ejeY_log)
        self.gridLayout_13.addWidget(self.ejeY_escala,3,2,1,2)
        self.gridLayout_13.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Mínimo", None, QtGui.QApplication.UnicodeUTF8)),4,1,1,1)
        self.ejeY_min=[Entrada_con_unidades(UI_pressure, unidades.Pressure, "Pressure"), Entrada_con_unidades(UI_temperature, unidades.Temperature, "Temperature"), Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat","Entropy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_specificVolume, unidades.SpecificVolume, "SpecificVolume")]
        for i in self.ejeY_min:
            i.valueChanged.connect(self.diagrama2D_ejeY)
            self.gridLayout_13.addWidget(i,4,2,1,2)
        self.gridLayout_13.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Máximo", None, QtGui.QApplication.UnicodeUTF8)),5,1,1,1)
        self.ejeY_max=[Entrada_con_unidades(UI_pressure, unidades.Pressure, "Pressure"), Entrada_con_unidades(UI_temperature, unidades.Temperature, "Temperature"), Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat","Entropy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy"), Entrada_con_unidades(UI_specificVolume, unidades.SpecificVolume, "SpecificVolume")]
        for i in self.ejeY_max:
            i.valueChanged.connect(self.diagrama2D_ejeY)
            self.gridLayout_13.addWidget(i,5,2,1,2)

        self.rejilla=QtGui.QCheckBox()
        self.rejilla.setText(QtGui.QApplication.translate("SteamTables", "Rejilla", None, QtGui.QApplication.UnicodeUTF8))
        self.rejilla.toggled.connect(self.rejilla_toggled)
        self.gridLayout_13.addWidget(self.rejilla,6,0,1,2)
        self.botonCalcular2 = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap(":/button/calculate.png")), QtGui.QApplication.translate("SteamTables", "Calcular", None, QtGui.QApplication.UnicodeUTF8))
        self.botonCalcular2.clicked.connect(self.botonCalcular_clicked)
        self.gridLayout_13.addWidget(self.botonCalcular2,6,2,1,1)
        self.gridLayout_13.addItem(QtGui.QSpacerItem(72, 34, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding), 6, 3, 1, 1)

        self.dockWidget_2D.setWidget(self.Dock_2D)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_2D)
        self.dockWidget_2D.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

        #Toolbox parámetros Puntos individuales
        self.dockWidget_Puntos = QtGui.QDockWidget(QtGui.QApplication.translate("SteamTables", "Puntos específicos", None, QtGui.QApplication.UnicodeUTF8))
        self.widget = QtGui.QWidget()
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.scrollArea = QtGui.QScrollArea(self.widget)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dockWidgetContents_2 = QtGui.QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.dockWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.dockWidget_Puntos.setWidget(self.widget)
        
        self.gridLayout_1 = QtGui.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Datos conocidos", None, QtGui.QApplication.UnicodeUTF8)),0,0,1,1)
        self.variablesCalculo = QtGui.QComboBox()
        self.variablesCalculo.setFixedWidth(100)
        self.variablesCalculo.setToolTip(QtGui.QApplication.translate("SteamTables", "p\tPresión\nT\tTemperatura\nh\tEntalpía\ns\tEntropía\nv\tVolumen específico\nx\tCalidad (cuando es vapor saturado)", None, QtGui.QApplication.UnicodeUTF8))
        self.variablesCalculo.setStatusTip(QtGui.QApplication.translate("SteamTables", "Definir variables impuestas", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.variablesCalculo,0,1,1,2)
        self.gridLayout_1.addItem(QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed), 1, 0, 1, 3)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)),6,0,1,1)
        self.presion=Entrada_con_unidades(UI_pressure, unidades.Pressure, "Pressure")
        self.presion.setStatusTip(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8))
        self.presion.valueChanged.connect(self.presion_editingFinished)
        self.gridLayout_1.addWidget(self.presion,6,1,1,2)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8)),7,0,1,1)
        self.temperatura=Entrada_con_unidades(UI_temperature, unidades.Temperature, "Temperature", spinbox=True, max=1080, step=1)
        self.temperatura.setStatusTip(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8))
        self.temperatura.valueChanged.connect(self.temperatura_editingFinished)
        self.gridLayout_1.addWidget(self.temperatura,7,1,1,2)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Volumen", None, QtGui.QApplication.UnicodeUTF8)),8,0,1,1)
        self.volumen=Entrada_con_unidades(UI_specificVolume, unidades.SpecificVolume, "SpecificVolume", spinbox=True)
        self.volumen.setStatusTip(QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8))
        self.volumen.valueChanged.connect(self.volumen_editingFinished)
        self.gridLayout_1.addWidget(self.volumen,8,1,1,2)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Entalpia", None, QtGui.QApplication.UnicodeUTF8)),9,0,1,1)
        self.entalpia=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy")
        self.entalpia.setStatusTip(QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8))
        self.entalpia.valueChanged.connect(self.entalpia_editingFinished)
        self.gridLayout_1.addWidget(self.entalpia,9,1,1,2)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8)),10,0,1,1)
        self.entropia=Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat","Entropy", spinbox=True)
        self.entropia.setStatusTip(QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8))
        self.entropia.valueChanged.connect(self.entropia_editingFinished)
        self.gridLayout_1.addWidget(self.entropia,10,1,1,2)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8)),11,0,1,1)
        self.fraccionVapor = Entrada_con_unidades(None, float, None, spinbox=True, max=1)
        self.fraccionVapor.setStatusTip(QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8))
        self.fraccionVapor.valueChanged.connect(self.fraccionVapor_editingFinished)
        self.gridLayout_1.addWidget(self.fraccionVapor,11,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8)),12,0,1,1)
        self.energiaInterna=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy", readOnly=True, retornar=False)
        self.energiaInterna.setStatusTip(QtGui.QApplication.translate("SteamTables", "Energía Interna", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.energiaInterna,12,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "E. Gibbs", None, QtGui.QApplication.UnicodeUTF8)),13,0,1,1)
        self.energiaGibbs=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy", readOnly=True, retornar=False)
        self.energiaGibbs.setStatusTip(QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.energiaGibbs,13,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "E. Helmholtz", None, QtGui.QApplication.UnicodeUTF8)),14,0,1,1)
        self.energiaHelmholtz=Entrada_con_unidades(UI_enthalpy, unidades.Enthalpy, "Enthalpy", readOnly=True, retornar=False)
        self.energiaHelmholtz.setStatusTip(QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.energiaHelmholtz,14,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8)),15,0,1,1)
        self.densidad=Entrada_con_unidades(UI_density, unidades.Density, "Density", readOnly=True, retornar=False)
        self.densidad.setStatusTip(QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.densidad,15,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8)),16,0,1,1)
        self.cp=Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat", readOnly=True, retornar=False)
        self.cp.setStatusTip(QtGui.QApplication.translate("SteamTables", "Capacidad calorífica a presión constante", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.cp,16,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8)),17,0,1,1)
        self.cv=Entrada_con_unidades(UI_specificHeat, unidades.SpecificHeat, "SpecificHeat", readOnly=True, retornar=False)
        self.cv.setStatusTip(QtGui.QApplication.translate("SteamTables", "Capacidad calorífica a volumen constante", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.cv,17,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Conductividad", None, QtGui.QApplication.UnicodeUTF8)),18,0,1,1)
        self.conductividad=Entrada_con_unidades(UI_thermalConductivity, unidades.ThermalConductivity, "ThermalConductivity", readOnly=True, retornar=False)
        self.conductividad.setStatusTip(QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.conductividad,18,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", u"Viscosidad", None, QtGui.QApplication.UnicodeUTF8)),19,0,1,1)
        self.viscosidad=Entrada_con_unidades(UI_viscosity, unidades.Viscosity, "Viscosity", readOnly=True, retornar=False)
        self.viscosidad.setStatusTip(QtGui.QApplication.translate("SteamTables", "Viscosidad dinámica", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.viscosidad, 19,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "V sonido", None, QtGui.QApplication.UnicodeUTF8)),20,0,1,1)
        self.velocidad=Entrada_con_unidades(UI_speed, unidades.Speed, "Speed", readOnly=True, retornar=False)
        self.velocidad.setStatusTip(QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_1.addWidget(self.velocidad,20,1,1,1)
        self.gridLayout_1.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Región", None, QtGui.QApplication.UnicodeUTF8)),21,0,1,1)
        self.region=Entrada_con_unidades(None, int, None, readOnly=True)
#        self.region = QtGui.QLineEdit()
#        self.region.setFixedSize(QtCore.QSize(85,24))
#        self.region.setReadOnly(True)
#        self.region.setAlignment(QtCore.Qt.AlignRight)
        self.gridLayout_1.addWidget(self.region,21,1,1,1)
        self.botonAdd=QtGui.QPushButton()
        self.botonAdd.setEnabled(False)
        self.botonAdd.setText(QtGui.QApplication.translate("SteamTables", "Añadir", None, QtGui.QApplication.UnicodeUTF8))
        self.botonAdd.setStatusTip(QtGui.QApplication.translate("SteamTables", "Añadir a la lista de puntos representados en la gráfica", None, QtGui.QApplication.UnicodeUTF8))
        self.botonAdd.clicked.connect(self.botonAdd_clicked)
        self.gridLayout_1.addWidget(self.botonAdd,22,0,1,1)
        self.botonLista=QtGui.QPushButton()
        self.botonLista.setMaximumWidth(80)
        self.botonLista.setText(QtGui.QApplication.translate("SteamTables", "Lista", None, QtGui.QApplication.UnicodeUTF8))
        self.botonLista.setStatusTip(QtGui.QApplication.translate("SteamTables", "Mostrar lista de puntos específicos representados en la gráfica", None, QtGui.QApplication.UnicodeUTF8))
        self.botonLista.clicked.connect(self.botonLista_clicked)
        self.gridLayout_1.addWidget(self.botonLista,22,1,1,2)
        self.gridLayout_1.addItem(QtGui.QSpacerItem(72, 34, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding), 23, 1, 1, 3)
        self.mostrarUnidades()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget_Puntos)
        self.dockWidget_Puntos.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        
        #Iniciar valores de widgets
        Ejes=["p,T", "p,h", "p,s", "p,v", "T,s", "T,x"]
        for i in Ejes:
            self.ejesTabla.addItem(i)
            self.variablesCalculo.addItem(i)
        Ejes2D=["p", "T", "s", "h", "u", "v"]
        for i in Ejes2D:
            self.ejeX.addItem(i)
            self.ejeY.addItem(i)
            
        self.matriz=[]
        self.saturacion=[]
        self.isoterma=[]
        self.isobara=[]
        self.isoentropica=[]
        self.isoentalpica=[]
        self.isocora=[]
        self.isoX=[]
        self.factorx, self.factory, self.factorz, self.factorx2, self.factory2=(0, 0, 0, 0, 0)
        self.ejeY_visible=0

        
        #Cargar configuración
        if self.Config.has_section("Table"):
            self.ejesTabla.setCurrentIndex(self.Config.getint("Table","Axis"))
            self.ejesTabla_currentIndexChanged(self.Config.getint("Table","Axis"))
            self.variableTabla.setCurrentIndex(self.Config.getint("Table","Calculate"))
            self.abscisaInicio.setText(self.Config.get("Table","x_start"))
            self.abscisaFin.setText(self.Config.get("Table","x_end"))
            self.abscisaIntervalo.setText(self.Config.get("Table","x_step"))
            self.ordenadaInicio.setText(self.Config.get("Table","y_start"))
            self.ordenadaFin.setText(self.Config.get("Table","y_end"))
            self.ordenadaIntervalo.setText(self.Config.get("Table","y_step"))
        if self.Config.has_section("General"):
            self.actionDibujarSaturacion.setChecked(self.Config.getboolean("General","Sat"))
            self.actionMostrarPuntos.setChecked(self.Config.getboolean("General","Points"))
            self.actionMostrarBarra.setChecked(self.Config.getboolean("General","Toolbar"))
            self.toolbar2D.setVisible(self.actionMostrarBarra.isChecked())
            self.toolbar3D.setVisible(self.actionMostrarBarra.isChecked())
            self.actionMostrarDelta.setChecked(self.Config.getboolean("General","Delta"))
            self.delta.setVisible(self.actionMostrarDelta.isChecked())
            self.action2D.setChecked(self.Config.getboolean("General","2D"))
            self.d2(self.action2D.isChecked())
            if self.Config.getboolean("General","Plot"):
                self.toolBox.setCurrentIndex(1)
            self.checkIsoTherm.setChecked(self.Config.getboolean("General","Isotherm"))
            self.checkIsoBar.setChecked(self.Config.getboolean("General","Isobar"))
            self.checkIsoEnth.setChecked(self.Config.getboolean("General","Isoenthalpic"))
            self.checkIsoEntr.setChecked(self.Config.getboolean("General","Isoentropic"))
            self.checkIsoVol.setChecked(self.Config.getboolean("General","Isochor"))
            self.checkIsoX.setChecked(self.Config.getboolean("General","Isoquality"))
        if self.Config.has_section("2D"):
            self.ejeX.setCurrentIndex(self.ejeX.findText(self.Config.get("2D", "Xvariable")))
            self.ejeXChanged(self.ejeX.currentIndex())
            self.ejeX_escala.setChecked(self.Config.getboolean("2D", "XScale"))
            self.ejeX_min[self.ejeX.currentIndex()].setValue(self.Config.getfloat("2D", "XMin"))
            self.ejeX_max[self.ejeX.currentIndex()].setValue(self.Config.getfloat("2D", "XMax"))
            self.ejeY.setCurrentIndex(self.ejeY.findText(self.Config.get("2D", "Yvariable")))
            self.ejeYChanged()
            self.ejeY_escala.setChecked(self.Config.getboolean("2D", "YScale"))
            self.ejeY_min[self.ejeY_visible].setValue(self.Config.getfloat("2D", "YMin"))
            self.ejeY_max[self.ejeY_visible].setValue(self.Config.getfloat("2D", "YMax"))
            self.rejilla.setChecked(self.Config.getboolean("2D", "Grid"))
        if self.Config.has_section("Points"):
            self.variablesCalculo.setCurrentIndex(self.Config.getint("Points", 'Variable'))
            self.variablesCalculo_currentIndexChanged(self.Config.getint("Points", 'Variable'))
            i=0
            self.puntos=[]
            while True:
                try:
                    punto=map(float, self.Config.get("Points", str(i)).split(","))
                except: break
                if punto[0]==0.0:
                    self.puntos.append(steam_Tx(punto[1], punto[2]))
                else:
                    self.puntos.append(steam_pT(punto[2], punto[1]))
                i+=1
            self.punto=self.puntos[-1]
            self.botonAdd.setEnabled(True)
            self.mostrarPropiedades()
        
        self.Isoterma=Iso()
        self.Isobara=Iso()
        self.Isoentropica=Iso()
        self.Isoentalpica=Iso()
        self.Isocora=Iso()
        self.IsoX=Iso()
        self.definirIsolineas()
    
        self.ejesTabla.currentIndexChanged.connect(self.ejesTabla_currentIndexChanged)
        self.variablesCalculo.currentIndexChanged.connect(self.variablesCalculo_currentIndexChanged)
        self.variableTabla.currentIndexChanged.connect(self.Calcular_Propiedades)
        self.ejeX.currentIndexChanged.connect(self.ejeXChanged)
        self.ejeY.currentIndexChanged.connect(self.ejeYChanged)
        self.checkIsoTherm.toggled.connect(self.mostrarIsoterma)
        self.checkIsoBar.toggled.connect(self.mostrarIsobara)
        self.checkIsoEnth.toggled.connect(self.mostrarIsoentalpica)
        self.checkIsoEntr.toggled.connect(self.mostrarIsoentropica)
        self.checkIsoVol.toggled.connect(self.mostrarIsocora)
        self.checkIsoX.toggled.connect(self.mostrarIsoX)


    def ayuda(self):
        open_new_tab("http://freesteam.sourceforge.net/example.php")


    def acerca(self):
        QtGui.QMessageBox.about(self,"Acerca de" ,"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'Nimbus Sans L'; font-size:9pt; font-weight:400; font-style:normal;">\n<table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="2" cellpadding="0">\n<tr>\n<td style=" vertical-align:top;">\n<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">freesteam</span> is an open source implementation of international-standard IAPWS-IF97 steam tables from the <a href="http://www.iapws.org"><span style=" text-decoration: underline; color:#0000ff;">International Association for the Properties of Water and Steam</span></a> (IAPWS). <span style=" font-weight:600;">freesteam</span> lets you compute water and steam properties for a wide range of pressures and temperatures: you can specify the state of the steam in terms of a variety of combinations of 'known' properties, then freesteam will solve and allow you to query to find the values of the 'unknown' properties.</p>\n<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Website: <a href="http://freesteam.sourceforge.net/"><span style=" text-decoration: underline; color:#0000ff;">http://freesteam.sourceforge.net/</span></a></p></td></tr></table></body></html>""")
        
    def acercaQt(self):
        QtGui.QMessageBox.aboutQt(self,"Acerca de Qt" )

    def exporttoCSV(self):
        """Guarda los datos de la tabla en un archivo csv"""
        fname = QtGui.QFileDialog.getSaveFileName(self, QtGui.QApplication.translate("SteamTables", u"Exportar datos", None, QtGui.QApplication.UnicodeUTF8), "./", "CSV (*.csv);;All archives (*.*)")
        if fname:
            texto = writer(open(fname, 'wb'), delimiter='\t')
            texto.writerow([""]+[str(i) for i in self.xdata[0]])
            for i, fila in enumerate(self.zdata):
                texto.writerow([str(self.ydata[i][0])]+[str(i) for i in fila])

    def preferencias(self):
        """Muestra el diálogo de configuración de preferencias"""
        dialog=Preferences()
        if dialog.exec_():
            self.Config.read("UI_steamTablesrc")
            self.actualizarConfiguracion()
            self.definirIsolineas()
        
    def closeEvent(self, event):
        """Guarda la configuración antes de salir"""
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if not Config.has_section("Table"):
            Config.add_section("Table")
        Config.set("Table", "Axis", self.ejesTabla.currentIndex())
        Config.set("Table", "Calculate", self.variableTabla.currentIndex())
        Config.set("Table", "x_start", self.abscisaInicio.text())
        Config.set("Table", "x_end", self.abscisaFin.text())
        Config.set("Table", "x_step", self.abscisaIntervalo.text())
        Config.set("Table", "y_start", self.ordenadaInicio.text())
        Config.set("Table", "y_end", self.ordenadaFin.text())
        Config.set("Table", "y_step", self.ordenadaIntervalo.text())
        if not Config.has_section("General"):
            Config.add_section("General")
        Config.set("General", "Sat", self.actionDibujarSaturacion.isChecked())
        Config.set("General", "Points", self.actionMostrarPuntos.isChecked())
        Config.set("General", "Toolbar", self.actionMostrarBarra.isChecked())
        Config.set("General", "Delta", self.actionMostrarDelta.isChecked())
        Config.set("General", "2D", self.action2D.isChecked())
        Config.set("General", "Plot", self.page_Plot.isVisible())
        Config.set("General", "Isotherm", self.checkIsoTherm.isChecked())
        Config.set("General", "Isobar", self.checkIsoBar.isChecked())
        Config.set("General", "Isoenthalpic", self.checkIsoEnth.isChecked())
        Config.set("General", "Isoentropic", self.checkIsoEntr.isChecked())
        Config.set("General", "Isochor", self.checkIsoVol.isChecked())
        Config.set("General", "Isoquality", self.checkIsoX.isChecked())
        if not Config.has_section("2D"):
            Config.add_section("2D")
        Config.set("2D", "Xvariable", self.ejeX.currentText())
        Config.set("2D", "XScale", self.ejeX_escala.isChecked())
        Config.set("2D", "XMin", self.ejeX_min[self.ejeX.currentIndex()].value)
        Config.set("2D", "XMax", self.ejeX_max[self.ejeX.currentIndex()].value)
        Config.set("2D", "Yvariable", self.ejeY.currentText())
        Config.set("2D", "YScale", self.ejeY_escala.isChecked())
        Config.set("2D", "YMin", self.ejeY_min[self.ejeY_visible].value)
        Config.set("2D", "YMax", self.ejeY_max[self.ejeY_visible].value)
        Config.set("2D", "Grid", self.rejilla.isChecked())
        if len(self.puntos)>0:
            Config.remove_section("Points")
            Config.add_section("Points")
            for i, punto in enumerate(self.puntos):
                if punto.region=="\x04":
                    Config.set("Points", str(i), "0"+","+str(punto.T)+","+str(punto.x))
                else:
                    Config.set("Points", str(i), "1"+","+str(punto.T)+","+str(punto.p))
            Config.set("Points", "Variable", self.variablesCalculo.currentIndex())
        Config.write(open("UI_steamTablesrc", "w"))
        event.accept()
        
                
                
    #Controles
    def ejesTabla_currentIndexChanged(self, indice):
        """Hace los cambios pertinentes en la gui cuando se cambian los ejes de la tabla 3D:
            Actualiza unidades mostradas en la entrada de datos de la tabla
            Actualiza los checkbox de isolineas habilitados (todos menos los de los ejes x e y)"""
        if indice==0:
            self.rellenar_variableTabla(0, 1)
            self.label_26.setText(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Pressure").text())
            self.label_27.setText(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Temperature").text())
            self.checkIsoBar.setEnabled(False)
            self.checkIsoTherm.setEnabled(False)
            self.checkIsoBar.setChecked(False)
            self.checkIsoTherm.setChecked(False)
            self.checkIsoEntr.setEnabled(True)
            self.checkIsoEnth.setEnabled(True)
            self.checkIsoVol.setEnabled(True)
        elif indice==1:
            self.rellenar_variableTabla(0, 3)
            self.label_26.setText(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Pressure").text())
            self.label_27.setText(QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Enthalpy").text())
            self.checkIsoBar.setEnabled(False)
            self.checkIsoBar.setChecked(False)
            self.checkIsoTherm.setEnabled(True)
            self.checkIsoEntr.setEnabled(True)
            self.checkIsoEnth.setEnabled(False)
            self.checkIsoEnth.setChecked(False)
            self.checkIsoVol.setEnabled(True)
        elif indice==2:
            self.rellenar_variableTabla(0, 4)
            self.label_26.setText(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Pressure").text())
            self.label_27.setText(QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificHeat", "Entropy").text())
            self.checkIsoBar.setEnabled(False)
            self.checkIsoBar.setChecked(False)
            self.checkIsoTherm.setEnabled(True)
            self.checkIsoEntr.setEnabled(False)
            self.checkIsoEntr.setChecked(False)
            self.checkIsoEnth.setEnabled(True)
            self.checkIsoVol.setEnabled(True)
        elif indice==3:
            self.rellenar_variableTabla(0, 2)
            self.label_26.setText(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Pressure").text())
            self.label_27.setText(QtGui.QApplication.translate("SteamTables", "Volumen", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificVolume").text())
            self.checkIsoBar.setEnabled(False)
            self.checkIsoBar.setChecked(False)
            self.checkIsoTherm.setEnabled(True)
            self.checkIsoEntr.setEnabled(True)
            self.checkIsoEnth.setEnabled(True)
            self.checkIsoVol.setEnabled(False)
            self.checkIsoVol.setChecked(False)
        elif indice==4:
            self.rellenar_variableTabla(1, 4)
            self.label_26.setText(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Temperature").text())
            self.label_27.setText(QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("SpecificHeat", "Entropy").text())
            self.checkIsoBar.setEnabled(True)
            self.checkIsoTherm.setEnabled(False)
            self.checkIsoTherm.setChecked(False)
            self.checkIsoEntr.setEnabled(False)
            self.checkIsoEntr.setChecked(False)
            self.checkIsoEnth.setEnabled(True)
            self.checkIsoVol.setEnabled(True)
        elif indice==5:
            self.rellenar_variableTabla(1, 13)
            self.label_26.setText(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8)+", %s" %config.Configuracion("Temperature").text())
            self.label_27.setText(QtGui.QApplication.translate("SteamTables", "Calidad", None, QtGui.QApplication.UnicodeUTF8))
            self.checkIsoBar.setEnabled(True)
            self.checkIsoTherm.setEnabled(False)
            self.checkIsoTherm.setChecked(False)
            self.checkIsoEntr.setEnabled(True)
            self.checkIsoEnth.setEnabled(True)
            self.checkIsoVol.setEnabled(True)

    def variablesCalculo_currentIndexChanged(self, indice):
        """Hace los cambios pertinentes en la gui cuando se cambian las variables impuestas de los puntos especificados:
            Resalta las variables a introducir
            Fija las el resto de variables para evitar su edición por el usuario"""
        if indice==0:
            self.presion.setReadOnly(False)
            self.presion.setResaltado(True)
            self.temperatura.setReadOnly(False)
            self.temperatura.setResaltado(True)
            self.entalpia.setReadOnly(True)
            self.entalpia.setResaltado(False)
            self.entropia.setReadOnly(True)
            self.entropia.setResaltado(False)
            self.volumen.setReadOnly(True)
            self.volumen.setResaltado(False)
            self.fraccionVapor.setReadOnly(True)
            self.fraccionVapor.setResaltado(False)
            self.presion.setRetornar(True)
            self.temperatura.setRetornar(True)
            self.entalpia.setRetornar(False)
            self.entropia.setRetornar(False)
            self.volumen.setRetornar(False)
        elif indice==1:
            self.entalpia.setReadOnly(False)
            self.entalpia.setResaltado(True)
            self.presion.setReadOnly(False)
            self.presion.setResaltado(True)
            self.temperatura.setReadOnly(True)
            self.temperatura.setResaltado(False)
            self.entropia.setReadOnly(True)
            self.entropia.setResaltado(False)
            self.volumen.setReadOnly(True)
            self.volumen.setResaltado(False)
            self.fraccionVapor.setReadOnly(True)
            self.fraccionVapor.setResaltado(False)
            self.presion.setRetornar(True)
            self.temperatura.setRetornar(False)
            self.entalpia.setRetornar(True)
            self.entropia.setRetornar(False)
            self.volumen.setRetornar(False)
        elif indice==2:
            self.entropia.setReadOnly(False)
            self.entropia.setResaltado(True)
            self.presion.setReadOnly(False)
            self.presion.setResaltado(True)
            self.temperatura.setReadOnly(True)
            self.temperatura.setResaltado(False)
            self.entalpia.setReadOnly(True)
            self.entalpia.setResaltado(False)
            self.volumen.setReadOnly(True)
            self.volumen.setResaltado(False)
            self.fraccionVapor.setReadOnly(True)
            self.fraccionVapor.setResaltado(False)
            self.presion.setRetornar(True)
            self.temperatura.setRetornar(False)
            self.entalpia.setRetornar(False)
            self.entropia.setRetornar(True)
            self.volumen.setRetornar(False)
        elif indice==3:
            self.volumen.setReadOnly(False)
            self.volumen.setResaltado(True)
            self.presion.setReadOnly(False)
            self.presion.setResaltado(True)
            self.temperatura.setReadOnly(True)
            self.temperatura.setResaltado(False)
            self.entropia.setReadOnly(True)
            self.entropia.setResaltado(False)
            self.entalpia.setReadOnly(True)
            self.entalpia.setResaltado(False)
            self.fraccionVapor.setReadOnly(True)
            self.fraccionVapor.setResaltado(False)
            self.presion.setRetornar(True)
            self.temperatura.setRetornar(False)
            self.entalpia.setRetornar(False)
            self.entropia.setRetornar(False)
            self.volumen.setRetornar(True)
        elif indice==4:
            self.entropia.setReadOnly(False)
            self.entropia.setResaltado(True)
            self.temperatura.setReadOnly(False)
            self.temperatura.setResaltado(True)
            self.entalpia.setReadOnly(True)
            self.entalpia.setResaltado(False)
            self.presion.setReadOnly(True)
            self.presion.setResaltado(False)
            self.volumen.setReadOnly(True)
            self.volumen.setResaltado(False)
            self.fraccionVapor.setReadOnly(True)
            self.fraccionVapor.setResaltado(False)
            self.presion.setRetornar(False)
            self.temperatura.setRetornar(True)
            self.entalpia.setRetornar(False)
            self.entropia.setRetornar(True)
            self.volumen.setRetornar(False)
        elif indice==5:
            self.fraccionVapor.setReadOnly(False)
            self.fraccionVapor.setResaltado(True)
            self.temperatura.setReadOnly(False)
            self.temperatura.setResaltado(True)
            self.entalpia.setReadOnly(True)
            self.entalpia.setResaltado(False)
            self.presion.setReadOnly(True)
            self.presion.setResaltado(False)
            self.volumen.setReadOnly(True)
            self.volumen.setResaltado(False)
            self.entropia.setReadOnly(True)
            self.entropia.setResaltado(False)
            self.presion.setRetornar(False)
            self.temperatura.setRetornar(True)
            self.entalpia.setRetornar(False)
            self.entropia.setRetornar(False)
            self.volumen.setRetornar(False)

    def presion_editingFinished(self):
        if self.variablesCalculo.currentIndex()==0:
            otro=self.temperatura
        elif self.variablesCalculo.currentIndex()==1:
            otro=self.entalpia
        elif self.variablesCalculo.currentIndex()==2:
            otro=self.entropia
        else:
            otro=self.volumen
        if otro.value and self.presion.value:
            self.calcularPropiedades()
        
    def temperatura_editingFinished(self):
        if self.variablesCalculo.currentIndex()==0:
            otro=self.presion
        elif self.variablesCalculo.currentIndex()==4:
            otro=self.entropia
        else:
            otro=self.fraccionVapor
        if otro.value and self.temperatura.value:
            self.calcularPropiedades()
        
    def entalpia_editingFinished(self):
        if self.presion.value and self.entalpia.value:
            self.calcularPropiedades()

    def entropia_editingFinished(self):
        if self.variablesCalculo.currentIndex()==2:
            otro=self.presion
        else:
            otro=self.temperatura
        if otro.value and self.entropia.value:
            self.calcularPropiedades()

    def volumen_editingFinished(self):
        if self.presion.value and self.volumen.value:
            self.calcularPropiedades()

    def fraccionVapor_editingFinished(self):
        if self.fraccionVapor.value>1.0 or self.fraccionVapor.value<0.0:
            self.fraccionVapor.clear()
            self.fraccionVapor.setFocus()
            valido=False
        else:
            valido=True
        if self.temperatura.value and valido:
            self.calcularPropiedades()

    def botonAdd_clicked(self):
        """Añade el punto especificado actual a la lista"""
        self.puntos.append(self.punto)
        self.calcularPuntos()
        self.dibujar()
    
    def botonLista_clicked(self):
        """Muestra la lista de puntos especificados por el usuario"""
        dialog=Ventana_Lista_Puntos(self.puntos, self)
        if dialog.exec_():
            self.puntos=dialog.puntos
            if dialog.group1.checkedId()!=-1:
                self.delta.setPunto(0, self.puntos[-2-dialog.group1.checkedId()])
            if dialog.group2.checkedId()!=-1:
                self.delta.setPunto(1, self.puntos[-2-dialog.group2.checkedId()])
            if self.delta.punto1 and self.delta.punto2:    
                self.plot_Delta()
            self.calcularPuntos()
            self.dibujar()

    def botonCalcular_clicked(self):
        """Método que calcula todos los datos de las tablas y gráficos"""
        self.progresbar.setVisible(True)
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando matriz...", None, QtGui.QApplication.UnicodeUTF8))
        self.progresbar.setValue(0)
        QtGui.QApplication.processEvents()
        self.calcularMatriz(0, 30)
        self.Calcular_Propiedades(35, 5)
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando línea de saturación...", None, QtGui.QApplication.UnicodeUTF8))
        QtGui.QApplication.processEvents()
        self.calcularSaturacion()
        if len(self.puntos)>0:
            self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando puntos personalizados...", None, QtGui.QApplication.UnicodeUTF8))
            QtGui.QApplication.processEvents()
            self.calcularPuntos()
        self.calcularIsoterma(40, 10)
        self.calcularIsobara(50, 10)
        self.calcularIsoentropica(60, 10)
        self.calcularIsoentalpica(70, 10)
        self.calcularIsocora(80, 10)
        self.calcularIsoX(90, 10)
        self.progresbar.setValue(100)
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Dibujando...", None, QtGui.QApplication.UnicodeUTF8))
        QtGui.QApplication.processEvents()
        self.dibujar()
        self.progresbar.setVisible(False)
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Listo", None, QtGui.QApplication.UnicodeUTF8))

    #Opciones gráficos
    def d2(self, activado):
        """Se ejecuta si se cambia el modo de gráfico a 2D"""
        self.dockWidget_Tabla.setVisible(not activado)
        self.dockWidget_2D.setVisible(activado)
        self.tabla.setVisible(not activado)
        self.diagrama2D.setVisible(activado)
        self.toolbar2D.setVisible(self.actionMostrarBarra.isChecked() and activado)
        self.diagrama3D.setVisible(not activado)
        self.toolbar3D.setVisible(self.actionMostrarBarra.isChecked() and not activado)
        self.checkIsoBar.setEnabled(True)
        self.checkIsoTherm.setEnabled(True)
        self.checkIsoEntr.setEnabled(True)
        self.checkIsoEnth.setEnabled(True)
        self.checkIsoVol.setEnabled(True)

    def click(self, event):
        if event.xdata and event.ydata:
            if self.ejeX.currentText()=="p":
                if self.ejeY.currentText()=="T":
                    vapor=steam_pT(event.xdata*self.factorx2, self.conv_T_inv(event.ydata))
                elif self.ejeY.currentText()=="s":
                    vapor=steam_ps(event.xdata*self.factorx2, event.ydata*self.factory2)
                elif self.ejeY.currentText()=="h":
                    vapor=steam_ph(event.xdata*self.factorx2, event.ydata*self.factory2)
                elif self.ejeY.currentText()=="u":
                    vapor=self.definirVapor(steam_ps, event.xdata*self.factorx2, lambda z: steam_ps(event.xdata*self.factorx2, float(z)).u-event.ydata*self.factory2, 5000., 1)
                elif self.ejeY.currentText()=="v":
                    vapor=steam_pv(event.xdata*self.factorx2, event.ydata*self.factory2)
            elif self.ejeX.currentText()=="T":
                if self.ejeY.currentText()=="p":
                    vapor=steam_pT(event.ydata*self.factory2, self.conv_T_inv(event.xdata))
                elif self.ejeY.currentText()=="s":
                    vapor=steam_Ts(self.conv_T_inv(event.xdata), event.ydata*self.factory2)
                elif self.ejeY.currentText()=="h":
                    vapor=self.definirVapor(steam_ph, event.ydata*self.factory2, lambda z: steam_ph(float(z), event.ydata*self.factory2).T-self.conv_T_inv(event.xdata), 100.)
                elif self.ejeY.currentText()=="u":
                    if steam_Tx(self.conv_T_inv(event.xdata), 0).u<event.ydata*self.factory2<steam_Tx(self.conv_T_inv(event.xdata), 1).u:
                        vapor=self.definirVapor(steam_Tx, self.conv_T_inv(event.xdata), lambda z: steam_Tx(self.conv_T_inv(event.xdata), float(z)).u-event.ydata*self.factory2, 0.5, 1)
                    else:
                        vapor=self.definirVapor(steam_pT, self.conv_T_inv(event.xdata), lambda z: steam_pT(float(z), self.conv_T_inv(event.xdata)).u-event.ydata*self.factory2, 100.)
                elif self.ejeY.currentText()=="v":
                    vapor=self.definirVapor(steam_pv, event.ydata*self.factory2, lambda z: steam_pv(float(z), event.ydata*self.factory2).T-self.conv_T_inv(event.xdata), 100.)
            elif self.ejeX.currentText()=="s":
                if self.ejeY.currentText()=="p":
                    vapor=steam_ps(event.ydata*self.factory2, event.xdata*self.factorx2)
                elif self.ejeY.currentText()=="T":
                    vapor=steam_Ts(self.conv_T_inv(event.ydata), event.xdata*self.factorx2)
                elif self.ejeY.currentText()=="h":
                    vapor=self.definirVapor(steam_ph, event.ydata*self.factory2, lambda z: steam_ph(float(z), event.ydata*self.factory2).s-event.xdata*self.factorx2, 100.)
                elif self.ejeY.currentText()=="u":
                    vapor=self.definirVapor(steam_ps, event.xdata*self.factorx2, lambda z: steam_ps(float(z), event.xdata*self.factorx2).u-event.ydata*self.factory2, 100.)
                elif self.ejeY.currentText()=="v":
                    vapor=self.definirVapor(steam_pv, event.ydata*self.factory2, lambda z: steam_pv(float(z), event.ydata*self.factory2).s-event.xdata*self.factorx2, 100.)
            elif self.ejeX.currentText()=="h":
                if self.ejeY.currentText()=="p":
                    vapor=steam_ph(event.ydata*self.factory2, event.xdata*self.factorx2)
                elif self.ejeY.currentText()=="T":
                    vapor=self.definirVapor(steam_ph, event.xdata*self.factorx2, lambda z: steam_ph(float(z), event.xdata*self.factorx2).T-self.conv_T_inv(event.ydata), 100.)
                elif self.ejeY.currentText()=="s":
                    vapor=self.definirVapor(steam_ph, event.xdata*self.factorx2, lambda z: steam_ph(float(z), event.xdata*self.factorx2).s-event.ydata*self.factory2, 100.)
                elif self.ejeY.currentText()=="u":
                    vapor=self.definirVapor(steam_ph, event.xdata*self.factorx2, lambda z: steam_ph(float(z), event.xdata*self.factorx2).u-event.ydata*self.factory2, 100.)
                elif self.ejeY.currentText()=="v":
                    vapor=self.definirVapor(steam_pv, event.ydata*self.factory2, lambda z: steam_pv(float(z), event.ydata*self.factory2).h-event.xdata*self.factorx2, 100.)
            elif self.ejeX.currentText()=="u":
                if self.ejeY.currentText()=="p":
                    vapor=self.definirVapor(steam_ps, event.ydata*self.factory2, lambda z: steam_ps(event.ydata*self.factory2, float(z)).u-event.xdata*self.factorx2, 5000., 1)
                elif self.ejeY.currentText()=="T":
                    if steam_Tx(self.conv_T_inv(event.ydata), 0).u<event.xdata*self.factorx2<steam_Tx(self.conv_T_inv(event.ydata), 1).u:
                        vapor=self.definirVapor(steam_Tx, self.conv_T_inv(event.ydata), lambda z: steam_Tx(self.conv_T_inv(event.ydata), float(z)).u-event.xdata*self.factorx2, 0.5, 1)
                    else:
                        vapor=self.definirVapor(steam_pT, self.conv_T_inv(event.ydata), lambda z: steam_pT(float(z), self.conv_T_inv(event.ydata)).u-event.xdata*self.factorx2, 100.)
                elif self.ejeY.currentText()=="s":
                    vapor=self.definirVapor(steam_ps, event.ydata*self.factory2, lambda z: steam_ps(float(z), event.ydata*self.factory2).u-event.xdata*self.factorx2, 100.)
                elif self.ejeY.currentText()=="h":
                    vapor=self.definirVapor(steam_ph, event.ydata*self.factory2, lambda z: steam_ph(float(z), event.ydata*self.factory2).u-event.xdata*self.factorx2, 100.)
                elif self.ejeY.currentText()=="v":
                    vapor=self.definirVapor(steam_pv, event.ydata*self.factory2, lambda z: steam_pv(float(z), event.ydata*self.factory2).u-event.xdata*self.factorx2, 100.)
            elif self.ejeX.currentText()=="v":
                if self.ejeY.currentText()=="p":
                    vapor=steam_pv(event.ydata*self.factory2, event.xdata*self.factorx2)
                elif self.ejeY.currentText()=="T":
                    vapor=self.definirVapor(steam_pv, event.xdata*self.factorx2, lambda z: steam_pv(float(z), event.xdata*self.factoryx).T-self.conv_T_inv(event.ydata), 100.)
                elif self.ejeY.currentText()=="s":
                    vapor=self.definirVapor(steam_pv, event.xdata*self.factorx2, lambda z: steam_pv(float(z), event.xdata*self.factorx2).s-event.ydata*self.factory2, 100.)
                elif self.ejeY.currentText()=="h":
                    vapor=self.definirVapor(steam_pv, event.xdata*self.factorx2, lambda z: steam_pv(float(z), event.xdata*self.factorx2).h-event.ydata*self.factory2, 100.)
                elif self.ejeY.currentText()=="u":
                    vapor=self.definirVapor(steam_pv, event.xdata*self.factorx2, lambda z: steam_pv(float(z), event.xdata*self.factorx2).u-event.ydata*self.factory2, 100.)
                    
            self.delta.addPunto(vapor)
            
            if self.delta.punto1 and self.delta.punto2:
                self.plot_Delta()

    def plot_Delta(self):
        if self.ejeX.currentText()=="p":
            x=[punto.p/self.factorx2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeX.currentText()=="T":
            x=[self.conv_T_inv(punto.T) for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeX.currentText()=="h":
            x=[punto.h/self.factorx2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeX.currentText()=="v":
            x=[punto.v/self.factorx2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeX.currentText()=="s":
            x=[punto.s/self.factorx2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeX.currentText()=="u":
            x=[punto.u/self.factorx2 for punto in [self.delta.punto1, self.delta.punto2]]
        if self.ejeY.currentText()=="p":
            y=[punto.p/self.factory2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeY.currentText()=="T":
            y=[self.conv_T_inv(punto.T) for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeY.currentText()=="h":
            y=[punto.h/self.factory2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeY.currentText()=="v":
            y=[punto.v/self.factory2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeY.currentText()=="s":
            y=[punto.s/self.factory2 for punto in [self.delta.punto1, self.delta.punto2]]
        elif self.ejeY.currentText()=="u":
            y=[punto.u/self.factory2 for punto in [self.delta.punto1, self.delta.punto2]]

        self.diagrama2D.lineDelta.xytext=(x[0], y[0])
        self.diagrama2D.lineDelta.xy=(x[1], y[1])
        self.diagrama2D.draw() 
            
    def definirVapor(self, definicion, y, iteracion=None, Zo=None, orden=0):
        """Define el vapor a partir de las coordenadas en el gráfico y de las magnitudes de los ejes del gráfico
        definicion: función de definición del vapor (steam_pT, steam_Tx...), si no está disponible será necesario indicar la función de iteración y aqui irían las variables de los ejes del diagrama
        y: valor de la variable conocida del gráfico
        iteracion: función de definición del vapor usada en la iteración
        Zo: valor inicial de iteración
        orden: indice que indica la posición de la variable de iteración
        """
        z=fsolve(iteracion, Zo)
        if orden:
            vapor=definicion(y, z)
        else:
            vapor=definicion(z, y)
        return vapor
            
        
        
        

    def mostrarBarra(self, bool):
        """Muestra la toolbar de matplotlib"""
        self.toolbar2D.setVisible(bool and self.action2D.isChecked())
        self.toolbar3D.setVisible(bool and self.action3D.isChecked())

    def mostrarDelta(self, bool):
        """Muestra las opciones de incremento de propiedades entre puntos"""
        self.delta.setVisible(bool)
        
    def mostrarPuntos(self, bool):
        """Muestra los puntos específicos"""
        for i in self.diagrama3D.puntos:
            i[0].set_visible(bool)
        for i in self.diagrama2D.puntos:
            i[0].set_visible(bool)
        self.diagrama3D.draw()
        self.diagrama2D.draw()
        
    def mostrarSaturacion(self, bool):
        """Muestra la línea de saturación"""
        self.diagrama3D.satliq[0].set_visible(bool)
        self.diagrama3D.satgas[0].set_visible(bool)
        self.diagrama2D.satliq[0].set_visible(bool)
        self.diagrama2D.satgas[0].set_visible(bool)
        self.diagrama3D.draw()
        self.diagrama2D.draw()

    def mostrarIsoentropica(self):
        """Muestra las líneas isoentrópicas"""
        for i in self.diagrama3D.Isoentropica:
            i[0].set_visible(self.checkIsoEntr.isChecked() and self.checkIsoEntr.isEnabled())
        for i in self.diagrama2D.Isoentropica:
            i[0].set_visible(self.checkIsoEntr.isChecked())
        for i in self.diagrama2D.Isoentropica_label:
            i.set_visible(self.checkIsoEntr.isChecked() and self.Isoentropica.label)
        self.diagrama3D.draw()
        self.diagrama2D.draw()
        
    def mostrarIsoentalpica(self, bool):
        """Muestra las líneas isoentálpicas"""
        for i in self.diagrama3D.Isoentalpica:
            i[0].set_visible(bool and  self.checkIsoEnth.isEnabled())
        for i in self.diagrama2D.Isoentalpica:
            i[0].set_visible(bool)
        for i in self.diagrama2D.Isoentalpica_label:
            i.set_visible(self.checkIsoEnth.isChecked() and self.Isoentalpica.label)
        self.diagrama3D.draw()
        self.diagrama2D.draw()

    def mostrarIsobara(self):
        """Muestra las líneas isobáras"""
        for i in self.diagrama3D.Isobara:
            i[0].set_visible(self.checkIsoBar.isChecked() and self.checkIsoBar.isEnabled())
        for i in self.diagrama2D.Isobara:
            i[0].set_visible(self.checkIsoBar.isChecked())
        for i in self.diagrama2D.Isobara_label:
            i.set_visible(self.checkIsoBar.isChecked() and self.Isobara.label)
        self.diagrama3D.draw()
        self.diagrama2D.draw()
        
    def mostrarIsoterma(self):
        """Muestra las líneas isotermas"""
        for i in self.diagrama3D.Isoterma:
            i[0].set_visible(self.checkIsoTherm.isChecked() and self.checkIsoTherm.isEnabled())
        for i in self.diagrama2D.Isoterma:
            i[0].set_visible(self.checkIsoTherm.isChecked())
        for i in self.diagrama2D.Isoterma_label:
            i.set_visible(self.checkIsoTherm.isChecked() and self.Isoterma.label)
        self.diagrama3D.draw()
        self.diagrama2D.draw()
        
    def mostrarIsocora(self):
        """Muestra las líneas isocoras"""
        for i in self.diagrama3D.Isocora:
            i[0].set_visible(self.checkIsoVol.isChecked() and self.checkIsoVol.isEnabled())
        for i in self.diagrama2D.Isocora:
            i[0].set_visible(self.checkIsoVol.isChecked())
        for i in self.diagrama2D.Isocora_label:
            i.set_visible(self.checkIsoVol.isChecked() and self.Isocora.label)
        self.diagrama3D.draw()
        self.diagrama2D.draw()
        
    def mostrarIsoX(self):
        """Muestra las líneas con igual fración de vapor"""
        for i in self.diagrama3D.IsoX:
            i[0].set_visible(self.checkIsoX.isChecked())
        for i in self.diagrama2D.IsoX:
            i[0].set_visible(self.checkIsoX.isChecked())
        for i in self.diagrama2D.IsoX_label:
            i.set_visible(self.checkIsoX.isChecked() and self.IsoX.label)
        self.diagrama3D.draw()
        self.diagrama2D.draw()


    def rellenar_variableTabla(self, i, j):
        """Actualiza los elementos disponibles para el tercer eje en función de los elejidos como ejes principales i, j"""
        self.variableTabla.clear()
        variables=[QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8),  QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8),  QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8)]
        del variables[j]
        del variables[i]
        for nombre in variables:
            self.variableTabla.addItem(nombre)

    def ejeXChanged(self, int):
        """Rellena las variables disponibles para el ejeY en el gráfico 2D, todos menos el que este activo en el ejeX"""
        self.ejeY.clear()
        Ejes2D=["p", "T", "s", "h", "u", "v"]
        del Ejes2D[int]
        for i in Ejes2D:
            self.ejeY.addItem(i)
            
        for i in self.ejeX_min:
            i.setVisible(False)
        self.ejeX_min[int].setVisible(True)
        for i in self.ejeX_max:
            i.setVisible(False)
        self.ejeX_max[int].setVisible(True)


    def ejeYChanged(self):
        unit=["p", "T", "s", "h", "u", "v"]
        int=unit.index(self.ejeY.currentText())
        self.ejeY_visible=int
        
        for i in self.ejeY_min:
            i.setVisible(False)
        self.ejeY_min[int].setVisible(True)
        for i in self.ejeY_max:
            i.setVisible(False)
        self.ejeY_max[int].setVisible(True)
        
            
    def dibujar(self):
        """Método que dibuja todos los datos pedidos"""
        self.progresbar.setValue(100)
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Dibujando...", None, QtGui.QApplication.UnicodeUTF8))
        QtGui.QApplication.processEvents()
        self.diagrama3D.plot_3D(self.etiquetas, self.xdata, self.ydata, self.zdata) 
        if len(self.puntos)>0:
            self.diagrama3D.plot_puntos(self.xi, self.yi, self.zi)
        self.diagrama3D.plot_sat(self.xsat, self.ysat, self.zsat)
        self.diagrama3D.plot_Isolinea("T", self.isoterma[0], self.isoterma[1], self.isoterma[2], self.Isoterma.Color, self.Isoterma.Grosor, self.Isoterma.Linea)
        self.diagrama3D.plot_Isolinea("P", self.isobara[0], self.isobara[1], self.isobara[2], self.Isobara.Color, self.Isobara.Grosor, self.Isobara.Linea)
        self.diagrama3D.plot_Isolinea("V", self.isocora[0], self.isocora[1], self.isocora[2], self.Isocora.Color, self.Isocora.Grosor, self.Isocora.Linea)
        self.diagrama3D.plot_Isolinea("H", self.isoentalpica[0], self.isoentalpica[1], self.isoentalpica[2], self.Isoentalpica.Color, self.Isoentalpica.Grosor, self.Isoentalpica.Linea)
        self.diagrama3D.plot_Isolinea("S", self.isoentropica[0], self.isoentropica[1], self.isoentropica[2], self.Isoentropica.Color, self.Isoentropica.Grosor, self.Isoentropica.Linea)
        self.diagrama3D.plot_Isolinea("X", self.isoX[0], self.isoX[1], self.isoX[2], self.IsoX.Color, self.IsoX.Grosor, self.IsoX.Linea)
        self.diagrama3D.axes3D.set_xlim3d(self.xdata[0][0], self.xdata[-1][-1])
        self.diagrama3D.axes3D.set_ylim3d(self.ydata[0][0], self.ydata[-1][-1])
        self.diagrama3D.axes3D.set_zlim3d(min(self.zdata), max(self.zdata))
        self.diagrama3D.draw()
        
        self.diagrama2D.plot_2D(self.etiquetas2, self.rejilla.isChecked())
        self.diagrama2D.plot_sat(self.xsat2, self.ysat2)
        self.diagrama2D.plot_Isolinea("T", self.isoterma2[0], self.isoterma2[1], self.isoterma[2], self.Isoterma.Color, self.Isoterma.Grosor, self.Isoterma.Linea)
        self.diagrama2D.plot_Isolinea("P", self.isobara2[0], self.isobara2[1], self.isobara[2], self.Isobara.Color, self.Isobara.Grosor, self.Isobara.Linea)
        self.diagrama2D.plot_Isolinea("V", self.isocora2[0], self.isocora2[1], self.isocora[2], self.Isocora.Color, self.Isocora.Grosor, self.Isocora.Linea)
        self.diagrama2D.plot_Isolinea("H", self.isoentalpica2[0], self.isoentalpica2[1], self.isoentalpica[2], self.Isoentalpica.Color, self.Isoentalpica.Grosor, self.Isoentalpica.Linea)
        self.diagrama2D.plot_Isolinea("S", self.isoentropica2[0], self.isoentropica2[1], self.isoentropica[2], self.Isoentropica.Color, self.Isoentropica.Grosor, self.Isoentropica.Linea)
        self.diagrama2D.plot_Isolinea("X", self.isoX2[0], self.isoX2[1], self.isoX[2], self.IsoX.Color, self.IsoX.Grosor, self.IsoX.Linea)
        if len(self.puntos)>0:
            self.diagrama2D.plot_puntos(self.xi2, self.yi2)

        self.diagrama2D.plot_labels("X", self.isoX2[2], self.isoX2[3], self.isoX2[4], self.isoX2[5], size=self.Config.get("General","fontSize"))
        self.diagrama2D.plot_labels("S", self.isoentropica2[2], self.isoentropica2[3], self.isoentropica2[4], self.isoentropica2[5], size=self.Config.get("General","fontSize"))
        self.diagrama2D.plot_labels("H", self.isoentalpica2[2], self.isoentalpica2[3], self.isoentalpica2[4], self.isoentalpica2[5], size=self.Config.get("General","fontSize"))
        self.diagrama2D.plot_labels("V", self.isocora2[2], self.isocora2[3], self.isocora2[4], self.isocora2[5], size=self.Config.get("General","fontSize"))
        self.diagrama2D.plot_labels("P", self.isobara2[2], self.isobara2[3], self.isobara2[4], self.isobara2[5], size=self.Config.get("General","fontSize"))
        self.diagrama2D.plot_labels("T", self.isoterma2[2], self.isoterma2[3], self.isoterma2[4], self.isoterma2[5], size=self.Config.get("General","fontSize"))

        self.mostrarSaturacion(self.actionDibujarSaturacion.isChecked())
        self.mostrarPuntos(self.actionMostrarPuntos.isChecked())
        self.mostrarIsoentropica()
        self.mostrarIsocora()
        self.mostrarIsoentalpica(self.checkIsoEnth.isChecked())
        self.mostrarIsobara()
        self.mostrarIsoterma()
        self.mostrarIsoX()
        self.mostrarPuntos(self.actionMostrarPuntos.isChecked())
        self.diagrama2D_ejeX()
        self.diagrama2D_ejeY()
        self.ejeX_log(self.ejeX_escala.isChecked())
        self.ejeY_log(self.ejeY_escala.isChecked())
        self.progresbar.setVisible(False)
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Listo...", None, QtGui.QApplication.UnicodeUTF8))

    def rejilla_toggled(self, bool):
        """Muestra o esconde la rejilla del gráfico 2D"""
        self.diagrama2D.axes2D.grid(bool)
        self.diagrama2D.draw()
        
    def diagrama2D_ejeX(self):
        """Define la orientación del eje x, creciente o decreciente"""
        if self.ejeX_min[self.ejeX.currentIndex()].value and self.ejeX_max[self.ejeX.currentIndex()].value:
            xmin=self.ejeX_min[self.ejeX.currentIndex()].value.config()
            xmax=self.ejeX_max[self.ejeX.currentIndex()].value.config()
            self.diagrama2D.axes2D.set_xlim(xmin, xmax)
            self.diagrama2D.axes2D.set_autoscalex_on(False)
        else:
            self.diagrama2D.axes2D.set_autoscalex_on(True)
        self.diagrama2D.draw()

    def diagrama2D_ejeY(self):
        """Define la orientación del eje y, creciente o decreciente"""
        if self.ejeY_min[self.ejeY_visible].value and self.ejeY_max[self.ejeY_visible].value:
            ymin=self.ejeY_min[self.ejeY_visible].value.config()
            ymax=self.ejeY_max[self.ejeY_visible].value.config()
            self.diagrama2D.axes2D.set_ylim(ymin, ymax)
            self.diagrama2D.axes2D.set_autoscaley_on(False)
        else:
            self.diagrama2D.axes2D.set_autoscaley_on(True)
        self.diagrama2D.draw()
        
    def ejeX_log(self, bool):
        """Define la escala del eje x, normal o logarítmica"""
        if bool:
            self.diagrama2D.axes2D.set_xscale("log")
        else:
            self.diagrama2D.axes2D.set_xscale("linear")
        self.diagrama2D.draw()

    def ejeY_log(self, bool):
        """Define la escala del eje y, normal o logarítmica"""
        if bool:
            self.diagrama2D.axes2D.set_yscale("log")
        else:
            self.diagrama2D.axes2D.set_yscale("linear")
        self.diagrama2D.draw()
    
    #Métodos de cálculo    
    def definirIsolineas(self):
        Isolineas=[self.Isoterma, self.Isobara, self.Isoentropica, self.Isoentalpica, self.Isocora, self.IsoX]
        iso=["Isotherm", "Isobar", "Isoentropic", "Isoenthalpic", "Isochor", "Isoquality"]
        for i, propiedad in enumerate(iso):
            if self.Config.has_section(propiedad):
                Isolineas[i].inicio=self.Config.getfloat(propiedad, 'Start')
                Isolineas[i].fin=self.Config.getfloat(propiedad, 'End')
                Isolineas[i].intervalo=self.Config.getfloat(propiedad, 'Step')
                Isolineas[i].Personalizar=self.Config.getboolean(propiedad, 'Custom')
                lista=[]
                if self.Config.get(propiedad, 'List')<>"":
                    for j in self.Config.get(propiedad, 'List').split(','):
                        lista.append(float(j))
                Isolineas[i].Lista=lista
                Isolineas[i].Critica=self.Config.getboolean(propiedad, 'Critic')
                Isolineas[i].Color=self.Config.get(propiedad, 'Color')
                Isolineas[i].Grosor=self.Config.getfloat(propiedad, 'lineWidth')
                Isolineas[i].Linea=self.Config.getint(propiedad, 'lineStyle')
                Isolineas[i].label=self.Config.getboolean(propiedad, 'Label')
                Isolineas[i].units=self.Config.getboolean(propiedad, 'Units')
                Isolineas[i].posicion=self.Config.getfloat(propiedad, 'Position')
    
    def factores_conversion(self):
        """Método que calcula los factores de conversión de unidades necesarios, tambien los textos"""
        indiceT=self.Config.getint("Units", "Temperature")
        if indiceT==0:
            self.conv_T=float
            self.conv_T_inv=float
        elif indiceT==1:
            self.conv_T=config.C2K
            self.conv_T_inv=config.K2C
        elif indiceT==2:
            self.conv_T=config.F2K
            self.conv_T_inv=config.K2F
        elif indiceT==3:
            self.conv_T=config.R2K
            self.conv_T_inv=config.K2R
        elif indiceT==4:
            self.conv_T=config.Re2K
            self.conv_T_inv=config.K2Re
            
        if self.ejesTabla.currentIndex()==0:
            abcisa="P, %s" % config.Configuracion("Pressure").text()
            ordenada="T, %s" % config.Configuracion("Temperature").text()
            self.factorx=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
            self.factory=0
        elif self.ejesTabla.currentIndex()==1:
            abcisa="P, %s" % config.Configuracion("Pressure").text()
            ordenada="h, %s" % config.Configuracion("Enthalpy").text()
            self.factorx=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
            self.factory=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        elif self.ejesTabla.currentIndex()==2:
            abcisa="P, %s" % config.Configuracion("Pressure").text()
            ordenada="s, %s" % config.Configuracion("SpecificHeat","Entropy").text()
            self.factorx=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
            self.factory=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat","Entropy").func())
        elif self.ejesTabla.currentIndex()==3:
            abcisa="P, %s" % config.Configuracion("Pressure").text()
            ordenada="v, %s" % config.Configuracion("SpecificVolume").text()
            self.factorx=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
            self.factory=unidades.SpecificVolume(1).unit(config.Configuracion("SpecificVolume").func())
        elif self.ejesTabla.currentIndex()==4:
            abcisa="T, %s" % config.Configuracion("Temperature").text()
            ordenada="s, %s" % config.Configuracion("SpecificHeat","Entropy").text()
            self.factorx=0
            self.factory=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat","Entropy").func())
        elif self.ejesTabla.currentIndex()==5:
            abcisa="T, %s" % config.Configuracion("Temperature").text()
            ordenada="x"
            self.factorx=0
            self.factory=1
            
        if self.ejeX.currentText()=="p":
            abcisa2="p, %s" % config.Configuracion("Pressure").text()
            self.factorx2=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
        elif self.ejeX.currentText()=="T":
            abcisa2="T, %s" % config.Configuracion("Temperature").text()
            self.factorx2=0
        elif self.ejeX.currentText()=="h":
            abcisa2="h, %s" % config.Configuracion("Enthalpy").text()
            self.factorx2=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        elif self.ejeX.currentText()=="v":
            abcisa2="v, %s" % config.Configuracion("SpecificVolume").text()
            self.factorx2=unidades.SpecificVolume(1).unit(config.Configuracion("SpecificVolume").func())
        elif self.ejeX.currentText()=="s":
            abcisa2="s, %s" % config.Configuracion("SpecificHeat","Entropy").text()
            self.factorx2=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat","Entropy").func())
        elif self.ejeX.currentText()=="u":
            abcisa2="u, %s" %config.Configuracion("Enthalpy").text()
            self.factorx2=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        if self.ejeY.currentText()=="p":
            ordenada2="p, %s" % config.Configuracion("Pressure").text()
            self.factory2=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
        elif self.ejeY.currentText()=="T":
            ordenada2="T, %s" % config.Configuracion("Temperature").text()
            self.factory2=0
        elif self.ejeY.currentText()=="h":
            ordenada2="h, %s" % config.Configuracion("Enthalpy").text()
            self.factory2=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        elif self.ejeY.currentText()=="v":
            ordenada2="v, %s" % config.Configuracion("SpecificVolume").text()
            self.factory2=unidades.SpecificVolume(1).unit(config.Configuracion("SpecificVolume").func())
        elif self.ejeY.currentText()=="s":
            ordenada2="s, %s" % config.Configuracion("SpecificHeat","Entropy").text()
            self.factory2=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat","Entropy").func())
        elif self.ejeY.currentText()=="u":
            ordenada2="u, %s" %config.Configuracion("Enthalpy").text()
            self.factory2=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())

        if self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8):
            texto="p, %s" %config.Configuracion("Pressure").text()
            self.factorz=unidades.Pressure(1).unit(config.Configuracion("Pressure").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8):
            texto="T, %s" %config.Configuracion("Temperature").text()
            self.factorz=0
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8):
            texto="v, %s" %config.Configuracion("SpecificVolume").text()
            self.factorz=unidades.SpecificVolume(1).unit(config.Configuracion("SpecificVolume").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8):
            texto="h, %s" %config.Configuracion("Enthalpy").text()
            self.factorz=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8):
            texto="s, %s" %config.Configuracion("SpecificHeat", "Entropy").text()
            self.factorz=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat", "Entropy").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8):
            texto="u, %s" %config.Configuracion("Enthalpy").text()
            self.factorz=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8):
            texto="Cp, %s" %config.Configuracion("SpecificHeat").text()
            self.factorz=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8):
            texto="Cv, %s" %config.Configuracion("SpecificHeat").text()
            self.factorz=unidades.SpecificHeat(1).unit(config.Configuracion("SpecificHeat").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8):
            texto=u"ρ, %s" %config.Configuracion("Density").text()
            self.factorz=unidades.Density(1).unit(config.Configuracion("Density").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8):
            texto="k, %s" %config.Configuracion("ThermalConductivity").text()
            self.factorz=unidades.ThermalConductivity(1).unit(config.Configuracion("ThermalConductivity").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8):
            texto=u"μ, %s" %config.Configuracion("Viscosity").text()
            self.factorz=unidades.Viscosity(1).unit(config.Configuracion("Viscosity").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8):
            texto="w, %s" %config.Configuracion("Speed").text()
            self.factorz=unidades.Speed(1).unit(config.Configuracion("Speed").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8):
            texto="x"
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8):
            texto="G, %s" %config.Configuracion("Enthalpy").text()
            self.factorz=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8):
            texto="A, %s" %config.Configuracion("Enthalpy").text()
            self.factorz=unidades.Enthalpy(1).unit(config.Configuracion("Enthalpy").func())
            
        self.etiquetas=[abcisa, ordenada, texto]
        self.etiquetas2=[abcisa2, ordenada2]


    def calcularMatriz(self, start=0, rango=40):
        """Método que actualiza los datos de matriz"""        
        xini=float(self.abscisaInicio.text())
        xfin=float(self.abscisaFin.text())
        xsalto=float(self.abscisaIntervalo.text())                
        xn=int((xfin-xini)/xsalto+1)
        yini=float(self.ordenadaInicio.text())
        yfin=float(self.ordenadaFin.text())
        ysalto=float(self.ordenadaIntervalo.text())
        yn=int((yfin-yini)/ysalto+1)
        self.tabla.setRowCount(yn)
        self.tabla.setColumnCount(xn)
        
        self.factores_conversion()
                    
        xi=arange(xini, xfin, xsalto)
        if (xfin-xini)/xsalto==float(int((xfin-xini)/xsalto)):
            xi=concatenate((xi, [xfin]))
        yi=arange(yini, yfin, ysalto)
        if (yfin-yini)/ysalto==float(int((yfin-yini)/ysalto)):
            yi=concatenate((yi, [yfin]))

        for i in range(len(xi)):
            headerItem = QtGui.QTableWidgetItem()
            headerItem.setText(str(xi[i]))
            self.tabla.setHorizontalHeaderItem(i,headerItem)
        for i in range(len(yi)):
            headerItem = QtGui.QTableWidgetItem()
            headerItem.setText(str(yi[i]))
            self.tabla.setVerticalHeaderItem(i,headerItem)
            
        xdata,ydata = meshgrid(xi, yi)
        self.matriz=[]

        for i in range(len(xi)):
            self.progresbar.setValue(start+rango*(i+1.)/len(xi))
            QtGui.QApplication.processEvents()
            fila=[]
            for j in range(len(yi)):
                if self.ejesTabla.currentIndex()==0:
                    vapor=steam_pT(xi[i]*self.factorx, self.conv_T(yi[j]))
                elif self.ejesTabla.currentIndex()==1:
                    vapor=steam_ph(xi[i]*self.factorx, yi[j]*self.factory)
                elif self.ejesTabla.currentIndex()==2:
                    vapor=steam_ps(xi[i]*self.factorx, yi[j]*self.factory)       
                elif self.ejesTabla.currentIndex()==3:
                    vapor=steam_pv(xi[i]*self.factorx, yi[j]*self.factory)     
                elif self.ejesTabla.currentIndex()==4:
                    if bounds_Ts(xi[i], yi[j], 0)==0:
                        vapor=steam_Ts(self.conv_T(xi[i]), yi[j]*self.factory)
                    else:
                        vapor=steam_Ts(TCRIT, steam_pT(PCRIT, TCRIT).s)
                elif self.ejesTabla.currentIndex()==5:
                    vapor=steam_Tx(self.conv_T(xi[i]), yi[j]) 
                fila.append(vapor)
                    
            self.matriz.append(fila)

        self.xdata=xdata
        self.ydata=ydata
        self.actionCSV.setEnabled(True)


    def Calcular_Propiedades(self, start, rango=5):
        """Método que actualiza los datos al cambiar la propiedad a mostrar"""
        if len(self.matriz)!=0:
            zdata = zeros(self.xdata.shape)
            
            for i, fila in enumerate(self.matriz):
                self.progresbar.setValue(start+rango*(i+1.)/len(self.matriz))
                QtGui.QApplication.processEvents()
                for j, vapor in enumerate(fila):
                    if self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.p/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8):
                        dato=self.conv_T_inv(vapor.T)
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.v/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.h/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.s/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.u/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.cp/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.cv/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.rho/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.k/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.mu/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8):
                        if vapor.region !='\x04' and vapor.region !='\x03':
                            dato=vapor.w/self.factorz
                        else:
                            dato=0.0
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8):
                        dato=vapor.x
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8):
                        dato=(vapor.h-vapor.T*vapor.s)/self.factorz
                    elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8):
                        dato=(vapor.u-vapor.T*vapor.s)/self.factorz
                    zdata[j, i]=dato

            for i, fila in enumerate(zdata):
                for j, dato in enumerate(fila):
                    self.tabla.setItem(i, j,QtGui.QTableWidgetItem(config.representacion(dato)))
                    self.tabla.item(i, j).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

            self.tabla.resizeColumnsToContents()
            self.toolBox.setItemText(self.toolBox.indexOf(self.page_1), QtGui.QApplication.translate("SteamTables", "Tabla", None, QtGui.QApplication.UnicodeUTF8)+"   %s - %s - %s" %(self.etiquetas[0], self.etiquetas[1], self.etiquetas[2]))
            self.zdata=zdata


    def calcularSaturacion(self):
        """Método que calcula datos de la línea de saturación"""
        TT0 = linspace(273.15, TCRIT, 200)
        psat = [psat_T(T) for T in TT0]
        
        if self.ejesTabla.currentIndex()==0:
            self.xsat=[[P/self.factorx for P in psat], [P/self.factorx for P in psat]]
            self.ysat=[[self.conv_T_inv(T) for T in TT0], [self.conv_T_inv(T) for T in TT0]]
        elif self.ejesTabla.currentIndex()==1:
            self.xsat=[[P/self.factorx for P in psat], [P/self.factorx for P in psat]]
            self.ysat=[[region4_Tx(T,0).h/self.factory for T in TT0], [region4_Tx(T,1).h/self.factory for T in TT0]]
        elif self.ejesTabla.currentIndex()==2:
            self.xsat=[[P/self.factorx for P in psat], [P/self.factorx for P in psat]]
            self.ysat=[[region4_Tx(T,0).s/self.factory for T in TT0], [region4_Tx(T,1).s/self.factory for T in TT0]]
        elif self.ejesTabla.currentIndex()==3:
            self.xsat=[[P/self.factorx for P in psat], [P/self.factorx for P in psat]]
            self.ysat=[[region4_Tx(T,0).v/self.factory for T in TT0], [region4_Tx(T,1).v/self.factory for T in TT0]]
        elif self.ejesTabla.currentIndex()==4:
            self.xsat=[[self.conv_T_inv(T) for T in TT0], [self.conv_T_inv(T) for T in TT0]]
            self.ysat=[[region4_Tx(T,0).s/self.factory for T in TT0], [region4_Tx(T,1).s/self.factory for T in TT0]]
        elif self.ejesTabla.currentIndex()==5:
            self.xsat=[[self.conv_T_inv(T) for T in TT0], [self.conv_T_inv(T) for T in TT0]]
            self.ysat=[[0]*100, [1]*100]
        
        if self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[P/self.factorz for P in psat], [P/self.factorz for P in psat]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[self.conv_T_inv(T) for T in TT0], [self.conv_T_inv(T) for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).v/self.factorz for T in TT0], [region4_Tx(T,1).v/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).h/self.factorz for T in TT0], [region4_Tx(T,1).h/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).s/self.factorz for T in TT0], [region4_Tx(T,1).s/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).u/self.factorz for T in TT0], [region4_Tx(T,1).u/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).cp/self.factorz for T in TT0], [region4_Tx(T,1).cp/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).cv/self.factorz for T in TT0], [region4_Tx(T,1).cv/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).rho/self.factorz for T in TT0], [region4_Tx(T,1).rho/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).k/self.factorz for T in TT0], [region4_Tx(T,1).k/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[region4_Tx(T,0).mu/self.factorz for T in TT0], [region4_Tx(T,1).mu/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[0 for T in TT0], [0 for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[0]*len(TT0), [1]*len(TT0)]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[(region4_Tx(T,0).h-T*region4_Tx(T,0).s)/self.factorz for T in TT0], [(region4_Tx(T,1).h-T*region4_Tx(T,1).s)/self.factorz for T in TT0]]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8):
            self.zsat=[[(region4_Tx(T,0).u-T*region4_Tx(T,0).s)/self.factorz for T in TT0], [(region4_Tx(T,1).u-T*region4_Tx(T,1).s)/self.factorz for T in TT0]]
        
        for i in range(len(self.xsat)):
            for j in range(len(self.xsat[i])-1, -1, -1):
                if self.xsat[i][j]<self.xdata[0][0] or self.xsat[i][j]>self.xdata[-1][-1] or self.ysat[i][j]<self.ydata[0][0] or self.ysat[i][j]>self.ydata[-1][-1]:
                    del self.xsat[i][j]
                    del self.ysat[i][j]
                    del self.zsat[i][j]
    
        if self.ejeX.currentText()=="p":
            self.xsat2=[[P/self.factorx2 for P in psat], [P/self.factorx2 for P in psat]]
        elif self.ejeX.currentText()=="T":
            self.xsat2=[[self.conv_T_inv(T) for T in TT0], [self.conv_T_inv(T) for T in TT0]]
        elif self.ejeX.currentText()=="h":
            self.xsat2=[[region4_Tx(T,0).h/self.factorx2 for T in TT0], [region4_Tx(T,1).h/self.factorx2 for T in TT0]]
        elif self.ejeX.currentText()=="v":
            self.xsat2=[[region4_Tx(T,0).v/self.factorx2 for T in TT0], [region4_Tx(T,1).v/self.factorx2 for T in TT0]]
        elif self.ejeX.currentText()=="s":
            self.xsat2=[[region4_Tx(T,0).s/self.factorx2 for T in TT0], [region4_Tx(T,1).s/self.factorx2 for T in TT0]]
        elif self.ejeX.currentText()=="u":
            self.xsat2=[[region4_Tx(T,0).u/self.factorx2 for T in TT0], [region4_Tx(T,1).u/self.factorx2 for T in TT0]]
        if self.ejeY.currentText()=="p":
            self.ysat2=[[P/self.factory2 for P in psat], [P/self.factory2 for P in psat]]
        elif self.ejeY.currentText()=="T":
            self.ysat2=[[self.conv_T_inv(T) for T in TT0], [self.conv_T_inv(T) for T in TT0]]
        elif self.ejeY.currentText()=="h":
            self.ysat2=[[region4_Tx(T,0).h/self.factory2 for T in TT0], [region4_Tx(T,1).h/self.factory2 for T in TT0]]
        elif self.ejeY.currentText()=="v":
            self.ysat2=[[region4_Tx(T,0).v/self.factory2 for T in TT0], [region4_Tx(T,1).v/self.factory2 for T in TT0]]
        elif self.ejeY.currentText()=="s":
            self.ysat2=[[region4_Tx(T,0).s/self.factory2 for T in TT0], [region4_Tx(T,1).s/self.factory2 for T in TT0]]
        elif self.ejeY.currentText()=="u":
            self.ysat2=[[region4_Tx(T,0).u/self.factory2 for T in TT0], [region4_Tx(T,1).u/self.factory2 for T in TT0]]


    def calcularPuntos(self):
        """Método que actualiza los datos de puntos definidos por el usuario"""
        if self.ejesTabla.currentIndex()==0:
            self.xi=[punto.p/self.factorx for punto in self.puntos]
            self.yi=[self.conv_T_inv(punto.T) for punto in self.puntos]
        elif self.ejesTabla.currentIndex()==1:
            self.xi=[punto.p/self.factorx for punto in self.puntos]
            self.yi=[punto.h/self.factory for punto in self.puntos]
        elif self.ejesTabla.currentIndex()==2:
            self.xi=[punto.p/self.factorx for punto in self.puntos]
            self.yi=[punto.s/self.factory for punto in self.puntos]
        elif self.ejesTabla.currentIndex()==3:
            self.xi=[punto.p/self.factorx for punto in self.puntos]
            self.yi=[punto.v/self.factory for punto in self.puntos]
        elif self.ejesTabla.currentIndex()==4:
            self.xi=[self.conv_T_inv(punto.T) for punto in self.puntos]
            self.yi=[punto.s/self.factory for punto in self.puntos]
        elif self.ejesTabla.currentIndex()==5:
            self.xi=[self.conv_T_inv(punto.T) for punto in self.puntos]
            self.yi=[punto.x for punto in self.puntos]
            
        if self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.p/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[self.conv_T_inv(punto.T) for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.v/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.h/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.s/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.u/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.cp/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.cv/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.rho/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.k/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.mu/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[0 for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[punto.x for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8):
            self.zi=[(punto.h-punto.T*punto.s)/self.factorz for punto in self.puntos]
        elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8):   
            self.zi=[(punto.u-punto.T*punto.s)/self.factorz for punto in self.puntos]
                
        if self.ejeX.currentText()=="p":
            self.xi2=[punto.p/self.factorx2 for punto in self.puntos]
        elif self.ejeX.currentText()=="T":
            self.xi2=[self.conv_T_inv(punto.T) for punto in self.puntos]
        elif self.ejeX.currentText()=="h":
            self.xi2=[punto.h/self.factorx2 for punto in self.puntos]
        elif self.ejeX.currentText()=="v":
            self.xi2=[punto.v/self.factorx2 for punto in self.puntos]
        elif self.ejeX.currentText()=="s":
            self.xi2=[punto.s/self.factorx2 for punto in self.puntos]
        elif self.ejeX.currentText()=="u":
            self.xi2=[punto.u/self.factorx2 for punto in self.puntos]
        if self.ejeY.currentText()=="p":
            self.yi2=[punto.p/self.factory2 for punto in self.puntos]
        elif self.ejeY.currentText()=="T":
            self.yi2=[self.conv_T_inv(punto.T) for punto in self.puntos]
        elif self.ejeY.currentText()=="h":
            self.yi2=[punto.h/self.factory2 for punto in self.puntos]
        elif self.ejeY.currentText()=="v":
            self.yi2=[punto.v/self.factory2 for punto in self.puntos]
        elif self.ejeY.currentText()=="s":
            self.yi2=[punto.s/self.factory2 for punto in self.puntos]
        elif self.ejeY.currentText()=="u":
            self.yi2=[punto.u/self.factory2 for punto in self.puntos]

        
    def isolineas(self, S, X, funcion, start, rango):
        """Librería de cálculo de los parámetros de las isolineas"""
        x=[]
        y=[]
        z=[]
        x2=[]
        y2=[]
        for i, propiedad in enumerate(S):
            self.progresbar.setValue(start+rango*(i+1.)/len(S))
            QtGui.QApplication.processEvents()
            if self.ejesTabla.currentIndex()==0:
                xi=[funcion(i, propiedad).p/self.factorx for i in X]
                yi=[self.conv_T_inv(funcion(i, propiedad).T) for i in X]
            elif self.ejesTabla.currentIndex()==1:
                xi=[funcion(i, propiedad).p/self.factorx for i in X]
                yi=[funcion(i, propiedad).h/self.factory for i in X]
            elif self.ejesTabla.currentIndex()==2:
                xi=[funcion(i, propiedad).p/self.factorx for i in X]
                yi=[funcion(i, propiedad).s/self.factory for i in X]
            elif self.ejesTabla.currentIndex()==3:
                xi=[funcion(i, propiedad).p/self.factorx for i in X]
                yi=[funcion(i, propiedad).v/self.factory for i in X]
            elif self.ejesTabla.currentIndex()==4:
                xi=[self.conv_T_inv(funcion(i, propiedad).T) for i in X]
                yi=[funcion(i, propiedad).s/self.factory for i in X]
            elif self.ejesTabla.currentIndex()==5:
                xi=[self.conv_T_inv(funcion(i, propiedad).T) for i in X]
                yi=[funcion(i, propiedad).x for i in X]
                
            if self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).p/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8):
                zi=[self.conv_T_inv(funcion(i, propiedad).T) for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).v/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).h/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).s/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía interna", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).u/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cp", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).cp/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Cv", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).cv/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).rho/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).k/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).mu/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Velocidad del sonido", None, QtGui.QApplication.UnicodeUTF8):
                zi=[0 for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Fracción de vapor", None, QtGui.QApplication.UnicodeUTF8):
                zi=[funcion(i, propiedad).x for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Gibbs", None, QtGui.QApplication.UnicodeUTF8):
                zi=[(funcion(i, propiedad).h-funcion(i, propiedad).T*funcion(i, propiedad).s)/self.factorz for i in X]
            elif self.variableTabla.currentText()==QtGui.QApplication.translate("SteamTables", "Energía de Helmholtz", None, QtGui.QApplication.UnicodeUTF8):
                zi=[(funcion(i, propiedad).u-funcion(i, propiedad).T*funcion(i, propiedad).s)/self.factorz for i in X]
                
            if self.ejeX.currentText()=="p":
                xi2=[funcion(i, propiedad).p/self.factorx2 for i in X]
            elif self.ejeX.currentText()=="T":
                xi2=[self.conv_T_inv(funcion(i, propiedad).T) for i in X]
            elif self.ejeX.currentText()=="h":
                xi2=[funcion(i, propiedad).h/self.factorx2 for i in X]
            elif self.ejeX.currentText()=="v":
                xi2=[funcion(i, propiedad).v/self.factorx2 for i in X]
            elif self.ejeX.currentText()=="s":
                xi2=[funcion(i, propiedad).s/self.factorx2 for i in X]
            elif self.ejeX.currentText()=="u":
                xi2=[funcion(i, propiedad).u/self.factorx2 for i in X]
            if self.ejeY.currentText()=="p":
                yi2=[funcion(i, propiedad).p/self.factory2 for i in X]
            elif self.ejeY.currentText()=="T":
                yi2=[self.conv_T_inv(funcion(i, propiedad).T) for i in X]
            elif self.ejeY.currentText()=="h":
                yi2=[funcion(i, propiedad).h/self.factory2 for i in X]
            elif self.ejeY.currentText()=="v":
                yi2=[funcion(i, propiedad).v/self.factory2 for i in X]
            elif self.ejeY.currentText()=="s":
                yi2=[funcion(i, propiedad).s/self.factory2 for i in X]
            elif self.ejeY.currentText()=="u":
                yi2=[funcion(i, propiedad).u/self.factory2 for i in X]
            x.append(xi)
            y.append(yi)
            z.append(zi)
            x2.append(xi2)
            y2.append(yi2)
        return x, y, z, x2, y2
 
    def labels(self, isolineas, x, y, pos):
        x_label=[]
        y_label=[]
        label=[]
        angle=[]
        for i in range(len(isolineas)):
            j=int(pos/100.*len(x[i]))
            x_label.append(x[i][j])
            y_label.append(y[i][j])
            label.append(config.representacion(isolineas[i]))
            if self.ejeX_escala.isChecked():
                fraccionx=(log(x[i][j+1])-log(x[i][j]))/(log(self.ejeX_max[self.ejeX.currentIndex()].value.config())-log(self.ejeX_min[self.ejeX.currentIndex()].value.config()))
            else:
                fraccionx=(x[i][j+1]-x[i][j])/(self.ejeX_max[self.ejeX.currentIndex()].value.config()-self.ejeX_min[self.ejeX.currentIndex()].value.config())
            if self.ejeY_escala.isChecked():
                fracciony=(log(y[i][j+1])-log(y[i][j]))/(log(self.ejeY_max[self.ejeY_visible].value.config())-log(self.ejeY_min[self.ejeY_visible].value.config()))
            else:
                fracciony=(y[i][j+1]-y[i][j])/(self.ejeY_max[self.ejeY_visible].value.config()-self.ejeY_min[self.ejeY_visible].value.config())
            try:
                angle.append(arctan(fracciony/fraccionx)*360/2/pi)
            except ZeroDivisionError:
                angle.append(90)
        return x_label, y_label, label, angle
        
        
    def calcularIsoentropica(self, start=85, rango=5):
        """Método que actualiza los datos de isoentrópicas"""
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando isoentrópicas...", None, QtGui.QApplication.UnicodeUTF8))
        if self.Isoentropica.Personalizar:
            S=self.Isoentropica.Lista
        else:
            S=arange(self.Isoentropica.inicio, self.Isoentropica.fin, self.Isoentropica.intervalo).tolist()
        if self.Isoentropica.Critica:
            SCRIT=steam_pT(PCRIT, TCRIT).s
            S.append(SCRIT)
        S2=S[:]
        X= logspace(-3, 3, 100)*1e5
        x, y, z, x2, y2=self.isolineas(S, X, steam_ps, start, rango)
        for i in range(len(S)-1, -1, -1):
            for j in range(len(X)-1, -1, -1):
                if bounds_ps(X[j], S[i], 0)<>0:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
                    del x2[i][j]
                    del y2[i][j]
            if len(x2[i])==0:
                del x2[i]
                del y2[i]
                S2.remove(S2[i])
        for i in range(len(S)-1, -1, -1):
            for j in range(len(x[i])-1, -1, -1):
                if x[i][j]<self.xdata[0][0] or x[i][j]>self.xdata[-1][-1] or y[i][j]<self.ydata[0][0] or y[i][j]>self.ydata[-1][-1]:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
            if len(x[i])==0:
                del x[i]
                del y[i]
                del z[i]        
                S.remove(S[i])
        x_label, y_label, label, angle=self.labels([unidades.SpecificHeat(i).config("Entropy") for i in S2], x2, y2, self.Isoentropica.posicion)
        self.isoentropica=[x, y, z]
        if self.Isoentropica.units:
            self.isoentropica2=[x2, y2, x_label, y_label, ["S="+i+config.Configuracion("SpecificHeat", "Entropy").text() for i in label], angle]
        else:
            self.isoentropica2=[x2, y2, x_label, y_label, label, angle]

    def calcularIsoentalpica(self, start=90, rango=5):
        """Método que actualiza los datos de isoentálpicas"""
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando isoentálpicas...", None, QtGui.QApplication.UnicodeUTF8))
        if self.Isoentalpica.Personalizar:
            H=self.Isoentalpica.Lista
        else:
            H=arange(self.Isoentalpica.inicio, self.Isoentalpica.fin, self.Isoentalpica.intervalo).tolist()
        if self.Isoentalpica.Critica:
            HCRIT=steam_pT(PCRIT, TCRIT).h
            H.append(HCRIT)
        H2=H[:]
        X= logspace(-3, 3, 100)*1e5
        x, y, z, x2, y2=self.isolineas(H, X, steam_ph, start, rango)
        for i in range(len(H)-1, -1, -1):
            for j in range(len(X)-1, -1, -1):
                if bounds_ph(X[j], H[i], 0)<>0:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
                    del x2[i][j]
                    del y2[i][j]
            if len(x2[i])==0:
                del x2[i]
                del y2[i]
                H2.remove(H2[i])
        for i in range(len(H)-1, -1, -1):
            for j in range(len(x[i])-1, -1, -1):
                if x[i][j]<self.xdata[0][0] or x[i][j]>self.xdata[-1][-1] or y[i][j]<self.ydata[0][0] or y[i][j]>self.ydata[-1][-1]:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
            if len(x[i])==0:
                del x[i]
                del y[i]
                del z[i]
                H.remove(H[i])
        x_label, y_label, label, angle=self.labels([unidades.Enthalpy(i).config() for i in H2], x2, y2, self.Isoentalpica.posicion)
        self.isoentalpica=[x, y, z]
        if self.Isoentalpica.units:
            self.isoentalpica2=[x2, y2, x_label, y_label, ["H="+i+config.Configuracion("Enthalpy").text() for i in label], angle]
        else:
            self.isoentalpica2=[x2, y2, x_label, y_label, label, angle]

    def calcularIsobara(self, start=80, rango=5):
        """Método que actualiza los datos de isobaras"""
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando isobaras...", None, QtGui.QApplication.UnicodeUTF8))
        if self.Isobara.Personalizar:
            P=self.Isobara.Lista
        else:
            P=arange(self.Isobara.inicio, self.Isobara.fin, self.Isobara.intervalo).tolist()
        if self.Isobara.Critica:
            P.append(PCRIT)
        X=linspace(0, 10000, 100)
        x, y, z, x2, y2=self.isolineas(X, P, steam_ps, start, rango)
        x=transpose(x)
        y=transpose(y)
        z=transpose(z)
        x2=transpose(x2)
        y2=transpose(y2)
        x=[list(i) for i in x]
        y=[list(i) for i in y]
        z=[list(i) for i in z]
        #Eliminamos puntos del grafico 3D fuera de los ejes
        for i in range(len(P)-1, -1, -1):
            for j in range(len(x[i])-1, -1, -1):
                if x[i][j]<self.xdata[0][0] or x[i][j]>self.xdata[-1][-1] or y[i][j]<self.ydata[0][0] or y[i][j]>self.ydata[-1][-1]:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
            if len(x[i])==0:
                del x[i]
                del y[i]
                del z[i]

        x_label, y_label, label, angle=self.labels([unidades.Pressure(i).config() for i in P], x2, y2, self.Isobara.posicion)
        self.isobara=[x, y, z]
        if self.Isobara.units:
            self.isobara2=[x2, y2, x_label, y_label, ["P="+i+config.Configuracion("Pressure").text() for i in label], angle]
        else:
            self.isobara2=[x2, y2, x_label, y_label, label, angle]

    def calcularIsoterma(self, start=75, rango=5):
        """Método que actualiza los datos de isotermas"""
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando isotermas...", None, QtGui.QApplication.UnicodeUTF8))
        if self.Isoterma.Personalizar:
            T=self.Isoterma.Lista
        else:
            T=arange(self.Isoterma.inicio, self.Isoterma.fin, self.Isoterma.intervalo).tolist()
        if self.Isoterma.Critica:
            T.append(TCRIT)
        X= logspace(-3, 3, 200)*1e5
        x, y, z, x2, y2=self.isolineas(T, X, steam_pT, start, rango)
        
        #Añadimos puntos interiores de la campana de saturación
        X=linspace(1, 0, 50)
        for i , t in enumerate(T):
            if t<TCRIT:
                xi, yi, zi, xi2, yi2=self.isolineas(X, [t], steam_Tx, start+rango, 0)
                temp=x2[i]+xi2[i]
                temp.sort(reverse=x2[i][0]>x2[i][-1])
                indice=temp.index(xi2[i][0])
                for j in range(len(xi2)):
                    x2[i].insert(indice+j, xi2[j][0])
                    y2[i].insert(indice+j, yi2[j][0])
                    
        #Eliminamos puntos del grafico 3D fuera de los ejes
        for i in range(len(T)-1, -1, -1):
            for j in range(len(x[i])-1, -1, -1):
                if x[i][j]<self.xdata[0][0] or x[i][j]>self.xdata[-1][-1] or y[i][j]<self.ydata[0][0] or y[i][j]>self.ydata[-1][-1]:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
            if len(x[i])==0:
                del x[i]
                del y[i]
                del z[i]
        
        x_label, y_label, label, angle=self.labels([unidades.Temperature(i).config() for i in T], x2, y2, self.Isoterma.posicion)
        self.isoterma=[x, y, z]
        if self.Isoterma.units:
            self.isoterma2=[x2, y2, x_label, y_label, ["T="+i+config.Configuracion("Temperature").text() for i in label], angle]
        else:
            self.isoterma2=[x2, y2, x_label, y_label, label, angle]

    def calcularIsocora(self, start=95, rango=5):
        """Método que actualiza los datos de isocoras"""
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando isocoras...", None, QtGui.QApplication.UnicodeUTF8))
        if self.Isocora.Personalizar:
            V=self.Isocora.Lista
        else:
            V=arange(self.Isocora.inicio, self.Isocora.fin, self.Isocora.intervalo).tolist()
        if self.Isocora.Critica:
            VCRIT=steam_pT(PCRIT, TCRIT).v
            V.append(VCRIT)
        V2=V[:]
        X= logspace(-3, 3, 300)*1e5
        x, y, z, x2, y2=self.isolineas(V, X, steam_pv, start, rango)
        for i in range(len(V)-1, -1, -1):
            for j in range(len(x[i])-1, -1, -1):
                if bounds_pv(X[j], V[i], 0)<>0:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
                    del x2[i][j]
                    del y2[i][j]
            if len(x2[i])==0:
                del x2[i]
                del y2[i]
                V2.remove(V2[i])
        for i in range(len(V)-1, -1, -1):
            for j in range(len(x[i])-1, -1, -1):
                if x[i][j]<self.xdata[0][0] or x[i][j]>self.xdata[-1][-1] or y[i][j]<self.ydata[0][0] or y[i][j]>self.ydata[-1][-1]:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
            if len(x[i])==0:
                del x[i]
                del y[i]
                del z[i]
                V.remove(V[i])
        x_label, y_label, label, angle=self.labels([unidades.SpecificVolume(i).config() for i in V2], x2, y2, self.Isocora.posicion)
        self.isocora=[x, y, z]     
        if self.Isocora.units:
            self.isocora2=[x2, y2, x_label, y_label, ["v="+i+config.Configuracion("SpecificVolume").text() for i in label], angle]
        else:
            self.isocora2=[x2, y2, x_label, y_label, label, angle]
        
    def calcularIsoX(self, start=95, rango=5):
        """Método que actualiza los datos de isocalidad"""
        self.statusbar.showMessage(QtGui.QApplication.translate("SteamTables", "Calculando isocalidades...", None, QtGui.QApplication.UnicodeUTF8))
        if self.IsoX.Personalizar:
            X=self.IsoX.Lista
        else:
            X=arange(self.IsoX.inicio, self.IsoX.fin, self.IsoX.intervalo)
        T= linspace(273.15, TCRIT, 100)
        x, y, z, x2, y2=self.isolineas(X, T, steam_Tx, start, rango)
        for i in range(len(X)-1, -1, -1):
            for j in range(len(T)-1, -1, -1):
                if x[i][j]<self.xdata[0][0] or x[i][j]>self.xdata[-1][-1] or y[i][j]<self.ydata[0][0] or y[i][j]>self.ydata[-1][-1]:
                    del x[i][j]
                    del y[i][j]
                    del z[i][j]
        x_label, y_label, label, angle=self.labels(X, x2, y2, self.IsoX.posicion)
        self.isoX=[x, y, z]        
        if self.IsoX.units:
            self.isoX2=[x2, y2, x_label, y_label, ["x="+i for i in label], angle]
        else:
            self.isoX2=[x2, y2, x_label, y_label, label, angle]

    def calcularPropiedades(self):
        """Calcula y muestra las propiedades del punto especificado"""
        if self.variablesCalculo.currentIndex()==0:
            p=self.presion.value
            T=self.temperatura.value
            vapor=steam_pT(p, T)
        elif self.variablesCalculo.currentIndex()==1:
            p=self.presion.value
            h=self.entalpia.value
            vapor=steam_ph(p, h)
        elif self.variablesCalculo.currentIndex()==2:
            p=self.presion.value
            s=self.entropia.value
            vapor=steam_ps(p, s)            
        elif self.variablesCalculo.currentIndex()==3:
            p=self.presion.value
            v=self.volumen.value
            vapor=steam_pv(p, v)            
        elif self.variablesCalculo.currentIndex()==4:
            T=self.temperatura.value
            s=self.entropia.value
            vapor=steam_Ts(T, s)            
        elif self.variablesCalculo.currentIndex()==5:
            T=self.temperatura.value
            x=self.fraccionVapor.value
            vapor=steam_Tx(T, x)  
        self.punto=vapor
        self.mostrarPropiedades()
        self.botonAdd.setEnabled(True) 
                
    def mostrarPropiedades(self):
        """Muestra los valores de las propiedades de la sección de puntos especificados por el usuario"""
        if self.punto<>0:
            self.presion.setValue(self.punto.p)
            self.temperatura.setValue(self.punto.T)
            self.volumen.setValue(self.punto.v)
            self.entalpia.setValue(self.punto.h)
            self.entropia.setValue(self.punto.s)
            self.fraccionVapor.setValue(self.punto.x)
            self.energiaInterna.setValue(self.punto.u)
            self.energiaGibbs.setValue(self.punto.h-self.punto.T*self.punto.s)
            self.energiaHelmholtz.setValue(self.punto.u-self.punto.T*self.punto.s)
            self.densidad.setValue(self.punto.rho)
            self.cp.setValue(self.punto.cp)
            self.cv.setValue(self.punto.cv)
            self.conductividad.setValue(self.punto.k)
            self.viscosidad.setValue(self.punto.mu)
            if self.punto.region !='\x04' and  self.punto.region !='\x03':
                self.velocidad.setValue(self.punto.w)
            else:
                self.velocidad.clear()
            if self.punto.region =='\x01':
                self.region.setValue(1)
            elif self.punto.region =='\x02':
                self.region.setValue(2)
            elif self.punto.region =='\x03':
                self.region.setValue(3)
            elif self.punto.region =='\x04':
                self.region.setValue(4)
            elif self.punto.region =='\x05':
                self.region.setValue(5)
                
    def actualizarConfiguracion(self):
        """Actualiza los diferentes parámetros que puedan cambiar al cerrar el dialogo de preferencias
            Factores de conversión si han cambiado las unidades
                Valores de la configuración de la tabla 3D
                Valores en la sección de puntos especificados por el usuario
            """
        #TODO: Añadir tareas al cambiar la configuración
        self.factores_conversion()
        if self.factorx2==0:  #El eje x es la temperatura
            xmax=unidades.Temperature(self.ejeX_max[self.ejeX.currentIndex()].value).unit(config.Configuracion("Temperature").func())
            xmin=unidades.Temperature(self.ejeX_min[self.ejeX.currentIndex()].value).unit(config.Configuracion("Temperature").func())
            self.ejeX_max[self.ejeX.currentIndex()].setValue(config.representacion(xmax.config()))
            self.ejeX_min[self.ejeX.currentIndex()].setValue(config.representacion(xmin.config()))
        else: #En cualquier otro caso basta con usar el factor de correción para ese eje
            xmax=float(self.ejeX_max[self.ejeX.currentIndex()].value)*self.factorx2
            xmin=float(self.ejeX_min[self.ejeX.currentIndex()].value)*self.factorx2
            self.ejeX_max[self.ejeX.currentIndex()].setValue(config.representacion(xmax/self.factorx2))
            self.ejeX_min[self.ejeX.currentIndex()].setValue(config.representacion(xmin/self.factorx2))
        if self.factory2==0:  
            ymax=unidades.Temperature(self.ejeY_max[self.ejeY_visible].value).unit(config.Configuracion("Temperature").func())
            ymin=unidades.Temperature(self.ejeY_min[self.ejeY_visible].value).unit(config.Configuracion("Temperature").func())
            self.ejeY_max[self.ejeY_visible].setValue(config.representacion(ymax.config()))
            self.ejeY_min[self.ejeY_visible].setValue(config.representacion(ymin.config()))
        else: 
            ymax=float(self.ejeY_max[self.ejeY_visible].value)*self.factory2
            ymin=float(self.ejeY_min[self.ejeY_visible].value)*self.factory2      
            self.ejeY_max[self.ejeY_visible].setValue(config.representacion(ymax/self.factory2))
            self.ejeY_min[self.ejeY_visible].setValue(config.representacion(ymin/self.factory2))
        if self.factory2==0:  
            self.ejeY_max[self.ejeY_visible].setValue(config.representacion(ymax.config))
            self.ejeY_min[self.ejeY_visible].setValue(config.representacion(ymin.config))
        else: 
            self.ejeY_max[self.ejeY_visible].setValue(config.representacion(ymax/self.factory2))
            self.ejeY_min[self.ejeY_visible].setValue(config.representacion(ymin/self.factory2))
            
        self.mostrarUnidades()

    def mostrarUnidades(self):
        """Muestra el texto de las unidades en función de la configuración"""
        self.presion.actualizar()
        self.temperatura.actualizar()
        self.volumen.actualizar()
        self.entropia.actualizar()
        self.entalpia.actualizar()
        self.energiaInterna.actualizar()
        self.energiaGibbs.actualizar()
        self.energiaHelmholtz.actualizar()
        self.densidad.actualizar()
        self.cp.actualizar()
        self.cv.actualizar()
        self.conductividad.actualizar()
        self.viscosidad.actualizar()
        self.velocidad.actualizar()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    locale = QtCore.QLocale.system().name()
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("UI_steamTables_" + locale, "i18n"):
        app.installTranslator(qtTranslator)
    SteamTables= Ui_SteamTables()
    SteamTables.show()
    sys.exit(app.exec_())
