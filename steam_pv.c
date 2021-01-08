/*
freesteam - IAPWS-IF97 steam tables library
Copyright (C) 2004-2009  John Pye

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

#define FREESTEAM_BUILDING_LIB
#include "steam_pv.h"

#include "region1.h"
#include "region2.h"
#include "region3.h"
#include "region4.h"
#include "b23.h"
#include "backwards.h"
#include "solver2.h"
#include "zeroin.h"

#include "common.h"

#include <stdio.h>
#include <stdlib.h>

int freesteam_bounds_pv(MyDouble p, MyDouble v, int verbose){
#ifndef HAVE_CADNA_H
#define BOUND_WARN(MSG) \
	if(verbose){\
		fprintf(stderr,"%s (%s:%d): WARNING " MSG " (p = %g MPa, v = %g m3/kg)\n"\
		,__func__,__FILE__,__LINE__,p/1e6,v);\
	}
#else
#define BOUND_WARN(MSG) \
	if(verbose){\
		fprintf(stderr,"%s (%s:%d): WARNING " MSG " (p = %s MPa, v = %s m3/kg)\n"\
		,__func__,__FILE__,__LINE__,strp(p/1e6),strp(v));\
	}
#endif

	if(p <= 0){
		BOUND_WARN("p <= 0");
		return 1;
	}
	if(p > IAPWS97_PMAX){
		BOUND_WARN("p > PMAX");
		return 2;
	}

	MyDouble vmin = freesteam_region1_v_pT(p,IAPWS97_TMIN);
	if(v < vmin){
		BOUND_WARN("v < v_region1(p,T_min)");
		return 3;
	}

	MyDouble vmax = freesteam_region2_v_pT(p,REGION2_TMAX);
	if(v>vmax){
		BOUND_WARN("v > v_region2(p,T_max)");
		return 4;
	}

	return 0;
#undef BOUND_WARN
}

int freesteam_region_pv(MyDouble p, MyDouble v){

	MyDouble p13 = freesteam_region4_psat_T(REGION1_TMAX);

	if(p > p13){
		MyDouble v13 = freesteam_region1_v_pT(p, REGION1_TMAX);
		if(v < v13) return 1;

		/* region 2-3 */
		MyDouble T23 = freesteam_b23_T_p(p);
		MyDouble v23 = freesteam_region2_v_pT(p,T23);
		if(v > v23) return 2;

		/* region 3? or high-pressure part of region 4? */
		if(p >= IAPWS97_PCRIT) return 3;

		MyDouble Tsat = freesteam_region4_Tsat_p(p);
		MyDouble vf = 1./ freesteam_region4_rhof_T(Tsat);
		if(v < vf) return 3;
		MyDouble vg = 1./ freesteam_region4_rhog_T(Tsat);
		if(v > vg) return 3;

		return 4;
	}else{
		MyDouble Tsat = freesteam_region4_Tsat_p(p);
		MyDouble vf = freesteam_region1_v_pT(p,Tsat);
		if(v < vf) return 1;

		MyDouble vg = freesteam_region2_v_pT(p,Tsat);
		if(v > vg) return 2;

		return 4;
	}
}


typedef struct SolvePVData_struct{
	MyDouble p, v;
} SolvePVData;

#define D ((SolvePVData *)user_data)
static ZeroInSubjectFunction pv_region1_fn;
MyDouble pv_region1_fn(MyDouble T, void *user_data){
	return D->v - freesteam_region1_v_pT(D->p, T);
}

static ZeroInSubjectFunction pv_region2_fn;
MyDouble pv_region2_fn(MyDouble T, void *user_data){
	return D->v - freesteam_region2_v_pT(D->p, T);
}
#undef D

typedef struct SolvePRhoData_struct{
	MyDouble p, rho;
} SolvePRhoData;

#define D ((SolvePRhoData *)user_data)
static ZeroInSubjectFunction pv_region3_fn;
MyDouble pv_region3_fn(MyDouble T, void *user_data){
	return D->p - freesteam_region3_p_rhoT(D->rho, T);
}
#undef D


