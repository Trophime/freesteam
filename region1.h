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

#ifndef FREESTEAM_REGION1_H
#define FREESTEAM_REGION1_H

#include "common.h"

FREESTEAM_DLL MyDouble freesteam_region1_u_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_v_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_s_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_h_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_cp_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_cv_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_w_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_a_pT(MyDouble p, MyDouble T);
FREESTEAM_DLL MyDouble freesteam_region1_g_pT(MyDouble p, MyDouble T);

/* used in calculations of derivatives, see derivs.c */
MyDouble freesteam_region1_alphav_pT(MyDouble p, MyDouble T);
MyDouble freesteam_region1_kappaT_pT(MyDouble p, MyDouble T);

#define REGION1_TMAX 623.15 /* K */

#endif

