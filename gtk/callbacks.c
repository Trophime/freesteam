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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

#include "freesteam-gtk.h"
#include <string.h>

void 
on_window_destroy (GtkObject *object, gpointer user_data)
{
  gtk_main_quit ();
}

void
on_quit_activate (GtkMenuItem *item, gpointer user_data)
{
  gtk_main_quit ();
}


void
on_aboutdialog_response (GtkDialog *dialog, gint response_id, gpointer user_data)
{
  TableData *data = (TableData *) user_data;

  if (response_id == GTK_RESPONSE_CANCEL)
    gtk_widget_hide (GTK_WIDGET (data->about));
}


void
on_about_activate (GtkMenuItem *item, gpointer user_data)
{
  TableData *data = (TableData *) user_data;

  gtk_widget_show(GTK_WIDGET(data->about));
}

/*
 * show solver status and errors on the status bar
 */

void status_bar_update(int code, TableData *data)
{
  if (code==DOMAIN_ERROR)
    {
      gtk_statusbar_push( data->solver_status, 0, "ERROR! Independent variable out of domain");
    }
  else if (code==READY)
    {
      gtk_statusbar_push( data->solver_status, 0, "Ready");
    }
  else if (code==PRINT_MESSAGE)
    {
      gtk_statusbar_push( data->solver_status, 0, data->status_string);
    }

}


void reset_table (TableData *data)
{
  int i, j =0;

  for (j=COL_LIQUID; j<NUM_COLS; j++)
    {
      gtk_tree_model_get_iter_first( GTK_TREE_MODEL(data->list), data->iter );

      for(i=0; i<_Nr_table_lines_; i++) 
	{
	  gtk_list_store_set( data->list, data->iter, j, 0.0, -1);
	  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter );
	}
    }
}


/*
 * setup the solver class and relative options for the independent variables 
 */

G_MODULE_EXPORT
void on_solver_class_changed (GtkComboBox *widget, gpointer user_data)
{
  TableData *data = (TableData *) user_data;

  gtk_entry_set_text (data->indep_var1_entry, "");
  gtk_entry_set_text (data->indep_var2_entry, "");

  if( gtk_combo_box_get_active( data->SolverClassCombo ) == SINGLE_PHASE_SOLVER )
    {
      gtk_combo_box_set_model( data->IndVariablesCombo, 
                               GTK_TREE_MODEL(data->IndVarsSinglePhaseModel)  );

      gtk_combo_box_set_active (data->IndVariablesCombo, 0);
    }
  else if( gtk_combo_box_get_active( data->SolverClassCombo ) == SATURATION_SOLVER )
    {
      gtk_combo_box_set_model( data->IndVariablesCombo, 
                               GTK_TREE_MODEL(data->IndVarsSaturationModel) );

      gtk_combo_box_set_active (data->IndVariablesCombo, 0);
    }

  reset_table (data);

}

/*
 * Put correct description in the independent variables labels
 */

