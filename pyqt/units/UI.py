#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from os import linesep
from ConfigParser import ConfigParser

from unidades import *
from config import Configuracion, representacion
from images import images_rc

Config=ConfigParser()
Config.read("UI_steamTablesrc")

class Entrada_con_unidades(QtGui.QWidget):
    """Clase que define el widget con entrada de datos y boton de dialogo de unidades"""
    valueChanged = QtCore.pyqtSignal(float)
    def __init__(self, dialogo, unidad, magnitud, UIconfig=None, retornar=True, readOnly=False, boton=True, texto=True, textounidad="", value=None, start=0, max=float("inf"), min=0, decimales=4, tolerancia=4, parent=None, width=85, resaltado=False, spinbox=False, suffix="", step=0.01, colorReadOnly=None, colorResaltado=None, frame=True):
        """
        Dialogo: el dialogo de unidades usado por el conversor de unidades
        unidad: la unidad que se va a usar
        magnitud: la magnitud para obtener la configuración
        UIconfig: magnitud secundaria en el caso de que sea diferente a la magnitud principal, por ejemplo entropia que usa la unidad del calor específico pero en la configuración puede definirse diferente que el propio calor específico
        retornar: boolean que indica si al cerrar el dialogo de unidades se cambia el valor de la entrada
        readOnly: boolean que indica si la entrada es editable
        boton: boolean que indica si se muestra el botón de unidades
        texto: boolean que indica si se muestra a la derecha del botón el texto con la unidad
        textounidad: texto a usar en el caso de unidades no habituales, magnitues adimensionales...
        value: opcionalmente se puede definir el valor inicial del widget
        start: valor inicial en el caso de que se use spinbox
        max: valor máximo que puede tomar el valor
        min: valor minimo que puede tomar el valor
        decimales: indica el número de decimales a mostrar en la entrada
        tolerancia: valor del exponente de la notación cientifica por encima del cual se usara notación cientifica
        width: anchura de la entrada de texto
        resaltado: boolean que indica si se debe mostrar la entrada resaltada
        spinbox: boolean que indica si se debe responder a las flechas arriba y abajo como si fuera un spinbox
        step: valor que indica el incremento que tendrá el valor al presionar las techas de fecha arriba y abajo, como el step de un spinbox
        colorResaltado: color del resaltado
        colorReadOnly: color de las entradas con readOnly
        frame: booleano que indica si se muestra frame
        """
        super(Entrada_con_unidades, self).__init__(parent)
        self.resize(self.minimumSize())
        self.dialogo=dialogo
        self.unidad=unidad
        self.magnitud=magnitud
        self.decimales=decimales
        self.tolerancia=tolerancia
        self.step=step
        self.spinbox=spinbox
        self.max=max
        self.suffix=suffix
        self.min=min
        self.start=start
        self.textounidad=textounidad
        if colorReadOnly:
            self.colorReadOnly=colorReadOnly
        else:
            self.colorReadOnly=QtGui.QColor(Config.get("General", 'ColorReadOnly'))
        if colorResaltado:
            self.colorResaltado=colorResaltado
        else:
            self.colorResaltado=QtGui.QColor(Config.get("General", 'ColorResaltado'))
        if UIconfig:
            self.UIconfig=UIconfig
        else:
            self.UIconfig=magnitud
        self.retornar=retornar
        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.entrada = QtGui.QLineEdit()
        self.entrada.setFixedSize(width, 24)
        self.entrada.editingFinished.connect(self.entrada_editingFinished)
        self.entrada.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        if unidad==int:
            if max==float("inf"):
                max=1000000000
            self.entrada.setValidator(QtGui.QIntValidator(min, max, self))
        else:
            self.entrada.setValidator(QtGui.QDoubleValidator(min, max, decimales, self))
        self.setReadOnly(readOnly)
        self.setRetornar(self.retornar)
        self.setFrame(frame)
        self.boton=boton
        layout.addWidget(self.entrada, 0, 1)
        if value==None:
            self.value=None
        else:
            self.setValue(value)
        if magnitud:
            if boton:
                self.unidades = QtGui.QToolButton()
                self.unidades.setFixedSize(12, 24)
                self.unidades.setText(".")
                self.unidades.setVisible(False)
                self.unidades.clicked.connect(self.unidades_clicked)
                layout.addWidget(self.unidades, 0, 1)
                
        if texto:
            self.texto = QtGui.QLabel()
            self.texto.setAlignment(QtCore.Qt.AlignVCenter)
            self.texto.setIndent(5)
            if UIconfig:
                self.texto.setText(Configuracion(self.magnitud, UIconfig).text())
            elif magnitud:
                self.texto.setText(Configuracion(self.magnitud).text())
            else:
                self.texto.setText(textounidad)
            layout.addWidget(self.texto, 0, 2)
                
        layout.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed), 0, 3)
        self.setResaltado(resaltado)

    def unidades_clicked(self):
        if self.magnitud=="Currency":
            dialog=self.dialogo.Dialog(self.value)
        else:
            dialog=self.dialogo(self.value)
        
        if dialog.exec_() and self.retornar:
            self.entrada.setText(config.representacion(dialog.value.config(self.UIconfig))+self.suffix)
            self.value=dialog.value
            self.valueChanged.emit(self.value)
            
    def entrada_editingFinished(self):
        if not self.readOnly:
            if self.unidad<>int:
                self.entrada.setText(representacion(float(self.entrada.text().replace(',', '.')), self.decimales, self.tolerancia))
            if self.magnitud:
                self.value=self.unidad(float(self.entrada.text())).unit(Configuracion(self.magnitud, self.UIconfig).func())
            else:
                self.value=self.unidad(self.entrada.text())
            self.valueChanged.emit(self.value)
            self.setToolTip()
        
    def actualizar(self):
        if self.value:
            self.value=self.unidad(self.value)
            self.entrada.setText(representacion(self.value.config(), self.decimales, self.tolerancia)+self.suffix)
        if  self.magnitud and self.texto:
            self.texto.setText(Configuracion(self.magnitud).text())
        
    def clear(self):
        self.entrada.setText("")
        self.value=None

    def setResaltado(self, bool):
        paleta = QtGui.QPalette()
        if bool:
            paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(self.colorResaltado))
        elif self.readOnly:
            paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(self.colorReadOnly))
        else:
            paleta.setColor(QtGui.QPalette.Base, QtGui.QColor("white"))
        self.entrada.setPalette(paleta)        

    def setReadOnly(self, readOnly):
        self.entrada.setReadOnly(readOnly)
        self.readOnly=readOnly

    def setRetornar(self, retornar):
        self.retornar=retornar
            
    def setValue(self, value):
        self.value=self.unidad(value)
        if self.magnitud:
            self.entrada.setText(representacion(self.value.config(self.UIconfig), self.decimales, self.tolerancia)+self.suffix)
        elif self.unidad==float:
            self.entrada.setText(representacion(self.value, self.decimales, self.tolerancia)+self.suffix)
        else:
            self.entrada.setText(str(self.value)+self.suffix)
        self.setToolTip()

    def setFrame(self, frame):
        self.entrada.setFrame(frame)
        self.frame=frame

    def setToolTip(self):
        try:
            lista=eval(Config.get('Tooltip',self.magnitud))
        except: lista=[]
        if len(lista)>0:
            valores=[]
            for i in lista:
                valores.append(representacion(self.value.list[i], self.decimales, self.tolerancia)+" "+texto[self.magnitud][i])
            self.entrada.setToolTip(linesep.join(valores))
            
    def keyPressEvent(self, e):
        """Metodo para poder manejar la pulsación de las techas arriba y abajo tal y como si fuera un spinbox"""
        if self.spinbox and not self.readOnly:
            if not self.value:
                self.value=self.start
            if e.key()==QtCore.Qt.Key_Up:
                valor=self.value+self.step
                if valor>self.max:
                    self.setValue(self.max)
                else:
                    self.setValue(valor)
            elif e.key()==QtCore.Qt.Key_Down:
                valor=self.value-self.step
                if valor<self.min:
                    self.setValue(self.min)
                else:
                    self.setValue(valor)
            self.valueChanged.emit(self.value)
            
    def enterEvent(self, event):
        if self.magnitud and self.boton:
            self.unidades.setVisible(True)
        
    def leaveEvent(self, event):
        if self.magnitud and self.boton:
            self.unidades.setVisible(False)


