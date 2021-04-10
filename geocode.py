from math import pi, cos
from matplotlib import pyplot
from osgeo import gdal
from scipy.constants import speed_of_light as c
from tqdm import tqdm
import datetime
import numpy
import os

from alos_slc import AlosPalsarSlc
from geo_to_rdr import llh_to_xyz
from caesar import xyz_to_rdr
from core import LinearSpace, Interval

dem = gdal.Open(os.path.expanduser("~/data/N37W123.hgt"))
slc = AlosPalsarSlc(os.path.expanduser("~/data/ALPSRP084780740-L1.1"))
f = gdal.Open(slc.vol)

# get HV band, containing complex data
print("reading image...")
radar_data = f.ReadAsArray()[0]
print("done.")

cs = slc.platform()
dem_array = dem.ReadAsArray()

deg_to_rad = lambda deg: deg * pi / 180

lon_start = -122.52
lat_start = 37.82
lon_scale = cos(deg_to_rad(lat_start))

x_res = int(360 * lon_scale)
y_res = int(360)
geocoded = numpy.zeros((y_res, x_res), dtype=numpy.float32)
geocode_x = numpy.linspace(lon_start, lon_start + .25 * lon_scale, x_res)
geocode_y = numpy.linspace(lat_start, lat_start - .25, y_res)

# set up azimuth time so that the sensing start is at t=0
azm_space = LinearSpace(1 / slc.prf)

range_pixel_spacing = c / (2 * slc.range_sampling_rate)
rng_space = LinearSpace(start=slc.img_record.range_first_sample, spacing=range_pixel_spacing)

dem_x_interval = Interval(min=0, max=dem.RasterXSize)
dem_y_interval = Interval(min=0, max=dem.RasterYSize)

geotransform = dem.GetGeoTransform()
dem_x_space = LinearSpace(start=geotransform[0], spacing=geotransform[1])
dem_y_space = LinearSpace(start=geotransform[3], spacing=geotransform[5])

for y_idx, lat_deg in enumerate(tqdm(geocode_y)):
    lat_rad = deg_to_rad(lat_deg)

    dem_y_idx = dem_y_space.index_of(lat_deg)
    if not dem_y_interval.half_open_contains(dem_y_idx):
        continue

    for x_idx, lon_deg in enumerate(geocode_x):
        lon_rad = deg_to_rad(lon_deg)

        dem_x_idx = dem_x_space.index_of(lon_deg)
        if not dem_x_interval.half_open_contains(dem_x_idx):
            continue

        hgt = dem_array[int(dem_y_idx), int(dem_x_idx)]

        xyz = llh_to_xyz(lon_rad, lat_rad, hgt)

        azm, rng = xyz_to_rdr(xyz, cs)
        azm_idx = azm_space.index_of(azm)
        rng_idx = rng_space.index_of(rng)

        #print(azm_idx, rng_idx)

        if azm_idx < 0 or azm_idx >= f.RasterYSize:
            continue
        if rng_idx < 0 or rng_idx >= f.RasterXSize:
            continue

        geocoded[y_idx, x_idx] = numpy.abs(radar_data[int(azm_idx), int(rng_idx)])

#pyplot.imsave("img.png", numpy.log(numpy.ma.array(geocoded, mask=(geocoded==0))))
pyplot.imshow(numpy.log(numpy.ma.array(geocoded, mask=(geocoded==0))))
pyplot.show()
