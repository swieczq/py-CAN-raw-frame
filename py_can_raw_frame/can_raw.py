
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
        #TODO: make init more readable, shorter      
        self._check_input_values(ID=ID,data=data,RTR=RTR,DLC=DLC)
        
        self.START_OF_FRAME: str = '0'
        self.IDE: str = '0'
        self.r0: str = '0'
        self.CRC: str = None
        self.CRC_del: str = '1'
        self.ACK: str = '0'
        self.ACK_del: str = '1'
        self.EOF: str = "1111111"
        self.IFS: str = "111"
        self.can_raw_frame: str = None

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

    def convert(self)->None:
        raw_can_frame=self.START_OF_FRAME+self.ID+self.RTR+self.IDE+self.r0+self.DLC+self.data
        self.CRC = self.calculate_crc(raw_can_frame)
        raw_can_frame=self.add_stuff_bits(raw_can_frame)
        raw_can_frame = raw_can_frame+self.CRC+self.CRC_del+self.ACK+self.ACK_del+self.EOF+self.IFS
        self.can_raw_frame = raw_can_frame

    def add_stuff_bits(self,message: str)->str:
        #TODO: beautify this function
        stuff_size=5
        i=0
        tmp=list(message)
        while i+stuff_size<=len(tmp):
            tmp_window=''.join(tmp[i:i+stuff_size])
            if(tmp_window=="11111"):
                tmp.insert(i+stuff_size,'0')
                i=i+stuff_size+1
                continue
            elif(tmp_window=="00000"):
                tmp.insert(i+stuff_size,'1')
                i=i+stuff_size+1
                continue
            else:
                i+=1
        return ''.join(tmp)

    def calculate_crc(self,message: str)->str:
        """CRC is calculated over all bits preceding CRC, without stuff bits"""
        crc_poly="1100010110011001"
        len_message = len(message)
        padding = (len(crc_poly)-1)*'0'
        padded_message = message + padding
        padded_message = list(padded_message)
        while '1' in padded_message[:len_message]:
            window_position=padded_message.index('1')
            for i in range(len(crc_poly)):
                padded_message[window_position+i] = str(int(crc_poly[i] != padded_message[window_position + i]))
        return ''.join(padded_message[len_message:])
        
    
    def __str__(self):
        return f"ID={self.ID}, data={self.data}, RTR={self.RTR}, DLC={self.DLC}, CRC={self.CRC}, \
            \n raw_frame={self.can_raw_frame}"

    def _check_input_values(self, *, ID: str, data: str, RTR: str, DLC:str)->None:
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
        frame=CanFrame(ID="10100", data="1")
    except Exception as e:
        print(e)
        return
    frame.convert()

    print(str(frame))

if __name__ == "__main__":
    main()