G_MODULE_EXPORT
void on_indep_variables_combo_changed (GtkComboBox *widget, gpointer user_data)
{
  TableData *data = (TableData *) user_data;

  gtk_entry_set_text (data->indep_var1_entry, "");
  gtk_entry_set_text (data->indep_var2_entry, "");

  /* the single phase solvers list is active */
  if( gtk_combo_box_get_active( data->SolverClassCombo ) == SINGLE_PHASE_SOLVER )
    {

    if( gtk_combo_box_get_active( data->IndVariablesCombo ) == SOLVER_PT )
      {
        gtk_label_set_text( data->IndVar1Label, "Pressure [bar]" );
        gtk_label_set_text( data->IndVar2Label, "Temperature [°C]" );
      }
    else if( gtk_combo_box_get_active( data->IndVariablesCombo ) == SOLVER_PH )
      {
        gtk_label_set_text( data->IndVar1Label, "Pressure [bar]" );
        gtk_label_set_text( data->IndVar2Label, "Enthalpy [kJ/kg]" );
      }
    else if( gtk_combo_box_get_active( data->IndVariablesCombo ) == SOLVER_PS )
      {
        gtk_label_set_text( data->IndVar1Label, "Pressure [bar]" );
        gtk_label_set_text( data->IndVar2Label, "Entropy [kJ/kg·K]" );
      }
    else if( gtk_combo_box_get_active( data->IndVariablesCombo ) == SOLVER_PU )
      {
        gtk_label_set_text( data->IndVar1Label, "Pressure [bar]" );
        gtk_label_set_text( data->IndVar2Label, "Internal energy [kJ/kg]" );
      }
    else if (gtk_combo_box_get_active( data->IndVariablesCombo ) == SOLVER_TS)
      {
        gtk_label_set_text( data->IndVar1Label, "Temperature [°C]" );
        gtk_label_set_text( data->IndVar2Label, "Entropy [kJ/kg·K]" );
      }
  }

  /* the saturated solvers list is active */
  else if( gtk_combo_box_get_active( data->SolverClassCombo ) == SATURATION_SOLVER )
  {
    if( gtk_combo_box_get_active( data->IndVariablesCombo ) == SAT_SOLVER_TX )
      {
        gtk_label_set_text( data->IndVar1Label, "Temperature [°C]" );
        gtk_label_set_text( data->IndVar2Label, "Quality [-]" );
      }
    else if( gtk_combo_box_get_active( data->IndVariablesCombo ) == SAT_SOLVER_PX )
      {
        gtk_label_set_text( data->IndVar1Label, "Pressure [bar]" );
        gtk_label_set_text( data->IndVar2Label, "Quality [-]" );
      }
    }

  reset_table (data);

}

/*
 * update table values after recalculation 
 */

