from math import sin, cos, sqrt
import numpy
import scipy.optimize

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

def xyz_to_rdr(xyz, platform, initial_guess=None):
    t0 = platform.start_time()
    tf = platform.end_time()

    # not actually, but has the same root for zero-doppler
    def doppler_eqn(t):
        posvel = platform(t)
        platform_pos = posvel[:3]
        platform_vel = posvel[3:]
        return numpy.dot(platform_vel, xyz - platform_pos)

    # solve for azimuth time
    if initial_guess is None:
        initial_guess = (tf + t0) / 2
    t = scipy.optimize.newton(doppler_eqn, initial_guess)

    # get corresponding platform position and slant range
    platform_pos = platform(t)[:3]
    slant_range = numpy.linalg.norm(xyz - platform_pos)

    # return results
    return t, slant_range
