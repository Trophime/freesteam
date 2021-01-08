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
#include "steam_Ts.h"

#include "region1.h"
#include "region2.h"
#include "region3.h"
#include "region4.h"
#include "zeroin.h"
#include "b23.h"
#include "solver2.h"
#include "backwards.h"
#include "bounds.h"

#include <stdlib.h>
#include <assert.h>
#include <math.h>

int freesteam_bounds_Ts(MyDouble T, MyDouble s, int verbose){
#ifndef HAVE_CADNA_H
#define BOUND_WARN(MSG) \
	if(verbose){\
		fprintf(stderr,"%s (%s:%d): WARNING " MSG " (T = %g, s = %g kJ/kgK)\n"\
		,__func__,__FILE__,__LINE__,T,s/1e3);\
	}
#else
#define BOUND_WARN(MSG) \
	if(verbose){\
		fprintf(stderr,"%s (%s:%d): WARNING " MSG " (T = %s, s = %s kJ/kgK)\n"\
		,__func__,__FILE__,__LINE__,strp(T),strp(s/1e3));\
	}
#endif

	if(T < IAPWS97_TMIN){
		BOUND_WARN("T < TMIN");
		return 1;
	}
	if(T > IAPWS97_TMAX + 1e-5){
		BOUND_WARN("T > TMAX");
		return 2;
	}

	MyDouble smax = freesteam_region2_s_pT(0.,T);
	if(s > smax){
		BOUND_WARN("s > smax");
		return 3;
	}

	if(T <= REGION1_TMAX){
		MyDouble smin = freesteam_region1_s_pT(IAPWS97_PMAX,T);
		if(s < smin){
			BOUND_WARN("s < smin (region 1)");
			return 4;
		}
	}else if(T > freesteam_b23_T_p(IAPWS97_PMAX)){
		MyDouble smin = freesteam_region2_s_pT(IAPWS97_PMAX,T);
		if(s < smin){
			BOUND_WARN("s < smin (region 2)");
			return 4;
		}
	}else{
		/* region 3, need to iterate */
		SteamState S = freesteam_bound_pmax_T(T);
		//assert(S.region==3);
		MyDouble smin = freesteam_s(S);
		if(s < smin){
			BOUND_WARN("s < smin (region 3)");
			return 4;
		}
	}
	return 0;
#undef BOUND_WARN
}

int freesteam_region_Ts(MyDouble T, MyDouble s){

	if(T <= REGION1_TMAX){
		MyDouble p = freesteam_region4_psat_T(T);
		MyDouble sf = freesteam_region1_s_pT(p,T);
		MyDouble sg = freesteam_region2_s_pT(p,T);
		if(s <= sf){
			return 1;
		}
		if(s >= sg){
			return 2;
		}
		return 4;
	}

	/* an optimisation, using known range of s values on b23 IAPWS97 sect 4, p 5 */
	//if(s > 5.261e3)return 2;

	//if(s < 3.6e3)return 3;

	MyDouble p23 = freesteam_b23_p_T(T);
	MyDouble s23 = freesteam_region2_s_pT(p23,T);
	if(s >= s23){
		return 2;
	}
	
	/* that leaves region 4 (near the C.P.) or region 3 */

	/* FIXME need this hack to make low-s part of region behave correctly */
	if(s < 3.7e3)return 3;

	/* FIXME iterate to improve location of saturation curve? */
	MyDouble psat = freesteam_region3_psat_s(s);
	MyDouble Tsat = freesteam_region4_Tsat_p(psat);
	if(T > Tsat)return 3;
	
	return 4;
}

typedef struct{
	MyDouble T, s, psat;
} SolveTSData;

#define D ((SolveTSData *)user_data)
static ZeroInSubjectFunction Ts_region1_fn, Ts_region2_fn, Ts_region4_fn1, Ts_region4_fn2;
MyDouble Ts_region1_fn(MyDouble p, void *user_data){
	return D->s - freesteam_region1_s_pT(p, D->T);
}
MyDouble Ts_region2_fn(MyDouble p, void *user_data){
	return D->s - freesteam_region2_s_pT(p, D->T);
}
MyDouble Ts_region3_fn(MyDouble rho, void *user_data){
	return D->s - freesteam_region3_s_rhoT(rho, D->T);
}

MyDouble Ts_region4_fn1(MyDouble x, void *user_data){
	/* for region 4 where T < REGION1_TMAX */
	MyDouble sf = freesteam_region1_s_pT(D->psat,D->T);
	MyDouble sg = freesteam_region2_s_pT(D->psat,D->T);
	return D->s - (sf + x*(sg-sf));
}

MyDouble Ts_region4_fn2(MyDouble x, void *user_data){
	/* for region 4 where T > REGION1_TMAX */
	MyDouble rhof = freesteam_region4_rhof_T(D->T);
	MyDouble rhog = freesteam_region4_rhog_T(D->T);
	MyDouble sf = freesteam_region3_s_rhoT(rhof,D->T);
	MyDouble sg = freesteam_region3_s_rhoT(rhog,D->T);
	/* TODO: iteratively improve guess with forward fns*/
	return D->s - (sf + x*(sg-sf));
}
#undef D

SteamState freesteam_set_Ts(MyDouble T, MyDouble s){
	MyDouble lb, ub, tol, sol = 0, err;
	SolveTSData D = {T, s, 0};

	int region = freesteam_region_Ts(T,s);
	//fprintf(stderr,"%s: region = %d\n",__func__,region);
	switch(region){
		case 1:
			lb = IAPWS97_PTRIPLE;
			ub = IAPWS97_PMAX;
			tol = 1e-9; /* ??? */
			zeroin_solve(&Ts_region1_fn, &D, lb, ub, tol, &sol, &err);
			assert(fabs(err/sol)<tol);
			return freesteam_region1_set_pT(sol,T);
		case 2:
			lb = 0.;
			ub = IAPWS97_PMAX;
			if(T > REGION1_TMAX && T < freesteam_b23_T_p(IAPWS97_PMAX)){
				ub = freesteam_b23_p_T(T);
			}		
			tol = 1e-9; /* ??? */
			zeroin_solve(&Ts_region2_fn, &D, lb, ub, tol, &sol, &err);
			//if(T > 600.)assert(fabs(err/sol)<tol);
			return freesteam_region2_set_pT(sol,T);
		case 3:
			lb = 0;
			ub = 1000;
			tol = 1e-9; /* ??? */
			zeroin_solve(&Ts_region3_fn, &D, lb, ub, tol, &sol, &err);
			assert(fabs(err/sol)<tol);
			return freesteam_region3_set_rhoT(sol,T);
		case 4:
			lb = 0.;
			ub = 1.;
			tol = 1e-12; /* ??? */
			D.psat = freesteam_region4_psat_T(T);
			zeroin_solve(
				(T < REGION1_TMAX ? &Ts_region4_fn1 : &Ts_region4_fn2)
				, &D, lb, ub, tol, &sol, &err
			);
			assert(fabs(err)<tol);
			return freesteam_region4_set_Tx(T,sol);
		default:
			/* ??? */
			fprintf(stderr,"%s (%s:%d): Region '%d' not implemented\n",__func__,__FILE__,__LINE__,region);
			exit(1);
	}
}


