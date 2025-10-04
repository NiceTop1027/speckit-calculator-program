"""
계산기 핵심 로직
Calculator core logic
"""
from decimal import Decimal
from typing import List, Optional
from .enums import CalculatorMode, AngleMode, OperationType
from .state import CalculatorState
from .memory import MemoryState
from .history import CalculationHistory, HistoryEntry
from . import operations


class Calculator:
    """계산기 핵심 클래스"""

    def __init__(self):
        self.state = CalculatorState()
        self.memory_state = MemoryState()
        self.history = CalculationHistory()

    def input_digit(self, digit: str) -> str:
        """숫자 입력"""
        # 유효한 입력인지 확인
        if digit not in '0123456789.':
            return self.state.display_text

        # 새 계산 시작 또는 연산자 입력 후
        if self.state.is_new_calculation:
            if digit == '.':
                self.state.display_text = "0."
            else:
                self.state.display_text = digit
            self.state.is_new_calculation = False
            return self.state.display_text

        # 소수점 중복 방지
        if digit == '.' and '.' in self.state.display_text:
            return self.state.display_text

        # 0 다음 숫자는 0 대체 (소수점 제외)
        if self.state.display_text == "0" and digit != '.':
            self.state.display_text = digit
            return self.state.display_text

        # 최대 32자 제한
        if len(self.state.display_text) >= 32:
            return self.state.display_text

        # 숫자 추가
        self.state.display_text += digit
        return self.state.display_text

    def input_operation(self, operation: OperationType) -> str:
        """연산자 입력"""
        current = Decimal(self.state.display_text)

        # 단항 연산자는 즉시 실행
        if operation in [OperationType.SQUARE, OperationType.SQRT, OperationType.RECIPROCAL,
                         OperationType.PERCENT, OperationType.NEGATE,
                         OperationType.SIN, OperationType.COS, OperationType.TAN,
                         OperationType.ASIN, OperationType.ACOS, OperationType.ATAN,
                         OperationType.SINH, OperationType.COSH, OperationType.TANH,
                         OperationType.LOG, OperationType.LN,
                         OperationType.EXP, OperationType.POWER10, OperationType.FACTORIAL]:
            result = self._execute_unary_operation(operation, current)
            self.state.display_text = self._format_result(result)
            self.state.current_value = result
            self.state.is_new_calculation = True
            return self.state.display_text

        # 이항 연산자
        # 이전 연산이 대기 중이면 먼저 계산
        if self.state.operation and self.state.previous_value is not None and not self.state.is_new_calculation:
            result = self._execute_binary_operation(
                self.state.operation,
                self.state.previous_value,
                current
            )
            self.state.display_text = self._format_result(result)
            self.state.current_value = result
            current = result

        self.state.previous_value = current
        self.state.operation = operation
        self.state.is_new_calculation = True

        return self.state.display_text

    def calculate(self) -> str:
        """= 버튼"""
        # 연산이 없으면 현재 값 반환
        if not self.state.operation:
            return self.state.display_text

        current = Decimal(self.state.display_text)

        # = 반복 누르기: 마지막 연산 반복
        if self.state.is_new_calculation and self.state.last_operation and self.state.last_operand:
            result = self._execute_binary_operation(
                self.state.last_operation,
                current,
                self.state.last_operand
            )
        else:
            # 일반 계산
            result = self._execute_binary_operation(
                self.state.operation,
                self.state.previous_value or Decimal('0'),
                current
            )
            # 마지막 연산 저장 (= 반복용)
            self.state.last_operation = self.state.operation
            self.state.last_operand = current

        # 히스토리에 추가
        expression = f"{self.state.previous_value or current} {self.state.operation.value} {current}"
        self.history.add_entry(expression, result)

        self.state.display_text = self._format_result(result)
        self.state.current_value = result
        self.state.previous_value = None
        self.state.operation = None
        self.state.is_new_calculation = True

        return self.state.display_text

    def clear(self) -> str:
        """C 버튼 (현재 입력만 지우기)"""
        self.state.clear_current()
        return "0"

    def clear_all(self) -> str:
        """CE 버튼 (전체 지우기)"""
        self.state.reset()
        return "0"

    def backspace(self) -> str:
        """← 버튼 (백스페이스)"""
        # 계산 결과나 새 계산이면 한 번에 지우기
        if self.state.is_new_calculation:
            self.state.display_text = "0"
            return "0"

        # 마지막 문자 제거
        if len(self.state.display_text) > 1:
            self.state.display_text = self.state.display_text[:-1]
        else:
            self.state.display_text = "0"

        return self.state.display_text

    def memory_clear(self) -> None:
        """MC (메모리 지우기)"""
        self.memory_state.clear()

    def memory_recall(self) -> str:
        """MR (메모리 불러오기)"""
        value = self.memory_state.recall()
        self.state.display_text = self._format_result(value)
        self.state.is_new_calculation = True
        return self.state.display_text

    def memory_add(self) -> None:
        """M+ (메모리에 더하기)"""
        current = Decimal(self.state.display_text)
        new_value = self.memory_state.stored_value + current
        operations.check_overflow(new_value)
        self.memory_state.add(current)
        # 디스플레이는 변경하지 않음

    def memory_subtract(self) -> None:
        """M- (메모리에서 빼기)"""
        current = Decimal(self.state.display_text)
        new_value = self.memory_state.stored_value - current
        operations.check_overflow(new_value)
        self.memory_state.subtract(current)
        # 디스플레이는 변경하지 않음

    def memory_store(self) -> None:
        """MS (메모리 저장)"""
        current = Decimal(self.state.display_text)
        self.memory_state.store(current)

    def set_mode(self, mode: CalculatorMode) -> None:
        """모드 변경"""
        self.state.mode = mode

    def set_angle_mode(self, angle_mode: AngleMode) -> None:
        """각도 단위 변경"""
        self.state.angle_mode = angle_mode

    def get_history(self) -> List[HistoryEntry]:
        """히스토리 조회"""
        return self.history.entries

    def clear_history(self) -> None:
        """히스토리 삭제"""
        self.history.clear()

    def get_display(self) -> str:
        """현재 디스플레이 텍스트"""
        return self.state.display_text

    def input_constant(self, constant: str) -> str:
        """상수 입력 (π, e)"""
        if constant == 'π':
            value = operations.PI
        elif constant == 'e':
            value = operations.E
        else:
            return self.state.display_text

        self.state.display_text = self._format_result(value)
        self.state.is_new_calculation = True
        return self.state.display_text

    def _execute_unary_operation(self, operation: OperationType, value: Decimal) -> Decimal:
        """단항 연산 실행"""
        if operation == OperationType.SQUARE:
            return operations.square(value)
        elif operation == OperationType.SQRT:
            return operations.sqrt(value)
        elif operation == OperationType.RECIPROCAL:
            return operations.reciprocal(value)
        elif operation == OperationType.PERCENT:
            return operations.percent(value)
        elif operation == OperationType.NEGATE:
            return operations.negate(value)
        elif operation == OperationType.SIN:
            return operations.sin_deg(value, self.state.angle_mode)
        elif operation == OperationType.COS:
            return operations.cos_deg(value, self.state.angle_mode)
        elif operation == OperationType.TAN:
            return operations.tan_deg(value, self.state.angle_mode)
        elif operation == OperationType.ASIN:
            return operations.asin_deg(value, self.state.angle_mode)
        elif operation == OperationType.ACOS:
            return operations.acos_deg(value, self.state.angle_mode)
        elif operation == OperationType.ATAN:
            return operations.atan_deg(value, self.state.angle_mode)
        elif operation == OperationType.SINH:
            return operations.sinh_func(value)
        elif operation == OperationType.COSH:
            return operations.cosh_func(value)
        elif operation == OperationType.TANH:
            return operations.tanh_func(value)
        elif operation == OperationType.LOG:
            return operations.log10_func(value)
        elif operation == OperationType.LN:
            return operations.ln_func(value)
        elif operation == OperationType.EXP:
            return operations.exp_func(value)
        elif operation == OperationType.POWER10:
            return operations.power10_func(value)
        elif operation == OperationType.FACTORIAL:
            return operations.factorial_func(value)
        else:
            return value

    def _execute_binary_operation(self, operation: OperationType, a: Decimal, b: Decimal) -> Decimal:
        """이항 연산 실행"""
        if operation == OperationType.ADD:
            return operations.add(a, b)
        elif operation == OperationType.SUBTRACT:
            return operations.subtract(a, b)
        elif operation == OperationType.MULTIPLY:
            return operations.multiply(a, b)
        elif operation == OperationType.DIVIDE:
            return operations.divide(a, b)
        else:
            return b

    def _format_result(self, value: Decimal) -> str:
        """결과를 디스플레이 형식으로 변환"""
        # 정수면 소수점 없이
        if value == int(value):
            result = str(int(value))
        else:
            # 불필요한 trailing 0 제거
            result = str(value)
            if '.' in result:
                result = result.rstrip('0').rstrip('.')

        # 과학적 표기법 (너무 크거나 작은 수)
        abs_value = abs(value)
        if abs_value > 1e10 or (abs_value < 1e-10 and abs_value != 0):
            result = f"{float(value):.10e}"

        # 32자 제한
        if len(result) > 32:
            result = result[:32]

        return result
