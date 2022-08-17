from py_can_raw_frame import __version__
from py_can_raw_frame.can_frame import CanFrame

#TODO: write more tests, more negative tests, divide into files

#basic tests
def test_version():
    assert __version__ == '0.1.0'

def test_CanFrame_init_default_ID():
    frame=CanFrame(ID="0", data="0")
    assert frame.ID == "00000000000"

def test_CanFrame_init_default_data():
    frame=CanFrame(ID="0", data="0")
    assert frame.data == "00000000"

def test_CanFrame_init_default_DLC():
    frame=CanFrame(ID="0", data="0")
    assert frame.DLC == "0001"

#data tests
def test_CanFrame_init_boundary_condition_data_lower():
    frame=CanFrame(ID="0", data="11111111")
    assert frame.data == "11111111"

def test_CanFrame_init_boundary_condition_data_higher():
    frame=CanFrame(ID="0", data="111111111")
    assert frame.data == "0000000111111111"

#class subfunctions tests
def test_CanFrame_stuff_bit_addition():
    frame=CanFrame(ID="0", data="1")
    result=frame.add_stuff_bits("11111")
    assert result=="111110"

#code integration
def test_CanFrame_raw_frame_generation():
    frame=CanFrame(ID="10100", data="1")
    frame.convert()
    assert frame.can_raw_frame=="0000010010100000100010000010011110111010100111011111111111"