"""
메모리 기능 상태 관리
Memory state management
"""
from decimal import Decimal


class MemoryState:
    """메모리 기능 상태"""

    def __init__(self):
        self.stored_value: Decimal = Decimal('0')
        self.is_empty: bool = True

    def clear(self) -> None:
        """MC (Memory Clear)"""
        self.stored_value = Decimal('0')
        self.is_empty = True

    def recall(self) -> Decimal:
        """MR (Memory Recall)"""
        return self.stored_value

    def add(self, value: Decimal) -> None:
        """M+ (Memory Add)"""
        self.stored_value += value
        self.is_empty = False

    def subtract(self, value: Decimal) -> None:
        """M- (Memory Subtract)"""
        self.stored_value -= value
        self.is_empty = False

    def store(self, value: Decimal) -> None:
        """MS (Memory Store)"""
        self.stored_value = value
        self.is_empty = False
