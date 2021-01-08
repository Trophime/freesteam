#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
import scipy.constants as k
from ConfigParser import ConfigParser

k.tonUS=2000*k.lb
k.tonUK = 2240*k.lb
k.slug = k.lb*k.g/k.foot
k.Rankine = 1/1.8 #only for differences
k.Reaumur=1/0.8

texto=dict(
            Temperature=['K',u'ºC',u'ºR',u'ºF',u'ºRe'], 
            Pressure=['Pa', 'hPa', 'kPa', 'MPa', 'bar', 'bar g', 'mbar', 'psi', 'psi g', 'atm', u'kg/cm²', u'kg/cm² g', 'mmH2O', 'cmH2O', 'mH2O', 'inH2O', 'ftH2O', 'mmHg', 'cmHg', 'inHg', 'ftHg', u'lb/cm²',u'lb/ft²', u'dyn/cm²' ], 
            Speed=['m/s', 'cm/s', 'mm/s', 'km/s', 'ft/s', 'ft/min',  'm/min', 'km/min','km/h',  'km/day', 'mph', QApplication.translate("unidades", "nudo", None, QApplication.UnicodeUTF8)], 
            Viscosity=[u'Pa·s', u'mPa·s', u'µPa·s', 'P', 'cP', u'dyn/s·cm²', u'µP', 'reyn', u'lb/ft·s', u'lbf/ft²', u'lbf/in²', u'lb/ft·h'], 
            Density=[u'kg/m³', u'g/cm³', u'g/m³', u'kg/cm³', u'lb/ft³',u'lb/inch³' , 'lb/galUK', 'lb/galUS', 'lb/bbl'], 
            ThermalConductivity=[u'W/m·K', u'J/h·m·K', u'cal/s·cm·K', u'cal/h·cm·K',u'kcal/h·m·K' , u'lbf/s·F', u'lb/ft·s³·F',u'Btu/h·ft·F'], 
            SpecificHeat=[u'J/kg·K', u'kJ/kg·K', u'kcal/kg·K', u'kcal/g·K', u'kWh/kg·K', u'Btu/lb·F'], 
            Enthalpy=['J/kg', 'kJ/kg', 'MJ/kg','cal/kg' , 'kcal/kg', 'cal/lb', 'Btu/lb'], 
            SpecificVolume=[u'm³/kg',u'cm³/g' , u'm³/g', u'cm³/kg', u'ft³/lb', u'in³/lb', 'gallon UK/lb', 'gallon US/lb', 'barril/lb', u'ft³/ton UK', u'ft³/ton US', u'ft³/slug', u'ft³/'+QApplication.translate("unidades", "onza", None, QApplication.UnicodeUTF8), u'in³/'+QApplication.translate("unidades", "onza", None, QApplication.UnicodeUTF8), 'gallon UK/'+QApplication.translate("unidades", "onza", None, QApplication.UnicodeUTF8), 'gallon US/'+QApplication.translate("unidades", "onza", None, QApplication.UnicodeUTF8)], 
           )
           
units=dict(
           Temperature=['K','C','R','F','Re'], 
           Pressure=['Pa', 'hPa', 'kPa', 'MPa', 'bar', 'barg', 'mbar', 'psi', 'psig', 'atm', 'kgcm2', 'kgcm2g', 'mmH2O', 'cmH2O', 'mH2O', 'inH2O', 'ftH2O', 'mmHg', 'cmHg', 'inHg', 'ftHg', 'lbcm2','lbft2', 'dyncm2' ], 
           Speed=['ms', 'cms', 'mms', 'kms', 'fts', 'ftmin',  'mmin', 'kmmin','kmh',  'kmday', 'mph', 'kt'], 
           Viscosity=['Pas', 'mPas', 'muPas', 'P', 'cP', 'dynscm2', 'microP', 'reyn', 'lbfts', 'lbfft2', 'lbfinch2', 'lbfth'], 
           Density=['kgm3', 'gcc', 'gm3', 'kgcc', 'lbft3','lbin3' , 'lbgalUK', 'lbgalUS', 'lbbbl'], 
           ThermalConductivity=['WmK', 'JhmK', 'calscmK', 'calhcmK','kcalhmK' , 'lbfsF', 'lbfts3F','BtuhftF'], 
           SpecificHeat=['JkgK', 'kJkgK', 'kcalkgK', 'kcalgK', 'kWhkgK', 'BtulbF'], 
           Enthalpy=['Jkg', 'kJkg', 'MJkg','calkg' , 'kcalkg', 'callb', 'Btulb'], 
           SpecificVolume=['m3kg','lkg' , 'm3g', 'cckg', 'ft3lb', 'inch3lb', 'galUKlb', 'galUSlb', 'bbllb', 'ft3tonUK', 'ft3tonUS', 'ft3slug',  'ft3oz', 'in3oz', 'galUKoz', 'galUSoz'], 
        )
        
tooltip=dict(
            Temperature=['Kelvin','Celsius','Rankine','Fahrenheit','Reaumur'], 
           Pressure=['Pascal', '', '', '', 'bar', '', '', QApplication.translate("unidades", "libras por pulgada cuadrada", None, QApplication.UnicodeUTF8), '', 'atm', 'kgcm2', 'kgcm2g', 'mmH2O', 'cmH2O', 'mH2O', 'inH2O', 'ftH2O', 'mmHg', 'cmHg', 'inHg', 'ftHg', 'lbcm2','lbft2', 'dyncm2' ], 
            Speed=['m/s', 'cm/s', 'mm/s', 'km/s', 'ft/s', 'ft/min',  'm/min', 'km/min','km/h',  'km/day', QApplication.translate("unidades", "millas por hora", None, QApplication.UnicodeUTF8), QApplication.translate("unidades", "nudo", None, QApplication.UnicodeUTF8)], 
            Viscosity=[u'Pa·s', u'mPa·s', u'µPa·s', 'Poise', 'centipoise', u'dyn/s·cm²', u'µP', 'reyn', u'lb/ft·s', u'lbf/ft²', u'lbf/in²', u'lb/ft·h'], 
            Density=[u'kg/m³', u'g/cm³', u'g/m³', u'kg/cm³', u'lb/ft³',u'lb/inch³' , 'lb/galUK', 'lb/galUS', 'lb/barril'], 
            ThermalConductivity=[u'W/m·K', u'J/h·m·K', u'cal/s·cm·K', u'cal/h·cm·K',u'kcal/h·m·K' , u'lbf/s·F', u'lb/ft·s³·F',u'Btu/h·ft·F'], 
            SpecificHeat=[u'J/kg·K', u'kJ/kg·K', u'kcal/kg·K', u'kcal/g·K', u'kWh/kg·K', u'Btu/lb·F'], 
            Enthalpy=['J/kg', 'kJ/kg', 'MJ/kg','cal/kg' , 'kcal/kg', 'cal/lb', 'Btu/lb'], 
           SpecificVolume=['m3kg','lkg' , 'm3g', 'cckg', 'ft3lb', 'inch3lb', 'galUKlb', 'galUSlb', 'bbllb', 'ft3tonUK', 'ft3tonUS', 'ft3slug',  'ft3oz', 'in3oz', 'galUKoz', 'galUSoz'], 
           )


