/*
This is a simple example of a C program that calculates using steam properties
from freesteam.

It demonstrates use of a few of the basic capabilities of freesteam. It
calculates the rise in temperature seen in isentropic compression of a sample
of steam initially at 1 bar, 400 K, to a final pressure of 10 bar. It also
calculates the saturation temperature for steam at that final pressure.
*/

#include <freesteam/common.h>
#include <freesteam/steam_ps.h>
#include <freesteam/steam_pT.h>
#include <freesteam/region4.h>
#include <stdio.h>

int main(void){

	fprintf(stderr,"\nThis example demonstrates use of a few of the basic"
		" capabilities of freesteam. It calculates the rise in temperature"
		" seen in isentropic compression of a sample of steam initially at"
		" 1 bar, 400 K, to a final pressure of 10 bar. It also calculates"
		" the saturation temperature for steam at that final pressure.\n\n"
	);

	MyDouble T = 400.; /* in Kelvin! */
	MyDouble p = 1e5; /* = 1 bar */

	#ifndef HAVE_CADNA_H
	fprintf(stderr,"Initial temperature = %f K, pressure = %f bar\n", T, p/1e5);
        #else
	fprintf(stderr,"Initial temperature = %s K, pressure = %s bar\n", strp(T), strp(p/1e5));
	#endif
	
	/* set a steam state of 1 bar, 400 K */
	SteamState S = freesteam_set_pT(1e5, 400);

	MyDouble s = freesteam_s(S);
	#ifndef HAVE_CADNA_H
	fprintf(stderr,"Entropy at initial state is %f kJ/kgK\n",s/1e3);
        #else
	fprintf(stderr,"Entropy at initial state is %s kJ/kgK\n",strp(s/1e3));
        #endif

	/* calculate a steam state with entropy from above and 10 bar pressure */
	SteamState S2 = freesteam_set_ps(10e5, s);

	MyDouble T2 = freesteam_T(S2);
	MyDouble p2 = freesteam_p(S2);

	/* output the new temperature */
	#ifndef HAVE_CADNA_H
	fprintf(stderr,"New temperature is %f K at %f bar\n", T2, p2/1e5);

	fprintf(stderr,"Check: final entropy is %f kJ/kgK\n", freesteam_s(S2)/1e3);
        #else
	fprintf(stderr,"New temperature is %s K at %s bar\n", strp(T2), strp(p2/1e5));

	fprintf(stderr,"Check: final entropy is %s kJ/kgK\n", strp(freesteam_s(S2)/1e3));
	#endif
	
	/* saturation temperature at final pressure */
	MyDouble Tsat = freesteam_region4_Tsat_p(p2);
	#ifndef HAVE_CADNA_H
	fprintf(stderr,"Saturation temperature at %f bar is %f K.\n\n",p2/1e5, Tsat);
	#else
	fprintf(stderr,"Saturation temperature at %s bar is %s K.\n\n",strp(p2/1e5), strp(Tsat));
	#endif

	return 0;
}

