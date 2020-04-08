from networks.geodesy.algorithms import *
import math


def diff_level_lat_lon(angle_diff):
    eps_sec = 1 / 3600 / 180 * math.pi  # one second in rad
    eps_min = 1 / 60 / 180 * math.pi  # one minute in rad
    eps_deg = 1 / 180 * math.pi  # one deg in rad

    if angle_diff <= eps_sec:
        message = 'Różnica nie przekracza jednej sekundy.'
    elif eps_sec < angle_diff <= eps_min:
        message = 'Różnica jest nie przekracza jednej minuty. '
    elif eps_min < angle_diff <= eps_deg:
        message = 'Różnica jest nie przekracza jednego stopnia. '
    else:
        message = 'Różnica jest większa niż jeden stopień.'
    return message


def diff_level_xyzh(cooridnate_difference, coordinate_name):
    if cooridnate_difference == 0:
        message = f'Wartość {coordinate_name} jest w porządku.'
    elif cooridnate_difference <= 0.001:
        message = f'Wartość {coordinate_name} niepoprawna. Różnica nie przekracza 1 mm.'
    else:
        diff = round(cooridnate_difference)
        message = f'Wartość {coordinate_name} niepoprawna. Bezwględna różnica wynosi ok. {round(diff, 0)} m.'

    return message


def check_hirvonen(x, y, z, fi, lbd, h, ellipsoid):
    """
    :param x: x coordinate in xyz datum
    :param y: y coordinate in xyz datum
    :param z: z coordinate in xyz datum
    :param fi: latitude
    :param lbd: longitude
    :param h: height
    :param ellipsoid: ellipsoid with all parameters
    :return: str with information if the computation is correct
    """
    fi_rad = deg2rad(fi)
    lbd_rad = deg2rad(lbd)
    fi_check, lbd_check, h_check = hirvonen(x, y, z, ellipsoid)
    eps = 0.0001 / 3600 / 180 * math.pi  # this is a level of computation accuracy

    dif_fi = abs(fi_rad - fi_check)
    dif_lbd = abs(lbd_rad - lbd_check)
    dif_h = abs(round(h, 3) - round(h_check, 3))

    message = []
    if dif_fi <= eps:
        message.append('Podana szerokość jest poprawna.')
    else:
        message.append(f'Podana szerokość jest niepoprawna. {diff_level_lat_lon(dif_fi)}')

    if dif_lbd <= eps:
        message.append('Podana długość jest poprawna.')
    else:
        message.append(f'Podana długość jest niepoprawna. {diff_level_lat_lon(dif_lbd)}')

    if dif_h <= 0.001:
        message.append('Podana wysokość jest poprawna.')
    else:
        message.append(diff_level_xyzh(dif_h, 'H'))

    return message


def check_fi_lbd_h_to_xyz(fi, lbd, h, x, y, z, ellipsoid):
    fi_rad = deg2rad(fi)
    lbd_rad = deg2rad(lbd)

    x_check, y_check, z_check = fi_lbd_h_to_xyz(fi_rad, lbd_rad, h, ellipsoid)
    dif_x = abs(round(x_check, 3) - round(x, 3))
    dif_y = abs(round(y_check, 3) - round(y, 3))
    dif_z = abs(round(z_check, 3) - round(z, 3))

    message = [diff_level_xyzh(dif_x, 'X'), diff_level_xyzh(dif_y, 'Y'), diff_level_xyzh(dif_z, 'Z')]

    return message


