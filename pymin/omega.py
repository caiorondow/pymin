from .multistage import Multistage
from math import ceil, log2, pow


class Omega(Multistage):


    def __init__(self, n : int, extras : int = 0, radix : int = 2) -> None:
        super().__init__()

        self.__SIZE      : int = n
        self.__EXTRAS    : int = ceil(pow(radix, extras))
        self.__RADIX     : int = radix
        self.__STAGES    : int = ceil(log2(n) / log2(radix)) + extras

        self.__WIND_BITS : int = ceil(log2(n)) 
        self.__EXTR_BITS : int = ceil(radix/2) * extras
        self.__PATH_BITS : int = 2 * self.__WIND_BITS + self.__EXTR_BITS
        self.__WIND_MASK : int = n-1
        self.__CONF_MASK : int = radix-1
        self.__SLID_RATE : int = ceil(radix/2)
        
        self.__switch : list = [None] * (self.len * self.stages)

    def route(self, requests : list[tuple[int,int]]) -> tuple[int,int]:
        clk = 0
        fail = 0
        pending_requests = requests.copy()

        while pending_requests:
            clk += 1
            current_requests = pending_requests.copy()
            pending_requests.clear()
            
            self.clear()
            
            for input, output in current_requests:
                if not self.one2one(input, output):
                    pending_requests.append((input, output))
                    fail += 1

        return clk, fail

    def one2one(self, input : int, output : int) -> bool:
        
        assert 0 <= input  < self.len, f"in one2one(self, input : int, output : int) -> bool\n\tinput must be in between [0, {self.len-1}], but is {input}."
        assert 0 <= output < self.len, f"in one2one(self, input : int, output : int) -> bool\n\toutput must be in between [0, {self.len-1}], but is {output}." 

        for extra in range(self.extras):

            found_path : bool = True
            path       : bool = self.__concat(input, extra, output)

            for stage in range(self.stages):
                
                row : int = self.__slide(path, stage)

                if not self.__is_path_available(path, row, stage):
                    found_path = False
                    break
            
            if found_path:
                self.__send_message(path)
                return True
        
        return False

    def clear(self):
        self.__switch : list = [None] * (self.len * self.stages)

    def __is_path_available(self, path : int, row : int, stage : int) -> bool:
        
        assert 0 <= path  < pow(2, self.__PATH_BITS), f"in __is_path_available(self, path : int, row : int, stage : int) -> bool\n\tpath must be in between [0, {pow(2, self.__PATH_BITS)-1}], but is {path}."
        assert 0 <= row   < self.len, f"in __is_path_available(self, path : int, row : int, stage : int) -> bool\n\trow must be in between [0, {self.len-1}], but is {row}."
        assert 0 <= stage < self.stages, f"in __is_path_available(self, path : int, row : int, stage : int) -> bool\n\tstage must be in between [0, {self.stages-1}], but is {stage}."

        idx : int = row * self.stages + stage

        is_path_free : bool = self.__switch[idx] == None
        is_multicast : bool = self.__switch[idx] == self.__config_bit(path, stage)

        return is_path_free or is_multicast

    def __send_message(self, path : int) -> None:
        
        assert 0 <= path  < pow(2, self.__PATH_BITS), f"in __send_message(self, path : int) -> None\n\tpath must be in between [0, {pow(2, self.__PATH_BITS)-1}], but is {path}."

        for stage in range(self.stages):
            row : int = self.__slide(path, stage)
            self.__switch[ row * self.stages + stage ] = self.__config_bit(path, stage)

    def __concat(self, input : int, extra : int, output : int) -> int:
        
        assert 0 <= input  < self.len, f"in __concat(self, input : int, extra : int, output : int) -> int\n\tinput must be in between [0, {self.len-1}], but is {input}."
        assert 0 <= output < self.len, f"in __concat(self, input : int, extra : int, output : int) -> int\n\toutput must be in between [0, {self.len-1}], but is {output}."
        assert 0 <= extra  < self.len, f"in __concat(self, input : int, extra : int, output : int) -> int\n\textra must be in between [0, {self.extras-1}], but is {extra}."

        return output | (extra << self.__WIND_BITS) | (input << (self.__WIND_BITS + self.__EXTR_BITS))
    
    def __slide(self, path : int, stage : int) -> int:

        assert 0 <= path  < pow(2, self.__PATH_BITS), f"in __slide(self, path : int, stage : int) -> int\n\tpath must be in between [0, {pow(2, self.__PATH_BITS)-1}], but is {path}."
        assert 0 <= stage < self.stages, f"in __slide(self, path : int, stage : int) -> int\n\tstage must be in between [0, {self.stages-1}], but is {stage}."

        return (path >> (self.__PATH_BITS - (stage + 1) * self.__SLID_RATE - self.__WIND_BITS)) & self.__WIND_MASK

    def __config_bit(self, path : int, stage : int) -> int:
    
        assert 0 <= path  < pow(2, self.__PATH_BITS), f"in __config_bit(self, path : int, stage : int) -> int\n\tpath must be in between [0, {pow(2, self.__PATH_BITS)-1}], but is {path}."
        assert 0 <= stage < self.stages, f"in __config_bit(self, path : int, stage : int) -> int\n\tstage must be in between [0, {self.stages-1}], but is {stage}."
    
        return (path >> (self.__PATH_BITS - (stage + 1) * self.__SLID_RATE)) & self.__CONF_MASK

    @property
    def len(self) -> int:
        return self.__SIZE

    @property
    def stages(self) -> int:
        return self.__STAGES
    
    @property
    def extras(self) -> int:
        return self.__EXTRAS

    @property
    def radix(self) -> int:
        return self.__RADIX

    def __str__(self):
        pass

    def __len__(self):
        return self.__SIZE