import pytest
from py_can_raw_frame import __version__
from py_can_raw_frame.can_frame import CanFrame

#TODO: write more tests, more negative tests, divide into files
#TODO: use fixtures and mockups

#basic tests
def test_version():
    assert __version__ == '0.1.0'

def test_CanFrame_init_ID():
    frame=CanFrame(ID="0", data="0")
    assert frame.ID == "00000000000"

def test_CanFrame_init_ID_value_error():
    with pytest.raises(ValueError):
        frame=CanFrame(ID="5", data="0")

def test_CanFrame_init_ID_too_great():
    with pytest.raises(ValueError):
        frame=CanFrame(ID="111111111111", data="0")

def test_CanFrame_init_data():
    frame=CanFrame(ID="0", data="0")
    assert frame.data == "00000000"

def test_CanFrame_init_data_value_error():
    with pytest.raises(ValueError):
        frame=CanFrame(ID="0", data="4")

def test_CanFrame_init_DLC():
    frame=CanFrame(ID="0", data="0")
    assert frame.DLC == "0001"

#data tests
def test_CanFrame_init_data_boundary_condition_lower():
    frame=CanFrame(ID="0", data="11111111")
    assert frame.data == "11111111"

def test_CanFrame_init_data_boundary_condition_higher():
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