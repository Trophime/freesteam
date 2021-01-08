#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from unidades import texto, units

class Configuracion():
    """Clase que define los valores de las unidades, a partir del archivo de configuración"""
    def __init__(self, magnitud, propiedad=0):
        """Magnitud: string que indica la magnitud deseada, Temperature, Pressure,..."""
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if propiedad==0:
            propiedad=magnitud
        self.magnitud=magnitud
        self.unidades=units[magnitud]
        self.textos=texto[magnitud]
        self.index=Config.getint("Units",propiedad)

        
    def text(self):
        """Devuelve el texto de la unidad, utilizado en label"""
        return self.textos[self.index]
        
    def func(self):
        """Devuelve el texto de definición de la unidad, utilizado en la definición de clases unidad"""
        return self.unidades[self.index]


def representacion(float, decimales=4, tol=4):
    """Función que expresa un valor de tipo float en la forma apropiada en función de su valor
    decimales: numero de decimales a usar en la representación del número
    tolerancia: valor por encima del cual se usa notacion científica"""
    if decimales>0:
        if 1*10**-tol<float<1*10**tol or -1*10**-tol>float>-1*10**tol:
            return str(round(float, decimales))
        elif float==0.0:
            return str(round(float, 1))
        else:
            return "%0.4e" % (float)
    else:
        return str(int(float))

def colors(int):
    """Función que devuelve una lista de colores con el número de elementos indicados"""
    
    if int<=3:
        return ["#0000ff","#00ff00","#ff0000"][:int]
    else:
        trios=int/3
        cojo=int%3
        colores=["#0000ff","#00ff00","#ff0000"]
        for i in range(1, trios):
            nuevo="#%2X%2X%2X" %(0,255/i,255/i)
            colores.append(nuevo.replace(" ", "0"))
            nuevo="#%2X%2X%2X" %(255/i,255/i,0)
            colores.append(nuevo.replace(" ", "0"))
            nuevo="#%2X%2X%2X" %(255/i,0,255/i)
            colores.append(nuevo.replace(" ", "0"))
        if cojo>=1:
            colores.append("#000000")
        if cojo==2:
            colores.append("#888888")
    return colores
        
def C2K(C):
    """Convert Celcius to Kelvin"""
    return C + 273.15

def K2C(K):
    """Convert Kelvin to Celcius"""
    return K - 273.15
    
def K2R(K):
    """Convert Kelvin to Rankine"""
    return K * 1.8
    
def R2K(K):
    """Convert Rankine to Kelvin"""
    return K / 1.8

def F2K(F):
    """Convert Fahrenheit to Kelvin"""
    return ((F - 32) / 1.8)+273.15

def K2F(K):
    """Convert Kelvin to Fahrenheit"""
    return 1.8*(K-273.15)+32
    
def Re2K(Re):
    """Convert Reaumur to Kelvin"""
    return (Re*1.25)+273.15

def K2Re(K):
    """Convert Kelvin to Reaumur"""
    return (K-273.15)/1.25

if __name__ == "__main__":
    print Re2K(80)
    print K2Re(373.15)
    print K2F(273.15)
    print F2K(32)
