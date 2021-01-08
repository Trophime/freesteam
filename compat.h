/*
freesteam - IAPWS-IF97 steam tables library
Copyright (C) 2004-2005  John Pye

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
/** @file
This file contains some initial attempts at a compatibility wrapping of
freesteam 2.0 to enable it to be called using syntax hopefully identical to, 
or at least approaching, that used in freesteam 0.8.1.

John Pye, Mar 2010.
*/

#ifndef FREESTEAM_COMPAT_H
#define FREESTEAM_COMPAT_H

extern "C"{
#include <freesteam/steam.h>
#include <freesteam/steam_ph.h>
#include <freesteam/steam_pT.h>
#include <freesteam/steam_ps.h>
#include <freesteam/steam_Ts.h>
#include <freesteam/steam_Tx.h>
#include <freesteam/region4.h>
};

template<class T>
T sq(const T& t){
	return t*t;
};

typedef MyDouble Num;

/* UNITS OF MEASUREMENT ALL REDUCED TO DOUBLES */

//--------------------------------
// BASE MEASURES

typedef MyDouble Mass;
typedef MyDouble Length;
typedef MyDouble Time;
typedef MyDouble Temperature;
typedef MyDouble Current;

//--------------------------------
// DERIVED MEASURES

typedef MyDouble Area;
typedef MyDouble Volume;

typedef MyDouble Density;
typedef MyDouble SpecificVolume;

typedef MyDouble DensityPerTime;

typedef MyDouble Frequency;

typedef MyDouble Force;
typedef MyDouble Pressure;
typedef MyDouble Velocity;
typedef MyDouble Acceleration;
typedef MyDouble Torque;
typedef MyDouble Energy;
typedef MyDouble Power;
typedef MyDouble SpecificEnergy;

typedef MyDouble DynamicViscosity;
typedef MyDouble KinematicViscosity;
typedef MyDouble PowerPerLength;
typedef MyDouble PressurePerLength;
typedef MyDouble ForcePerLength;
typedef MyDouble PowerPerMass;

typedef MyDouble DensitySpecificEnergyPerTime;

typedef MyDouble VolFlowRate;
typedef MyDouble MassFlowRate;
typedef MyDouble MassFlowRatePerLength;
typedef MyDouble MassFlowRatePerTime;

typedef MyDouble HeatFlux;
typedef MyDouble MassFlux;

// Thermodynamics

typedef MyDouble Entropy;
typedef MyDouble SpecificEntropy;
typedef MyDouble ThermalConductivity;
typedef MyDouble HeatTransferCoefficient;
typedef MyDouble ThermalResistance;

typedef MyDouble HeatCapacityPerLength;
typedef MyDouble PowerPerTemperature;

typedef MyDouble ThermalExpansionCoefficient;

// Electrical

typedef MyDouble Charge;
typedef MyDouble ElecPotential;
typedef MyDouble Capacitance;
typedef MyDouble Resistance;
typedef MyDouble Conductance;


//----------------------------------------------
// BASE UNITS FOR BASE MEASURES

#define kilogram 1.0
#define metre 1.0
#define second 1.0
#define Kelvin 1.0
#define ampere 1.0

//------------------------------------
// SOME ALTERNATIVE NAMES

typedef Velocity Speed;
typedef Length Distance;
typedef Energy Heat;
typedef Heat Work;		// nice

typedef Power HeatRate;
typedef PowerPerLength HeatRatePerLength;
typedef PowerPerTemperature HeatRatePerTemperature;

typedef Pressure Stress;
typedef HeatTransferCoefficient HTCoeff;
typedef SpecificEntropy SpecificHeatCapacity;	// not the same but the units are the same
typedef SpecificHeatCapacity SpecHeatCap;
typedef SpecificHeatCapacity SpecificGasConstant;
typedef SpecificGasConstant SpecGasConst;

typedef ForcePerLength SurfaceTension;

//------------------------------------
// SI MULTIPLIERS

const MyDouble Tera = 1e12;
const MyDouble Giga = 1e9;
const MyDouble Mega = 1e6;
const MyDouble kilo = 1e3;
const MyDouble hecta = 1e2;
const MyDouble Deca = 10;
const MyDouble deci = 0.1;
const MyDouble centi = 1e-2;
const MyDouble milli = 1e-3;
const MyDouble micro = 1e-6;

//------------------------------------
// COMMON MEASURES (SI)

const Mass gram = milli * kilogram;
const Mass kg = kilogram;

