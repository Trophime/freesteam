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
#ifndef FREESTEAM_STEAM_H
#define FREESTEAM_STEAM_H

#include "common.h"

#include <stdio.h>

typedef struct SteamState_R1_struct{
	MyDouble p, T;
} SteamState_R1;

typedef struct SteamState_R2_struct{
	MyDouble p, T;
} SteamState_R2;

typedef struct SteamState_R3_struct{
	MyDouble rho, T;
} SteamState_R3;

typedef struct SteamState_R4_struct{
	MyDouble T, x;
} SteamState_R4;

typedef struct SteamState_struct{
	char region;
	union U {
		SteamState_R1 R1;
		SteamState_R2 R2;
		SteamState_R3 R3;
		SteamState_R4 R4;
		
		#if HAVE_CADNA_H && defined(__cplusplus)
		U() { 
		   new( &R1 ) SteamState_R1(); 
		   new( &R2 ) SteamState_R2(); 
		   new( &R3 ) SteamState_R3(); 
		   new( &R4 ) SteamState_R4(); 
		}
		#endif
	} SteamState_U ;
} SteamState;

FREESTEAM_DLL int freesteam_region(SteamState S);

FREESTEAM_DLL SteamState freesteam_region1_set_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL SteamState freesteam_region2_set_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL SteamState freesteam_region3_set_rhoT(MyDouble rho, MyDouble T);
FREESTEAM_DLL SteamState freesteam_region4_set_Tx(MyDouble T, MyDouble x);

FREESTEAM_DLL int freesteam_fprint(FILE *f, SteamState S);

#if 0
# define FREESTEAM_DEBUG(NAME,STATE)\
	fprintf(stderr,"%s (%s:%d): %s ",__func__,__FILE__,__LINE__,NAME);\
	freesteam_fprint(stderr,S);
#else
# define FREESTEAM_DEBUG(NAME,STATE)
#endif

typedef MyDouble SteamPropertyFunction(SteamState S);

FREESTEAM_DLL MyDouble freesteam_p(SteamState S);
FREESTEAM_DLL MyDouble freesteam_T(SteamState S);
FREESTEAM_DLL MyDouble freesteam_rho(SteamState S);
FREESTEAM_DLL MyDouble freesteam_v(SteamState S);
FREESTEAM_DLL MyDouble freesteam_u(SteamState S);
FREESTEAM_DLL MyDouble freesteam_h(SteamState S);
FREESTEAM_DLL MyDouble freesteam_s(SteamState S);
FREESTEAM_DLL MyDouble freesteam_cp(SteamState S);
FREESTEAM_DLL MyDouble freesteam_cv(SteamState S);
FREESTEAM_DLL MyDouble freesteam_w(SteamState S);

FREESTEAM_DLL MyDouble freesteam_x(SteamState S);

FREESTEAM_DLL MyDouble freesteam_mu(SteamState S);
FREESTEAM_DLL MyDouble freesteam_k(SteamState S);

#endif


