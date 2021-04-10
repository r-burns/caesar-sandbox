# ALOS L1.1 parser
#
# References:
# https://earth.esa.int/documents/10174/2835664/ALOS-PALSAR-CEOS-Products-Format-Specifications.pdf
# https://www.ga.gov.au/__data/assets/pdf_file/0019/11719/GA10287.pdf

import struct, os, numpy
from collections import namedtuple

def make_parser(name, contents):
    file_format = "".join(x[1] for x in contents)
    fields = " ".join(x[0] for x in contents)

    mytype = namedtuple(name, fields)
    return lambda data: mytype._make(struct.unpack(file_format, data))

leaderfile_contents = [
    ("", ">"), # Big-endian
    ("record_num", "I"),
    ("r1_subtype", "B"),
    ("type_code", "B"),
    ("r2_subtype", "B"),
    ("r3_subtype", "B"),
    ("record_length", "I"),
    ("flag", "2s"),
    ("continuation_flag", "2s"),
    ("doc_id", "12s"),
    ("doc_rev", "2s"),
    ("desc_rev", "2s"),
    ("version", "12s"),
    ("file_num", "I"),
    ("file_name", "16s"),
    ("sequence_number_flag", "4s"),
    ("sequence_number_location", "8s"),
    ("sequence_number_length", "4s"),
    ("record_code_flag", "4s"),
    ("record_code_location", "8s"),
    ("record_code_length", "4s"),
    ("record_length_flag", "4s"),
    ("record_length_location", "8s"),
    ("record_length_length", "4s"),
    ("", "68x"), # blanks

    ("dataset_summary_record_count", "6s"),
    ("dataset_summary_record_length", "6s"),
    ("map_projection_record_count", "6s"),
    ("map_projection_record_length", "6s"),
    ("platform_pos_record_count", "6s"),
    ("platform_pos_record_length", "6s"),
]

parse_leaderfile = make_parser("Leaderfile", leaderfile_contents)

if __name__ == "__main__":

    leaderfile_filename = os.path.expanduser("./ALPSRP084780740-L1.1/LED-ALPSRP084780740-H1.1__A")
    with open(leaderfile_filename, 'rb') as f:
        led_data = f.read()

    file_descriptor_record = led_data[:720]
    dataset_summary_record = led_data[720:720 + 4096]
    platform_record_data = led_data[720 + 4096:720 + 4096 + 4680]

    leaderfile = parse_leaderfile(led_data[0:216])

    assert(leaderfile.record_num == 1)
    assert(leaderfile.r1_subtype == 11)
    assert(leaderfile.type_code == 192)
    assert(leaderfile.r2_subtype == 18)
    assert(leaderfile.r3_subtype == 18)
    assert(leaderfile.record_length == 720)
    assert(leaderfile.flag == b"A ")
    assert(leaderfile.continuation_flag == b"  ")
    assert(leaderfile.doc_id == b"CEOS-SAR-CCT")
    assert(leaderfile.doc_rev == b" A")
    assert(leaderfile.desc_rev == b" A")
    assert(leaderfile.sequence_number_flag == b"FSEQ")
    assert(leaderfile.sequence_number_location == b"       1")
    assert(leaderfile.sequence_number_length == b"   4")
    assert(leaderfile.record_code_flag == b"FTYP")
    assert(leaderfile.record_code_location == b"       5")
    assert(leaderfile.record_code_length == b"   4")
    assert(leaderfile.record_length_flag == b"FLGT")
    assert(leaderfile.record_length_location == b"       9")
    assert(leaderfile.record_length_length == b"   4")

    assert(leaderfile.dataset_summary_record_count  == b"     1")
    assert(leaderfile.dataset_summary_record_length == b"  4096")
    assert(leaderfile.map_projection_record_count  == b"     0")
    assert(leaderfile.map_projection_record_length == b"     0")
    assert(leaderfile.platform_pos_record_count  == b"     1")
    assert(leaderfile.platform_pos_record_length == b"  4680")

platform_record_contents = [
    ("", ">"), # Big-endian
    ("record_sequence_number", "I"),
    ("record_1_subtype_code", "B"),
    ("record_type_code", "B"),
    ("record_2_subtype_code", "B"),
    ("record_3_subtype_code", "B"),
    ("record_length", "I"),
    ("orbital_elements_designator", "32s"),
    ("first_position_vector", "48s"),
    ("first_velocity_vector", "48s"),
    ("num_points", "4s"),
    ("year", "4s"),
    ("month", "4s"),
    ("day", "4s"),
    ("day_of_year", "4s"),
    ("seconds_of_day", "22s"),
    ("time_interval", "22s"),
    ("reference_coordinate_system", "64s"),
    ("greenwich_mean_hour_angle", "22s"), # unused
    ("along_track_position_error", "16s"), # unused
    ("across_track_position_error", "16s"), # unused
    ("radial_position_error", "16s"), # unused
    ("", "48x"), # reserved

    # 28 state-vectors of pos/vel in x/y/z
    ("statevecs", str(22 * 3 * 2 * 28) + "s")
]

def segments(size, ary):
    while len(ary) > 0:
        yield ary[:size]
        ary = ary[size:]

parse_platform = make_parser("PlatformRecord", platform_record_contents)

def get_platform(leader_fname):
    with open(leader_fname, 'rb') as f:
        led_data = f.read()

    file_descriptor_record = led_data[:720]
    dataset_summary_record = led_data[720:720 + 4096]
    platform_record_data = led_data[720 + 4096:720 + 4096 + 4680]

    return parse_platform(platform_record_data[0:4082])

dataset_summary_contents = [
    ("", ">"), # Big-endian

    ("", "324x"), # TODO
    ("center_line_no", "8s"), # TODO
    ("center_pixel_no", "8s"), # TODO
    ("", "370x"), # TODO

    ("sampling_rate", "16s"), # MHz
    ("", "3370x"), # TODO
]
parse_dataset_summary = make_parser("DatasetSummaryRecord", dataset_summary_contents)

def get_dataset_summary(leader_fname):
    with open(leader_fname, 'rb') as f:
        led_data = f.read()

    file_descriptor_record = led_data[:720]
    dataset_summary_record = led_data[720:720 + 4096]

    return parse_dataset_summary(dataset_summary_record)

    return platform

img_record_contents = [
    ("", ">"), # Big-endian
    ("", "8x"),
    ("", "12x"), # TODO
    ("left_fill", "I"),
    ("pixel_count", "I"),
    ("right_fill", "I"),

    ("update_flag", "I"),
    ("year", "I"),
    ("day_of_year", "I"),
    ("ms_of_day", "I"),

    ("", "8x"), # TODO

    ("prf", "I"), # mHz

    ("", "56x"), # TODO
    ("range_first_sample", "I"),
    ("sample_delay", "I"),
]
parse_img = make_parser("SignalDataRecord", img_record_contents)
def get_img_record(img_fname):

    img_record_size = 124

    with open(img_fname, 'rb') as f:
        img_data = f.read(720 + img_record_size)

    img_data = img_data[720:] # trim file descriptor
    img = parse_img(img_data[:img_record_size])
    assert(img.left_fill == 0)
    assert(img.right_fill == 0)
    assert(img.pixel_count > 0)
    assert(img.sample_delay == 0)
    assert(img.update_flag == 0)
    return img