class CellEditor(QtGui.QItemDelegate):
    """Clase que define el widget usado para editar datos numéricos en tablas, forzando que la entrada sea numérica"""
    def __init__(self, parent=None):
        super(CellEditor, self).__init__(parent)

    def createEditor(self, parent, option, index):
        widget=QtGui.QLineEdit(parent)
        widget.setAlignment(QtCore.Qt.AlignRight)
        widget.setValidator(QtGui.QDoubleValidator(self))
        return widget
        
class CheckEditor(QtGui.QItemDelegate):
    """Clase que define un checkbox usado en tablas"""
    def __init__(self, parent=None):
        super(CheckEditor, self).__init__(parent)

    def createEditor(self, parent, option, index):
        widget=QtGui.QCheckBox(parent)
        return widget

class Converter(QtGui.QDialog):
    """Clase genérica de conversor de unidades"""
    def __init__(self, magnitud, unidad, titulo, valor=None, parent=None):
        """magnitud: String con el código de la magnitud
        unidad: Nombre de la unidad a usar
        titulo: titulo de la ventana
        valor: opcionalmente se puede iniciar el dialogo con este valor"""
        super(Converter, self).__init__(parent)
        self.texto=texto[magnitud]
        self.unit=units[magnitud]
        self.tooltip=tooltip[magnitud]
        self.unidad=unidad
        if valor:
            self.value=self.unidad(valor)
        self.setWindowTitle(titulo)
        self.semaforo=QtCore.QSemaphore(1)
        self.gridLayout = QtGui.QGridLayout(self)
        self.tabla=QtGui.QTableWidget()
        self.tabla.setRowCount(len(self.texto))
        self.tabla.setColumnCount(1)
        self.tabla.setItemDelegateForColumn(0, CellEditor(self))
        self.tabla.horizontalHeader().setVisible(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        if magnitud in ["SpecificVolume", "Density", "MassFlow", "VolFlow", "ThermalConductivity", "HeatTransfCoef"]:
            self.resize(215, self.minimumHeight())
        else:
            self.resize(self.minimumSize())

        if magnitud in ["Temperature", "Area", "Volume",  "Length", "Angle", "Time"]:
            x=15
        elif magnitud in["ThermalConductivity"]:
            x=10
        elif magnitud in ["Speed", "Mass", "Acceleration", "Energy", "Enthalpy", "MassFlow", "Diffusivity", "Tension", "Solubility_parameter", "HeatTransfCoef"]:
            x=5
        else: x=0
        self.gridLayout.addItem(QtGui.QSpacerItem(x,15,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),1,0,1,1)
        self.gridLayout.addItem(QtGui.QSpacerItem(x,15,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),1,2,1,1)

        for i in range(len(self.texto)):
            self.tabla.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(self.texto[i]))
            self.tabla.setRowHeight(i,24)
            self.tabla.setItem(i, 0, QtGui.QTableWidgetItem(""))
            self.tabla.item(i, 0).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        for i in range(len(self.tooltip)):
            self.tabla.item(i, 0).setToolTip(self.tooltip[i])
        
        if valor:
            self.rellenarTabla(self.value)
            self.tabla.resizeColumnsToContents()
        self.tabla.setFixedHeight(len(self.texto)*24+4)
        self.gridLayout.addWidget(self.tabla, 1, 1, 1, 1)
        
        self.tabla.cellChanged.connect(self.actualizar)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox,2,0,1,3)

    def rellenarTabla(self, valor):
        for i in range(len(valor.list)):
            self.tabla.item(i, 0).setText(representacion(valor.list[i]))
            
    def actualizar(self, fila, columna):
        if self.semaforo.available()>0:
            self.semaforo.acquire(1)
            self.value=self.unidad(float(self.tabla.item(fila, columna).text())).unit(self.unit[fila])
            self.rellenarTabla(self.value)
            self.semaforo.release(1)


