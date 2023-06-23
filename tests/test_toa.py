import os

from psrdb.utils.toa import toa_line_to_dict, toa_dict_to_line

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')

def test_toa_line_to_dict_to_line():
    """
    Test that toa_line_to_dict(toa_line_to_str(toa_dict)) == toa_dict
    """
    toa_file = os.path.join(TEST_DATA_DIR, "J1705-1903_2020-12-24-07:06:49_zap.4ch1p12t.ar.tim")
    with open(toa_file, "r") as f:
        toa_lines = f.readlines()
        for toa_line in toa_lines[1:]:
            input_toa_line = toa_line.rstrip("\n")
            toa_dict = toa_line_to_dict(input_toa_line)
            output_toa_line = toa_dict_to_line(toa_dict)
            print(input_toa_line)
            print(output_toa_line)
            assert input_toa_line == output_toa_line