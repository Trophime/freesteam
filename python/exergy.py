# coding=utf-8
import freesteam

class SpecificFlowExergyFunctor:
	def __init__(self, p0, T0):
		self.ref = freesteam.steam_pT(p0,T0)
		if self.ref.region == 4:
			raise RuntimeError("Can't have a reference state in the saturation region")

	def __call__(self, state):
		return state.h - self.ref.h - self.ref.T * (state.s - self.ref.s)

class SpecificExergyFunctor:
	def __init__(self, p0, T0):
		self.ref = freesteam.steam_pT(p0,T0)
		if self.ref.region == 4:
			raise RuntimeError("Can't have a reference state in the saturation region")

	def __call__(self, state):
		return state.u - self.ref.u - self.ref.T * (state.s - self.ref.s) + self.ref.p * (state.v - self.ref.v)

if __name__=='__main__':
	# run example code

	def print_ex(N,S):
		print "%s: exergy at p=%0.0f, T=%0.0f°C: ef = %.1f kJ/kg (h = %.1f kJ/kgK)" % (N, S.p/1e5,  S.T-273.15, exf(S)/1e3, S.h/1e3)

	p0 = 1e5
	T0 = 273.15 + 20
	exf = SpecificFlowExergyFunctor(p0, T0)
	
	p = 40e5
	T = 273.15 + 550
	S1 = freesteam.steam_pT(p,T)
	print_ex("S1",S1)

	p = 38e5
	T = 273.15 + 550
	S2 = freesteam.steam_pT(p,T)
	print_ex("S2",S2)

	p = 35e5
	T = 273.15 + 550
	S3 = freesteam.steam_pT(p,T)
	print_ex("S3",S3)

	p = 0.2e5
	T = 273.15 + 80
	S0 = freesteam.steam_pT(p,T)
	print_ex("S0",S0)

	print "from %0.0f to %0.0f bar, %.2f %% of exergy is lost" % (S1.p/1e5, S2.p/1e5, ((exf(S1) - exf(S2))/(exf(S1)-exf(S0)))*100)
	print "from %0.0f to %0.0f bar, %.2f %% of exergy is lost" % (S1.p/1e5, S3.p/1e5, ((exf(S1) - exf(S3))/(exf(S1)-exf(S0)))*100)