class UI_temperature(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_temperature, self).__init__("Temperature", Temperature, QtGui.QApplication.translate("unidades", "Temperatura", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)
            
class UI_speed(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_speed, self).__init__("Speed", Speed, QtGui.QApplication.translate("unidades", "Velocidad", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)

class UI_specificVolume(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_specificVolume, self).__init__("SpecificVolume", SpecificVolume, QtGui.QApplication.translate("unidades", "Volumen específico", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)
        
class UI_density(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_density, self).__init__("Density", Density, QtGui.QApplication.translate("unidades", "Densidad", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)

class UI_pressure(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_pressure, self).__init__("Pressure", Pressure, QtGui.QApplication.translate("unidades", "Presión", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)
        
class UI_enthalpy(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_enthalpy, self).__init__("Enthalpy", Enthalpy, QtGui.QApplication.translate("unidades", "Entalpía", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)
        
class UI_specificHeat(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_specificHeat, self).__init__("SpecificHeat", SpecificHeat, QtGui.QApplication.translate("unidades", "Calor específico", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)
        
class UI_thermalConductivity(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_thermalConductivity, self).__init__("ThermalConductivity", ThermalConductivity, QtGui.QApplication.translate("unidades", "Conductividad térmica", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)

class UI_tension(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_tension, self).__init__("Tension", Tension, QtGui.QApplication.translate("unidades", "Tensión superficial", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)
        
class UI_viscosity(Converter):
    def __init__(self, valor=None, parent=None):
        super(UI_viscosity, self).__init__("Viscosity", Viscosity, QtGui.QApplication.translate("unidades", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8), valor=valor, parent=parent)


class ConfUnit(QtGui.QDialog):
    """Clase que define el widget con la configuración de unidades"""
    def __init__(self, parent=None):
        super(ConfUnit, self).__init__(parent)
        self.Layout = QtGui.QGridLayout(self)
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle(QtGui.QApplication.translate("SteamTables", "Sistema de unidades", None, QtGui.QApplication.UnicodeUTF8))
        self.Layout.addWidget(self.groupBox, 0, 1, 1, 5)
        self.gridLayout_12 = QtGui.QGridLayout(self.groupBox)
        self.SI = QtGui.QRadioButton(QtGui.QApplication.translate("SteamTables", "SI", None, QtGui.QApplication.UnicodeUTF8))
        self.SI.toggled.connect(self.si)
        self.gridLayout_12.addWidget(self.SI, 0, 1, 1, 1)
        self.English = QtGui.QRadioButton(QtGui.QApplication.translate("SteamTables", "Inglés", None, QtGui.QApplication.UnicodeUTF8))
        self.English.toggled.connect(self.english)
        self.gridLayout_12.addWidget(self.English, 0, 2, 1, 1)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),1,0,1,6)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Presión", None, QtGui.QApplication.UnicodeUTF8)), 2, 1, 1, 1)
        self.conf_presion = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_presion, 2, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Temperatura", None, QtGui.QApplication.UnicodeUTF8)), 3, 1, 1, 1)
        self.conf_temperatura = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_temperatura, 3, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Volumen", None, QtGui.QApplication.UnicodeUTF8)), 4, 1, 1, 1)
        self.conf_volumen = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_volumen, 4, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Entalpía", None, QtGui.QApplication.UnicodeUTF8)), 5, 1, 1, 1)
        self.conf_entalpia = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_entalpia, 5, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Entropía", None, QtGui.QApplication.UnicodeUTF8)), 6, 1, 1, 1)
        self.conf_entropia= QtGui.QComboBox()
        self.Layout.addWidget(self.conf_entropia, 6, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Densidad", None, QtGui.QApplication.UnicodeUTF8)), 7, 1, 1, 1)
        self.conf_densidad = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_densidad, 7, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Conductividad", None, QtGui.QApplication.UnicodeUTF8)), 8, 1, 1, 1)
        self.conf_conductividad = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_conductividad, 8, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Capacidad calorífica", None, QtGui.QApplication.UnicodeUTF8)), 9, 1, 1, 1)
        self.conf_capacidad = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_capacidad, 9, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Viscosidad", None, QtGui.QApplication.UnicodeUTF8)), 10, 1, 1, 1)
        self.conf_viscosidad = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_viscosidad, 10, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Velocidad", None, QtGui.QApplication.UnicodeUTF8)), 11, 1, 1, 1)
        self.conf_velocidad = QtGui.QComboBox()
        self.Layout.addWidget(self.conf_velocidad, 11, 2, 1, 1)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),12,1,1,6)
        
        for i in texto['Temperature']:
            self.conf_temperatura.addItem(i)
        for i in texto['Pressure']:
            self.conf_presion.addItem(i)
        for i in texto['SpecificVolume']:
            self.conf_volumen.addItem(i)
        for i in texto['Enthalpy']:
            self.conf_entalpia.addItem(i)
        for i in texto['SpecificHeat']:
            self.conf_entropia.addItem(i)
            self.conf_capacidad.addItem(i)
        for i in texto['Density']:
            self.conf_densidad.addItem(i)
        for i in texto['ThermalConductivity']:
            self.conf_conductividad.addItem(i)
        for i in texto['Viscosity']:
            self.conf_viscosidad.addItem(i)
        for i in texto['Speed']:
            self.conf_velocidad.addItem(i)
            
        if Config.has_section("Units"):
            self.conf_temperatura.setCurrentIndex(Config.getint("Units","Temperature"))
            self.conf_presion.setCurrentIndex(Config.getint("Units","Pressure"))
            self.conf_volumen.setCurrentIndex(Config.getint("Units","SpecificVolume"))
            self.conf_entalpia.setCurrentIndex(Config.getint("Units","Enthalpy"))
            self.conf_entropia.setCurrentIndex(Config.getint("Units","Entropy"))
            self.conf_densidad.setCurrentIndex(Config.getint("Units","Density"))
            self.conf_conductividad.setCurrentIndex(Config.getint("Units","ThermalConductivity"))
            self.conf_capacidad.setCurrentIndex(Config.getint("Units","SpecificHeat"))
            self.conf_viscosidad.setCurrentIndex(Config.getint("Units","Viscosity"))
            self.conf_velocidad.setCurrentIndex(Config.getint("Units","Speed"))

    def english(self, bool):
        """Configura las unidades acorde con el sistema británico de unidades"""
        self.conf_temperatura.setCurrentIndex(self.conf_temperatura.findText('F'))
        self.conf_presion.setCurrentIndex(self.conf_presion.findText('psi'))
        self.conf_volumen.setCurrentIndex(self.conf_volumen.findText(u'ft³/lb'))
        self.conf_densidad.setCurrentIndex(self.conf_densidad.findText(u'lb/ft³'))
        self.conf_conductividad.setCurrentIndex(self.conf_conductividad.findText(u'Btu/h·ft·F'))
        self.conf_capacidad.setCurrentIndex(self.conf_capacidad.findText(u'Btu/lb·F'))
        self.conf_entalpia.setCurrentIndex(self.conf_entalpia.findText(u'Btu/lb'))
        self.conf_velocidad.setCurrentIndex(self.conf_velocidad.findText(u'ft/s'))
        self.conf_viscosidad.setCurrentIndex(self.conf_viscosidad.findText(u'cP'))
        self.conf_entropia.setCurrentIndex(self.conf_entropia.findText(u'Btu/lb·F'))
        
    def si(self, bool):
        """Configura las unidades acorde con el sistema internacional de unidades"""
        self.conf_temperatura.setCurrentIndex(self.conf_temperatura.findText('K'))
        self.conf_presion.setCurrentIndex(self.conf_presion.findText('bar'))
        self.conf_volumen.setCurrentIndex(self.conf_volumen.findText(u'm³/kg'))
        self.conf_densidad.setCurrentIndex(self.conf_densidad.findText(u'kg/m³'))
        self.conf_conductividad.setCurrentIndex(self.conf_conductividad.findText(u'W/m·K'))
        self.conf_capacidad.setCurrentIndex(self.conf_capacidad.findText(u'kJ/kg·K'))
        self.conf_entalpia.setCurrentIndex(self.conf_entalpia.findText(u'kJ/kg'))
        self.conf_velocidad.setCurrentIndex(self.conf_velocidad.findText(u'm/s'))
        self.conf_viscosidad.setCurrentIndex(self.conf_viscosidad.findText(u'Pa·s'))
        self.conf_entropia.setCurrentIndex(self.conf_entropia.findText(u'kJ/kg·K'))

    def aceptar(self, Config):
        if not Config.has_section("Units"):
            Config.add_section("Units")
        Config.set("Units", "Temperature", self.conf_temperatura.currentIndex())
        Config.set("Units", "Pressure", self.conf_presion.currentIndex())
        Config.set("Units", "Density", self.conf_densidad.currentIndex())
        Config.set("Units", "ThermalConductivity", self.conf_conductividad.currentIndex())
        Config.set("Units", "SpecificHeat", self.conf_capacidad.currentIndex())
        Config.set("Units", "SpecificVolume", self.conf_volumen.currentIndex())
        Config.set("Units", "Enthalpy", self.conf_entalpia.currentIndex())
        Config.set("Units", "Speed", self.conf_velocidad.currentIndex())
        Config.set("Units", "Viscosity", self.conf_viscosidad.currentIndex())
        Config.set("Units", "Entropy", self.conf_entropia.currentIndex())


class ConfTooltip(QtGui.QDialog):
    """Clase que define el widget con la configuración de ventanas emergentes con unidades alternativas"""
    def __init__(self, parent=None):
        super(ConfTooltip, self).__init__(parent)
        self.Layout = QtGui.QGridLayout(self)
        self.eleccion=QtGui.QComboBox()
        self.Layout.addWidget(self.eleccion, 0, 0, 1, 1)
        self.stacked = QtGui.QStackedWidget()
        self.eleccion.currentIndexChanged.connect(self.stacked.setCurrentIndex)
        self.Layout.addWidget(self.stacked, 1, 0, 1, 1)
        self.magnitudes=["Temperature", "Pressure", "Speed", "Viscosity", "Density", "ThermalConductivity", "SpecificHeat", "Enthalpy", "SpecificVolume"]
        self.title=["Temperatura", "Presión", "Velocidad", "Viscosidad", "Densidad", "Conductividad térmica", "Calor específico", "Entalpía", "Volumen específico"]
        self.tabla=[]
        for i, magnitud in enumerate(self.magnitudes):
            textos=texto[magnitud]
            unit=units[magnitud]
            self.tabla.append(QtGui.QTableWidget())
            self.stacked.addWidget(self.tabla[i])
            
            self.tabla[i].setRowCount(len(textos))
            self.tabla[i].setColumnCount(1)
            self.tabla[i].setColumnWidth(0, 16)
            self.tabla[i].setMaximumHeight(200)
            self.tabla[i].setItemDelegateForColumn(0, CheckEditor(self))
            self.tabla[i].horizontalHeader().setVisible(False)
            for j in range(len(textos)):
                self.tabla[i].setVerticalHeaderItem(j, QtGui.QTableWidgetItem(textos[j]))
                self.tabla[i].setRowHeight(j,24)
                self.tabla[i].setItem(j, 0, QtGui.QTableWidgetItem(""))
                self.tabla[i].item(j, 0).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                self.tabla[i].openPersistentEditor(self.tabla[i].item(j, 0))
            self.tabla[i].setFixedHeight(len(textos)*24+4)        
            self.rellenar(magnitud, i)
            self.eleccion.addItem(QtGui.QApplication.translate("SteamTables", self.title[i], None, QtGui.QApplication.UnicodeUTF8))
            
    def rellenar(self, magnitud, tabla):
        lista=eval(Config.get("Tooltip",magnitud))
        for i in lista:
            self.tabla[tabla].item(i, 0).setText("true")

    def aceptar(self, Config):
        if not Config.has_section("Tooltip"):
            Config.add_section("Tooltip")
        for i, tabla in enumerate(self.tabla):
            lista=[]
            for j in range(tabla.rowCount()):
                if tabla.item(j, 0).text()=="true":
                    lista.append(j)
            Config.set("Tooltip", self.magnitudes[i], lista)


class Isolinea(QtGui.QDialog):
    """Clase generica de widget con la configuración de isolineas"""
    def __init__(self, UI, unidad, magnitud, ConfSection, parent=None):
        """UI: dialogo de conversión de unidades
        unidad: la clase unidad que define la magnitud de las variables
        magnitud: texto con la magnitud a usar"""
        super(Isolinea, self).__init__(parent)
        self.ConfSection=ConfSection
        self.magnitud=magnitud
        self.unidad=unidad
        self.Layout = QtGui.QGridLayout(self)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 0, 1, 1, 4)        
        self.label1 = QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Inicio", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.Layout.addWidget(self.label1, 1, 1, 1, 1)
        self.inicio =Entrada_con_unidades(UI, unidad, magnitud, boton=False, texto=False)
        self.Layout.addWidget(self.inicio, 2, 1, 1, 1)
        self.label2 = QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Fin", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.Layout.addWidget(self.label2, 1, 2, 1, 1)
        self.fin =Entrada_con_unidades(UI, unidad, magnitud, boton=False, texto=False)
        self.Layout.addWidget(self.fin, 2, 2, 1, 1)
        self.label3 = QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Intervalo", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.Layout.addWidget(self.label3, 1, 3, 1, 1)
        if magnitud=="Temperature":
            self.intervalo =Entrada_con_unidades(UI, DeltaT, magnitud, boton=False)
        else:
            self.intervalo =Entrada_con_unidades(UI, unidad, magnitud, boton=False)
        self.Layout.addWidget(self.intervalo, 2, 3, 1, 2)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 3, 1, 1, 4)        
        self.Personalizar = QtGui.QCheckBox(QtGui.QApplication.translate("SteamTables", "Personalizar", None, QtGui.QApplication.UnicodeUTF8))
        self.Layout.addWidget(self.Personalizar, 4, 1, 1, 4)
        self.Lista = QtGui.QLineEdit()
        self.Layout.addWidget(self.Lista, 5, 1, 1, 4)
        self.Personalizar.toggled.connect(self.inicio.setDisabled)
        self.Personalizar.toggled.connect(self.fin.setDisabled)
        self.Personalizar.toggled.connect(self.intervalo.setDisabled)
        self.Personalizar.toggled.connect(self.Lista.setEnabled)
        self.Layout.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 6, 1, 1, 4) 
        if magnitud:
            self.Critica = QtGui.QCheckBox(QtGui.QApplication.translate("SteamTables", "Incluir linea del punto crítico", None, QtGui.QApplication.UnicodeUTF8))
            self.Layout.addWidget(self.Critica, 7, 1, 1, 4)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 8, 1, 1, 4)                
        self.groupbox = QtGui.QGroupBox(QtGui.QApplication.translate("SteamTables", "Estilo de línea", None, QtGui.QApplication.UnicodeUTF8))
        self.Layout.addWidget(self.groupbox, 9, 1, 1, 4)
        self.horizontalLayout= QtGui.QHBoxLayout(self.groupbox)
        self.Grosor = QtGui.QDoubleSpinBox()
        self.Grosor.setFixedWidth(60)
        self.Grosor.setAlignment(QtCore.Qt.AlignRight)
        self.Grosor.setRange(0.1, 5)
        self.Grosor.setDecimals(1)
        self.Grosor.setSingleStep(0.1)
        self.horizontalLayout.addWidget(self.Grosor)
        self.Linea = QtGui.QComboBox()
        self.Linea.setFixedWidth(80)
        self.Linea.setIconSize(QtCore.QSize(35, 18))
        lineas=[":/button/line.png", ":/button/dash.png", ":/button/line-dot.png", ":/button/dot.png"]
        for i in lineas:
            self.Linea.addItem(QtGui.QIcon(QtGui.QPixmap(i)), "")
        self.horizontalLayout.addWidget(self.Linea)
        self.ColorButton = QtGui.QToolButton()
        self.ColorButton.clicked.connect(self.ColorButtonClicked)
        self.horizontalLayout.addWidget(self.ColorButton)
        self.horizontalLayout.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed))        
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 10, 1, 1, 1)
        
        self.Label=QtGui.QCheckBox(QtGui.QApplication.translate("SteamTables", "Etiqueta", None, QtGui.QApplication.UnicodeUTF8))
        self.Layout.addWidget(self.Label,11,1,1,1)
        self.unit=QtGui.QCheckBox(QtGui.QApplication.translate("SteamTables", "Unidades en las etiquetas", None, QtGui.QApplication.UnicodeUTF8))
        self.Layout.addWidget(self.unit,12,1,1,3)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Posición", None, QtGui.QApplication.UnicodeUTF8)),13,1,1,1)
        self.Posicion=QtGui.QSlider(QtCore.Qt.Horizontal)
        self.Posicion.valueChanged.connect(self.PosicionChanged)
        self.Layout.addWidget(self.Posicion,13,2,1,1)
        self.label5=QtGui.QLabel(str(self.Posicion.value()))
        self.label5.setAlignment(QtCore.Qt.AlignRight)
        self.Layout.addWidget(self.label5,13,1,1,1)
        self.Layout.addItem(QtGui.QSpacerItem(10,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding), 14, 1, 1, 1)
        
        if Config.has_section(ConfSection):
            self.inicio.setValue(Config.getfloat(ConfSection, 'Start'))
            self.fin.setValue(Config.getfloat(ConfSection, 'End'))
            self.intervalo.setValue(Config.getfloat(ConfSection, 'Step'))
            self.Personalizar.setChecked(Config.getboolean(ConfSection, 'Custom'))
            
            if Config.get(ConfSection, 'List')<>"":
                T=[]
                for i in Config.get(ConfSection, 'List').split(','):
                    if magnitud==None:
                        T.append(representacion(float(i)))
                    else:
                        T.append(representacion(unidad(float(i)).config()))
                self.Lista.setText(",".join(T))
            if magnitud:
                self.Critica.setChecked(Config.getboolean(ConfSection, 'Critic'))
            self.Color=QtGui.QColor(Config.get(ConfSection, 'Color'))
            self.ColorButton.setPalette(QtGui.QPalette(self.Color))
            self.inicio.setDisabled(self.Personalizar.isChecked())
            self.fin.setDisabled(self.Personalizar.isChecked())
            self.intervalo.setDisabled(self.Personalizar.isChecked())
            self.Lista.setEnabled(self.Personalizar.isChecked())
            self.Grosor.setValue(Config.getfloat(ConfSection, 'lineWidth'))
            self.Linea.setCurrentIndex(Config.getint(ConfSection, 'lineStyle'))
            self.Label.setChecked(Config.getboolean(ConfSection, 'Label'))
            self.unit.setChecked(Config.getboolean(ConfSection, 'Units'))
            self.Posicion.setValue(Config.getint(ConfSection, 'Position'))
        
    def PosicionChanged(self, valor):
        self.label5.setText(str(self.Posicion.value()))
        
    def ColorButtonClicked(self):
        """Dialogo de selección de color"""
        dialog=QtGui.QColorDialog(self.Color, self)
        if dialog.exec_():
            self.ColorButton.setPalette(QtGui.QPalette(dialog.currentColor()))
            self.Color=dialog.currentColor()
            
    def aceptar(self, Config):
        if not Config.has_section(self.ConfSection):
            Config.add_section(self.ConfSection)
        Config.set(self.ConfSection, "Start", self.inicio.value)
        Config.set(self.ConfSection, "End", self.fin.value)
        Config.set(self.ConfSection, "Step", self.intervalo.value)
        Config.set(self.ConfSection, "Custom", self.Personalizar.isChecked())
        T=[]
        if not self.Lista.text().isEmpty():
            T1=self.Lista.text().split(',')
            for i in T1:
                if self.magnitud==None:
                    T.append(representacion(float(i)))
                else:
                    T.append(representacion(self.unidad(float(i)).unit(Configuracion(self.magnitud).func())))
        Config.set(self.ConfSection, "List", ",".join(T))
        if self.magnitud:
            Config.set(self.ConfSection, "Critic", self.Critica.isChecked())
        Config.set(self.ConfSection, "Color", self.Color.name())
        Config.set(self.ConfSection, "lineWidth", self.Grosor.value())
        Config.set(self.ConfSection, "lineStyle", self.Linea.currentIndex())
        Config.set(self.ConfSection, "Label", self.Label.isChecked())
        Config.set(self.ConfSection, "Units", self.unit.isChecked())
        Config.set(self.ConfSection, "Position", self.Posicion.value())
        

