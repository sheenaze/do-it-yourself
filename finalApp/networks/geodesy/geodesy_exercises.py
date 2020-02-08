from networks.geodesy.algorithms import *

class Excercise1:
    def __init__(self, data):
        self.XA = data[0]
        self.YA = data[1]
        self.ZA = data[2]
        self.distance = data[3]
        self.zenith = data[4]
        self.azimuth = data[5]

    def lat_long_H_A(self):
        return hirvonen(self.XA, self.YA, self.ZA)

    def local_neu(self):
        return np.array(neu_vector(self.azimuth, self.zenith, self.distance))

    def DeltaX(self):
        fi = self.lat_long_H_A()[0]
        lbd = self.lat_long_H_A()[1]
        D = neu2XYZ(fi, lbd)
        return np.matmul(D, self.local_neu())

    def XYZ_B(self):
        return np.array([self.XA, self.YA, self.ZA]) + self.DeltaX()

    def lat_long_H_B(self):
        XB = self.XYZ_B()[0]
        YB = self.XYZ_B()[1]
        ZB = self.XYZ_B()[2]
        return hirvonen(XB, YB, ZB)


# student = Excercise1(getData(5))
# print(student.lat_long_H_A())
# print(student.local_neu())
# print(student.DeltaX())
# print(student.XYZ_B())
# FLH = student.lat_long_H_B()
# print(degreesToDMS(FLH[0]/mt.pi*180))
# print(degreesToDMS(FLH[1]/mt.pi*180))
# print(FLH[2])
