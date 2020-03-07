from networks.geodesy.algorithms import *


class Excercise1:
    def __init__(self, data):
        self.XA = data[0]
        self.YA = data[1]
        self.ZA = data[2]
        self.distance = data[3]
        self.zenith = data[4] * mt.pi / 180
        self.azimuth = data[5] * mt.pi / 180

    def lat_long_height_point_1(self):
        return hirvonen(self.XA, self.YA, self.ZA)

    def local_neu(self):
        return np.array(neu_vector(self.azimuth, self.zenith, self.distance))

    def delta_xyz(self):
        fi = self.lat_long_height_point_1()[0]
        lbd = self.lat_long_height_point_1()[1]
        transformation_matrix = neu_to_xyz(fi, lbd)
        return np.matmul(transformation_matrix, self.local_neu())

    def xyz_point_2(self):
        return np.array([self.XA, self.YA, self.ZA]) + self.delta_xyz()

    def lat_long_height_point_2(self):
        xb = self.xyz_point_2()[0]
        yb = self.xyz_point_2()[1]
        zb = self.xyz_point_2()[2]
        return hirvonen(xb, yb, zb)

# student = Excercise1(getData(5))
# print(student.lat_long_H_A())
# print(student.local_neu())
# print(student.DeltaX())
# print(student.XYZ_B())
# FLH = student.lat_long_H_B()
# print(degreesToDMS(FLH[0]/mt.pi*180))
# print(degreesToDMS(FLH[1]/mt.pi*180))
# print(FLH[2])
