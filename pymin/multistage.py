from abc import ABC, abstractmethod

class Multistage(ABC):
    @abstractmethod
    def route(self, requests : list[tuple[int,int]]) -> tuple[int,int]:
        """
        Routes a batch of requests through the multistage network.

        Parameters:
        requests (list[tuple[int, int]]): A list of tuples, where each tuple represents a request
                                            with the format (input_node, output_node).

        Returns:
        tuple[int, int]: A tuple representing the status of the routing operation, which may include
                         information such as success or failure codes or the number of successfully 
                         routed requests.
        """
        pass

    @abstractmethod
    def one2one(self, input : int, output : int) -> bool:
        """
        Routes a single request from a specific input node to a specific output node.

        Parameters:
        input (int): The index of the input node from which the request originates.
        output (int): The index of the output node to which the request is destined.

        Returns:
        bool: True if the routing was successful, False otherwise.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the current state of the multistage network.

        This method resets any internal data structures, removes any existing requests, and prepares
        the network for a new set of routing operations. It does not return any value.
        """
        pass

    @property
    @abstractmethod
    def len(self) -> int:
        pass

    @property
    @abstractmethod
    def stages(self) -> int:
        pass

    @property
    @abstractmethod
    def extras(self) -> int:
        pass

    @property
    @abstractmethod
    def radix(self) -> int:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass