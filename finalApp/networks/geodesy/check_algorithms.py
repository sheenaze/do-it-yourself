from networks.geodesy.algorithms import *
import math


def diff_level_lat_lon(angle_diff):
    eps_sec = 1 / 3600 / 180 * math.pi  # one second in rad
    eps_min = 1 / 60 / 180 * math.pi  # one minute in rad
    eps_deg = 1 / 180 * math.pi  # one deg in rad

    if angle_diff <= eps_sec:
        message = 'Różnica nie przekracza jednej sekundy.'
    elif eps_sec < angle_diff < eps_min:
        message = 'Różnica jest nie przekracza jednej minuty. '
    elif eps_min < angle_diff < eps_deg:
        message = 'Różnica jest nie przekracza jednego stopnia. '
    else:
        message = 'Różnica jest większa niż jeden stopień.'
    return message


def diff_level_xyzh(cooridnate_difference, coordinate_name):
    if cooridnate_difference == 0:
        message = f'Współrzędna {coordinate_name} jest w porządku.'
    elif cooridnate_difference <= 1:
        message = f'Współrzędna {coordinate_name} niepoprawna. Różnica nie przekracza 1 m.'
    else:
        diff = round(cooridnate_difference)
        message = f'Współrzędna {coordinate_name} niepoprawna. Bezwględna różnica wynosi ok. {round(diff, 0)} m.'

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

    message = []
    message.append(diff_level_xyzh(dif_x, 'X'))
    message.append(diff_level_xyzh(dif_y, 'Y'))
    message.append(diff_level_xyzh(dif_z, 'Z'))

    return message


if __name__ == '__main__':
    X = 3648420
    Y = 1474120
    Z = 5003200

    fi, lbd, h = hirvonen(X, Y, Z, GRS80)
    fi = fi * 180 / math.pi
    lbd = lbd * 180 / math.pi
    h = h

    print(degrees_to_dms(fi))
    print(degrees_to_dms(lbd))
    print(h)

    print(fi, lbd, h)
    info = check_hirvonen(X, Y, Z, fi, lbd, h, GRS80)
    print(info)

    fi_new = deg2rad(52)
    lbd_new = deg2rad(21)
    H_new = 100
    x_new, y_new, z_new = fi_lbd_h_to_xyz(fi_new, lbd_new, H_new, GRS80)

    print(x_new, y_new, z_new)
