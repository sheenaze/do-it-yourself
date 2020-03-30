import math as mt
import numpy as np


def validate_coordinates(angle):
    return 0 <= angle <= 2 * mt.pi


def deg2rad(angle):
    return angle * mt.pi / 180


def middle_point_coordinates(x1, x2, y1, y2):
    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2
    return xm, ym


def degrees_to_dms(degrees):
    deg_floored = mt.floor(degrees)
    minutes = (degrees - deg_floored) * 60
    min_floored = mt.floor(minutes)
    seconds = round((minutes - min_floored) * 60, 5)
    return [deg_floored, min_floored, seconds]


class GRS80:
    a_axis = 6378137
    e2 = 0.00669438002290
    f = 1 / 298.25722210
    b_axis = a_axis - a_axis * f
    e2p = round((a_axis ** 2 - b_axis ** 2) / b_axis ** 2, 13)

    e4 = e2 ** 2
    e6 = e2 ** 3
    A0 = 1 - e2 / 4 - 3 * e4 / 64 - 5 * e6 / 256
    A2 = 3 / 8 * (e2 + e4 / 4 + 15 * e6 / 128)
    A4 = 15 / 256 * (e4 + 3 * e6 / 4)
    A6 = 35 * e6 / 3072


def get_data(number, group=1):
    try:
        if group == 1:
            x = 3648420.000
            y = 1474120.000
            z = 5003100.000 + int(number) * 20
            s = 450 + number
            zenith = 73.0
            azimuth = 30.0 + number
            return [x, y, z, s, zenith, azimuth]
        else:
            return 'Podano nieprawidłowy numer grupy'
    except TypeError:
        return 'Podany numer grupy nie jest wartością liczbową'


def n_radius(fi, a_axis=GRS80.a_axis, e2=GRS80.e2):
    nominator = a_axis
    denominator = mt.sqrt(1 - e2 * (mt.sin(fi)) ** 2)
    return nominator / denominator


def m_radius(fi, a_axis=GRS80.a_axis, e2=GRS80.e2):
    nominator = a_axis * (1 - e2)
    denominator = (mt.sqrt(1 - e2 * (mt.sin(fi)) ** 2)) ** 3
    return nominator / denominator


def hirvonen(x, y, z, ellipsoid):
    e2 = ellipsoid.e2
    radius = mt.sqrt(x ** 2 + y ** 2)
    fi = mt.atan(z / radius * (1 - e2) ** (-1))
    n = n_radius(fi)
    h = radius / mt.cos(fi) - n
    eps = 1
    while eps > (0.00001 * mt.pi / (180 * 3600)):
        fi0 = fi
        fi = mt.atan((z / radius) / (1 - e2 * (n / (n + h))))
        n = n_radius(fi)
        h = radius / mt.cos(fi) - n
        eps = abs(fi0 - fi)
    lbd = mt.atan2(y, x) if mt.atan2(y, x) >= 0 else mt.atan2(y, x) + 2 * mt.pi
    return [fi, lbd, h]


def fi_lbd_h_to_xyz(fi, lbd, h, ellipsoid):
    e2 = ellipsoid.e2
    n = n_radius(fi)
    x = (n + h) * mt.cos(fi) * mt.cos(lbd)
    y = (n + h) * mt.cos(fi) * mt.sin(lbd)
    z = (n * (1 - e2) + h) * mt.sin(fi)
    return [x, y, z]


def neu_vector(azimuth, zenith, distance):
    north = distance * mt.sin(zenith) * mt.cos(azimuth)
    east = distance * mt.sin(zenith) * mt.sin(azimuth)
    up = distance * mt.cos(zenith)
    return [north, east, up]


def neu_to_xyz(fi, lbd):
    r1 = [-mt.sin(fi) * mt.cos(lbd), -mt.sin(lbd), mt.cos(fi) * mt.cos(lbd)]
    r2 = [-mt.sin(fi) * mt.sin(lbd), mt.cos(lbd), mt.cos(fi) * mt.sin(lbd)]
    r3 = [mt.cos(fi), 0, mt.sin(fi)]
    return np.array([r1, r2, r3])


