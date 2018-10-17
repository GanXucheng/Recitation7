import numpy as np
import matplotlib.pyplot as plt

blue = (114/255., 158/255., 206/255.)
orange = (255/255., 158/255., 74/255.)
green = (103/255., 191/255., 92/255.)
red = (237/255., 102/255., 93/255.)


#============================================================================
#	Definition for my class to numerically solve the 
#	2nd order ODE d^2x/dt^2 = f(x).  The user
#	specifies f(x) (ode.fxn) and the integration scheme
#	(ode.scheme) to be used at runtime.
#============================================================================
class ode:

	x0 = 0.0
	v0 = 0.0

	ts = None
	xs = None
	vs = None

	fxn = None
	args = None
	scheme = None
	
	def __init__(self, fxn, scheme):
	
		self.fxn = fxn
		self.scheme = scheme
	
	def setInitConditions(self, x0, v0):
		
		self.x0 = x0
		self.v0 = v0

	def setArgs(self, *args):
		self.args = args

	def evolve(self, t0, tf, N):
		
		h = (tf-t0)/float(N)
		print "t: ", "[{0:f}, {1:f}]".format( t0,tf )
		print "Timestep: ", h

		ts = np.zeros(N)
		xs = np.zeros(N)
		vs = np.zeros(N)

		x = self.x0
		v = self.v0
		for i in range(N):
			x, v = self.scheme( x, v, h, self.fxn, *self.args )	
			t = t0 + i*h
			ts[i] = t
			xs[i] = x
			vs[i] = v

		self.ts = ts
		self.xs = xs
		self.vs = vs
		
	def get_analytic(self):
		#Would have to change what happens here for different functions
		k = self.args[0]
		m = self.args[1]
		w = k/m
		return np.cos( w*self.ts )

	def plot(self, E_flag=None ):
		
		x_true = self.get_analytic()
		if E_flag is not True:
			fig, ax = plt.subplots(1,1)
			ax.plot( self.ts, self.xs, color=blue, marker='o', ls='', ms=3, mew=0.3)
			ax.plot( self.ts, x_true, color=red, lw=1.5 )
			ax.set_xlabel( 'time', fontsize=12 )
			ax.set_ylabel( r'$x_n$', fontsize=16 )
		else:
			fig, ax = plt.subplots( 2, 1)
			ax[0].plot( self.ts, x_true, color=red, lw=1.5 ) 
			ax[0].plot( self.ts, self.xs, marker = 'o', color=blue, ls='', ms=3, mew=0.3)
			ax[0].set_ylabel(r'$x_n$', fontsize=16)

			kin = 0.5*self.vs*self.vs
			pot = 0.5*self.xs*self.xs
			tot = kin+pot
			ax[1].plot( self.ts, kin, color=green,lw=1.5, label=r'$E_k$' )
			ax[1].plot( self.ts, pot, color=blue, lw=1.5, label=r'$U$' )
			ax[1].plot( self.ts, tot, color=red,  lw=2.5, label=r'$E_{tot}$' )
			ax[1].set_ylabel(r'$E$', fontsize=16 )
			ax[1].set_xlabel('time', fontsize=12 )
			ax[1].legend( loc='best' )		



def feuler( x, v, h, f, *args ):
    vn = v + h*f(x, *args)
    xn = x + h*v
    return xn, vn

def hooke( x, k, m ):
    return -float(k)/float(m)*x



if __name__=='__main__':

	N = 500
	tf = 30

	x0 = 1.0
	v0 = 0.0

	k = 1.0
	m = 1.0

	#Create an ode object to integrate hookes law using forward euler
	q = ode(hooke, feuler)
	#Set my objects initial conditions and specify the extra arguments needed by hooke()
	q.setInitConditions( x0, v0 )
	q.setArgs( k, m )

	#Evolve and plot
	q.evolve( 0.0, tf, N )
	q.plot( E_flag=True )

	plt.show()
	