def check_neu_xyz(dX, dY, dZ, north, east, up, fi, lbd, Neu2XYZ=False):
    fi_rad = deg2rad(fi)
    lbd_rad = deg2rad(lbd)
    neu = np.array([north, east, up]).reshape((3, 1))
    dxyz = np.array([dX, dY, dZ]).reshape((3, 1))
    message = []
    if Neu2XYZ:
        D = neu_to_xyz(fi_rad, lbd_rad)
        dxyz_test = np.round(np.dot(D, neu), 3)
        diff = np.round(np.abs(dxyz_test - dxyz), 3)
        print(diff[0, 0], diff[1, 0], diff[2, 0])
        message.append(diff_level_xyzh(diff[0, 0], 'dX'))
        message.append(diff_level_xyzh(diff[1, 0], 'dY'))
        message.append(diff_level_xyzh(diff[2, 0], 'dZ'))

    else:
        D = np.transpose(neu_to_xyz(fi_rad, lbd_rad))
        neu_test = np.round(np.dot(D, dxyz), 3)

        diff = np.round(np.abs(neu_test - neu), 3)
        print(diff[0, 0], diff[1, 0], diff[2, 0])
        message.append(diff_level_xyzh(diff[0, 0], 'n'))
        message.append(diff_level_xyzh(diff[1, 0], 'e'))
        message.append(diff_level_xyzh(diff[2, 0], 'u'))

    return message


def check_kivioja(fiA, lbdA, AzAB, s, n, fiB, lbdB, AzBA):
    if type(kivioja_algorithm(deg2rad(fiA), deg2rad(lbdA), deg2rad(AzAB), s, n)) == str:
        message = [kivioja_algorithm(deg2rad(fiA), deg2rad(lbdA), deg2rad(AzAB), s, n)]
    else:
        fiB_test, lbdB_test, AzBA_test = kivioja_algorithm(deg2rad(fiA), deg2rad(lbdA), deg2rad(AzAB), s, n)
        fiB_rad = deg2rad(fiB)
        lbdB_rad = deg2rad(lbdB)
        AzBA_rad = deg2rad(AzBA)

        diff_fi = abs(fiB_rad - fiB_test)
        diff_lbd = abs(lbdB_rad - lbdB_test)
        diff_Az = abs(AzBA_rad - AzBA_test)
        eps_Az = 0.001 / 3600 / 180 * math.pi
        eps = 0.0001 / 3600 / 180 * math.pi

        message = []
        if diff_fi <= eps:
            message.append('Podana szerokość jest poprawna.')
        else:
            message.append(f'Podana szerokość jest niepoprawna. {diff_level_lat_lon(diff_fi)}')

        if diff_lbd <= eps:
            message.append('Podana długość jest poprawna.')
        else:
            message.append(f'Podana długość jest niepoprawna. {diff_level_lat_lon(diff_lbd)}')

        if diff_Az <= eps_Az:
            message.append('Podany azymut odwrotny jest poprawny.')
        else:
            message.append(f'Podany azymut odwrotny jest t niepoprawny. {diff_level_lat_lon(diff_Az)}')

    return message


def check_vincenty(fiA, lbdA, fiB, lbdB, AzAB, AzBA, s):
    AzAB_test, AzBA_test, s_test = vincenty_algorithm(deg2rad(fiA), deg2rad(lbdA), deg2rad(fiB), deg2rad(lbdB))
    AzAB_rad = deg2rad(AzAB)
    AzBA_rad = deg2rad(AzBA)
    diff_AzAB = abs(AzAB_rad - AzAB_test)
    diff_AzBA = abs(AzBA_rad - AzBA_test)
    diff_s = abs(s - s_test)
    eps_Az = 0.01 / 3600 / 180 * math.pi
    message = []

    if diff_AzAB <= eps_Az:
        message.append('Podany azymut AB jest poprawny.')
    else:
        message.append(f'Podany azymut AB jest niepoprawny. {diff_level_lat_lon(diff_AzAB)}')

    if diff_AzBA <= eps_Az:
        message.append('Podany azymut BA jest poprawny.')
    else:
        message.append(f'Podany azymut BA jest niepoprawny. {diff_level_lat_lon(diff_AzBA)}')

    if diff_s <= 0.001:
        message.append('Podana odległość jest poprawna.')
    else:
        message.append(diff_level_xyzh(diff_s, 's'))

    return message