def kivioj_method(fi_p, lbd_p, azim_ell, dist_ell, lines_number):
    ds = dist_ell / lines_number
    if ds > 1500:
        return 'Odcinki przekraczają 1500m, podać inną liczbę odcinków'
    else:
        fi = fi_p
        lbd = lbd_p
        az = azim_ell
        i = 1
        while i <= lines_number:
            # First step - first increment
            n = n_radius(fi)
            m = m_radius(fi)
            d_fi = ds * mt.cos(az) / m
            d_az = ds * mt.tan(fi) * mt.sin(az) / n
            # Second step - Fi and Az at in the middle of the line segment
            fi_m = fi + d_fi / 2
            az_m = az + d_az / 2
            # Third step - second increment based on the middle line values of Fi and Azs
            n_m = n_radius(fi_m)
            m_m = m_radius(fi_m)
            fi += ds * mt.cos(az_m) / m_m
            lbd += ds * mt.sin(az_m) / n_m / mt.cos(fi_m)
            az += ds * mt.sin(az_m) * mt.tan(fi_m) / n_m
            i += 1
        fi_k = fi
        lbd_k = lbd
        az_k = az + mt.pi if az <= mt.pi else az - mt.pi
        return [fi_k, lbd_k, az_k]


def vincenty_algorithm(fi_1, lbd_1, fi_2, lbd_2, b_axis=GRS80.b_axis, f=GRS80.f, e2p=GRS80.e2p):
    cos_alpha2, cos_lbd, sin_lbd, sig, cos_sig, cos_2sigm, sin_sig = [0, 0, 0, 0, 0, 0, 0]

    u1 = mt.atan(mt.tan(fi_1) * (1 - f))
    cos_u1 = mt.cos(u1)
    sin_u1 = mt.sin(u1)

    u2 = mt.atan(mt.tan(fi_2) * (1 - f))
    cos_u2 = mt.cos(u2)
    sin_u2 = mt.sin(u2)
    # First approximation of Lbd = L
    lambda_difference = lbd_2 - lbd_1
    eps = 1
    lbd = lambda_difference

    while abs(eps) > 10 ** (-12):
        lbd0 = lbd
        sin_lbd = mt.sin(lbd)
        cos_lbd = mt.cos(lbd)
        sin_sig = mt.sqrt((cos_u2 * sin_lbd) ** 2 + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lbd) ** 2)
        cos_sig = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lbd
        sig = mt.asin(sin_sig)
        sin_alpha = cos_u1 * cos_u2 * sin_lbd / sin_sig
        cos_alpha2 = 1 - sin_alpha ** 2
        cos_2sigm = cos_sig - 2 * sin_u1 * sin_u2 / cos_alpha2 if sin_u1 != 0 and sin_u2 != 0 else cos_sig
        c_component = f / 16 * cos_alpha2 * (4 + f * (4 - 3 * cos_alpha2))
        lbd = lambda_difference + (1 - c_component) * f * sin_alpha * (
                sig + c_component * sin_sig * (cos_2sigm + c_component * cos_sig * (-1 + 2 * cos_2sigm ** 2)))
        eps = lbd - lbd0

    u2 = cos_alpha2 * e2p
    a_component = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    b_component = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    delta_sig = b_component * sin_sig * (cos_2sigm + b_component / 4 * (
            cos_sig * (-1 + 2 * cos_2sigm ** 2) - b_component / 6 * cos_2sigm * (-3 + 4 * cos_2sigm ** 2)))
    s = b_axis * a_component * (sig - delta_sig)
    az_12 = mt.atan2(cos_u2 * sin_lbd, cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lbd)
    az_21 = mt.atan2(cos_u1 * sin_lbd, -sin_u1 * cos_u2 + cos_u1 * sin_u2 * cos_lbd)

    return [az_12, az_21, s]