class General(QtGui.QDialog):
    """Clase con el widget de las características generales"""
    def __init__(self, parent=None):
        super(General, self).__init__(parent)
        self.Layout = QtGui.QGridLayout(self)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 0, 1, 1, 4)        
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Color del resaltado:", None, QtGui.QApplication.UnicodeUTF8)), 1, 1, 1, 1)
        self.ColorButtonResaltado = QtGui.QToolButton()
        self.ColorButtonResaltado.clicked.connect(self.ColorButtonResaltadoClicked)
        self.Layout.addWidget(self.ColorButtonResaltado, 1, 2, 1, 1)
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Color no editables:", None, QtGui.QApplication.UnicodeUTF8)), 2, 1, 1, 1)
        self.ColorButtonReadOnly = QtGui.QToolButton()
        self.ColorButtonReadOnly.clicked.connect(self.ColorButtonReadOnlyClicked)
        self.Layout.addWidget(self.ColorButtonReadOnly, 2, 2, 1, 1)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 2, 1, 1, 4)        
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Tamaño gráficos", None, QtGui.QApplication.UnicodeUTF8)),3,1,1,1)
        self.tamano=QtGui.QSlider(QtCore.Qt.Horizontal)
        self.tamano.setRange(10, 150)
        self.tamano.valueChanged.connect(self.PosicionChanged)
        self.Layout.addWidget(self.tamano,3,3,1,1)
        self.label=QtGui.QLabel()
        self.label.setText(str(self.tamano.value()))
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.Layout.addWidget(self.label,3,2,1,1)
        self.Layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed), 4, 1, 1, 4)        
        self.Layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("SteamTables", "Tamaño de letra para las etiquetas:", None, QtGui.QApplication.UnicodeUTF8)), 5, 1, 1, 2)
        self.PointSize = QtGui.QComboBox()
        self.PointSize.addItem("xx-small")
        self.PointSize.addItem("x-small")
        self.PointSize.addItem("small")
        self.PointSize.addItem("medium")
        self.PointSize.addItem("large")
        self.PointSize.addItem("x-large")
        self.PointSize.addItem("xx-large")
        self.Layout.addWidget(self.PointSize, 5, 3, 1, 1)
        
        self.Layout.addItem(QtGui.QSpacerItem(10,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding), 14, 1, 1, 4)
        
        if Config.has_section("General"):
            self.ColorResaltado=QtGui.QColor(Config.get("General", 'ColorResaltado'))
            self.ColorButtonResaltado.setPalette(QtGui.QPalette(self.ColorResaltado))
            self.ColorReadOnly=QtGui.QColor(Config.get("General", 'ColorReadOnly'))
            self.ColorButtonReadOnly.setPalette(QtGui.QPalette(self.ColorReadOnly))
            self.tamano.setValue(Config.getint("General", 'dpi'))
            self.PointSize.setCurrentIndex(self.PointSize.findText(Config.get("General", 'fontSize')))
        
    def PosicionChanged(self, valor):
        self.label.setText(str(self.tamano.value()))
        
    def ColorButtonResaltadoClicked(self):
        """Dialogo de selección de color"""
        dialog=QtGui.QColorDialog(self.ColorResaltado, self)
        if dialog.exec_():
            self.ColorButtonResaltado.setPalette(QtGui.QPalette(dialog.currentColor()))
            self.ColorResaltado=dialog.currentColor()

    def ColorButtonReadOnlyClicked(self):
        dialog=QtGui.QColorDialog(self.ColorReadOnly, self)
        if dialog.exec_():
            self.ColorButtonReadOnly.setPalette(QtGui.QPalette(dialog.currentColor()))
            self.ColorReadOnly=dialog.currentColor()

    def aceptar(self, Config):
        if not Config.has_section("General"):
            Config.add_section("General")
        Config.set("General", "ColorResaltado", self.ColorResaltado.name())
        Config.set("General", "ColorReadOnly", self.ColorReadOnly.name())
        Config.set("General", "dpi", self.tamano.value())
        Config.set("General", "fontSize", self.PointSize.currentText())