class Temperature(float):
    """Clase que modela la magnitud temperatura
    Unidades soportadas:
    * Kelvin (por defecto)
    * Celsius
    * Fahrenheit
    * Rankine
    * Reaumur
    """
    
    def __init__(self,data):
        self.data = float(data)

    def C2K(self, C):
        """Convert Celcius to Kelvin"""
        return C + 273.15

    def K2C(self, K):
        """Convert Kelvin to Celcius"""
        return K - 273.15
        
    def K2R(self, K):
        """Convert Kelvin to Rankine"""
        return K * 1.8
        
    def R2K(self, K):
        """Convert Rankine to Kelvin"""
        return K / 1.8

    def F2K(self, F):
        """Convert Fahrenheit to Kelvin"""
        return ((F - 32) / 1.8)+273.15

    def K2F(self, K):
        """Convert Kelvin to Fahrenheit"""
        return 1.8*(K-273.15)+32
        
    def Re2K(self, Re):
        """Convert Reaumur to Kelvin"""
        return (Re*1.25)+273.15

    def K2Re(self, K):
        """Convert Kelvin to Reaumur"""
        return (K-273.15)/1.25
        
    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='K'):
        if units == 'K':
            return self.__factory(self.data)
        elif units == 'C':
            return self.__factory(self.C2K(self.data))
        elif units == 'F':
            return self.__factory(self.F2K(self.data))
        elif units == 'R':
            return self.__factory(self.R2K(self.data))
        elif units == 'Re':
            return self.__factory(self.Re2K(self.data))
        else:
            raise ValueError("Wrong temperature input code")
        
    @property
    def K(self):
        return self.__factory(self.data)
    @property
    def C(self):
        return self.__factory(self.K2C(self.data))
    @property
    def F(self):
        return self.__factory(self.K2F(self.data))
    @property
    def R(self):
        return self.__factory(self.K2R(self.data))
    @property
    def Re(self):
        return self.__factory(self.K2Re(self.data))
    @property
    def list(self):
        return self.K, self.C, self.R, self.F, self.Re
        
    def config(self, magnitud="Temperature"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.C
        elif Config.getint('Units',magnitud)==2:
            return self.R
        elif Config.getint('Units',magnitud)==3:
            return self.F
        elif Config.getint('Units',magnitud)==4:
            return self.Re
        else:
            return self.K


class DeltaT(float):
    """Clase que modelo la magnitud Diferencia de temperatura
    Las unidades soportadas son:
    * Kelvin, Celsius (K) por defecto
    * Rankine, Fahrenheit (R)
    * Reaumur (Re)
    """
    
    def __init__(self,data):
        self.data = float(data)        
        
    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='K'):
        if units == 'K':
            return self.__factory(self.data)
        elif units == 'C':
            return self.__factory(self.data)
        elif units == 'F':
            return self.__factory(self.data*k.Rankine)
        elif units == 'R':
            return self.__factory(self.data*k.Rankine)
        elif units == 'Re':
            return self.__factory(self.data*k.Reaumur)
        else:
            raise ValueError("Wrong delta temperature input code")

    @property
    def K(self):
        return self.__factory(self.data)
    @property
    def C(self):
        return self.__factory(self.data)
    @property
    def F(self):
        return self.__factory(self.data/k.Rankine)
    @property
    def R(self):
        return self.__factory(self.data/k.Rankine)
    @property
    def Re(self):
        return self.__factory(self.data/k.Reaumur)
    @property
    def list(self):
        return self.K, self.C, self.R, self.F, self.Re
        
    def config(self, magnitud="Temperature"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.C
        elif Config.getint('Units',magnitud)==2:
            return self.R
        elif Config.getint('Units',magnitud)==3:
            return self.F
        elif Config.getint('Units',magnitud)==4:
            return self.Re
        else:
            return self.K

class Speed(float):
    """Clase que modela la magnitud velocidad
    Las magnitudes soportadas son:
    * metro por segundo (ms) por defecto
    * centimetro por segundo (cms)
    * milimetro por segundo (mms)
    * kilometro por segundo (kms)
    * metros por minuto (mmin)
    * kilometros por minuto (kmmin)
    * kilometros por hora (kmh)
    * metros por día (mday)
    * kilometros por día (kmday)
    * pies por segundo (fts)
    * pies por minuto (ftmin)
    * millas por hora (mph)
    * nudos (kt)
    """

    def __init__(self,data):
        self.data = float(data)
        
    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='ms'):
        if units == 'ms':
            return self.__factory(self.data)
        elif units == 'cms':
            return self.__factory(self.data*k.centi)
        elif units == 'mms':
            return self.__factory(self.data*k.milli)
        elif units == 'kms':
            return self.__factory(self.data*k.kilo)
        elif units == 'mmin':
            return self.__factory(self.data/k.minute)
        elif units == 'kmmin':
            return self.__factory(self.data*k.kilo/k.minute)
        elif units == 'kmh':
            return self.__factory(self.data*k.kilo/k.hour)
        elif units == 'mday':
            return self.__factory(self.data/k.day)
        elif units == 'kmday':
            return self.__factory(self.data*k.kilo/k.day)
        elif units == 'fts':
            return self.__factory(self.data*k.foot)
        elif units == 'ftmin':
            return self.__factory(self.data*k.foot/k.minute)
        elif units == 'fth':
            return self.__factory(self.data*k.foot/k.hour)
        elif units == 'ftday':
            return self.__factory(self.data*k.foot/k.day)
        elif units == 'inchs':
            return self.__factory(self.data*k.inch)
        elif units == 'inchmin':
            return self.__factory(self.data*k.inch/k.minute)
        elif units == 'mph':
            return self.__factory(self.data*k.mile/k.hour)
        elif units == 'kt':
            return self.__factory(self.data*k.nautical_mile/k.hour)
        else:
            raise ValueError("Wrong speed input code")
            
    @property
    def ms(self):
        return self.__factory(self.data)
    @property
    def cms(self):
        return self.__factory(self.data/k.centi)
    @property
    def mms(self):
        return self.__factory(self.data/k.milli)
    @property
    def kms(self):
        return self.__factory(self.data/k.kilo)
    @property
    def mmin(self):
        return self.__factory(self.data*k.minute)
    @property
    def kmmin(self):
        return self.__factory(self.data/k.kilo*k.minute)
    @property
    def kmh(self):
        return self.__factory(self.data/k.kilo*k.hour)
    @property
    def mday(self):
        return self.__factory(self.data*k.day)
    @property
    def kmday(self):
        return self.__factory(self.data/k.kilo*k.day)
    @property
    def fts(self):
        return self.__factory(self.data/k.foot)
    @property
    def ftmin(self):
        return self.__factory(self.data/k.foot*k.minute)
    @property
    def fth(self):
        return self.__factory(self.data/k.foot*k.hour)
    @property
    def ftday(self):
        return self.__factory(self.data/k.foot*k.day)
    @property
    def inchs(self):
        return self.__factory(self.data/k.inch)
    @property
    def inchmin(self):
        return self.__factory(self.data/k.inch*k.minute)
    @property
    def mph(self):
        return self.__factory(self.data/k.mile*k.hour)
    @property
    def kt(self):
        return self.__factory(self.data/k.nautical_mile*k.hour)        
    @property
    def list(self):
        return self.ms, self.cms, self.mms, self.kms, self.fts, self.ftmin, self.mmin, self.kmmin, self.kmh, self.kmday, self.mph, self.kt

    def config(self, magnitud="Speed"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.cms
        elif Config.getint('Units',magnitud)==2:
            return self.mms
        elif Config.getint('Units',magnitud)==3:
            return self.kms
        elif Config.getint('Units',magnitud)==4:
            return self.fts
        elif Config.getint('Units',magnitud)==5:
            return self.ftmin
        elif Config.getint('Units',magnitud)==6:
            return self.mmin
        elif Config.getint('Units',magnitud)==7:
            return self.kmmin
        elif Config.getint('Units',magnitud)==8:
            return self.kmh
        elif Config.getint('Units',magnitud)==9:
            return self.kmday
        elif Config.getint('Units',magnitud)==10:
            return self.mph
        elif Config.getint('Units',magnitud)==11:
            return self.kt
        else:
            return self.ms
        

class SpecificVolume(float):
    """Clase que modela la magnitud volumen específico
    Las magnitudes soportadas son:
    * metro cúbico por kilogramo (m3kg) por defecto (igual que l/gr
    * litro por kilogramo (lkg) (igual que cc/g, ml/g)
    * metro cúbico por gramo (m3g)
    * centímetro cúbico por kilogramo (cckg)
    * pie cúbico por libra (ft3lb)
    * pulgada cúbica (lbin3)
    * galón UK  por libra (galUKlb)
    * galón US  por libra(galUSlb)
    * barril por libra (bbllb)
    * pie cúbico por slug (ft3slug)
    * pie cúbico por onzas (ft3oz)
    * pulgada cubica por onzas (inch3oz)
    * galón UK por onzas (galUKoz)
    * galón US por onzas (galUSoz)    
    """


    def __init__(self,data):
        self.data = float(data)

    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='m3kg'):
        if units == 'm3kg' or units == 'lg':
            return self.__factory(self.data)
        elif units == 'lkg' or units == 'ccg' or units == 'mlg':
            return self.__factory(self.data*k.liter)
        elif units == 'm3g':
            return self.__factory(self.data*k.gram)
        elif units == 'cckg':
            return self.__factory(self.data*k.micro)
        elif units == 'ft3lb':
            return self.__factory(self.data/k.pound*k.foot**3)
        elif units == 'inch3lb':
            return self.__factory(self.data/k.pound*k.inch**3)
        elif units == 'galUKlb':
            return self.__factory(self.data/k.pound*k.gallon_imp)
        elif units == 'galUSlb':
            return self.__factory(self.data/k.pound*k.gallon)
        elif units == 'bbllb':
            return self.__factory(self.data/k.pound*k.bbl)
        elif units == 'ft3tonUK':
            return self.__factory(self.data/k.tonUK*k.foot**3)
        elif units == 'ft3tonUS':
            return self.__factory(self.data/k.tonUS*k.foot**3)
        elif units == 'ft3slug':
            return self.__factory(self.data/k.slug*k.foot**3)
        elif units == 'ft3oz':
            return self.__factory(self.data/k.oz*k.foot**3)
        elif units == 'inch3oz':
            return self.__factory(self.data/k.oz*k.inch**3)
        elif units == 'galUKoz':
            return self.__factory(self.data/k.oz*k.gallon_imp)
        elif units == 'galUSoz':
            return self.__factory(self.data/k.oz*k.gallon)
        else:
            raise ValueError("Wrong specific volume input code")
            
    @property
    def m3kg(self):
        return self.__factory(self.data)
    @property
    def lg(self):
        return self.__factory(self.data)
    @property
    def ccg(self):
        return self.__factory(self.data/k.liter)
    @property
    def mlg(self):
        return self.__factory(self.data/k.liter)
    @property
    def lkg(self):
        return self.__factory(self.data/k.liter)
    @property
    def m3g(self):
        return self.__factory(self.data*k.gram)
    @property
    def cckg(self):
        return self.__factory(self.data/k.micro)
    @property
    def ft3lb(self):
        return self.__factory(self.data/k.foot**3*k.pound)
    @property
    def inch3lb(self):
        return self.__factory(self.data/k.inch**3*k.pound)
    @property
    def galUKlb(self):
        return self.__factory(self.data/k.gallon_imp*k.pound)
    @property
    def galUSlb(self):
        return self.__factory(self.data/k.gallon*k.pound)
    @property
    def bbllb(self):
        return self.__factory(self.data/k.bbl*k.pound)
    @property
    def ft3tonUK(self):
        return self.__factory(self.data/k.foot**3*k.tonUK)
    @property
    def ft3tonUS(self):
        return self.__factory(self.data/k.foot**3*k.tonUS)
    @property
    def ft3slug(self):
        return self.__factory(self.data*k.slug/k.foot**3)
    @property
    def ft3oz(self):
        return self.__factory(self.data/k.foot**3*k.oz)
    @property
    def inch3oz(self):
        return self.__factory(self.data/k.inch**3*k.oz)
    @property
    def galUKoz(self):
        return self.__factory(self.data/k.gallon_imp*k.oz)
    @property
    def galUSoz(self):
        return self.__factory(self.data/k.gallon*k.oz)
    @property
    def list(self):
        return self.m3kg, self.lkg, self.m3g, self.cckg, self.ft3lb, self.inch3lb, self.galUKlb, self.galUSlb, self.bbllb, self.ft3tonUK, self.ft3tonUS, self.ft3slug, self.ft3oz, self.inch3oz, self.galUKoz, self.galUSoz

    def config(self, magnitud="SpecificVolume"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.lkg
        elif Config.getint('Units',magnitud)==2:
            return self.m3g
        elif Config.getint('Units',magnitud)==3:
            return self.cckg
        elif Config.getint('Units',magnitud)==4:
            return self.ft3lb
        elif Config.getint('Units',magnitud)==5:
            return self.inch3lb
        elif Config.getint('Units',magnitud)==6:
            return self.galUKlb
        elif Config.getint('Units',magnitud)==7:
            return self.galUSlb
        elif Config.getint('Units',magnitud)==8:
            return self.bbllb            
        elif Config.getint('Units',magnitud)==9:
            return self.ft3tonUK
        elif Config.getint('Units',magnitud)==10:
            return self.ft3tonUS
        elif Config.getint('Units',magnitud)==11:
            return self.ft3slug
        elif Config.getint('Units',magnitud)==12:
            return self.ft3oz
        elif Config.getint('Units',magnitud)==13:
            return self.in3oz
        elif Config.getint('Units',magnitud)==14:
            return self.galUKoz
        elif Config.getint('Units',magnitud)==15:
            return self.galUSoz
        else:
            return self.m3kg


class Density(float):
    """Clase que modela la magnitud densidad
    Las magnitudes soportadas son:
    * kilogramos por metro cúbico (kgm3) por defecto (igual que gr/l)
    * kilogramos por litro (kgl) (igual que g/cc, g/ml)
    * gramos por metro cúbico (gm3)
    * kilogramos por centímetro cúbico (kgcc)
    * libras por pie cúbico (lbft3)
    * libras por pulgada cúbica (lbin3)
    * libras por galón UK (lbgalUK)
    * libras por galón US (lbgalUS)
    * libras por barril (lbbbl)
    * tonelada UK por pie cúbico (tonUKft3)
    * tonelada US por pie cúbico (tonUSft3)
    * slug por pie cúbico (slugft3)
    * onzas por pie cúbico (ozft3)
    * onzas por pulgada cubica (ozin3)
    * onzas por galón UK (ozgalUK)
    * onzas por galón US (ozgalUS)    
    """


    def __init__(self,data):
        self.data = float(data)
        
    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='kgm3'):
        if units == 'kgm3' or units == 'gl':
            return self.__factory(self.data)
        elif units == 'kgl' or units == 'gcc' or units == 'gml':
            return self.__factory(self.data/k.liter)
        elif units == 'gm3':
            return self.__factory(self.data*k.gram)
        elif units == 'kgcc':
            return self.__factory(self.data/k.micro)
        elif units == 'lbft3':
            return self.__factory(self.data*k.pound/k.foot**3)
        elif units == 'lbin3':
            return self.__factory(self.data*k.pound/k.inch**3)
        elif units == 'lbgalUK':
            return self.__factory(self.data*k.pound/k.gallon_imp)
        elif units == 'lbgalUS':
            return self.__factory(self.data*k.pound/k.gallon)
        elif units == 'lbbbl':
            return self.__factory(self.data*k.pound/k.bbl)
        elif units == 'tonUKft3':
            return self.__factory(self.data*k.tonUK/k.foot**3)
        elif units == 'tonUSft3':
            return self.__factory(self.data*k.tonUS/k.foot**3)
        elif units == 'slugft3':
            return self.__factory(self.data*k.slug/k.foot**3)
        elif units == 'ozft3':
            return self.__factory(self.data*k.oz/k.foot**3)
        elif units == 'ozin3':
            return self.__factory(self.data*k.oz/k.inch**3)
        elif units == 'ozgalUK':
            return self.__factory(self.data*k.oz/k.gallon_imp)
        elif units == 'ozgalUS':
            return self.__factory(self.data*k.oz/k.gallon)
        else:
            raise ValueError("Wrong density input code")
            
    @property
    def kgm3(self):
        return self.__factory(self.data)
    @property
    def gl(self):
        return self.__factory(self.data)
    @property
    def gcc(self):
        return self.__factory(self.data*k.liter)
    @property
    def gml(self):
        return self.__factory(self.data*k.liter)
    @property
    def kgl(self):
        return self.__factory(self.data*k.liter)
    @property
    def gm3(self):
        return self.__factory(self.data/k.gram)
    @property
    def kgcc(self):
        return self.__factory(self.data*k.micro)
    @property
    def lbft3(self):
        return self.__factory(self.data*k.foot**3/k.pound)
    @property
    def lbin3(self):
        return self.__factory(self.data*k.inch**3/k.pound)
    @property
    def lbgalUK(self):
        return self.__factory(self.data*k.gallon_imp/k.pound)
    @property
    def lbgalUS(self):
        return self.__factory(self.data*k.gallon/k.pound)
    @property
    def lbbbl(self):
        return self.__factory(self.data*k.bbl/k.pound)
    @property
    def tonUKft3(self):
        return self.__factory(self.data*k.foot**3/k.tonUK)
    @property
    def tonUSft3(self):
        return self.__factory(self.data*k.foot**3/k.tonUS)
    @property
    def slugft3(self):
        return self.__factory(self.data/k.slug*k.foot**3)
    @property
    def ozft3(self):
        return self.__factory(self.data*k.foot**3/k.oz)
    @property
    def ozin3(self):
        return self.__factory(self.data*k.inch**3/k.oz)
    @property
    def ozgalUK(self):
        return self.__factory(self.data*k.gallon_imp/k.oz)
    @property
    def ozgalUS(self):
        return self.__factory(self.data*k.gallon/k.oz)
    @property
    def list(self):
        return self.kgm3, self.gcc, self.gm3, self.kgcc, self.lbft3, self.lbin3, self.lbgalUK,  self.lbgalUS,  self.lbbbl, self.tonUKft3, self.tonUSft3, self.slugft3, self.ozft3, self.ozin3, self.ozgalUK, self.ozgalUS

    def config(self, magnitud='Density'):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.gcc
        elif Config.getint('Units',magnitud)==2:
            return self.gm3
        elif Config.getint('Units',magnitud)==3:
            return self.kgcc
        elif Config.getint('Units',magnitud)==4:
            return self.lbft3
        elif Config.getint('Units',magnitud)==5:
            return self.lbin3
        elif Config.getint('Units',magnitud)==6:
            return self.lbgalUK
        elif Config.getint('Units',magnitud)==7:
            return self.lbgalUS
        elif Config.getint('Units',magnitud)==8:
            return self.lbbbl
        elif Config.getint('Units',magnitud)==9:
            return self.tonUKft3
        elif Config.getint('Units',magnitud)==10:
            return self.tonUSft3
        elif Config.getint('Units',magnitud)==11:
            return self.slugft3
        elif Config.getint('Units',magnitud)==12:
            return self.ozft3
        elif Config.getint('Units',magnitud)==13:
            return self.ozin3
        elif Config.getint('Units',magnitud)==14:
            return self.ozgalUK
        elif Config.getint('Units',magnitud)==15:
            return self.ozgalUS
        else:
            return self.kgm3