def gk_direct(fi, lbd, lbd0, ellipsoid):
    a_axis = ellipsoid.a_axis
    e2p = ellipsoid.e2p

    t = mt.tan(fi)
    eta2 = e2p * mt.cos(fi) ** 2
    lambda_difference = lbd - lbd0
    n = n_radius(fi)

    a0 = ellipsoid.A0
    a2 = ellipsoid.A2
    a4 = ellipsoid.A4
    a6 = ellipsoid.A6

    sig = a_axis * (a0 * fi - a2 * mt.sin(2 * fi) + a4 * mt.sin(4 * fi) - a6 * mt.sin(6 * fi))
    x1 = lambda_difference ** 2 / 12 * mt.cos(fi) ** 2 * (5 - t ** 2 + 9 * eta2 + 4 * eta2 ** 2)
    x2 = lambda_difference ** 4 / 360 * mt.cos(fi) ** 4 * (61 - 58 * t ** 2 + t ** 4 + 270 * eta2 - 330 * eta2 * t ** 2)
    x = sig + lambda_difference ** 2 / 2 * n * mt.sin(fi) * mt.cos(fi) * (1 + x1 + x2)
    y1 = lambda_difference ** 2 / 6 * mt.cos(fi) ** 2 * (1 - t ** 2 + eta2)
    y2 = lambda_difference ** 4 / 120 * mt.cos(fi) ** 4 * (5 - 18 * t ** 2 + t ** 4 + 14 * eta2 - 58 * eta2 * t ** 2)
    y = lambda_difference * n * mt.cos(fi) * (1 + y1 + y2)
    return [x, y]


def gk_back(x_gk, y_gk, lbd0, ellipsoid):
    a_axis = ellipsoid.a_axis
    e2p = ellipsoid.e2p

    a0 = ellipsoid.A0
    a2 = ellipsoid.A2
    a4 = ellipsoid.A4
    a6 = ellipsoid.A6

    sig = x_gk
    fi1 = sig / (a_axis * a0)
    eps = 1
    while abs(eps) > 10 ** (-12):
        fi0 = fi1
        fi1 = (sig / a_axis + a2 * mt.sin(2 * fi0) - a4 * mt.sin(4 * fi0) + a6 * mt.sin(6 * fi0)) / a0
        eps = fi1 - fi0

    t = mt.tan(fi1)
    eta2 = e2p * mt.cos(fi1) ** 2
    n = n_radius(fi1)
    m = m_radius(fi1)

    f1 = -y_gk ** 2 / 12 / n ** 2 * (5 + 3 * t ** 2 + eta2 - 9 * eta2 * t ** 2)
    f2 = y_gk ** 4 / 360 / n ** 4 * (61 + 90 * t ** 2 + 45 * t ** 4)
    fi = fi1 - y_gk ** 2 * t / 2 / m / n * (1 + f1 + f2)
    l1 = -y_gk ** 2 / 6 / n ** 2 * (1 + 2 * t ** 2 + eta2)
    l2 = y_gk ** 4 / 120 / n ** 4 * (5 + 28 * t ** 2 + 24 * t ** 4 + 6 * eta2 + 8 * eta2 * t ** 2)
    lbd = lbd0 + y_gk / n / mt.cos(fi1) * (1 + l1 + l2)

    return [fi, lbd]


def to_datum_2000(x_gk, y_gk, zone):
    if zone in [5, 6, 7, 8]:
        m0 = 0.999923
        x2000 = x_gk * m0
        y2000 = y_gk * m0 + zone * 10 ** 6 + 500000
        return [x2000, y2000]
    else:
        return 'Zły numer strefy'


def from_datum_2000(x2000, y2000, zone):
    m0 = 0.999923
    x_gk = x2000 / m0
    y_gk = (y2000 - zone * 10 ** 6 - 500000) / m0
    return [x_gk, y_gk]


def to_datum_1992(x_gk, y_gk):
    m0 = 0.9993
    x1992 = x_gk * m0 - 5300000
    y1992 = y_gk * m0 + 500000
    return [x1992, y1992]


def from_datum_1992(x1992, y1992):
    m0 = 0.9993
    x_gk = (x1992 + 5300000) / m0
    y_gk = (y1992 - 500000) / m0
    return [x_gk, y_gk]