class ConfIsolineas(QtGui.QDialog):
    """Clase que define el widget de configuración de isolineas"""
    def __init__(self, parent=None):
        super(ConfIsolineas, self).__init__(parent)
        self.Layout = QtGui.QGridLayout(self)
        self.comboIsolineas=QtGui.QComboBox()
        self.Layout.addWidget(self.comboIsolineas, 0, 0, 1, 1)
        self.Isolineas = QtGui.QStackedWidget()
        self.comboIsolineas.currentIndexChanged.connect(self.Isolineas.setCurrentIndex)
        self.Layout.addWidget(self.Isolineas, 1, 0, 1, 1)
        self.Isoterma = Isolinea(UI_temperature, Temperature, "Temperature", "Isotherm")
        self.Isolineas.addWidget(self.Isoterma)
        self.Isobara = Isolinea(UI_pressure, Pressure, "Pressure", "Isobar")
        self.Isolineas.addWidget(self.Isobara)
        self.Isoentalpica = Isolinea(UI_enthalpy, Enthalpy, "Enthalpy", "Isoenthalpic")
        self.Isolineas.addWidget(self.Isoentalpica)
        self.Isoentropica = Isolinea(UI_specificHeat, SpecificHeat, "SpecificHeat", "Isoentropic")
        self.Isolineas.addWidget(self.Isoentropica)
        self.Isocora = Isolinea(UI_specificVolume, SpecificVolume, "SpecificVolume", "Isochor")
        self.Isolineas.addWidget(self.Isocora)
        self.Isocalidad = Isolinea(None, float, None, "Isoquality")
        self.Isolineas.addWidget(self.Isocalidad)
            
        self.comboIsolineas.addItem(QtGui.QApplication.translate("SteamTables", "Isoterma", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIsolineas.addItem(QtGui.QApplication.translate("SteamTables", "Isobara", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIsolineas.addItem(QtGui.QApplication.translate("SteamTables", "Isoentálpica", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIsolineas.addItem(QtGui.QApplication.translate("SteamTables", "Isoentrópica", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIsolineas.addItem(QtGui.QApplication.translate("SteamTables", "Isocora", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIsolineas.addItem(QtGui.QApplication.translate("SteamTables", "Isocalidad", None, QtGui.QApplication.UnicodeUTF8))
        
    def aceptar(self):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        self.Isoterma.aceptar(Config)
        self.Isobara.aceptar(Config)
        self.Isoentalpica.aceptar(Config)
        self.Isoentropica.aceptar(Config)
        self.Isocora.aceptar(Config)
        self.Isocalidad.aceptar(Config)
        Config.write(open("UI_steamTablesrc", "w"))

class Preferences(QtGui.QDialog):
    """Clase que define la ventana de configuración de preferencias"""
    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.setWindowTitle(QtGui.QApplication.translate("SteamTables", "Preferencias", None, QtGui.QApplication.UnicodeUTF8))
        self.Layout = QtGui.QGridLayout(self)
        self.stacked = QtGui.QStackedWidget()
        self.Layout.addWidget(self.stacked, 1, 1, 2, 1)
        self.lista=QtGui.QListWidget()
        self.lista.currentRowChanged.connect(self.stacked.setCurrentIndex)
        self.Layout.addWidget(self.lista, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.aceptar)
        self.buttonBox.rejected.connect(self.reject)
        self.Layout.addWidget(self.buttonBox, 3, 0, 1, 2)
        
        self.general=General()
        self.stacked.addWidget(self.general)
        self.lista.addItem(QtGui.QListWidgetItem(QtGui.QApplication.translate("SteamTables", "General", None, QtGui.QApplication.UnicodeUTF8)))
        self.unidades=ConfUnit()
        self.stacked.addWidget(self.unidades)
        self.lista.addItem(QtGui.QListWidgetItem(QtGui.QApplication.translate("SteamTables", "Unidades", None, QtGui.QApplication.UnicodeUTF8)))
        self.tooltip=ConfTooltip()
        self.stacked.addWidget(self.tooltip)
        self.lista.addItem(QtGui.QListWidgetItem(QtGui.QIcon(QtGui.QPixmap(":/button/tooltip.png")), QtGui.QApplication.translate("SteamTables", "Unidades emergentes", None, QtGui.QApplication.UnicodeUTF8)))
        self.Isolineas=ConfIsolineas()
        self.stacked.addWidget(self.Isolineas)
        self.lista.addItem(QtGui.QApplication.translate("SteamTables", "Isolíneas", None, QtGui.QApplication.UnicodeUTF8))

    def aceptar(self):
        self.Isolineas.aceptar()
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        self.general.aceptar(Config)
        self.unidades.aceptar(Config)
        self.tooltip.aceptar(Config)
        Config.write(open("UI_steamTablesrc", "w"))
        self.accept()
        
    def closeEvent(self, event):
        dialog=QtGui.QMessageBox.question(self,QtGui.QApplication.translate("SteamTables", "Salir", None, QtGui.QApplication.UnicodeUTF8), QtGui.QApplication.translate("SteamTables", "¿Guardar cambios?", None, QtGui.QApplication.UnicodeUTF8), QtGui.QMessageBox.Yes| QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if dialog == QtGui.QMessageBox.Yes:
            self.aceptar()
        else:
            event.accept()

class Iso():
    def __init__(self):
        self.inicio=0.0
        self.fin=0.0
        self.intervalo=0.0
        self.Personalizar=False
        self.Lista=[]
        self.Critica=False
        self.Color=""
        self.Grosor=0.0
        self.Linea=0
        self.label=False
        self.units=False
        self.posicion=0
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dialogo = Preferences()
    dialogo.show()
    sys.exit(app.exec_())