class Pressure(float):
    """Class that models a Pressure measure with conversion utilities
    Suported units are
    * Pascal (Pa)
    * Megapascal (MPa)
    * Hectopascal (hPa)
    * Kilopascal (kPa)
    * Bar (bar)
    * Bar sobre la presión atmosférica (barg)
    * Milibar (mbar)
    * Libras por pulgada cuadrada (psi)
    * Libras por pulgada cuadrada sobre la presión atmosférica (psig)
    * Atmósfera (atm)
    * Atmósfera técnica, kg/cm2 (kgcm2)
    * Atmósfera técnica sobre la presión atmósferíca (kgcm2g)
    * Milímetros de columna de agua (mmH2O)
    * Metro de columna de agua (mH2O)
    * Centímetros de columna de agua (cmH2O)
    * Pulgadas de columna de agua (inH2O)
    * Pies de columna de agua (ftH2O)
    * Milimetros de mercurio (mmHg)
    * Torricelli (torr)
    * Centímetros de mercurio (cmHg)
    * Pulgadas de mercurio (inHg)
    * Pies de mercurio (ftHg)
    * Libras por centímetro curadrado (lbcm2)
    * Libras por pie cuadrado (lbft2)
    * Dinas por centimetro cuadrado (dyncm2)
    """
    
    def __init__(self,data):
        self.data = float(data)

    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a Measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='Pa'):
        if units == 'Pa':
            return self.__factory(self.data)
        elif units == 'MPa':
            return self.__factory(k.mega*self.data)
        elif units == 'hPa':
            return self.__factory(k.hecto*self.data)
        elif units == 'kPa':
            return self.__factory(k.kilo*self.data)
        elif units == 'bar':
            return self.__factory(self.data*k.bar)
        elif units == 'baria':
            return self.__factory(self.data*0.1)
        elif units == 'barg':
            return self.__factory(self.data*k.bar+k.atm)
        elif units == 'mbar':
            return self.__factory(self.data*k.bar/k.kilo)
        elif units == 'psi':
            return self.__factory(self.data*k.psi)
        elif units == 'psig':
            return self.__factory(self.data*k.psi+k.atm)
        elif units == 'atm':
            return self.__factory(self.data*k.atm)
        elif units == 'kgcm2':                      #también llamada atmósfera técnica
            return self.__factory(self.data*k.g*10000)
        elif units == 'kgcm2g':                      
            return self.__factory(self.data*k.g*10000+k.atm)
        elif units == 'mmH2O':
            return self.__factory(self.data*(k.g))
        elif units == 'mH2O':
            return self.__factory(self.data*(k.g*k.kilo))
        elif units == 'cmH2O':
            return self.__factory(self.data*(k.g*10))
        elif units == 'inH2O':
            return self.__factory(self.data*(k.g*k.kilo*k.inch))
        elif units == 'ftH2O':
            return self.__factory(self.data*(k.g*k.kilo*k.foot))
        elif units == 'mmHg':
            return self.__factory(self.data*k.torr)
        elif units == 'cmHg':
            return self.__factory(self.data*k.torr*10)
        elif units == 'inHg':
            return self.__factory(self.data*k.torr*k.inch*k.kilo)
        elif units == 'ftHg':
            return self.__factory(self.data*k.torr*k.foot*k.kilo)
        elif units == 'torr':
            return self.__factory(self.data*k.torr)
        elif units == 'lbcm2':
            return self.__factory(self.data*k.g*k.pound*10000)
        elif units == 'lbft2':
            return self.__factory(self.data*k.g*k.pound/k.foot**2)
        elif units == 'dyncm2':
            return self.__factory(self.data*k.dyn/k.centi**2)
        else:
            raise ValueError("wrong pressure unit input code")

    @property
    def MPa(self):
        return self.__factory(self.data/k.mega)
    @property
    def Pa(self):
        return self.__factory(self.data)
    @property
    def bar(self):
        return self.__factory(self.data/k.bar)
    @property
    def baria(self):
        return self.__factory(self.data*10)
    @property
    def barg(self):
        return self.__factory((self.data-k.atm)/k.bar)
    @property
    def kPa(self):
        return self.__factory(self.data/1000)
    @property
    def hPa(self):
        return self.__factory(self.data/100)
    @property
    def psi(self):
        return self.__factory(self.data/k.psi)
    @property
    def psig(self):
        return self.__factory((self.data-k.atm)/k.psi)
    @property
    def mbar(self):
        return self.__factory(self.data/100)
    @property
    def atm(self):
        return self.__factory(self.data/k.atm)
    @property
    def mmH2O(self):
        return self.__factory(self.data/(k.g))
    @property
    def mH2O(self):
        return self.__factory(self.data/(k.g*k.kilo))
    @property
    def cmH2O(self):
        return self.__factory(self.data/(k.g*10))
    @property
    def mmHg(self):
        return self.__factory(self.data/(k.torr))
    @property
    def cmHg(self):
        return self.__factory(self.data/(k.torr*10))
    @property
    def ftH2O(self):
        return self.__factory(self.data/(k.g*k.kilo*k.foot))
    @property
    def inH2O(self):
        return self.__factory(self.data/(k.g*k.kilo*k.inch))
    @property
    def inHg(self):
        return self.__factory(self.data/(k.torr*k.inch*k.kilo))
    @property
    def ftHg(self):
        return self.__factory(self.data/(k.torr*k.foot*k.kilo))
    @property
    def torr(self):
        return self.__factory(self.data/k.torr)
    @property
    def kgcm2(self):
        return self.__factory(self.data/k.g/10000)
    @property
    def kgcm2g(self):
        return self.__factory((self.data-k.atm)/(k.g*10000))
    @property
    def lbcm2(self):
        return self.__factory((self.data)/(k.g*k.pound*10000))
    @property
    def lbft2(self):
        return self.__factory((self.data)/(k.g*k.pound/k.foot**2))
    @property
    def dyncm2(self):
        return self.__factory((self.data)/(k.dyn/k.centi**2))
    @property
    def list(self):
        return self.Pa, self.hPa, self.kPa, self.MPa, self.bar, self.barg, self.mbar, self.psi, self.psig, self.atm, self.kgcm2, self.kgcm2g, self.mmH2O, self.cmH2O, self.mH2O, self.inH2O, self.ftH2O, self.mmHg, self.cmHg, self.inHg, self.ftHg, self.lbcm2, self.lbft2, self.dyncm2

    def config(self, magnitud="Pressure"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.hPa
        elif Config.getint('Units',magnitud)==2:
            return self.kPa
        elif Config.getint('Units',magnitud)==3:
            return self.MPa
        elif Config.getint('Units',magnitud)==4:
            return self.bar
        elif Config.getint('Units',magnitud)==5:
            return self.barg
        elif Config.getint('Units',magnitud)==6:
            return self.mbar
        elif Config.getint('Units',magnitud)==7:
            return self.psi
        elif Config.getint('Units',magnitud)==8:
            return self.psig
        elif Config.getint('Units',magnitud)==9:
            return self.atm
        elif Config.getint('Units',magnitud)==10:
            return self.kgcm2
        elif Config.getint('Units',magnitud)==11:
            return self.kgcm2g
        elif Config.getint('Units',magnitud)==12:
            return self.mmH2O
        elif Config.getint('Units',magnitud)==13:
            return self.cmH2O
        elif Config.getint('Units',magnitud)==14:
            return self.mH2O
        elif Config.getint('Units',magnitud)==15:
            return self.inH2O
        elif Config.getint('Units',magnitud)==16:
            return self.ftH2O
        elif Config.getint('Units',magnitud)==17:
            return self.mmHg
        elif Config.getint('Units',magnitud)==18:
            return self.cmHg
        elif Config.getint('Units',magnitud)==19:
            return self.inHg
        elif Config.getint('Units',magnitud)==20:
            return self.ftHg
        elif Config.getint('Units',magnitud)==21:
            return self.lbcm2
        elif Config.getint('Units',magnitud)==22:
            return self.lbft2
        elif Config.getint('Units',magnitud)==23:
            return self.dyncm2
        else:
            return self.Pa


class Enthalpy(float):
    """
    Clase que modela la magnitud entalpía (base másica).
    Las unidades soportadas son:
    * Julios por kg (Jkg) por defecto
    * Kilojulios por kg (kJkg)
    * Megajulios por kg (MJkg)
    * Kilowatios hora por kg (kWhkg)
    * Calorias por kg (calkg)
    * Kilocalorias por kg (kcalkg)
    * Calorías por gramo (calg)
    * Calorías por libra (callb)
    * Kilocalorias por g (kcalg)
    * Btu por libra (Btulb)
    
    Para obtener el valor expresado en moles multiplicar por el peso molecular
    """

    def __init__(self,data):
        self.data = float(data)

    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='Jkg'):
        if units == 'Jkg':
            return self.__factory(self.data)
        elif units == 'kJkg' or units == 'Jg':
            return self.__factory(self.data*k.kilo)
        elif units == 'MJkg':
            return self.__factory(self.data*k.mega)
        elif units == 'kWhkg':
            return self.__factory(self.data*k.hour*k.kilo)
        elif units == 'calkg':
            return self.__factory(self.data*k.calorie)
        elif units == 'kcalkg' or units == 'calg':
            return self.__factory(self.data*k.calorie*k.kilo)
        elif units == 'callb':
            return self.__factory(self.data*k.calorie/k.lb)
        elif units == 'kcalg':
            return self.__factory(self.data*k.calorie*k.mega)
        elif units == 'Btulb':
            return self.__factory(self.data*k.Btu/k.lb)
        raise ValueError("wrong enthalpy unit input code")
    @property
    def Jkg(self):
        return self.__factory(self.data)
    @property
    def kJkg(self):
        return self.__factory(self.data/k.kilo)
    @property
    def Jg(self):
        return self.__factory(self.data/k.kilo)
    @property
    def MJkg(self):
        return self.__factory(self.data/k.mega)
    @property
    def kWhkg(self):
        return self.__factory(self.data/k.kilo/k.hour)
    @property
    def calkg(self):
        return self.__factory(self.data/k.calorie)
    @property
    def kcalkg(self):
        return self.__factory(self.data/k.kilo/k.calorie)
    @property
    def calg(self):
        return self.__factory(self.data/k.kilo/k.calorie)
    @property
    def callb(self):
        return self.__factory(self.data*k.lb/k.calorie)
    @property
    def kcalg(self):
        return self.__factory(self.data/k.mega/k.calorie)
    @property
    def Btulb(self):
        return self.__factory(self.data*k.lb/k.Btu)
    @property
    def list(self):
        return self.Jkg, self.kJkg, self.MJkg, self.calkg, self.kcalkg, self.callb, self.Btulb
    
    def config(self, magnitud='Enthalpy'):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.kJkg
        elif Config.getint('Units',magnitud)==2:
            return self.MJkg
        elif Config.getint('Units',magnitud)==3:
            return self.calkg
        elif Config.getint('Units',magnitud)==4:
            return self.kcalkg
        elif Config.getint('Units',magnitud)==5:
            return self.callb
        elif Config.getint('Units',magnitud)==6:
            return self.Btulb
        else:
            return self.Jkg        


