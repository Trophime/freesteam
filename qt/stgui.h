#ifndef MYQTAPP_H
#define MYQTAPP_H
 
#include "ui_ST.h"

extern "C"{
#include "../steam.h"
};

class st_QtGUI : public QWidget, private Ui::st_QtDLG
{
    Q_OBJECT
 
public:
    st_QtGUI(QWidget *parent = 0);

	QString state1;
	SteamState S1;

	void GetPrint();

public slots:
	int eval_state();
	int set_solver_list();
	int set_input_edit();
	
};

#endif