const Length centimetre = metre / 100.0;
const Length kilometre = 1000.0 * metre;

const Area metre2 = metre * metre;
const Area hectare = (100.0 * metre) * (100.0 * metre);

const Volume metre3 = metre2 * metre;
const Volume litre = milli * metre3;
const Volume centimetre3 =
    (centi * metre) * (centi * metre) * (centi * metre);

const Time minute = 60.0 * second;
const Time hour = 60.0 * minute;
const Time day = 24.0 * hour;

const Frequency Hertz = 1.0 / second;

const Force Newton = kilogram * metre / (second * second);

const Pressure Pascal = Newton / (metre * metre);
const Pressure bar = 100.0 * kilo * Pascal;
const Pressure MPa = Mega * Pascal;
const Pressure kPa = kilo * Pascal;
const Energy Joule = Newton * metre;
const Energy kJ = kilo * Joule;
const Energy Btu = 1055.05585262 * Joule;

const Power Watt = Joule / second;

const HeatFlux W_m2 = Watt / metre2;

const MyDouble Percent = 1.0 / 100;

//------------------------------------
// THERMODYNAMIC MEASURES

const SpecificEnergy kJ_kg = kilo * Joule / kilogram;
const SpecificEnergy J_kg = Joule / kilogram;

const SpecificEntropy kJ_kgK = kilo * Joule / kilogram / Kelvin;
const SpecificEntropy J_kgK = Joule / kilogram / Kelvin;

const HeatTransferCoefficient W_m2K = Watt / metre2 / Kelvin;
const ThermalConductivity W_mK = Watt / metre / Kelvin;
const ThermalConductivity mW_mK = milli * W_mK;
const Density kg_m3 = kilogram / metre3;
const SpecificVolume m3_kg = metre3 / kilogram;

const MassFlowRate kg_s = kilogram / second;
const VolFlowRate m3_s = metre3 / second;

const HeatCapacityPerLength J_mK = Joule / metre / Kelvin;

//------------------------------------
// ELECTRICAL STUFF

const ElecPotential volt = Watt / ampere;
const Charge Coulomb = ampere * second;
const Capacitance Farad = volt / Coulomb;
const Resistance Ohm = volt / ampere;

//------------------------------------
// SOME IMPERIAL MEASURES

const Temperature Rankin = 0.556 * Kelvin;
const Frequency RPM = 1. / minute;

const Length yard =  0.9144 * metre;
const Length foot = yard / 3.;
const Length inch = foot / 12.;
const Length mile = 1760. * yard;

const Mass lbm = 0.45359237 * kilogram;
const Acceleration grav_accel = 9.80665 * metre / second / second;
const Force lbf = grav_accel * lbm;
const Pressure lbf_in2 = lbf / inch / inch;

//------------------------------------
// HANDLING TEMPERATURES

const Temperature ZeroCelsius = 273.15 * Kelvin;
const Temperature ZeroFahrenheit = ZeroCelsius - 32.0 * Rankin;

/**
	Convert a temperature (in Kelvin) to Celsius.
	@return the temperature, as a plain 'MyDouble' type
*/
inline MyDouble
tocelsius(const Temperature& T){
	MyDouble d = *reinterpret_cast<const MyDouble*>(&T);
	return d - 273.15;
}

/**
	Convert a Celsius temperature to Kelvin
	@param T_C MyDouble value for the temperature in degrees
	@return Temperature object (Kelvin)
*/
inline Temperature
fromcelsius(const MyDouble &T_C){
	return (T_C * Kelvin) + ZeroCelsius;
}

/**
	Convert from Fahrenheit temperature to Temperature object (Kelvin)
*/
inline MyDouble
tofahrenheit(const Temperature &T){
	return (T - ZeroFahrenheit) / Rankin;
}

/// Convert Temperature object to Fahrenheit
/**
	@return temperature in Fahrenheit (as type 'MyDouble')
*/
inline Temperature
fromfahrenheit(const MyDouble &T_F){
	return (T_F * Rankin) + ZeroFahrenheit;
}

// USEFUL CONSTANTS

/// Stefan-Boltzmann Constant (radiation)
const MyDouble SIGMA_C = (5.670e-8) * W_m2 /sq(sq(Kelvin));

/* STEAM-SPECIFIC CONSTANTS */


const SpecificGasConstant R=0.461526 * kJ_kgK; // Specific gas constant for water from IF97

#define REG4_TOL 0.001		// relative err on pressures considerd to be equal to psat.