class SpecificHeat(float):
    """Clase que modela la magnitud calor específico, capacidades caloríficas, entropia específica...
    Las magnitudes soportadas son:
    * Julios por kilogramo y kelvin (JkgK) por defecto
    * kilojulios por kilogramo y kelvin (kJkgK)
    * julio por gramo y kelvin (JgK)
    * Calorias por kilogramo y kelvin (kcalkgK)
    * Calorías por gramo y kelvin (calgK)
    * kilocalorias por gramo y kelvin (kcalgK)
    * kilowatio hora por kilogramo y kelvin (kWhkgK)
    * Btu por libra y fahrenheit (BtulbF)

    """

    def __init__(self,data):
        self.data = float(data)
        
    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='JkgK'):
        if units == 'JkgK':
            return self.__factory(self.data)
        elif units == 'kJkgK' or units == "JgK":
            return self.__factory(self.data*k.kilo)
        elif units == 'kcalkgK' or units == "calgK":
            return self.__factory(self.data*k.calorie*k.kilo)
        elif units == 'kcalgK':
            return self.__factory(self.data*k.calorie*k.kilo**2)
        elif units == 'kWhkgK':
            return self.__factory(self.data*k.kilo*k.hour)
        elif units == 'BtulbF':
            return self.__factory(self.data*k.Btu/k.lb/k.Rankine)
        else:
            raise ValueError("Wrong Specific heat input code")
    @property
    def JkgK(self):
        return self.__factory(self.data)
    @property
    def kJkgK(self):
        return self.__factory(self.data/k.kilo)
    @property
    def JgK(self):
        return self.__factory(self.data/k.kilo)
    @property
    def kcalkgK(self):
        return self.__factory(self.data/k.calorie/k.kilo)
    @property
    def calgK(self):
        return self.__factory(self.data/k.calorie/k.kilo)
    @property
    def kcalgK(self):
        return self.__factory(self.data/k.calorie/k.kilo**2)
    @property
    def kWhkgK(self):
        return self.__factory(self.data/k.kilo/k.hour)
    @property
    def BtulbF(self):
        return self.__factory(self.data*k.lb*k.Rankine/k.Btu)
    @property
    def list(self):
        return self.JkgK, self.kJkgK, self.kcalkgK, self.kcalgK, self.kWhkgK, self.BtulbF
        
    def config(self, magnitud="SpecificHeat"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.kJkgK
        elif Config.getint('Units',magnitud)==2:
            return self.kcalkgK
        elif Config.getint('Units',magnitud)==3:
            return self.kcalgK
        elif Config.getint('Units',magnitud)==4:
            return self.kWhkgK
        elif Config.getint('Units',magnitud)==5:
            return self.BtulbF
        else:
            return self.JkgK
            

class ThermalConductivity(float):
    """Clase que modela la magnitud conductividad térmica
    Las magnitudes soportadas son:
    * Watios por metro y Kelvin (WmK) por defecto
    * Julio por hora metro y Kelvin (JhmK)
    * Kilojulio por hora metro y Kelvin (kJhmK)
    * calorias por segundo, centimetro y kelvin (calscmK)
    * calorias por hora, centimetro y kelvin (calhcmK)
    * calorias por hora, milimetro y kelvin (calhmmK)
    * kcalorias por hora metro y kelvin (kcalhmK)
    * libra fuerza por segundo y fahrenheit (lbfsF)
    * libra pie por segundo cubico y fahrenheit (lbfts3F)
    * Btu por hora pie y fahrenheit (BtuhftF)

    """

    def __init__(self,data):
        self.data = float(data)
        
    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='WmK'):
        if units == 'WmK':
            return self.__factory(self.data)
        elif units == 'JhmK':
            return self.__factory(self.data/k.hour)
        elif units == 'kJhmK':
            return self.__factory(self.data*k.kilo/k.hour)
        elif units == 'calscmK':
            return self.__factory(self.data*k.calorie/k.centi)
        elif units == 'calhcmK':
            return self.__factory(self.data*k.calorie/k.centi/k.hour)
        elif units == 'calhmmK':
            return self.__factory(self.data*k.calorie/k.milli/k.hour)
        elif units == 'kcalhmK':
            return self.__factory(self.data*k.calorie*k.kilo/k.hour)
        elif units == 'lbfsF':
            return self.__factory(self.data*k.lbf/k.Rankine)
        elif units == 'lbfts3F':
            return self.__factory(self.data*k.lb*k.foot/k.Rankine)
        elif units == 'BtuhftF':
            return self.__factory(self.data*k.Btu/k.hour/k.foot/k.Rankine)
        else:
            raise ValueError("Wrong thermal conductivity input code")

    @property
    def WmK(self):
        return self.__factory(self.data)
    @property
    def JhmK(self):
        return self.__factory(self.data*k.hour)
    @property
    def kJhmK(self):
        return self.__factory(self.data*k.hour/k.kilo)
    @property
    def calscmK(self):
        return self.__factory(self.data*k.centi/k.calorie)
    @property
    def calhcmK(self):
        return self.__factory(self.data*k.centi*k.hour/k.calorie)
    @property
    def calhmmK(self):
        return self.__factory(self.data*k.milli*k.hour/k.calorie)
    @property
    def kcalhmK(self):
        return self.__factory(self.data*k.hour/k.calorie/k.kilo)
    @property
    def lbfsF(self):
        return self.__factory(self.data*k.Rankine/k.lbf)
    @property
    def lbfts3F(self):
        return self.__factory(self.data*k.Rankine/k.lb/k.foot)
    @property
    def BtuhftF(self):
        return self.__factory(self.data*k.hour*k.foot*k.Rankine/k.Btu)
    @property
    def list(self):
        return self.WmK, self.JhmK, self.calscmK, self.calhcmK, self.kcalhmK, self.lbfsF, self.lbfts3F, self.BtuhftF
        
    def config(self, magnitud='ThermalConductivity'):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.JhmK
        elif Config.getint('Units',magnitud)==2:
            return self.calscmK
        elif Config.getint('Units',magnitud)==3:
            return self.calhcmK
        elif Config.getint('Units',magnitud)==4:
            return self.kcalhmK
        elif Config.getint('Units',magnitud)==5:
            return self.lbfsF
        elif Config.getint('Units',magnitud)==6:
            return self.lbfts3F
        elif Config.getint('Units',magnitud)==7:
            return self.BtuhftF
        else:
            return self.WmK        


