from abc import ABC, abstractmethod

class AiCallerStrategy(ABC):

    @abstractmethod
    def requestAi(self, prompt):
        pass

