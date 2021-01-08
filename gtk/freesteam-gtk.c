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

#ifndef GTK_GLADE_FILE
# define GTK_GLADE_FILE "freesteam-gtk.glade"
#endif
#ifndef GTK_GLADE_DIR
# define GTK_GLADE_DIR "."
#endif
#ifdef _WIN32
# define PATH_SEP "\\"
#else
# define PATH_SEP "/"
#endif

int main (int argc, char *argv[]){
    GtkBuilder *builder; 
    GtkWidget *window;
    GtkTreeIter iter;

    gtk_init(&argc, &argv);
 
    builder = gtk_builder_new();

	FILE *f = fopen(GTK_GLADE_DIR PATH_SEP GTK_GLADE_FILE,"r");
	if(f){
		fclose(f);
	    gtk_builder_add_from_file(builder, GTK_GLADE_DIR PATH_SEP GTK_GLADE_FILE, NULL);
	}else if((f = fopen(GTK_GLADE_FILE,"r"))){
		fclose(f);
	    gtk_builder_add_from_file(builder, GTK_GLADE_FILE, NULL);
	}else{
		fprintf(stderr,"ERROR: unable to locate Glade file" GTK_GLADE_DIR PATH_SEP GTK_GLADE_FILE ". Exiting.\n");
		return 1;
	}	
		
    window = GTK_WIDGET(gtk_builder_get_object(builder, "window"));

    /* define and fill in the data structure containing steam table data */
    TableData data;
    
    data.iter = &iter;
    data.solver_status = GTK_STATUSBAR(gtk_builder_get_object(builder, "statusbar"));

    data.indep_var1_entry = GTK_ENTRY(gtk_builder_get_object(builder, "indep_var1_entry"));
    data.indep_var2_entry = GTK_ENTRY(gtk_builder_get_object(builder, "indep_var2_entry"));

    data.SolverClassCombo  = GTK_COMBO_BOX(gtk_builder_get_object(builder, "solver_class_combo") );
    data.IndVariablesCombo = GTK_COMBO_BOX(gtk_builder_get_object(builder, "indep_variables_combo") );

    data.list                    = GTK_LIST_STORE(gtk_builder_get_object(builder, "liststore"));
    data.IndVarsSinglePhaseModel = GTK_LIST_STORE(gtk_builder_get_object(builder, "indep_vars_single_phase_liststore"));
    data.IndVarsSaturationModel  = GTK_LIST_STORE(gtk_builder_get_object(builder, "indep_vars_saturation_liststore"));

    data.IndVar1Label = GTK_LABEL(gtk_builder_get_object(builder, "indep_var1_label") );
    data.IndVar2Label = GTK_LABEL(gtk_builder_get_object(builder, "indep_var2_label") );

    data.about = GTK_DIALOG(gtk_builder_get_object(builder, "aboutdialog"));

    gtk_builder_connect_signals(builder, &data);

    gtk_statusbar_push(data.solver_status, 0, "Ready");
    gtk_widget_show(window); 
    gtk_main();

    return 0;
}


