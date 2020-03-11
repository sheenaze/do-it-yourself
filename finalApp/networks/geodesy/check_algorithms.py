from networks.geodesy.algorithms import *
import math


def diff_level(angle_diff):
    eps_sec = 1 / 3600 / 180 * math.pi  # one second in rad
    eps_min = 1 / 60 / 180 * math.pi  # one minute in rad
    eps_deg = 1 / 180 * math.pi  # one deg in rad

    message = ''
    if angle_diff <= eps_sec:
        message += 'Różnica nie przekracza jednej sekundy. \n'
    elif eps_sec < angle_diff < eps_min:
        message += 'Różnica jest nie przekracza jednej minuty. \n'
    elif eps_min < angle_diff < eps_deg:
        message += 'Różnica jest nie przekracza jednego stopnia. \n'
    else:
        message += 'Różnica jest większa niż jeden stopień. \n'
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
        message.append(f'Podana szerokość jest niepoprawna. {diff_level(dif_fi)}')

    if dif_lbd <= eps:
        message.append('Podana długość jest poprawna.')
    else:
        message.append(f'Podana długość jest niepoprawna. {diff_level(dif_lbd)}')

    if dif_h <= 0.001:
        message.append('Podana wysokość jest poprawna.')
    elif 0.01 >= dif_h > 0.001:
        message.append('Podana wysokość nie jest poprawna. Różnica nie przekracza 1 cm.')
    elif 0.1 >= dif_h > 0.01:
        message.append('Podana wysokość nie jest poprawna. Różnica nie przekracza 10 cm.')
    elif 1 >= dif_h > 0.1:
        message.append('Podana wysokość nie jest poprawna. Różnica nie przekracza 1 m.')
    else:
        message.append('Podana wysokość nie jest poprawna. Różnica przekracza 1 m.')

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
