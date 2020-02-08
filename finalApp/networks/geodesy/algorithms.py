import math as mt

def degreesToDMS(degrees):
    D = mt.floor(degrees)
    m = (degrees-D)*60
    M = mt.floor(m)
    S = (m-M)*60
    return [D, M, S]

class GRS80():
    a = 6378137
    e2 = 0.00669438002290
    f = 1/298.25722210
    b = a-a*f
    e2p = round((a**2-b**2)/b**2,13)

def getData(number, group=1):
    try:
        if group == 1:
            X = 3648420.000
            Y = 1474120.000
            Z = 5003100.000+int(number)*20
            s = 450 + number
            z = 73.0
            A = 30.0+number
            return [X, Y, Z, s, z, A]
        else:
            return 'Podano nieprawidłowy numer grupy'
    except:
        return 'Podany numer grupy nie jest wartością liczbową'


def N_radius(fi, a = GRS80.a, e2 = GRS80.e2):
    nom = a
    den = mt.sqrt(1-e2*(mt.sin(fi))**2)
    return nom/den


def M_radius(fi, a = GRS80.a, e2 = GRS80.e2):
    nom = a*(1-e2)
    den = (mt.sqrt(1-e2*(mt.sin(fi))**2))**3
    return nom/den

def hirvonen(X, Y, Z, e2 = GRS80.e2):
    radius = mt.sqrt(X**2+Y**2)
    fi = mt.atan(Z/radius*(1-e2)**(-1))
    N = N_radius(fi)
    H = radius/mt.cos(fi)-N
    eps = 1
    while eps>(0.00001*mt.pi/(180*3600)):
        fi0 = fi
        fi = mt.atan((Z/radius)/(1-e2*(N/(N+H))))
        N = N_radius(fi)
        H = radius / mt.cos(fi) - N
        eps = abs(fi0-fi)
    lbd = mt.atan2(Y,X) if mt.atan2(Y,X) >=0 else mt.atan2(Y,X)+2*mt.pi
    return [fi, lbd, H]

print(getData(9))
print(N_radius(52*mt.pi/180))
print(M_radius(52*mt.pi/180))
data = getData(9)
FLH = hirvonen(data[0], data[1], data[2])
print(degreesToDMS(FLH[0]*180/mt.pi))
print(degreesToDMS(FLH[1]*180/mt.pi))
print(FLH[2])
print(FLH[0])
print(FLH[1])

