from reader_l11 import get_platform, get_img_record, get_dataset_summary, segments
import os
from datetime import datetime, timedelta
import caesar
from caesar import Orbit
import numpy

# ALOS-1 PALSAR SLC file, level 1.1, JAXA format
class AlosPalsarSlc:

    def __init__(self, basedir):
        files = os.listdir(basedir)

        led = [f for f in files if f.startswith("LED-")]
        assert len(led) >= 1, "No leader file found"
        assert len(led) <= 1, "Multiple candidate leader files found"
        self.led = os.path.join(basedir, led[0])

        vol = [f for f in files if f.startswith("VOL-")]
        assert len(vol) >= 1, "No vol file found"
        assert len(vol) <= 1, "Multiple candidate vol files found"
        self.vol = os.path.join(basedir, vol[0])

        img = [f for f in files if f.startswith("IMG-")]
        assert len(img) >= 1, "No image files found"
        assert len(img) <= 2, "Too many image polarizations found"
        self.img = os.path.join(basedir, img[0])

        platform = get_platform(self.led)
        assert(platform.record_sequence_number == 3)
        assert(platform.record_1_subtype_code == 18)
        assert(platform.record_type_code == 30)
        assert(platform.record_2_subtype_code == 18)
        assert(platform.record_3_subtype_code == 20)
        assert(platform.record_length == 4680)
        assert(int(platform.orbital_elements_designator) == 2)
        assert(int(platform.num_points) == 28)
        self.platform_record = platform


        self.img_record = get_img_record(self.img)
        self.dset = get_dataset_summary(self.led)

        self.range_sampling_rate = 1e6 * float(self.dset.sampling_rate)

        self.prf = self.img_record.prf / 1000 # convert mHz to Hz

    def platform(self):

        platform_record = self.platform_record
        img_record = self.img_record

        platform_start_utc = datetime(int(platform_record.year), 1, 1) \
            + timedelta(days=int(platform_record.day_of_year) - 1) \
            + timedelta(seconds=float(platform_record.seconds_of_day))
        sensing_start_utc = datetime(img_record.year, 1, 1) \
            + timedelta(days=img_record.day_of_year - 1) \
            + timedelta(seconds=img_record.ms_of_day / 1000)

        posvel = list(map(float, segments(22, platform_record.statevecs)))
        dt = float(platform_record.time_interval)
        platform_start = (platform_start_utc - sensing_start_utc).total_seconds()

        return Orbit(platform_start, dt, posvel)

    @staticmethod
    def spheroid():
        # ALOS orbits earth
        return caesar.wgs84_ellipsoid
