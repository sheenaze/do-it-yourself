import numpy as np

data = np.array([[1,	1,	2,	16.925,	0.007],
                 [2,	1,	3,	10.047,	0.004],
                 [3,	1,	5,	8.537, 0.005],
                 [4,	2,	4,	-4.678,	0.006],
                 [5,	2,	5,	-8.383, 0.004],
                 [6,	2,	6,	-1.215,	0.006],
                 [7,	3,	6,	5.654,	0.005],
                 [8,	3,	7,	0.750,	0.006],
                 [9,	4,	5,	-3.708,	0.004],
                 [10,	4,	6,	3.462,	0.004],
                 [11,	4,	7,	-1.441,	0.007],
                 [12,	2,	101, -2.791, 0.003],
                 [13,	5,	102	,-5.987, 0.008],
                 [14,	6,	103	,-8.318, 0.005]])
# data = np.array([[1,	2,	16.925,	0.007],
#                  [1,	3,	10.047,	0.004],
#                  [1,	5,	8.537, 0.005],
#                  [2,	4,	-4.678,	0.006],
#                  [2,	5,	-8.383,	0.004],
#                  [2,	6,	-1.215,	0.006],
#                  [3,	6,	5.654,	0.005],
#                  [3,	7,	0.750,	0.006],
#                  [4,	5,	-3.708,	0.004],
#                  [4,	6,	3.462,	0.004],
#                  [4,	7,	-1.441,	0.007],
#                  [2,	101, -2.791, 0.003],
#                  [5,	102	,-5.987, 0.008],
#                  [6,	103	,-8.318, 0.005]])

consts = np.array(
[[101,221.6500],
[102,210.0821],
[103,214.9079]],
)



