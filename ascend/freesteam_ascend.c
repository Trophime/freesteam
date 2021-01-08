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
#include "../steam_ph.h"
#include "../steam_pT.h"
#include "../derivs.h"
#include "../region4.h"
#include "../viscosity.h"

#include <ascend/general/platform.h>
#include <ascend/utilities/error.h>
#include <ascend/compiler/extfunc.h>

/* #define BBOX_DEBUG */

/**
	ASCEND external evaluation function
	Outputs: T
	Inputs: p, h
	@return 0 on success
*/
int Tvsx_ph_calc(struct BBoxInterp *bbox,
		int ninputs, int noutputs,
		double *inputs, double *outputs,
		double *jacobian
){
	(void)bbox; (void)jacobian; // not used
	(void)ninputs; (void)noutputs; // not used currently

#if 0
	ASC_ASSERT(ninputs==2);
	ASSERT(noutputs==2);
#endif

	// convert inputs to freesteam dimensionful values
	double p = inputs[0]; /* ASCEND uses SI units, so no conversion needed */
	double h = inputs[1]; /* ASCEND uses SI units, so no conversion needed */

#ifdef BBOX_DEBUG
	ERROR_REPORTER_HERE(ASC_USER_NOTE,
		"Evaluating with p = %f bar, h = %f kJ/kg"
		,p,h
	);
#endif

	SteamState S;
	S = freesteam_set_ph(p,h);
	double T, dTdh_p, dTdp_h;
	double v, dvdh_p, dvdp_h;
	double s, dsdh_p, dsdp_h;

	double x, dxdh_p, dxdp_h;
	switch(bbox->task){
	case bb_func_eval:
		T = freesteam_T(S);
		v = freesteam_v(S);
		s = freesteam_s(S);
		if(S.region==3){
			/* nonsense value */
			x = 0.5;
		}else{
			x = freesteam_x(S);
		}

#ifdef BBOX_DEBUG
		ERROR_REPORTER_HERE(ASC_USER_NOTE,
			"Got result T = %f K"
			,T
		);
#endif
		outputs[0] = T;
		outputs[1] = v;
		outputs[2] = s;
		outputs[3] = x;

		/* TODO add error checks here, surely? */
		return 0;
	case bb_deriv_eval:
		/*fprintf(stderr,"derivative evaluation, region %d\n",S.region);*/
		dTdp_h = freesteam_deriv(S,"Tph");
		dTdh_p = freesteam_deriv(S,"Thp");
		dvdp_h = freesteam_deriv(S,"vph");
		dvdh_p = freesteam_deriv(S,"vhp");
		dsdp_h = freesteam_deriv(S,"sph");
		dsdh_p = freesteam_deriv(S,"shp");
		switch(S.region){
			case 4:
				dxdp_h = freesteam_deriv(S,"xph");
				dxdh_p = freesteam_deriv(S,"xhp");
				break;
			default:
				/* try to 'slope' the solver into the saturation region */
				dxdp_h = 0;
				dxdh_p = 0.001;
				break;
		}
#ifdef BBOX_DEBUG
		ERROR_REPORTER_HERE(ASC_USER_NOTE,
			"Got result (dT/dp)h = %g, (dT/dh)p = %g K/Pa",dTdp_h,dTdh_p
		);
		ERROR_REPORTER_HERE(ASC_USER_NOTE,
			"Got result (dv/dp)h = %g, (dv/dh)p = %g K/Pa",dvdp_h,dvdh_p
		);
#endif
		jacobian[0] = dTdp_h;
		jacobian[1] = dTdh_p;
		jacobian[2] = dvdp_h;
		jacobian[3] = dvdh_p;
		jacobian[4] = dsdp_h;
		jacobian[5] = dsdh_p;
		jacobian[6] = dxdp_h;
		jacobian[7] = dxdh_p;
		return 0;
	default:
		ERROR_REPORTER_HERE(ASC_PROG_ERR,"Invalid call, unknown bbox->task");
		return 1;
	}
}


