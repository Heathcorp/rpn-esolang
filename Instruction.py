from abc import ABC, abstractmethod

class opcode(ABC):
    @abstractmethod
    def operate(self, stack):
        pass

class add(opcode):
    def operate(self, stack):
        val1 = stack[len(stack) - 1]
        stack.pop()

        head = len(stack) - 1
        val2 = stack[head]
        stack[head] = val1 + val2