void update_table_liststore( int column, int reset, TableData *data , SteamState *S)
{

  if (reset) reset_table (data);


  gtk_tree_model_get_iter_first( GTK_TREE_MODEL(data->list), data->iter );
  gtk_list_store_set( data->list, data->iter, column, freesteam_p(*S) * 1e-5, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_T(*S) - 273.15, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_h(*S) * 1e-3, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_s(*S) * 1e-3, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_u(*S) * 1e-3, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_v(*S), -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_rho(*S), -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_cp(*S) * 1e-3, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_cv(*S) * 1e-3, -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 

  gtk_list_store_set( data->list, data->iter, column, freesteam_x(*S), -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_k(*S), -1);

  gtk_tree_model_iter_next( GTK_TREE_MODEL(data->list), data->iter ); 
  gtk_list_store_set( data->list, data->iter, column, freesteam_mu(*S), -1);

}


int eval_state (TableData *data)
{
  double var1, var2;

  int active_sol_class;
  int active_sol;

  /* read input without units conversion */
  var1 = atof (gtk_entry_get_text (data->indep_var1_entry) );
  var2 = atof (gtk_entry_get_text (data->indep_var2_entry) );

  active_sol_class = gtk_combo_box_get_active (data->SolverClassCombo);
  active_sol = gtk_combo_box_get_active (data->IndVariablesCombo);

  /* single phase state */
  /**********************/

  if( active_sol_class == SINGLE_PHASE_SOLVER )
    {

      switch (active_sol)
	{
	 
	case SOLVER_PT:

	  if (1)
	    data->S = freesteam_set_pT (var1*1e+5, var2+273.15);
	  else
	    return DOMAIN_ERROR;

	  break;


	case SOLVER_PH:

	  if (!freesteam_bounds_ph (var1*1e+5, var2*1e+3, VERBOSE))
	    {
	      data->S = freesteam_set_ph (var1 * 1e+5, var2 * 1e+3);

	      if (data->S.region == REGION_4)
		{
		  var1 = freesteam_region4_Tsat_p (var1 * 1e+5); /* T in K */
		  data->SLiq = freesteam_set_Tx (var1, 0.0);
		  data->SVap = freesteam_set_Tx (var1, 1.0);
		  data->SMix = data->S;
		}
	    }
	  else
	    return DOMAIN_ERROR;

	  break;


	case SOLVER_PS:

	  if (!freesteam_bounds_ps (var1*1e+5, var2*1e+3, VERBOSE))
	    {
	      data->S = freesteam_set_ps (var1 * 1e+5, var2 * 1e+3);
	    }
	  else
	    return DOMAIN_ERROR;

	  break;

	case SOLVER_PU:

	  data->S = freesteam_set_pu (var1 * 1e+5, var2 * 1e+3);

	  break;


	case SOLVER_PV:

	  if (freesteam_bounds_pv (var1 * 1e+5, var2, VERBOSE))
	    {
	      data->S = freesteam_set_pv (var1 * 1e+5, var2);
	    }
	  else
	    return DOMAIN_ERROR;

	  break; 


	case SOLVER_TS:
	
	  if (!freesteam_bounds_Ts (var1+273.15, var2*1e+3, VERBOSE))
	    {
	      data->S = freesteam_set_Ts( var1 + 273.15, var2 * 1e+3);
	    }
	  else
	    return DOMAIN_ERROR;

	} /* switch */
   
    }

  /* saturation state */
  /********************/
  else if (active_sol_class == SATURATION_SOLVER)
    {
      data->S.region = REGION_4;

      switch (active_sol)
	{

	case SAT_SOLVER_TX:
      
	  if (!freesteam_bounds_Tx (var1 + 273.15, var2, 1))
	    {
	      data->SLiq = freesteam_set_Tx (var1 + 273.15, 0.0);
              data->SVap = freesteam_set_Tx (var1 + 273.15, 1.0);
              data->SMix = freesteam_set_Tx (var1 + 273.15, var2);
	    }
	  else
	    return DOMAIN_ERROR;

	  break;
	
	case SAT_SOLVER_PX:
	  if (1)
	    {
	      var1 = freesteam_region4_Tsat_p (var1 * 1e+5); /* T in K */
	      data->SLiq = freesteam_set_Tx (var1, 0.0);
	      data->SVap = freesteam_set_Tx (var1, 1.0);
	      data->SMix = freesteam_set_Tx (var1, var2);
	    }
	  else
	    return DOMAIN_ERROR;

	  break;
	}
    }

  /* solution found for new state */

  switch (data->S.region)
    {
    case REGION_1:

      update_table_liststore( COL_LIQUID, 1, data, &data->S );
      break;


    case REGION_2:

      update_table_liststore( COL_VAPOUR, 1,  data, &data->S );
      break;

    case REGION_3:

      update_table_liststore( COL_LIQUID, 1, data, &data->S );
      break;


    case REGION_4:

      update_table_liststore (COL_VAPOUR, 0, data, &data->SVap);
      update_table_liststore (COL_LIQUID, 0, data, &data->SLiq);
      update_table_liststore (COL_MIXED , 0, data, &data->SMix);
      break;


    case REGION_5:

      update_table_liststore( COL_VAPOUR, 1,  data, &data->S );
      break;
    }

  return 0;
}


/*
 * when the independent variable 1 is modified
 */

G_MODULE_EXPORT
void on_indep_var1_entry_editing_done(GtkEntry *cell_editable,
                                      gpointer  user_data)
{
  TableData *data = (TableData *) user_data;
  int code;

  status_bar_update (READY, data);
  code = eval_state (data);

  if (code==DOMAIN_ERROR) reset_table (data);

  status_bar_update (code, data);
}


/*
 * when the independent variable 2 is modified
 */

G_MODULE_EXPORT
void on_indep_var2_entry_editing_done(GtkEntry *cell_editable,
                                      gpointer  user_data)
{  
  TableData *data = (TableData *) user_data;

  int code;

  status_bar_update (READY, data);
  code = eval_state (data);

  if (code==DOMAIN_ERROR) reset_table (data);

  status_bar_update (code, data);
}