/**
	ASCEND external evaluation function
	Outputs: mu, k, rho, cp
	Inputs: p, T
	@return 0 on success
*/
int mukrhocp_pT_calc(struct BBoxInterp *bbox,
		int ninputs, int noutputs,
		double *inputs, double *outputs,
		double *jacobian
){
	(void)bbox; (void)jacobian; // not used
	(void)ninputs; (void)noutputs; // not used currently

	// convert inputs to freesteam dimensionful values
	double p = inputs[0]; /* ASCEND uses SI units, so no conversion needed */
	double T = inputs[1]; /* ASCEND uses SI units, so no conversion needed */

#ifdef BBOX_DEBUG
	ERROR_REPORTER_HERE(ASC_USER_NOTE,
		"Evaluating with p = %f bar, T = %f K = %f C"
		,p,T,T-273.15
	);
#endif

	SteamState S;
	S = freesteam_set_pT(p,T);
	double mu = freesteam_mu(S);
	double k = freesteam_k(S);
	double rho = freesteam_rho(S);
	double cp = freesteam_cp(S);

#ifdef BBOX_DEBUG
	ERROR_REPORTER_HERE(ASC_USER_NOTE,
		"Got mu = %f, k = %f, rho = %f, cp = %f"
		, mu, k, rho, cp
	);
#endif

	outputs[0] = mu;
	outputs[1] = k;
	outputs[2] = rho;
	outputs[3] = cp;

	return 0;
}

int mu_Tv_calc(struct BBoxInterp *bbox, int ninputs, int noutputs,
	double *inputs, double *outputs, double *jacobian
){
	(void)bbox; (void)jacobian; // not used
	(void)ninputs; (void)noutputs; // not used currently

	double T = inputs[0];
	double rho = 1./inputs[1];

	/* TODO make checks of two-phase region, act accordingly */
	double mu = freesteam_mu_rhoT(rho,T);

	outputs[0] = mu;
	return 0;
}

int k_Tv_calc(struct BBoxInterp *bbox, int ninputs, int noutputs,
	double *inputs, double *outputs, double *jacobian
){
	(void)bbox; (void)jacobian; (void)ninputs; (void)noutputs; // not used currently

	double T = inputs[0];
	double rho = 1./inputs[1];

	/* TODO make checks of two-phase region, act accordingly */
	double k = freesteam_k_rhoT(rho,T);

	outputs[0] = k;
	return 0;
}

/*============== a few quick single-input, single output routines ============*/

#define FREESTEAM_SISO_FUNCS(D,X)\
	D(Tsat_p\
		, double T = freesteam_region4_Tsat_p(inputs[0])\
		, T\
		, 1./freesteam_region4_dpsatdT_T(T)\
		, "[T] = freesteam_Tsat_p(p)"\
	) X\
	D(psat_T\
		, double T = inputs[0]\
		, freesteam_region4_psat_T(T)\
		, freesteam_region4_dpsatdT_T(T)\
		, "[p] = freesteam_psat_T(T)"\
	) X\
	D(hf_p\
		, double T = freesteam_region4_Tsat_p(inputs[0])\
		, freesteam_h(freesteam_region4_set_Tx(T, 0.))\
		, freesteam_region4_dAdTx('h',freesteam_region4_set_Tx(T, 0.))/freesteam_region4_dpsatdT_T(T)\
		, "[hf] = freesteam_hf_p(p)"\
	) X \
	D(hg_p\
		, double T = freesteam_region4_Tsat_p(inputs[0])\
		, freesteam_h(freesteam_region4_set_Tx(T, 1.))\
		, freesteam_region4_dAdTx('h',freesteam_region4_set_Tx(T, 1.))/freesteam_region4_dpsatdT_T(T)\
		, "[hg] = freesteam_hg_p(p)"\
	) X \
	D(sf_p\
		, double T = freesteam_region4_Tsat_p(inputs[0])\
		, freesteam_s(freesteam_region4_set_Tx(T, 0.))\
		, freesteam_region4_dAdTx('s',freesteam_region4_set_Tx(T, 0.))/freesteam_region4_dpsatdT_T(T)\
		, "[sf] = freesteam_sf_p(p)"\
	) X \
	D(sg_p\
		, double T = freesteam_region4_Tsat_p(inputs[0])\
		, freesteam_s(freesteam_region4_set_Tx(T, 1.))\
		, freesteam_region4_dAdTx('s',freesteam_region4_set_Tx(T, 1.))/freesteam_region4_dpsatdT_T(T)\
		, "[sg] = freesteam_sg_p(p)"\
	) X \
	D(sf_T\
		, double T = inputs[0];CONSOLE_DEBUG("sf(%f) --> %f",T, freesteam_s(freesteam_region4_set_Tx(T, 0.)))\
		, freesteam_s(freesteam_region4_set_Tx(T, 0.))\
		, freesteam_region4_dAdTx('s',freesteam_region4_set_Tx(T, 0.))\
		, "[sf] = freesteam_sf_T(T)"\
	) X \
	D(sg_T\
		, double T = inputs[0]\
		, freesteam_s(freesteam_region4_set_Tx(T, 1.))\
		, freesteam_region4_dAdTx('s',freesteam_region4_set_Tx(T, 1.))\
		, "[sg] = freesteam_sg_T(T)"\
	) X \
	D(hf_T\
		, double T = inputs[0];CONSOLE_DEBUG("hf(%f) --> %f",T, freesteam_h(freesteam_region4_set_Tx(T, 0.)))\
		, freesteam_h(freesteam_region4_set_Tx(T, 0.))\
		, freesteam_region4_dAdTx('h',freesteam_region4_set_Tx(T, 0.))\
		, "[hf] = freesteam_hf_T(T)"\
	) X \
	D(hg_T\
		, double T = inputs[0]\
		, freesteam_h(freesteam_region4_set_Tx(T, 1.))\
		, freesteam_region4_dAdTx('h',freesteam_region4_set_Tx(T, 1.))\
		, "[hg] = freesteam_hg_T(T)"\
	)

