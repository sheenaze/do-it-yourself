import math as mt
import numpy as np

def ValidateCoor(angle):
    return 0<= angle <= 2*mt.pi

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

def XYZ_from_FiLbdH(fi, lbd, H, e2 = GRS80.e2):
    N = N_radius(fi)
    X = (N+H)*mt.cos(fi)*mt.cos(lbd)
    Y = (N+H)*mt.cos(fi)*mt.sin(lbd)
    Z = (N*(1-e2)+H)*mt.sin(fi)
    return [X, Y, Z]

def neu_vector(azimuth, zenith, distance):
    n = distance*mt.sin(zenith)*mt.cos(azimuth)
    e = distance*mt.sin(zenith)*mt.sin(azimuth)
    u = distance*mt.cos(zenith)
    return [n, e, u]

def neu2XYZ(fi, lbd):
    r1 = [-mt.sin(fi)*mt.cos(lbd), -mt.sin(lbd), mt.cos(fi)*mt.cos(lbd)]
    r2 = [-mt.sin(fi)*mt.sin(lbd),  mt.cos(lbd), mt.cos(fi)*mt.sin(lbd)]
    r3 = [mt.cos(fi), 0, mt.sin(fi)]
    return np.array([r1, r2, r3])


def kiviojMethod(FiP, LbdP, Az_ell, dist_ell, n):
    ds = dist_ell/n
    if ds>1500:
        return 'Odcinki przekraczają 1500m, podać inną liczbę odcinków'
    else:
        Fi = FiP
        Lbd = LbdP
        Az = Az_ell
        i = 1
        while i<=n:
            # First step - first increment
            N = N_radius(Fi)
            M = M_radius(Fi)
            dFi = ds*mt.cos(Az)/M
            dA = ds*mt.tan(Fi)*mt.sin(Az)/N
            # Second step - Fi and Az at in the middle of the line segment
            Fim = Fi+dFi/2
            Am = Az+dA/2
            # Third step - second increment based on the middle line values of Fi and Azs
            Nm = N_radius(Fim)
            Mm = M_radius(Fim)
            Fi += ds*mt.cos(Am)/Mm
            Lbd += ds*mt.sin(Am)/Nm/mt.cos(Fim)
            Az += ds*mt.sin(Am)*mt.tan(Fim)/Nm
            i+=1
        FiK = Fi
        LbdK = Lbd
        AzK = Az + mt.pi if Az <=mt.pi else Az-mt.pi
        return [FiK, LbdK, AzK]


def vincentyAlgorithm(FiP, LbdP, FiK, LbdK,  b = GRS80.b, f = GRS80.f, e2p = GRS80.e2p):
    U1 = mt.atan(mt.tan(FiP)*(1-f))
    cosU1 = mt.cos(U1)
    sinU1 = mt.sin(U1)

    U2 = mt.atan(mt.tan(FiK)*(1-f))
    cosU2 = mt.cos(U2)
    sinU2 = mt.sin(U2)
    #First approximation of Lbd = L
    L = LbdK-LbdP
    eps = 1
    Lbd = L
    while abs(eps) > 10**(-12):
        Lbd0 = Lbd
        sinLbd = mt.sin(Lbd)
        cosLbd = mt.cos(Lbd)
        sinSig = mt.sqrt((cosU2*sinLbd)**2+(cosU1*sinU2-sinU1*cosU2*cosLbd)**2)
        cosSig = sinU1 * sinU2 + cosU1 * cosU2 * cosLbd
        Sig = mt.asin(sinSig)
        sinAlpha = cosU1*cosU2*sinLbd/sinSig
        cosAlpha2 = 1-sinAlpha**2
        cos2Sigm = cosSig-2*sinU1*sinU2/cosAlpha2
        C = f/16*cosAlpha2*(4+f*(4-3*cosAlpha2))
        Lbd = L+(1-C)*f*sinAlpha*(Sig+C*sinSig*(cos2Sigm+C*cosSig*(-1+2*cos2Sigm**2)))
        eps = Lbd - Lbd0

    u2 = cosAlpha2*e2p
    A = 1+u2/16384*(4096+u2*(-768+u2*(320-175*u2)))
    B = u2/1024*(256+u2*(-128+u2*(74-47*u2)))
    deltaSig = B*sinSig*(cos2Sigm+B/4*(cosSig*(-1+2*cos2Sigm**2)-B/6*cos2Sigm*(-3+4*cos2Sigm**2)))
    s = b*A*(Sig-deltaSig)
    AzPK = mt.atan2(cosU2*sinLbd, cosU1*sinU2-sinU1*cosU2*cosLbd)
    AzKP = mt.atan2(cosU1*sinLbd, -sinU1*cosU2+cosU1*sinU2*cosLbd)

    return [AzPK, AzKP, s]


def GK_direct(Fi, Lbd, Lbd0, a = GRS80.a, e2 = GRS80.e2, e2p = GRS80.e2p):
    t = mt.tan(Fi)
    eta2 = e2p*mt.cos(Fi)**2
    l = Lbd-Lbd0
    N = N_radius(Fi)

    e4 = e2**2
    e6 = e2**3
    A0 = 1-e2/4-3*e4/64-5*e6/256
    A2 = 3/8*(e2+e4/4+15*e6/128)
    A4 = 15/256*(e4+3*e6/4)
    A6 = 35*e6/3072

    sig = a*(A0*Fi-A2*mt.sin(2*Fi)+A4*mt.sin(4*Fi)-A6*mt.sin(6*Fi))
    x1 = l**2/12*mt.cos(Fi)**2*(5-t**2+9*eta2+4*eta2**2)
    x2 = l**4/360*mt.cos(Fi)**4*(61-58*t**2+t**4+270*eta2-330*eta2*t**2)
    X = sig + l**2/2*N*mt.sin(Fi)*mt.cos(Fi)*(l+x1+x2)
    y1 = l**2/6*mt.cos(Fi)**2*(1-t**2+eta2)
    y2 = l**4/120*mt.cos(Fi)**4*(5-18*t**2+t**4+14*eta2-58*eta2*t**2)
    Y = l*N*mt.cos(Fi)*(l+y1+y2)
    return [X, Y]

def datum2000(Fi, Lbd, zone):
    if zone in [5, 6, 7, 8]:
        Lbd0 = zone*3*mt.pi/180
        XY = GK_direct(Fi, Lbd, Lbd0)
        m0 = 0.999923
        X2000 = XY[0]*m0
        Y2000 = XY[1]*m0 + zone*10**6+500000
        return [X2000, Y2000]
    else:
        return 'Zły numer strefy'


c = mt.pi/180
FLA = kiviojMethod(52*c, 21*c, 45*c, 28000,28)
print(FLA)
print(degreesToDMS(FLA[0]/c))
print(degreesToDMS(FLA[1]/c))
print(degreesToDMS(FLA[2]/c))

Reverse = vincentyAlgorithm(52*c, 21*c, FLA[0], FLA[1])
print(degreesToDMS(Reverse[0]/c))
print(degreesToDMS(Reverse[1]/c))
print(Reverse[2])

# print(getData(9))
# print(N_radius(52*mt.pi/180))
# print(M_radius(52*mt.pi/180))
# data = getData(5)
# FLH = hirvonen(data[0], data[1], data[2])
# print(degreesToDMS(FLH[0]*180/mt.pi))
# print(degreesToDMS(FLH[1]*180/mt.pi))
# print(FLH[2])
# print(FLH[0])
# print(FLH[1])
#
# print(data[5], data[4], data[3])
# print(neu_vector(data[5], data[4], data[3]))
# print(neu2XYZ(FLH[0], FLH[1]))