class Viscosity(float):
    """Clase que modela la magnitud viscosidad dinámica
    Las magnitudes soportadas son:
    * Pascal por segundo (Pas) por defecto
    * Milipascal por segundo (mPas)
    * Micropascal por segundo (muPas)
    * Dinas segundo por centimetro cuadrado (dynscm2)
    * Poise (P)
    * Centipoise (cP)
    * Reyn (reyn)
    * libra (masa) por pie y segundo (lbfts)
    * libra (fuerza) por segundo entre pie cuadrado (lbfft2)
    * libra (fuerza) por segundo entre pulgada cuadrada (lbfinch2)
    * libra (masa) por pie y hora (lbfth)
    """
    
    def __init__(self,data):
        self.data = float(data)

    @classmethod
    def __factory(cls,data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self,units='Pas'):
        if units == 'Pas':
            return self.__factory(self.data)
        elif units == 'mPas':
            return self.__factory(self.data*k.milli)
        elif units == 'muPas':
            return self.__factory(self.data*k.micro)
        elif units == 'P':
            return self.__factory(self.data*0.1)
        elif units == 'cP'or units == 'dynscm2':
            return self.__factory(self.data*k.milli)
        elif units == 'microP':
            return self.__factory(self.data*0.1*k.micro)
        elif units == 'reyn':
            return self.__factory(self.data*k.g*k.pound/k.inch**2)
        elif units == 'lbfts':
            return self.__factory(self.data*k.pound/k.foot)
        elif units == 'lbfft2':
            return self.__factory(self.data*k.g*k.pound/k.foot**2)
        elif units == 'lbfinch2':
            return self.__factory(self.data*k.g*k.pound/k.inch**2)
        elif units == 'lbfth':
            return self.__factory(self.data*k.pound/k.foot/k.hour)
        else:
            raise ValueError("wrong viscosity unit input code")

    @property
    def Pas(self):
        return self.__factory(self.data)
    @property
    def mPas(self):
        return self.__factory(self.data/k.milli)
    @property
    def muPas(self):
        return self.__factory(self.data/k.micro)
    @property
    def dynscm2(self):
        return self.__factory(self.data/0.1)
    @property
    def P(self):
        return self.__factory(self.data/0.1)
    @property
    def cP(self):
        return self.__factory(self.data/k.milli)
    @property
    def microP(self):
        return self.__factory(self.data/0.1/k.micro)
    @property
    def reyn(self):
        return self.__factory(self.data/(k.g*k.pound/k.inch**2))
    @property
    def lbfts(self):
        return self.__factory(self.data/(k.pound/k.foot))
    @property
    def lbfft2(self):
        return self.__factory(self.data/(k.g*k.pound/k.foot**2))
    @property
    def lbfinch2(self):
        return self.__factory(self.data/(k.g*k.pound/k.inch**2))
    @property
    def lbfth(self):
        return self.__factory(self.data/(k.pound/k.foot/k.hour))
    @property
    def list(self):
        return self.Pas, self.mPas, self.muPas, self.P, self.cP, self.dynscm2, self.microP, self.reyn, self.lbfts, self.lbfft2, self.lbfinch2, self.lbfth
        
    def config(self, magnitud="Viscosity"):
        Config=ConfigParser()
        Config.read("UI_steamTablesrc")
        if Config.getint('Units',magnitud)==1:
            return self.mPas
        elif Config.getint('Units',magnitud)==2:
            return self.muPas
        elif Config.getint('Units',magnitud)==3:
            return self.P
        elif Config.getint('Units',magnitud)==4:
            return self.cP
        elif Config.getint('Units',magnitud)==5:
            return self.dynscm2
        elif Config.getint('Units',magnitud)==6:
            return self.microP
        elif Config.getint('Units',magnitud)==7:
            return self.reyn
        elif Config.getint('Units',magnitud)==8:
            return self.lbfts
        elif Config.getint('Units',magnitud)==9:
            return self.lbfft2
        elif Config.getint('Units',magnitud)==10:
            return self.lbfinch2
        elif Config.getint('Units',magnitud)==11:
            return self.lbfth
        else:
            return self.Pas        


if __name__ == "__main__":
    T=Temperature(273.15)
    print T.C,  T,  T.F, T.R, T.Re
    print T.config
#
#    P=Pressure(760).unit("mmHg")
#    print "kPa: ",  P.kPa
#    print "atm: ",  P.atm
#    print "kgcm2: ",  P.kgcm2
#    print "bar: ", P.bar
#    print "barg: ", P.barg
#    print "mbar: ", P.mbar
#    print "mH2O: ", P.mH2O
#    print "ftH20: ", P.ftH2O
#    print "torr: ", P.torr
#    print "inHg: ", P.inHg
#    print "psi : ",  P.psi
#
#    l=SpecificHeat(1).unit("BtulbF")
#    print "J/kgK, kJ/kgK: ", l.JkgK, l.kJkgK
#    print "kcal/kgK, kcal/gK: ", l.kcalkgK, l.kcalgK
#    print "Btu/lbF: ", l.BtulbF
#
#    H=Enthalpy(-18130.1).unit("Btulb")
#    print H.kJkg
#
#    R=SpecificVolume(1).unit("m3kg")
#    print "m3/kg, l/kg: ", R.m3kg, R.lkg

