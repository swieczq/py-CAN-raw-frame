
from typing import Final


CAN_ID_LEN: Final[int]  =11
BYTE: Final[int]        =8
DLC_LEN: Final[int]     =4


class CanFrame:
    """Holds and converts CAN frame information to raw can frame"""
    def __init__(self, *, ID: str, data: str, RTR: str="0", DLC:str=None):
        #TODO: add safety checks for incorrect input
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


    def __str__(self):
        return f"ID={self.ID}, data={self.data}, RTR={self.RTR}, DLC={self.DLC}"


def main():
    frame=CanFrame(ID="1", data="1")
    print(str(frame))

if __name__ == "__main__":
    main()