/*
Steam Table GUI Implementation
using freesteam IAPWS-IF97 steam tables library and Gtk+2 toolkit
Copyright (C) 2010  Carlo Tegano

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.*/


#ifndef FREESTEAM_GTK_H
#define FREESTEAM_GTK_H

#include <gtk/gtk.h>

#ifdef FREESTEAM_LOCAL
#include <steam_ph.h>
#include <steam_ps.h>
#include <steam_pT.h>
#include <steam_pu.h>
#include <steam_pv.h>
#include <steam_Ts.h>
#include <steam_Tx.h>
#include <steam_uv.h>
#include <region4.h>
#else
#include <freesteam/steam_ph.h>
#include <freesteam/steam_ps.h>
#include <freesteam/steam_pT.h>
#include <freesteam/steam_pu.h>
#include <freesteam/steam_pv.h>
#include <freesteam/steam_Ts.h>
#include <freesteam/steam_Tx.h>
#include <freesteam/steam_uv.h>
#include <freesteam/region4.h>
#endif

#include <stdlib.h>

#define _Nr_table_lines_ 12
#define VERBOSE 1

enum
  {
    READY = 0,
    DOMAIN_ERROR,
    PRINT_MESSAGE
  };

/* columns of the steam table */
enum
  {
    COL_PROPERTY = 0,
    COL_UNITS,
    COL_LIQUID,
    COL_MIXED,
    COL_VAPOUR,
    NUM_COLS
  };

enum
  {
    OUT_OF_LIMITS = 0,
    REGION_1,
    REGION_2,
    REGION_3,
    REGION_4,
    REGION_5
  };

/* solver classes */
enum
  {
    SINGLE_PHASE_SOLVER = 0,
    SATURATION_SOLVER
  };

/* independent variables allowed combinations, i.e. the available solvers */
enum
  {
    SOLVER_PT = 0,
    SOLVER_PH ,
    SOLVER_PS ,
    SOLVER_PU ,
    SOLVER_PV,
    SOLVER_TS
  };

enum
  {
    SAT_SOLVER_TX = 0,
    SAT_SOLVER_PX
  };


/* struct to pass all necessary user data to callbacks */
typedef struct _TableData TableData;
struct _TableData
{
  SteamState S;
  SteamState SLiq;
  SteamState SVap;
  SteamState SMix;

  unsigned int region;

  gchar status_string[128];

  GtkTreeIter  *iter;

  GtkStatusbar *solver_status;

  GtkEntry *indep_var1_entry;
  GtkEntry *indep_var2_entry;

  GtkLabel *IndVar1Label;
  GtkLabel *IndVar2Label;

  GtkComboBox *SolverClassCombo;
  GtkComboBox *IndVariablesCombo;

  GtkListStore *list;
  GtkListStore *IndVarsSinglePhaseModel;
  GtkListStore *IndVarsSaturationModel;

  GtkDialog *about;
};


#endif /* FREESTEAM_GTK_H */

