
from msilib.schema import Error
from typing import Final


CAN_ID_LEN: Final[int]      = 11
CAN_MAX_ID_VAL: Final[int]  = 2047
BYTE: Final[int]            = 8
DLC_LEN: Final[int]         = 4
CAN_MAX_DLC_VAL: Final[int] = 15
CAN_MAX_DATA_VAL: Final[int]= 2**64-1



class CanFrame:
    """Holds and converts CAN frame information to a raw can frame"""
    def __init__(self, *, ID: str, data: str, RTR: str="0", DLC:str=None):
        self.START_OF_FRAME: str = '0'
        self.IDE: str = '0'
        self.r0: str = '0'

        #TODO: add safety checks for incorrect input        
        self._check_input_values(self,ID=ID,data=data,RTR=RTR,DLC=DLC)
        self.ID=ID.zfill(CAN_ID_LEN)
        self.RTR=RTR
        if self.RTR=="0":
            if(len(data)%BYTE==0):
                proper_datalen=len(data)
            else:
                missing_bits=BYTE-len(data)%BYTE
                proper_datalen=len(data)+missing_bits
            self.data=data.zfill(proper_datalen)
        else:
            self.data=""

        
        if(self.RTR=="0"):
            DLC_int=int(len(self.data)/BYTE)
            self.DLC=bin(DLC_int)[2:] #bin() starts with 0b
            self.DLC=self.DLC.zfill(DLC_LEN)
        else:
            self.DLC=DLC

    def convert(self):
        raw_can_frame=self.START_OF_FRAME+self.ID+self.RTR+self.IDE+self.r0+self.DLC+self.data
        pass
    
    def calculate_crc(self,message):
        pass
    
    def __str__(self):
        return f"ID={self.ID}, data={self.data}, RTR={self.RTR}, DLC={self.DLC}"

    def _check_input_values(self, *, ID: str, data: str, RTR: str, DLC:str):
        if int(data,2)>CAN_MAX_DATA_VAL:
            raise ValueError("Wrong data value")
        if DLC is not None and int(DLC,2)>CAN_MAX_DLC_VAL:
            raise ValueError("Wrong DLC value")
        if int(ID,2) > CAN_MAX_ID_VAL:
            raise ValueError("Wrong ID value")
        if RTR != "0" and RTR!="1":
            raise ValueError("Wrong RTR value")



def main():
    try:
        frame=CanFrame(ID="1", data="1")
    except Exception as e:
        print(e)
        return
    print(str(frame))

if __name__ == "__main__":
    main()