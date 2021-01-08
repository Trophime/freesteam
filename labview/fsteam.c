#include "fsteam.h"
#include "freesteam/steam.h"
#include "freesteam/steam_pT.h"
#include "freesteam/region4.h"

double density(double TK, double pPa) {

	SteamState S;
	double rho;
	
	S = freesteam_set_pT(pPa, TK);
	rho = freesteam_rho(S);
			
	return rho; // kg/m^3
	
}

double enthalpy(double TK, double pPa) {

	SteamState S;
	double h;
	
	S = freesteam_set_pT(pPa, TK);
	h = freesteam_h(S);
			
	return h; // J/kg
	
}

double entropy(double TK, double pPa) {

	SteamState S;
	double s;
	
	S = freesteam_set_pT(pPa, TK);
	s = freesteam_s(S);
			
	return s; // J/(kg*K)
	
}

double internal_energy(double TK, double pPa) {

	SteamState S;
	double u;
	
	S = freesteam_set_pT(pPa, TK);
	u = freesteam_u(S);
			
	return u; // J/kg
	
}

double specific_volume(double TK, double pPa) {

	SteamState S;
	double v;

	S = freesteam_set_pT(pPa, TK);
	v = freesteam_v(S);

	return v; // m^3/kg

}

double isobaric_heat_capacity(double TK, double pPa) {

	SteamState S;
	double cp;

	S = freesteam_set_pT(pPa, TK);
	cp = freesteam_cp(S);

	return cp; // J/(kg*K)

}

double isochoric_heat_capacity(double TK, double pPa) {

	SteamState S;
	double cv;

	S = freesteam_set_pT(pPa, TK);
	cv = freesteam_cv(S);

	return cv; // J/(kg*K)

}

double speed_of_sound(double TK, double pPa) {

	SteamState S;
	double w;

	S = freesteam_set_pT(pPa, TK);
	w = freesteam_w(S);

	return w; // m/s

}

double saturated_quality(double TK, double pPa) {

	SteamState S;
	double x;

	S = freesteam_set_pT(pPa, TK);
	x = freesteam_x(S);

	return x; // dimensionless; 0 <= x <= 1

}

double dynamic_viscosity(double TK, double pPa) {

	SteamState S;
	double mu;

	S = freesteam_set_pT(pPa, TK);
	mu = freesteam_mu(S);

	return mu; // Pa*s

}

double thermal_conductivity(double TK, double pPa) {

	SteamState S;
	double k;

	S = freesteam_set_pT(pPa, TK);
	k = freesteam_k(S);

	return k; // W/(m*K)

}

double saturated_boiling_temp(double pPa) {

	double Tb;

	Tb = freesteam_region4_Tsat_p(pPa);
	
	return Tb; // K

}

double enthalpy_of_vaporization(double TK) {

	double Dhv, hg, hf;
	double liquid = 0;
	double vapor = 1;

	hf = freesteam_region4_h_Tx(TK, liquid);
	hg = freesteam_region4_h_Tx(TK, vapor);

	Dhv = hg - hf;

	return Dhv; // J/kg

}
