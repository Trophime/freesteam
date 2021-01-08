#ifndef __FSTEAM_H__
#define __FSTEAM_H__

extern double density(double TK, double pPa);
extern double enthalpy(double TK, double pPa);
extern double entropy(double TK, double pPa);
extern double internal_energy(double TK, double pPa);
extern double specific_volume(double TK, double pPa);
extern double isobaric_heat_capacity(double TK, double pPa);
extern double isochoric_heat_capacity(double TK, double pPa);
extern double speed_of_sound(double TK, double pPa);
extern double saturated_quality(double TK, double pPa);
extern double dynamic_viscosity(double TK, double pPa);
extern double thermal_conductivity(double TK, double pPa); 
extern double saturated_boiling_temp(double pPa);
extern double enthalpy_of_vaporization(double TK);

#endif  /* ndef __FSTEAM_H__ */
