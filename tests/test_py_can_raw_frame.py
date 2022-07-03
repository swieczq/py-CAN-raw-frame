from py_can_raw_frame import __version__
from py_can_raw_frame.can_raw import CanFrame

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