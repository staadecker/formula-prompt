from formula_prog import FormulaSet


class Econ:
    @staticmethod
    def _description_find_yield():
        return ("Present value", float), ("Coupon value", float), ("Number of periods", float), ("Face value", float)

    @staticmethod
    def find_yield(P, A, N, F):
        increment = 0.01
        y = 0.001
        threshold = 0.000005
        increasing = True

        def find_present(y):
            return A * (1 - (1 + y) ** (-N)) / y + F * (1 + y) ** (-N)

        while True:
            P_guess = find_present(y)

            if P - threshold < P_guess < P + threshold:
                break
            elif P_guess > P:
                y += increment
                if not increasing:
                    increment /= 2
                increasing = True
            else:
                y -= increment
                if increasing:
                    increment /= 2
                increasing = False
            print(y)

        print(f"yield rate: %.3f +/- %.4f %%" % (y * 100, threshold * 100))

    @staticmethod
    def _description_annuity_factor():
        return ("number of periods", float), ("rate (percent)", float)

    @staticmethod
    def annuity_factor(N, r):
        r /= 100
        factor = (1 - (1 + r) ** (-N)) / r
        print("P/A= %.7f" % factor)
        print("A/P= %.7f" % (1 / factor))

    @staticmethod
    def _description_geometric_factor():
        return ("number of periods", float), ("rate (percent)", float), ("gradient rate (percent)", float)

    @staticmethod
    def geometric_factor(N, i, g):
        i /= 100
        g /= 100
        factor = (((1 + g) / (1 + i)) ** N - 1) / (g - i)
        print("P/geom= %.7f" % factor)
        print("geom/P= %.7f" % (1 / factor))


if __name__ == "__main__":
    formula_set = FormulaSet(Econ)
    formula_set.run()
