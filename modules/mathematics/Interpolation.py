import logging
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline, CubicHermiteSpline, CubicSpline

numberOfInterpolationPoints = 10


# argsForFunction must be a tuple
def InterpolateFunctionMaximum(f, interval, argsForFunction, precisionLevel=1, isParallel=False):
    fx = lambda x: f(*argsForFunction, x)
    execute = lambda xPts: [fx(x) for x in xPts]

    def __recursiveInterpolate(subInterval, currentLevel):
        # ----- THE FOLLOWING CODE IS FOR RANDOMIZING ADDITIONAL POINTS FOR EXTRA PRECISION USUALLY UNNECESSARY -----
        # dataset = set(np.linspace(subInterval[0], subInterval[1], num=numberOfInterpolationPoints))
        # while len(dataset) < 2 * numberOfInterpolationPoints:
        #     dataset.add(random.uniform(subInterval[0], subInterval[1]))
        # xPoints = np.sort(list(dataset))
        # --------- END OF RANDOMIZING ADDITIONAL POINTS -----------------
        xPoints = np.linspace(subInterval[0], subInterval[1], num=numberOfInterpolationPoints)
        logging.debug(f'Level: {currentLevel}, xPoints: {xPoints}')
        xMax, yMax = __interpolateMaximum(fx, xPoints, execute(xPoints), interval)
        if currentLevel == 1: return xMax, yMax
        step = (subInterval[1] - subInterval[0]) / (2 * (numberOfInterpolationPoints - 1))
        logging.info(f'x max: {xMax}, step: {step}')
        return __recursiveInterpolate((max(interval[0], xMax - step), min(interval[1], xMax + step)), currentLevel - 1)

    return __recursiveInterpolate(interval, precisionLevel)


def __interpolateMaximum(f, xPoints, yPoints, interval):
    interpolations = [__cubicSplineInterpolationMaxes, __univariateSplineInterpolationMaxes,
                      __cubicHermiteSplineInterpolationMaxes]
    return max(
        [*[(x, f(x)) for x in [inter(xPoints, yPoints) for inter in interpolations] if
           x is not None and interval[0] <= x <= interval[1]],
         *[(x, yPoints[index]) for index, x in enumerate(xPoints)]], key=lambda x: x[1])


def __cubicSplineInterpolationMaxes(xPoints, yPoints):
    f = CubicSpline(xPoints, yPoints)
    fd = f.derivative()
    fdd = fd.derivative()
    roots = {}
    [roots.update({x: f(x)}) for x in fd.roots(extrapolate=False) if fdd(x) < 0]
    return max(roots, key=roots.get) if roots else None


def __univariateSplineInterpolationMaxes(xPoints, yPoints):
    f = InterpolatedUnivariateSpline(xPoints, yPoints, k=4)
    fd = f.derivative()
    fdd = fd.derivative()
    roots = {}
    [roots.update({x: f(x)}) for x in fd.roots() if fdd(x) < 0]
    return max(roots, key=roots.get) if roots else None


def __cubicHermiteSplineInterpolationMaxes(xPoints, yPoints):
    _, axs = plt.subplots()

    def derivative_via_neighbors(index) -> float:
        return (yPoints[index + 1] - yPoints[index - 1]) / (xPoints[index + 1] - xPoints[index - 1])

    roots = {}
    for i in range(len(xPoints) - 2):
        spline = CubicHermiteSpline(
            [xPoints[i], xPoints[i + 1]],
            [yPoints[i], yPoints[i + 1]],
            [derivative_via_neighbors(i), derivative_via_neighbors(i + 1)],
        )
        spline_x = np.linspace(*spline.x)
        spline_y = spline(spline_x)
        axs.plot(spline_x, spline_y, "r-")
        fd = spline.derivative()
        fdd = fd.derivative()
        [roots.update({x: spline(x)}) for x in fd.roots() if fdd(x) < 0]
    return max(roots, key=roots.get) if roots else None
