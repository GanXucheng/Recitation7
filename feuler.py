import numpy as np
import matplotlib.pyplot as plt

blue = (114/255., 158/255., 206/255.)
orange = (255/255., 158/255., 74/255.)
green = (103/255., 191/255., 92/255.)
red = (237/255., 102/255., 93/255.)

def feuler( x, v, h, f, *args ):
    vn = v + h*f(x, *args)
    xn = x + h*v
    return xn, vn

def hooke( x, k, m ):
    return -float(k)/float(m)*x

def evolve( x0, v0, t0, tf, N, f ):

    h = (tf-t0)/float(N)
    print 'Timestep ', h

    ts = np.zeros(N)
    xs = np.zeros(N)
    vs = np.zeros(N)

    x = x0
    v = v0
    k = 1.0
    m = 1.0
    for i in range(N):
        x, v = feuler( x, v, h, hooke, k, m )
        t = i*h
        ts[i] = t
        xs[i] = x
        vs[i] = v

    kin = 0.5*m*vs*vs
    pot = 0.5*k*xs*xs
    Etot = kin + pot

    return xs, ts, (kin, pot, Etot)


if __name__=='__main__':

    N = 500
    tf = 30

    x0 = 1.0
    v0 = 0.0

    xs, ts, E = evolve( x0, v0, 0.0, tf, N, hooke )

    w = 1.0
    x_true = np.cos( w*ts )

    fig, ax = plt.subplots( 2, 1)
    ax[0].plot( ts, x_true, color=red, lw=1.0 ) 
    ax[0].plot( ts, xs, marker = 'o', color=blue, ls='', ms=3, mew=0.3)
    ax[0].set_ylabel(r'$x_n$', fontsize=16)

    ax[1].plot( ts, E[0], color=green, label=r'$E_k$' )
    ax[1].plot( ts, E[1], color=blue, label=r'$U$' )
    ax[1].plot( ts, E[2], color=red, label=r'$E_{tot}$' )
    ax[1].set_ylabel(r'$E$', fontsize=16 )
    ax[1].set_xlabel('time', fontsize=12 )
    ax[1].legend( loc='best' )
    plt.show()






