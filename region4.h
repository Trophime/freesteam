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

#ifndef FREESTEAM_REGION4_H
#define FREESTEAM_REGION4_H

#include "common.h"

FREESTEAM_DLL MyDouble freesteam_region4_psat_T(MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region4_Tsat_p(MyDouble p);

FREESTEAM_DLL MyDouble freesteam_region4_rhof_T(MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region4_rhog_T(MyDouble T);

FREESTEAM_DLL MyDouble freesteam_region4_v_Tx(MyDouble T, MyDouble x);
FREESTEAM_DLL MyDouble freesteam_region4_u_Tx(MyDouble T, MyDouble x);
FREESTEAM_DLL MyDouble freesteam_region4_h_Tx(MyDouble T, MyDouble x);
FREESTEAM_DLL MyDouble freesteam_region4_s_Tx(MyDouble T, MyDouble x);
FREESTEAM_DLL MyDouble freesteam_region4_cp_Tx(MyDouble T, MyDouble x);
FREESTEAM_DLL MyDouble freesteam_region4_cv_Tx(MyDouble T, MyDouble x);

FREESTEAM_DLL MyDouble freesteam_region4_dpsatdT_T(MyDouble T);

#endif