SteamState freesteam_set_pv(MyDouble p, MyDouble v){
	SteamState S;
	S.region = (char)freesteam_region_pv(p,v);
#if 0
	int status;
#endif
	switch(S.region){
		case 1:
			/* iterate T to get correct value of v */
			S.SteamState_U.R1.p = p;
			S.SteamState_U.R1.T = freesteam_region4_Tsat_p(p);
			{
				MyDouble lb = IAPWS97_TMIN;
				MyDouble ub = REGION1_TMAX;
				MyDouble tol = 1e-9; /* ??? */
				MyDouble sol, err;
				SolvePVData D = {p, v};
				zeroin_solve(&pv_region1_fn, &D, lb, ub, tol, &sol, &err);
				S.SteamState_U.R1.T = sol;
				/* FIXME check convergence! */
			}
#if 0
			S = freesteam_solver2_region1('p','v', p, v, S, &status);
			if(status){
				fprintf(stderr,"%s: WARNING: Failed to converge in region 1\n",__func__);
			}
#endif
			break;
		case 2:
			/* iterate T to get correct value of v */
			S.SteamState_U.R2.p = p;
			S.SteamState_U.R2.T = freesteam_region4_Tsat_p(p);
			{
				MyDouble lb = IAPWS97_TMIN;
				MyDouble ub = IAPWS97_TMAX;
				MyDouble tol = 1e-9; /* ??? */
				MyDouble sol, err;
				SolvePVData D = {p, v};
				zeroin_solve(&pv_region2_fn, &D, lb, ub, tol, &sol, &err);
				S.SteamState_U.R2.T = sol;
				/* FIXME check convergence! */
			}

#if 0
			S.SteamState_U.R2.p = p;
			S.SteamState_U.R2.T = freesteam_region4_Tsat_p(p);
			S = freesteam_solver2_region2('p','v', p, v, S, &status);
			if(status){
				fprintf(stderr,"%s: WARNING: Failed to converge in region 2\n",__func__);
			}
#endif
			break;
		case 3:
			S.SteamState_U.R3.rho = 1./ v;
			S.SteamState_U.R3.T = REGION1_TMAX;
			{
				MyDouble lb = REGION1_TMAX;
				MyDouble ub = IAPWS97_TMAX;
				MyDouble tol = 1e-12; /* ??? */
				MyDouble sol, err;
				SolvePRhoData D = {p, S.SteamState_U.R3.rho};
				zeroin_solve(&pv_region3_fn, &D, lb, ub, tol, &sol, &err);
				S.SteamState_U.R3.T = sol;
				//fprintf(stderr,"%s: (p = %f MPa,v = %f m3/kg) region 3, error in p = %f\n",__func__,p,v, err);
				/* FIXME check convergence! */
			}
#if 0
			S = freesteam_solver2_region3('p','v', p, v, S, &status);
			if(status){
				fprintf(stderr,"%s: WARNING: Failed to converge in region 3\n",__func__);
			}
#endif
			break;
		case 4:
			S.SteamState_U.R4.T = freesteam_region4_Tsat_p(p);
			//fprintf(stderr,"%s: region 4, Tsat = %g\n",__func__,S.SteamState_U.R4.T);
			MyDouble vf, vg;
			if(S.SteamState_U.R4.T <= REGION1_TMAX){
				vf = freesteam_region1_v_pT(p,S.SteamState_U.R4.T);
				vg = freesteam_region2_v_pT(p,S.SteamState_U.R4.T);
			}else{
				/* TODO iteratively improve estimate of T */
				vf = 1./ freesteam_region4_rhof_T(S.SteamState_U.R4.T);
				vg = 1./ freesteam_region4_rhog_T(S.SteamState_U.R4.T);
			}
			S.SteamState_U.R4.x = (v - vf)/(vg - vf);
	}
	return S;
}

