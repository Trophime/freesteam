/* 
Qt-based GUI for freesteam 2.0. Work in progress.

Based on contributions from Carlo Tegano <carlotorres95@gmail.com>.

Thanks Carlo!

Extensive changes were required to make the GUI work with freesteam-2.0. Haven't
yet completed the work, but shouldn't take much more to fix up the missing and
remaining broken stuff.
*/

#include <QtGui> 
#include "stgui.h"

#include <fstream>
#include <iostream>
#include <cmath>
#include <stdexcept>

extern "C"{
#include <../steam_pT.h>
#include <../steam_ph.h>
#include <../steam_ps.h>
#include <../steam_pv.h>
#include <../steam_Ts.h>
#include <../steam_Tx.h>
#include <../region4.h>
};

#include <QApplication>
 
int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    st_QtGUI *dialog = new st_QtGUI;
 
    dialog->show();
    return app.exec();
}

typedef enum {SOLVE_PT = 0, SOLVE_PH, SOLVE_PS, SOLVE_PV, SOLVE_PRHO, SOLVE_TS, SOLVE_TX, SOLVE_NUM_TYPES} SolverEnum;

const char *solve_descrip[SOLVE_NUM_TYPES] = {
	 "(p,T)   Pressure - temperature"
	,"(p,h)   Pressure - enthalpy"
	,"(p,s)   Pressure - entropy"
	,"(p,v)   Pressure - specific volume"
	,"(p,rho) Pressure - density"
	,"(T,s)   Temperature - entropy"
	,"(T,x)   Temperature - quality"
};

#define SOLVER_FAILED 0
#define PRECISION 0.0001

#define BAR 1e5
#define KJ_KG 1e3
#define KJ_KGK 1e3
#define KG_M3 1
#define M3_KG 1
#define W_MK 1

static double fromcelsius(double TC){
	return TC + IAPWS97_TMIN;
}

static double tocelsius(double TK){
	return TK - IAPWS97_TMIN;
}

// if we include <QtGui> there is no need to include every class used: <QString>, <QFileDialog>,...
 
st_QtGUI::st_QtGUI(QWidget *parent){
	(void)parent;

    setupUi(this); // this sets up GUI

	connect( lineEdit_input_p,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_T,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_h,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_s,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_u,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_v,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_rho,	SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_cp,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_cv,		SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );
	connect( lineEdit_input_qual,	SIGNAL( editingFinished() ), this, SLOT( eval_state() ) );

	/* connect( checkBox_sat, SIGNAL( toggled(bool) ), this, SLOT( set_solver_list() ) ); */

	connect( comboBox_solverType, SIGNAL( currentIndexChanged(int) ), this, SLOT( set_input_edit() ) );

	// let all the sovers to be displayed
	comboBox_solverType->setMaxVisibleItems(16);

	// allow word wrap in the cerr label
	label_cerr->setWordWrap(1);


	set_solver_list();
}

static double get_value(QLineEdit *obj){
	QString str = obj->text();
	bool ok;
	double val = str.toDouble(&ok);
	if(!ok){
		throw std::runtime_error("Unable to calculate: invalid input");
	}
	return val;
}


//			==> SOLVE THE DESIRED STEAM STATE <==
int st_QtGUI::eval_state(){

	int solvertype = comboBox_solverType->currentIndex();

	double p1, T1, h1, s1, v1, rho1, x1;

	try{
		switch(solvertype){

		case SOLVE_PT:
			//solve steam state
			p1 = BAR * get_value(lineEdit_input_p);
			T1 = fromcelsius(get_value(lineEdit_input_T));

			S1 = freesteam_set_pT(p1, T1);
			break;
		case SOLVE_PH:
			p1 = BAR * (get_value(lineEdit_input_p));
			h1 = KJ_KG * (get_value(lineEdit_input_h));	

			S1 = freesteam_set_ph(p1, h1);
			break;
		case SOLVE_PS:
			p1 = BAR * (get_value(lineEdit_input_p));
			s1 = KJ_KGK * (get_value(lineEdit_input_s));	

			S1 = freesteam_set_ps(p1, s1);
			break;
		case SOLVE_PV:
			p1 = BAR * (get_value(lineEdit_input_p));
			v1 = M3_KG * (get_value(lineEdit_input_v));	

			S1 = freesteam_set_pv(p1, v1);
			break;
		case SOLVE_PRHO:
			p1 = BAR * (get_value(lineEdit_input_p));
			rho1 = KG_M3 * (get_value(lineEdit_input_rho));	

			S1 = freesteam_set_pv(p1, 1./rho1);
			break;
		case SOLVE_TS:
			T1 = fromcelsius(get_value(lineEdit_input_T));
			s1 = KJ_KGK * (get_value(lineEdit_input_s));	

			S1 = freesteam_set_Ts(T1, s1);
			break;
		case SOLVE_TX:
			T1 = fromcelsius(get_value(lineEdit_input_T));
			x1 = get_value(lineEdit_input_qual);	

			S1 = freesteam_set_Tx(T1, x1);
			break;		default:
			throw std::runtime_error("Unknown solver type");
		}

		//get data from solver and put in the labels		
		GetPrint();

	}catch(std::exception &E){
		label_cerr->setText(QString(E.what()));
		return SOLVER_FAILED;
	}

	// success: clean cerr output
	label_cerr->setText("ready");

	return 0;	
}

