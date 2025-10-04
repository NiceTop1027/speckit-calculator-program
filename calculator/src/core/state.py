"""
계산기 상태 관리
Calculator state management
"""
from decimal import Decimal
from typing import Optional
from .enums import CalculatorMode, AngleMode, OperationType


class CalculatorState:
    """계산기의 현재 상태"""

    def __init__(self):
        self.current_value: Decimal = Decimal('0')
        self.previous_value: Optional[Decimal] = None
        self.operation: Optional[OperationType] = None
        self.mode: CalculatorMode = CalculatorMode.STANDARD
        self.angle_mode: AngleMode = AngleMode.DEGREES
        self.is_new_calculation: bool = True
        self.display_text: str = "0"
        self.last_operation: Optional[OperationType] = None
        self.last_operand: Optional[Decimal] = None

    def reset(self) -> None:
        """상태 초기화 (CE 버튼)"""
        self.current_value = Decimal('0')
        self.previous_value = None
        self.operation = None
        self.is_new_calculation = True
        self.display_text = "0"
        self.last_operation = None
        self.last_operand = None

    def clear_current(self) -> None:
        """현재 입력만 지우기 (C 버튼)"""
        self.current_value = Decimal('0')
        self.display_text = "0"
        self.is_new_calculation = True
