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
        self.a = -3
        self.b = 3
        self.h = 0.05
        self.result = []

    def Func(self, x):
        return math.exp(x)

    def f(self, x, y, dxdy):
        return (math.exp(x) + y + dxdy) / 3

    #def Func(self, x):
    #    return -math.cos(3*x)/5 + math.sin(2*x) + math.cos(2*x)

    #def f(self, x, y, dxdy):
    #    return math.cos(3*x) - 4*y

    def g(self, x, y, dxdy):
        return dxdy

    def RK4(self, x, y, dxdy):
        resultK = dxdy    
        resultQ = y     

        k1 = self.h * self.f(x, y, dxdy)
        q1 = self.h * self.g(x, y, dxdy)

        k2 = self.h * self.f(x + self.h / 2.0, y + q1 / 2.0, dxdy + k1 / 2.0)
        q2 = self.h * self.g(x + self.h / 2.0, y + q1 / 2.0, dxdy + k1 / 2.0)

        k3 = self.h * self.f(x + self.h / 2.0, y + q2 / 2.0, dxdy + k2 / 2.0)
        q3 = self.h * self.g(x + self.h / 2.0, y + q2 / 2.0, dxdy + k2 / 2.0)

        k4 = self.h * self.f(x + self.h, y + q3, dxdy + k3)
        q4 = self.h * self.g(x + self.h, y + q3, dxdy + k3)

        resultK += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        resultQ += (q1 + 2.0 * q2 + 2.0 * q3 + q4) / 6.0

        return [resultK, resultQ]

    def Resolution(self, Y0):
        self.result.clear()
        curX = self.x0
        y = Y0[0]
        dxdy = Y0[1]

        # Решеник диффура Рунге-Куттом
        while curX < self.xN:
            result = self.RK4(curX, y, dxdy)
            curX += self.h
            dxdy = result[0]
            y = result[1]
            self.result.append([curX, y, dxdy])

        exodus = []
        exodus.append(self.result[-1])
        self.result.clear()

        # Двойной пересчет
        deltaY = 100
        deltaDxDy = 100
        while deltaY > (15 * E) or deltaDxDy > (15 * E):
            curX = self.x0
            y = Y0[0]
            dxdy = Y0[1]
            self.h = self.h / 2
            while curX < self.xN:
                result = self.RK4(curX, y, dxdy)
                curX += self.h
                dxdy = result[0]
                y = result[1]
                self.result.append([curX, y, dxdy])
            exodus.append(self.result[-1])
            deltaY = abs(exodus[-2][1] - exodus[-1][1])
            deltaDxDy = abs(exodus[-2][2] - exodus[-1][2])
            if deltaY > (15 * E) or deltaDxDy > (15 * E):
                self.result.clear()

        self.h = 0.05
        return [y, dxdy]

    def Graph(self, X, Y, descr, figureNum):
        plt.figure(figureNum)
        plt.plot(X, Y, label = descr)
        plt.legend()

    def Output(self):
        X = []
        Y = []
        dxdy = []
        orig = []
        for i in range(len(self.result)):
            X.append(self.result[i][0])
            Y.append(self.result[i][1])
            dxdy.append(self.result[i][2])
            orig.append(self.Func(X[i]))

        self.Graph(X, Y, "Y", 0)
        self.Graph(X, dxdy, "dxdy", 1)
        self.Graph(X, orig, "Original", 2)

        for i in range(len(self.result)):
            print(self.result[i])
            print()

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