def check_gauss_kruger(fi, lbd, lbd0, XGK, YGK, direct=True):
    if lbd0 != 19 and abs(lbd - lbd0) >= 1.5:
        message = ['Błędny południk osiowy!']
    else:
        fi_rad = deg2rad(fi)
        lbd_rad = deg2rad(lbd)
        lbd0_rad = deg2rad(lbd0)
        message = []
        if direct:
            X_test, Y_test = gk_direct(fi_rad, lbd_rad, lbd0_rad)
            X_diff = abs(round(X_test, 3) - round(XGK, 3))
            Y_diff = abs(round(Y_test, 3) - round(YGK, 3))
            message.append(diff_level_xyzh(X_diff, 'XGK'))
            message.append(diff_level_xyzh(Y_diff, 'YGK'))
        else:
            fi_test, lbd_test = gk_back(round(XGK, 3), round(YGK, 3), lbd0_rad)
            diff_fi = abs(fi_rad - fi_test)
            diff_lbd = abs(lbd_rad - lbd_test)
            eps = 0.0001 * mt.pi / 180
            if diff_fi <= eps:
                message.append('Podana szerokość jest poprawna.')
            else:
                message.append(f'Podana szerokość jest niepoprawna. {diff_level_lat_lon(diff_fi)}')

            if diff_lbd <= eps:
                message.append('Podana szerokość jest poprawna.')
            else:
                message.append(f'Podana szerokość jest niepoprawna. {diff_level_lat_lon(diff_lbd)}')

    return message


if __name__ == '__main__':
    X = 3648420
    Y = 1474120
    Z = 5003200

    fi_rad, lbd_rad, h = hirvonen(X, Y, Z, GRS80)
    fi = fi_rad * 180 / math.pi
    lbd = lbd_rad * 180 / math.pi
    h = h

    print(f'Fi: {degrees_to_dms(fi)}')
    print(f"Lbd: {degrees_to_dms(lbd)}")
    print(h)

    print(fi, lbd, h)
    info = check_hirvonen(X, Y, Z, fi, lbd, h, GRS80)
    print(info)

    fi_new = deg2rad(52)
    lbd_new = deg2rad(21)
    H_new = 100
    x_new, y_new, z_new = fi_lbd_h_to_xyz(fi_new, lbd_new, H_new, GRS80)

    print(x_new, y_new, z_new)

    n, e, u = neu_vector(deg2rad(35), deg2rad(73), 455)
    neu = np.array([n, e, u])
    D = neu_to_xyz(fi_rad, lbd_rad)
    dx, dy, dz = np.dot(D, neu.reshape((3, 1)))

    print(f'NEU: {n, e, u}')
    print(f'dXYZ: {dx, dy, dz}')
    print(check_neu_xyz(dx, dy, dz, n, e, u, fi, lbd, True))

    fiB, lbdB, AzBA = kivioja_algorithm(fi_rad, lbd_rad, deg2rad(45), 28000, 28)

    AzAB_test, AzBA_test, s_test = vincenty_algorithm(deg2rad(fi), deg2rad(lbd), fiB, lbdB)

    print(f'AzAB: {degrees_to_dms(AzAB_test * 180 / mt.pi)}')
    print(f"AzBA: {degrees_to_dms(AzBA_test * 180 / mt.pi)}")
    print(f"s: {s_test}")

    fiB = fiB * 180 / math.pi
    lbdB = lbdB * 180 / math.pi
    AzBA = AzBA * 180 / math.pi

    print(f'Fi: {degrees_to_dms(fiB)}')
    print(f"Lbd: {degrees_to_dms(lbdB)}")
    print(f"AzBA: {degrees_to_dms(AzBA)}")

    text = check_vincenty(fi, lbd, fiB, lbdB, 45, AzBA, 28000)
    print(text)

    c = mt.pi/180
    X, Y = gk_direct(52 * c, 22 * c, 21 * c, GRS80)
    print(check_gauss_kruger(52, 22, 21, X, Y, direct=True))
    print(check_gauss_kruger(52+0.9/3600, 22+1/3600, 21, X, Y, direct=False))