class LevelingAdjustment:
    def __init__(self, data, const_points, points=None):
        self.const_points = const_points
        self.points = points
        self.data = data


    def points_list(self):
        all_points = [int(num) for num in data[:, 1:2]] +[int(num) for num in data[:, 2:3]]
        points_list = []
        for i in all_points:
            if i not in points_list:
                points_list.append(i)
        points_list.sort()
        return points_list

    def points_to_find(self):
        all_points = [int(num) for num in data[:, 1:2]] +[int(num) for num in data[:, 2:3]]
        points_list = []
        consts = self.const_points
        for i in all_points:
            if i not in points_list and i not in consts[:,0]:
                points_list.append(i)
        points_list.sort()
        return points_list


    def points_height(self):
        if self.points is not None:
            points = self.points
            return points
        else:
            num_points = len(self.points_list())
            points = self.const_points
            data = self.data[:,1:]
            while len(points) < num_points:
                for row in data:
                    pp = row[0]
                    pk = row[1]
                    dh = row[2]
                    if pp in points[:,0] and pk not in points[:,0]:
                        ind =np.where(points[:,0] == pp)[0][0] #(points[:,0] == pp).tolist().index(True)
                        H = points[ind,1]+dh
                        points = np.append(points, [[pk, H]], axis = 0)
                    elif pk in points[:,0] and pp not in points[:,0]:
                        ind =np.where(points[:,0] == pk)[0][0]#(points[:,0] == pk).tolist().index(True)
                        H = points[ind,1]-dh
                        points = np.append(points, [[pp, H]], axis = 0)
            points = points[points[:,0].argsort()]
            return points[:-3,:]

    def A_matrix(self):
        points = self.points_to_find()
        num_cols= len(points)
        num_rows = len(self.data)
        matrix = np.zeros((num_rows, num_cols))

        for i in range(0,num_rows):
            for j in range(0, num_cols):
                if points[j] == self.data[i, 1]:
                    matrix[i, j] = -1
                elif points[j] == self.data[i, 2]:
                    matrix[i, j] = 1

        return matrix


    def P_matrix(self):
        variances = [1/(sig)**2 for sig in self.data[:,-1]]
        return np.diag(variances)


    def L_vector(self):
        if self.points is None:
            points = np.append(self.points_height(), self.const_points, axis=0)
        else:
            points = np.append(self.points, self.const_points, axis = 0)
        vector =[]
        for row in self.data:
            pp = np.where(points[:,0] == row[1])[0][0]
            pk = np.where(points[:,0] == row[2])[0][0]
            dh = points[pk, 1] - points[pp,1]
            l = dh - row[3]
            vector.append([l])
        return np.array(vector)

    def ATPA_matrix(self):
        A = self.A_matrix()
        AT =  np.transpose(A)
        P = self.P_matrix()
        return np.matmul(np.matmul(AT, P),A)

    def ATPL_matrix(self):
        L = self.L_vector()
        AT = np.transpose(self.A_matrix())
        P = self.P_matrix()
        return np.matmul(np.matmul(AT, P),L)

    def x_vector(self):
        ATPA_inv = np.linalg.inv(self.ATPA_matrix())
        ATPL = self.ATPL_matrix()
        return -np.matmul(ATPA_inv, ATPL)

    def V_vector(self):
        A = self.A_matrix()
        x = self.x_vector()
        L = self.L_vector()
        return np.add(np.matmul(A,x),L)

    def HW_vector(self):
        points = self.points_height()
        dH = self.x_vector()
        points[:,1] = np.add(points[:,1], dH.reshape((len(dH),)))
        return points

    def obsW_matrix(self):
        V = self.V_vector()
        obs = self.data[:,1:4]
        obs[:,-1] = np.add(obs[:,-1],V.reshape((len(V),)))
        return obs

    def sigma0(self):
        V = self.V_vector()
        VT = np.transpose(V)
        P = self.P_matrix()
        n = len(self.data)
        r = len(self.points_to_find())
        VTPV = np.matmul(np.matmul(VT, P), V)
        sigma = (VTPV/(n-r))**(1/2)
        return sigma

    def Cx_matrix(self):
        sigma2 = self.sigma0()**2
        ATPA_inv = np.linalg.inv(self.ATPA_matrix())
        C =sigma2*ATPA_inv
        return C

    def mx_vector(self):
        C = self.Cx_matrix()
        mx = np.sqrt(np.diag(C))
        return mx

    def CobsW_matrix(self):
        A = self.A_matrix()
        AT = np.transpose(A)
        Cx = self.Cx_matrix()
        C = np.matmul(np.matmul(A,Cx),AT)
        return C


    def CV_matrix(self):
        P_inv = np.linalg.inv(self.P_matrix())
        CobsW = self.CobsW_matrix()
        CV = self.sigma0()**2*P_inv-CobsW
        return CV

    def mObsW_vector(self):
        C = self.CobsW_matrix()
        mOb= np.sqrt(np.diag(C))
        return mOb

    def mV_vector(self):
        C = self.CV_matrix()
        mV= np.sqrt(np.diag(C))
        return mV


    def final_control(self):
        obsW = self.obsW_matrix()
        points = self.HW_vector()
        points = np.append(points, self.const_points, axis=0)
        vector =[]
        for row in obsW:
            pp = np.where(points[:,0] == row[0])[0][0]
            pk = np.where(points[:,0] == row[1])[0][0]
            dh = points[pk, 1] - points[pp,1]
            l = dh - row[2]
            vector.append(l)
        return np.round(np.array(vector), 14)

    def controls(self):
        AT = np.transpose(self.A_matrix())
        P = self.P_matrix()
        V = self.V_vector()
        VT = np.transpose(V)
        L = self.L_vector()
        ATPV = np.matmul(np.matmul(AT,P),V)
        VTPV = np.matmul(np.matmul(VT,P),V)
        VTPL = np.matmul(np.matmul(VT,P),L)
        control_1 = np.round(ATPV,10) == 0
        control_2 = np.round(VTPL,10) == np.round(VTPV,10)
        return control_1+control_2



network = LevelingAdjustment(data, consts)
# points = network.points_height()
# print(network.points_to_find())
# print(network.points_height())
# print(network.P_matrix())
# print(network.A_matrix())
# print(network.ATPA_matrix())
# print(network.ATPL_matrix())
# print(network.L_vector())
# print(network.x_vector())
# print(network.V_vector())
# print(network.controls())
# print(network.HW_vector())
# print(network.obsW_matrix())
# print(network.final_control())
# print(network.controls())
# print(network.sigma0())
# print(network.mx_vector())
# print(network.mV_vector())
# print(network.mObsW_vector())