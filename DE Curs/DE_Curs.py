import math
import matplotlib.pyplot as plt

E = 0.00001

class DiffEq():
    def __init__(self):
        self.x0 = 0
        self.y0 = 1
        self.xN = 1
        self.yN = 2.718

        #self.x0 = 0
        #self.y0 = 0.8
        #self.xN = 1
        #self.yN = 0.691149
        self.a = 0
        self.b = 1
        self.h = 0.05
        self.result = []

    def Func(self, x):
        return math.exp(x)

    def f(self, x, y, z):
        return (math.exp(x) + y + z) / 3

    #def Func(self, x):
    #    return -math.cos(3*x)/5 + math.sin(2*x) + math.cos(2*x)

    #def f(self, x, y, z):
    #    return math.cos(3*x) - 4*y

    def g(self, x, y, z):
        return z

    def RK4(self, x, y, z):
        resultK = z     # y
        resultQ = y     # y'

        k1 = self.h * self.f(x, y, z)
        q1 = self.h * self.g(x, y, z)

        k2 = self.h * self.f(x + self.h / 2.0, y + q1 / 2.0, z + k1 / 2.0)
        q2 = self.h * self.g(x + self.h / 2.0, y + q1 / 2.0, z + k1 / 2.0)

        k3 = self.h * self.f(x + self.h / 2.0, y + q2 / 2.0, z + k2 / 2.0)
        q3 = self.h * self.g(x + self.h / 2.0, y + q2 / 2.0, z + k2 / 2.0)

        k4 = self.h * self.f(x + self.h, y + q3, z + k3)
        q4 = self.h * self.g(x + self.h, y + q3, z + k3)

        resultK += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        resultQ += (q1 + 2.0 * q2 + 2.0 * q3 + q4) / 6.0

        return [resultK, resultQ]

    def Resolution(self, Y0):
        self.result.clear()
        curX = 0
        y = Y0[0]
        z = Y0[1]
        count = 0

        # Решеник диффура Рунге-Куттом
        while curX < self.xN:
            result = self.RK4(curX, y, z)
            curX += self.h
            z = result[0]
            y = result[1]
            self.result.append([curX, y, z])

        # Двойной пересчет
        delta = 0
        while delta > (15 * E):
            self.h = self.h / 2
            while curX < self.xN:
                result = self.RK4(curX, y, z)
                curX += self.h
                z = result[0]
                y = result[1]
                self.result.append([curX, y, z])
            count += 1
            delta = self.result[-1][1] - self.result[-2][1]


        print("количество итераций = ", count)

        self.h = 0.05
        return [y, z]

    def Graph(self, X, Y, descr, figureNum):
        plt.figure(figureNum)
        plt.plot(X, Y, label = descr)
        plt.legend()

    def Output(self):
        X = []
        Y = []
        z = []
        inX = []
        for i in range(len(self.result)):
            X.append(self.result[i][0])
            Y.append(self.result[i][1])
            z.append(self.result[i][2])
            inX.append(self.Func(X[i]))

        self.Graph(X, Y, "Y", 0)
        self.Graph(X, z, "z", 1)
        self.Graph(X, inX, "Right", 2)

        for i in range(len(self.result)):
            print(self.result[i])

        plt.show()

    def Calc(self):
        # Стреляем на А
        Y0 = [self.y0, self.a]
        yA = self.Resolution(Y0)[0]

        # Стреляем на B
        Y0 = [self.y0, self.b]
        yB = self.Resolution(Y0)[0]

        # Если недолет больше E, меняем траекторию
        while abs(yB - yA) > E:
            self.c = (self.b + self.a) / 2
            Y0 = [self.y0, self.c]

            # Стреляем между прошлыми точками
            yС = self.Resolution(Y0)[0]
            if self.yN < yС:   
                self.b = self.c
                yB = yС
            else:
                self.a = self.c
                yA = yС

        self.Output()

if __name__ == '__main__':
    result = DiffEq()
    result.Calc()