const Temperature TB_HIGH = 863.15 * Kelvin;
const Temperature T_MIN = ZeroCelsius;
const Temperature T_MAX = 1073.15 * Kelvin;
const Temperature T_CRIT = 647.096 * Kelvin;	// critical-point temperature
const Temperature T_TRIPLE = 273.16 * Kelvin;	// triple-point temperature
const Temperature REG2_TEMP_REF = 540.0 * Kelvin;
const Temperature REG1_TEMP_REF = 1386.0 * Kelvin;
const Temperature REG1_T_LOW = ZeroCelsius;
const Temperature REG2_T_LOW = ZeroCelsius;
const Temperature REG2_T_HIGH = T_MAX;

const Temperature T_REG1_REG3 = 623.15 * Kelvin;
const Temperature TB_LOW = T_REG1_REG3;

const Temperature T_MIN_VOL = fromcelsius(3.984);

const Pressure P_MAX = 100.0 * MPa;
const Pressure PB_LOW = 16.5292 * MPa;
const Pressure P_MIN = 0.0 * Pascal;
const Pressure P_CRIT = 22.064 * MPa;	// critical-point pressure
const Pressure P_TRIPLE = 611.657 * Pascal;	// triple-point pressure
const Pressure REG4_P_MIN = 611.213 * Pascal;	// minimum pressure for region 4 (IF-97 eq 31 & p 35) / [MPa]
const Pressure REG2_P_HIGH = P_MAX;
const Pressure REG1_P_HIGH = P_MAX;
const Pressure REG1_PRES_REF = 16.53 * MPa;
const Pressure REG2_PRES_REF = 1.0 * MPa;

const Density RHO_CRIT = 322.0 * kg / metre3;	// critical-point density / [kg/m³]

/// @see http://www.iapws.org/relguide/visc.pdf#page=7 Eq (4)
const DynamicViscosity IAPS85_VISC_REF = 55.071 * micro * Pascal * second;
/// @see http://www.iapws.org/relguide/visc.pdf#page=7 Eq (2)
const Density IAPS85_DENS_REF = 317.763 * kg_m3;
/// @see http://www.iapws.org/relguide/visc.pdf#page=7 Eq (1)
const Temperature IAPS85_TEMP_REF = 647.226 * Kelvin;
/// @see http://www.iapws.org/relguide/visc.pdf#page=7 Eq (4)
const Pressure IAPS85_PRES_REF = 22.115 * MPa;	// MPa (THIS IS *NOT* EQUAL TO P_CRIT!)

const Temperature IAPS85_TEMP_REG2_REF = 540.0 * Kelvin;

const Pressure STEAM_P_EPS = 1.0e-5 * MPa;
const Temperature STEAM_T_EPS = 5.0e-4 * Kelvin;

const Temperature EPS_T_CRIT=0.00007 * Kelvin;

const Temperature T_CRIT_PLUS=(T_CRIT + STEAM_T_EPS);

const Density REG3_ZEROIN_DENS_MAX = 765.0 * kg_m3;
const Density REG3_ZEROIN_TOL= 1e-18 * kg_m3;

#define MPA_TO_BAR(PRES) (((Num)(PRES)) * 10.0      )
#define BAR_TO_MPA(PRES) (((Num)(PRES)) * 0.1       )
#define PA_TO_MPA(PRES)  (((Num)(PRES)) * 0.000001  )
#define MPA_TO_PA(PRES)  (((Num)(PRES)) * 1.0E6     )
#define KJKG_TO_JKG(JKG) (((Num)(KJKG)) * 1000.0    )
#define BAR_TO_PA(PRES)  (((Num)(PRES)) * 100.0E3   )
#define KPA_TO_MPA(PRES) (((Num)(PRES)) * 0.001     )

#define W_TO_KW(W) (((Num)(W))*0.001)
#define KJ_TO_J(KJ) (((Num)(KJ))*0.001)
#define J_TO_KJ(J) (((Num)(J))*0.001)

const Acceleration GRAV = 9.81 * Newton / kg;	// N/kg, gravitation acceleration

#ifndef PI
# define PI 3.14159265358
#endif

typedef enum{SOLVE_IENERGY, SOLVE_ENTHALPY, SOLVE_ENTROPY, SOLVE_CP, SOLVE_CV, SOLVE_TEMPERATURE, SOLVE_PRESSURE} SolveParam;

