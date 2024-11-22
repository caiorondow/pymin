from .multistage import Multistage, Package
from math import ceil, log2, pow

class Omega(Multistage):
    def __init__(self, n : int, extras : int = 0, radix : int = 2) -> None:
        super().__init__()

        self.__SIZE   : int = n
        self.__EXTRAS : int = ceil(pow(radix, extras))
        self.__RADIX  : int = radix
        self.__STAGES : int = ceil(log2(n) / log2(radix)) + extras

        self.__WINDOW_SIZE : int = ceil(log2(n))
        self.__SLIDE_RATE  : int = ceil(radix/2)
        self.__EXTRA_SIZE  : int = ceil(radix/2) * extras

        self.__switch : list = [None] * (self.len * self.stages)

    def route(self, requests : list[Package]) -> tuple[int,int]:
        
        clk = 0
        fail = 0
        pending_requests = requests.copy()

        while pending_requests:
            
            clk += 1
            
            current_requests = pending_requests.copy()
            pending_requests.clear()
            
            self.clear()
            
            for request in current_requests:
                if not self.one2one(request.source, request.target):
                    pending_requests.append(request)
                    fail += 1
             
        return clk, fail

    def one2one(self, input : int, output : int) -> bool:
        
        assert 0 <= input  < self.len
        assert 0 <= output < self.len

        for extra in range(self.extras):
            
            word : int = self.__concat(input, extra, output)

            if self.__backtracking(word):
                self.__update(word)
                return True
        
        return False

    def clear(self):
        self.__switch : list = [None] * (self.len * self.stages)

    def __has_conflict(self, source : int, target : int) -> bool:
        return target != None and source != target
    
    def __backtracking(self, word : int) -> tuple:

        for stage in range(self.stages):

            port : int = self.__slide(word, stage)

            source : int = self.__config_bit(word, stage)
            target : int = self.__switch[port * self.stages + stage]

            if self.__has_conflict(source, target):
                return False
            
        return True

    def __update(self, path : int) -> None:
        for stage in range(self.stages):

            port : int = self.__slide(path, stage)

            source : int = self.__config_bit(path, stage)
            self.__switch[port * self.stages + stage] = source

    def __concat(self, input : int, extra : int, output : int) -> int:
        
        assert 0 <= input  < self.len
        assert 0 <= output < self.len
        assert 0 <= extra  < self.len

        return output | (extra << self.__WINDOW_SIZE) | (input << (self.__WINDOW_SIZE + self.__EXTRA_SIZE))
    
    def __slide(self, path : int, stage : int) -> int:
        assert 0 <= stage < self.stages
        return (path >> (self.__SLIDE_RATE * stage)) & (self.len - 1)

    def __config_bit(self, path : int, stage : int) -> int:
        assert 0 <= stage < self.stages
        return (path >> (self.__SLIDE_RATE * stage + self.__WINDOW_SIZE)) & (self.radix - 1)

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
        s=""
        for row in range(self.len):
            for stage in reversed(range(self.stages)):
                s += str(self.__switch[row * self.stages + stage]) + "\t"
            s += "\n"
        return s

    def __len__(self):
        return self.__SIZE