#define FREESTEAM_SISO_WRAP(FN,PRECALC,VALCODE,JACCODE,DOCSTRING)\
	int FN##_calc(struct BBoxInterp *bbox,\
		int ninputs, int noutputs,\
		double *inputs, double *outputs,\
		double *jacobian\
	){\
		if(ninputs!=1 || noutputs!=1)return 1;\
		PRECALC;\
		switch(bbox->task){\
		case bb_func_eval:\
			outputs[0] = VALCODE;\
			return 0;\
		case bb_deriv_eval:\
			jacobian[0] = JACCODE;\
			return 0;\
		default:\
			ERROR_REPORTER_HERE(ASC_PROG_ERR,"Invalid call, unknown bbox->task");\
		}\
		return 1;\
	}

#define FREESTEAM_SISO_DECL(FN,PRECALC,VALCODE,JACCODE,DOCSTRING)\
	result += CreateUserFunctionBlackBox("freesteam_" #FN\
		, NULL /* alloc */\
		, FN##_calc /* value */\
		, FN##_calc /* deriv */\
		, NULL /* deriv2 */\
		, NULL /* free */\
		, 1,1 /* inputs, outputs */\
		, DOCSTRING " (see http://freesteam.sf.net)"\
		, 0.0\
	);


#define X
FREESTEAM_SISO_FUNCS(FREESTEAM_SISO_WRAP,X)
#undef X

/*----------------------- REGISTRATION --------------------------*/

FREESTEAM_EXPORT int freesteam_register(){
		int result = 0;

#ifdef BBOX_DEBUG
		CONSOLE_DEBUG("Initialising freesteam...");
#endif
		result += CreateUserFunctionBlackBox("freesteam_Tvsx_ph"
			, NULL /* alloc */
			, Tvsx_ph_calc /* value */
			, Tvsx_ph_calc /* deriv */
			, NULL /* deriv2 */
			, NULL /* free */
			, 2,4 /* inputs, outputs */
			, "[T,v,s,x] = freesteam_Tvsx_ph(p,h) (see http://freesteam.sf.net)"
			, 0.0
		);

		result += CreateUserFunctionBlackBox("freesteam_mukrhocp_pT"
			, NULL /* alloc */
			, mukrhocp_pT_calc /* value */
			, NULL /* deriv */
			, NULL /* deriv2 */
			, NULL /* free */
			, 2,4 /* inputs, outputs */
			, "[mu,k,rho,cp] = freesteam_mukrhocp_pT(p,T) (see http://freesteam.sf.net)"
			, 0.0
		);

		result += CreateUserFunctionBlackBox("freesteam_mu_Tv"
			, NULL /* alloc */
			, mu_Tv_calc /* value */
			, NULL /* deriv */
			, NULL /* deriv2 */
			, NULL /* free */
			, 2,1 /* inputs, outputs */
			, "[mu] = freesteam_mu_Tv(T,v) (see http://freesteam.sf.net)"
			, 0.0
		);

		result += CreateUserFunctionBlackBox("freesteam_k_Tv"
			, NULL /* alloc */
			, k_Tv_calc /* value */
			, NULL /* deriv */
			, NULL /* deriv2 */
			, NULL /* free */
			, 2,1 /* inputs, outputs */
			, "[k] = freesteam_k_Tv(T,v) (see http://freesteam.sf.net)"
			, 0.0
		);

#define X
FREESTEAM_SISO_FUNCS(FREESTEAM_SISO_DECL,X)
#undef X

		return result;
}
