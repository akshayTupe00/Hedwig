from abc import ABC, abstractmethod

class ServiceWorker(ABC):
    @abstractmethod
    def call(self, body):
        """This is an abstract method that must be implemented in derived classes"""
        pass