def convergence(fi, lbd, lbd0, e2p=GRS80.e2p):
    t = mt.tan(fi)
    eta2 = e2p * mt.cos(fi) ** 2
    lambda_difference = lbd - lbd0
    conv = lambda_difference * mt.sin(fi) * (1 + lambda_difference ** 2 / 3 * mt.cos(fi) ** 2 * (
            1 + 3 * eta2 + 2 * eta2 ** 2) + lambda_difference ** 4 / 15 * mt.cos(fi) ** 4 * (2 - t ** 2))
    return conv


def direction_reduction(x_1, y_1, x_2, y_2, lbd0, ellipsoid):
    xm, ym = middle_point_coordinates(x_1, x_2, y_1, y_2)

    fi_lbd = gk_back(xm, ym, lbd0, ellipsoid)
    fi = fi_lbd[0] * mt.pi / 180
    m = m_radius(fi)
    n = n_radius(fi)
    r_m = mt.sqrt(m * n)

    reduction_12 = (x_2 - x_1) * (2 * y_1 + y_1) / (6 * r_m ** 2)
    reduction_21 = (x_1 - x_2) * (y_1 + 2 * y_2) / (6 * r_m ** 2)
    return [reduction_12, reduction_21]


def distance_reduction(x_1, y_1, x_2, y_2, lbd0, ellipsoid):
    x_m = (x_1 + x_2) / 2
    y_m = (y_1 - y_2) / 2

    fi_lbd = gk_back(x_m, y_m, lbd0, ellipsoid)
    fi = fi_lbd[0] * mt.pi / 180
    m = m_radius(fi)
    n = n_radius(fi)
    r_m = mt.sqrt(m * n)
    return (y_1 ** 2 + y_1 * y_2 + y_2 ** 2) / (6 * r_m ** 2)


def transformation(coordinates_to_transform, m=1 + 0.8407728 * 10 ** -6, ex=-1.7388854 * 10 ** -6,
                   ey=-0.256146 * 10 ** -6,
                   ez=4.0896031 * 10 ** -6, t_x=-33.4297, t_y=146.5746, t_z=76.2865):
    rotation_matrix = np.array([[m, ez, -ey], [-ez, m, ex], [ey, -ex, m]])
    translation_vector = np.array([[t_x], [t_y], [t_z]])
    return np.matmul(rotation_matrix, coordinates_to_transform) + translation_vector


if __name__ == '__main__':
    c = mt.pi / 180
    FLA = kivioj_method(0 * c, 21 * c, 45 * c, 28000, 28)
    print(FLA)
    # print(degrees_to_dms(FLA[0] / c))
    # print(degrees_to_dms(FLA[1] / c))
    # print(degrees_to_dms(FLA[2] / c))

    Reverse = vincenty_algorithm(0 * c, 21 * c, 0, 22*c)
    print(degrees_to_dms(Reverse[0] / c))
    print(degrees_to_dms(Reverse[1] / c))
    print(Reverse[2])

    # XY = gk_direct(52 * c, 22 * c, 21 * c, GRS80)
    # print(XY)
    #
    # FIL = gk_back(XY[0], XY[1], 21 * c, GRS80)
    # print(degrees_to_dms(FIL[0] / c))
    # print(degrees_to_dms(FIL[1] / c))
    #
    # coordinates = np.array([[1], [2], [1]])
    # print(transformation(coordinates))

    # print(get_data(9))
    # print(n_radius(52*mt.pi/180))
    # print(m_radius(52*mt.pi/180))
    # data = get_data(5)
    # FLH = hirvonen(data[0], data[1], data[2], GRS80)
    # print(degrees_to_dms(FLH[0]*180/mt.pi))
    # print(degrees_to_dms(FLH[1]*180/mt.pi))
    # print(FLH[2])
    # print(FLH[0])
    # print(FLH[1])
    #
    # print(data[5], data[4], data[3])
    # print(neu_vector(data[5], data[4], data[3]))
    # print(neu_to_xyz(FLH[0], FLH[1]))
