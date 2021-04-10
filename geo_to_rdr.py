from math import sin, cos, sqrt
import numpy

a = 6378137.
e2 = 0.0066943799901

def r_east(lat):
    # radius of ellipsoid in East direction (assuming latitude-wise symmetry)
    return a / sqrt(1. - e2 * sin(lat)**2)

def llh_to_xyz(lon, lat, hgt):
    # radius of earth in east direction
    re = r_east(lat)
    x = (re + hgt) * cos(lat) * cos(lon)
    y = (re + hgt) * cos(lat) * sin(lon)
    # adjust radius for eccentricity
    z = (re * (1. - e2) + hgt) * sin(lat)
    return numpy.array([x, y, z])