static const char *whichstate(SteamState S){
	if(S.region == 4){
		return "Saturated";
	}
	double T = freesteam_T(S);
	double p = freesteam_p(S);
	if(T > IAPWS97_TCRIT && p > IAPWS97_PCRIT){
		return "Supercrit";
	}

	double psat = freesteam_region4_psat_T(T);
	if(p > psat){
		return "Subcooled";
	}

	if(p < psat){
		return "Superheated";
	}

	if(S.region!=4){
		throw std::runtime_error("Should be region 4!");
	}

	if(S.R4.x == 0){
		return "Sat. liq.";
	}

	if(S.R4.x == 1){
		return "Sat. vap.";
	}

	return "Saturated";
}


//	=======  GET DATA FROM SOLVER AND PRINT THEM  =======

void st_QtGUI::GetPrint(){
	QString mytext;

	double cp = freesteam_cp(S1);
	double cv = freesteam_cv(S1);
	label_output_p->setText(mytext.setNum( freesteam_p(S1) / BAR,     'f',6 ));
	label_output_h->setText(mytext.setNum( freesteam_h(S1) / KJ_KG,   'f',6 ));
	label_output_T->setText(mytext.setNum( tocelsius(freesteam_T(S1)),'f',6 ));
	label_output_u->setText(mytext.setNum( freesteam_u(S1) / KJ_KG,   'f',6 ));
	label_output_s->setText(mytext.setNum( freesteam_s(S1) / KJ_KGK,  'f',6 ));
	label_output_v->setText(mytext.setNum( freesteam_v(S1) / M3_KG,   'f',6 ));
	label_output_rho->setText(mytext.setNum(freesteam_rho(S1) / KG_M3,'f',6 ));
	label_output_cp->setText(mytext.setNum( cp / KJ_KGK,              'f',6 ));
	label_output_cv->setText(mytext.setNum( cv / KJ_KGK,              'f',6 ));
	/*label_output_mu->setText(mytext.setNum( freesteam_mu(S1),          'f',6 ));*/
	label_output_k->setText(mytext.setNum( freesteam_k(S1) / W_MK,    'f',6 ));
	label_output_qual->setText(mytext.setNum(freesteam_x(S1),         'f',6 ));
	label_output_cp_cv->setText(mytext.setNum(cp/cv,                  'f',6 ));
	label_output_fluid_state->setText(whichstate(S1));
}

//	=======  SET UP THE GUI  =======

int st_QtGUI::set_solver_list(){
	comboBox_solverType->clear();
	for(int i=0; i < SOLVE_NUM_TYPES; ++i){
		comboBox_solverType->addItem(solve_descrip[i]);
	}
	return 0;
}

int st_QtGUI::set_input_edit()
{
	//disable all entries
	lineEdit_input_p->setEnabled(0);
	lineEdit_input_T->setEnabled(0);
	lineEdit_input_h->setEnabled(0);
	lineEdit_input_s->setEnabled(0);
	lineEdit_input_u->setEnabled(0);
	lineEdit_input_v->setEnabled(0);
	lineEdit_input_rho->setEnabled(0);
	lineEdit_input_cp->setEnabled(0);
	lineEdit_input_cv->setEnabled(0);
	lineEdit_input_qual->setEnabled(0);

	//clear all entries
	lineEdit_input_p->clear();
	lineEdit_input_T->clear();
	lineEdit_input_h->clear();
	lineEdit_input_s->clear();
	lineEdit_input_u->clear();
	lineEdit_input_v->clear();
	lineEdit_input_rho->clear();
	lineEdit_input_cp->clear();
	lineEdit_input_cv->clear();
	lineEdit_input_qual->clear();

	int solvertype = comboBox_solverType->currentIndex();
	switch(solvertype){

	case SOLVE_PT:
		//solve steam state
		lineEdit_input_p->setEnabled(1);
		lineEdit_input_T->setEnabled(1);
		break;
	case SOLVE_PH:
		lineEdit_input_p->setEnabled(1);
		lineEdit_input_h->setEnabled(1);
		break;
	case SOLVE_PS:
		lineEdit_input_p->setEnabled(1);
		lineEdit_input_s->setEnabled(1);
		break;
	case SOLVE_PV:
		lineEdit_input_p->setEnabled(1);
		lineEdit_input_v->setEnabled(1);
		break;
	case SOLVE_PRHO:
		lineEdit_input_p->setEnabled(1);
		lineEdit_input_rho->setEnabled(1);
		break;
	case SOLVE_TS:
		lineEdit_input_T->setEnabled(1);
		lineEdit_input_s->setEnabled(1);
		break;
	case SOLVE_TX:
		lineEdit_input_T->setEnabled(1);
		lineEdit_input_qual->setEnabled(1);
		break;
	default:
		throw std::runtime_error("Unknown solver type");
	}

	return 0;
}