typedef SteamState SteamSolveFunction(MyDouble, MyDouble);
typedef int SteamRegionFunction(MyDouble, MyDouble);
typedef int SteamBoundsFunction(MyDouble, MyDouble, int);

class SteamCalculator{
	private:
		SteamState S;

	public:
		SteamCalculator(){
			S.region = 1;
			S.SteamState_U.R1.T = 300;
			S.SteamState_U.R1.p = 1e5;
		}

		SteamCalculator(const SteamState &S1){
			S = S1;
		}

		/// Copy constructor
		SteamCalculator(const SteamCalculator & original){
			S = original.S;
		}
	
		/// Assignment operator (assigns a copy)
		SteamCalculator const &operator=(SteamCalculator const &original){
			S = original.S;
		}

		// Destructor
		~SteamCalculator(){}

		// Defining state, simple methods

		inline void set_pT(const Pressure &p, const Temperature &T){
			S = freesteam_set_pT(p,T);
		}

		inline void setSatWater_p(const Pressure &p){
			S = freesteam_set_Tx(freesteam_region4_Tsat_p(p), 0.0);
		}

		inline void setSatSteam_p(const Pressure &p){
			S = freesteam_set_Tx(freesteam_region4_Tsat_p(p), 1.0);
		}

		inline void setSatWater_T(const Temperature &T){
			S = freesteam_set_Tx(T, 0.0);
		}

		inline void setSatSteam_T(const Temperature &T){
			S = freesteam_set_Tx(T, 1.0);
		}

		inline void setRegion1_pT(const Pressure &p, const Temperature &T){
			S.region = 1;
			S.SteamState_U.R1.p = p;
			S.SteamState_U.R1.T = T;
		}

		inline void setRegion2_pT(const Pressure &p, const Temperature &T){
			S.region = 2;
			S.SteamState_U.R2.p = p;
			S.SteamState_U.R2.T = T;
		}

		inline void setRegion4_Tx(const Temperature &T, const Num &x){
			S.region = 4;
			S.SteamState_U.R4.T = T;
			S.SteamState_U.R4.x = x;
		}

		inline void setRegion3_rhoT(const Density &rho, const Temperature &T){
			S.region = 3;
			S.SteamState_U.R3.T = T;
			S.SteamState_U.R3.rho = rho;
		}

		// Methods to return properties and state

		inline int whichRegion(void) const{
			return S.region;
		}

		inline MyDouble temp() const{return freesteam_T(S);}
		inline MyDouble pres() const{return freesteam_p(S);}
		inline MyDouble dens() const{return 1./freesteam_v(S);}
		inline MyDouble specvol() const{return freesteam_v(S);}
		inline MyDouble specienergy() const{return freesteam_u(S);}
		inline MyDouble specentropy() const{return freesteam_s(S);}
		inline MyDouble specenthalpy() const{return freesteam_h(S);}
		inline MyDouble speccp() const{return freesteam_cp(S);}
		inline MyDouble speccv() const{return freesteam_cv(S);}
		inline MyDouble quality() const{return freesteam_x(S);}
		inline MyDouble dynvisc() const{return freesteam_mu(S);}
		inline MyDouble conductivity() const{return freesteam_k(S);}
};

template<SolveParam FirstProp, SolveParam SecondProp>
class Solver2{

	private:
		SteamSolveFunction *solvefunc;
		SteamRegionFunction *regionfunc;
		SteamBoundsFunction *boundfunc;

	public:
		Solver2();
		~Solver2(){}

		inline int whichRegion(const MyDouble &fp, const MyDouble &sp){return (*regionfunc)(fp,sp);}
		inline SteamCalculator solve(const MyDouble &fp, const MyDouble &sp){return SteamCalculator((*solvefunc)(fp,sp));}

		/* ignore any provided guesses, we can't use those currently in freesteam 2.0 */
		inline SteamState solve(const MyDouble &fp, const MyDouble &sp, const SteamCalculator firstguess){return (*solvefunc)(fp,sp);}
};

template<>
Solver2<SOLVE_PRESSURE, SOLVE_TEMPERATURE>::Solver2()
	: solvefunc(&freesteam_set_ph), regionfunc(&freesteam_region_ph), boundfunc(&freesteam_bounds_ph)
	{}

template<>
Solver2<SOLVE_TEMPERATURE, SOLVE_ENTROPY>::Solver2()
	: solvefunc(&freesteam_set_Ts), regionfunc(&freesteam_region_Ts), boundfunc(&freesteam_bounds_Ts)
	{}

#endif

