"""
계산기 메인 윈도우
Calculator main window
"""
import tkinter as tk
from typing import Dict, Callable
from functools import partial
from ..core.calculator import Calculator
from ..core.enums import CalculatorMode, OperationType, AngleMode
from .display import DisplayWidget
from .buttons import ButtonLayout


class MainWindow:
    """메인 윈도우"""

    def __init__(self, calculator: Calculator):
        self.calc = calculator
        self.root = tk.Tk()
        self.root.title("계산기")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#F0F0F0')

        # 디스플레이
        self.display = DisplayWidget(self.root)

        # 버튼 레이아웃
        self.buttons = ButtonLayout(self.root)

        # 이벤트 핸들러 매핑
        self.handlers = self._create_handlers()

        # 표준 모드로 시작
        self.buttons.create_standard_buttons(self.handlers)

        # 키보드 바인딩
        self._bind_keyboard()

        # 현재 각도 모드
        self.angle_mode_btn = None

    def run(self) -> None:
        """애플리케이션 실행"""
        self.root.mainloop()

    def update_display(self, text: str) -> None:
        """디스플레이 업데이트"""
        self.display.text = text

    def switch_mode(self, mode: CalculatorMode) -> None:
        """모드 전환"""
        self.calc.set_mode(mode)
        if mode == CalculatorMode.SCIENTIFIC:
            self.root.geometry("600x600")
            self.buttons.create_scientific_buttons(self.handlers)
        else:
            self.root.geometry("400x500")
            self.buttons.create_standard_buttons(self.handlers)

    def show_error(self, message: str) -> None:
        """에러 메시지 표시"""
        self.update_display(message)
        # 2초 후 복원 (실제로는 타이머 필요하지만 간단히 처리)
        self.root.after(2000, lambda: self.update_display(self.calc.get_display()))

    def _create_handlers(self) -> Dict[str, Callable]:
        """버튼 핸들러 생성"""
        handlers = {}

        # 숫자 버튼 - partial 사용으로 빠른 바인딩
        for digit in '0123456789.':
            handlers[digit] = partial(self._handle_digit, digit)

        # 연산자 버튼 - partial 사용
        handlers['+'] = partial(self._handle_operation, OperationType.ADD)
        handlers['-'] = partial(self._handle_operation, OperationType.SUBTRACT)
        handlers['×'] = partial(self._handle_operation, OperationType.MULTIPLY)
        handlers['÷'] = partial(self._handle_operation, OperationType.DIVIDE)
        handlers['√'] = partial(self._handle_operation, OperationType.SQRT)
        handlers['x²'] = partial(self._handle_operation, OperationType.SQUARE)
        handlers['1/x'] = partial(self._handle_operation, OperationType.RECIPROCAL)
        handlers['%'] = partial(self._handle_operation, OperationType.PERCENT)
        handlers['+/-'] = partial(self._handle_operation, OperationType.NEGATE)

        # 공학용 연산자
        handlers['sin'] = partial(self._handle_operation, OperationType.SIN)
        handlers['cos'] = partial(self._handle_operation, OperationType.COS)
        handlers['tan'] = partial(self._handle_operation, OperationType.TAN)
        handlers['asin'] = partial(self._handle_operation, OperationType.ASIN)
        handlers['acos'] = partial(self._handle_operation, OperationType.ACOS)
        handlers['atan'] = partial(self._handle_operation, OperationType.ATAN)
        handlers['log'] = partial(self._handle_operation, OperationType.LOG)
        handlers['ln'] = partial(self._handle_operation, OperationType.LN)
        handlers['eˣ'] = partial(self._handle_operation, OperationType.EXP)
        handlers['10ˣ'] = partial(self._handle_operation, OperationType.POWER10)
        handlers['n!'] = partial(self._handle_operation, OperationType.FACTORIAL)

        # 기능 버튼
        handlers['='] = self._handle_calculate
        handlers['C'] = self._handle_clear
        handlers['CE'] = self._handle_clear_all
        handlers['←'] = self._handle_backspace

        # 메모리 버튼
        handlers['MC'] = self._handle_memory_clear
        handlers['MR'] = self._handle_memory_recall
        handlers['M+'] = self._handle_memory_add
        handlers['M-'] = self._handle_memory_subtract
        handlers['MS'] = self._handle_memory_store

        # 상수
        handlers['π'] = partial(self._handle_constant, 'π')
        handlers['e'] = partial(self._handle_constant, 'e')

        # 각도 모드 전환
        handlers['도/라디안'] = self._toggle_angle_mode

        return handlers

    def _handle_digit(self, digit: str) -> None:
        """숫자 입력 처리"""
        try:
            result = self.calc.input_digit(digit)
            self.update_display(result)
        except Exception as e:
            self.show_error(str(e))

    def _handle_operation(self, operation: OperationType) -> None:
        """연산자 입력 처리"""
        try:
            result = self.calc.input_operation(operation)
            self.update_display(result)
        except ZeroDivisionError as e:
            self.show_error("0으로 나눌 수 없습니다")
        except ValueError as e:
            self.show_error("잘못된 입력입니다")
        except OverflowError as e:
            self.show_error("오버플로")

    def _handle_calculate(self) -> None:
        """= 버튼 처리"""
        try:
            result = self.calc.calculate()
            self.update_display(result)
        except ZeroDivisionError:
            self.show_error("0으로 나눌 수 없습니다")
        except ValueError:
            self.show_error("잘못된 입력입니다")
        except OverflowError:
            self.show_error("오버플로")

    def _handle_clear(self) -> None:
        """C 버튼 처리"""
        result = self.calc.clear()
        self.update_display(result)

    def _handle_clear_all(self) -> None:
        """CE 버튼 처리"""
        result = self.calc.clear_all()
        self.update_display(result)

    def _handle_backspace(self) -> None:
        """← 버튼 처리"""
        result = self.calc.backspace()
        self.update_display(result)

    def _handle_memory_clear(self) -> None:
        """MC 버튼 처리"""
        self.calc.memory_clear()

    def _handle_memory_recall(self) -> None:
        """MR 버튼 처리"""
        result = self.calc.memory_recall()
        self.update_display(result)

    def _handle_memory_add(self) -> None:
        """M+ 버튼 처리"""
        try:
            self.calc.memory_add()
        except OverflowError:
            self.show_error("오버플로")

    def _handle_memory_subtract(self) -> None:
        """M- 버튼 처리"""
        try:
            self.calc.memory_subtract()
        except OverflowError:
            self.show_error("오버플로")

    def _handle_memory_store(self) -> None:
        """MS 버튼 처리"""
        self.calc.memory_store()

    def _handle_constant(self, constant: str) -> None:
        """상수 입력 처리"""
        result = self.calc.input_constant(constant)
        self.update_display(result)

    def _toggle_angle_mode(self) -> None:
        """각도 모드 전환"""
        if self.calc.state.angle_mode == AngleMode.DEGREES:
            self.calc.set_angle_mode(AngleMode.RADIANS)
            new_text = "라디안"
        else:
            self.calc.set_angle_mode(AngleMode.DEGREES)
            new_text = "도"

        # 버튼 텍스트 업데이트
        if '도/라디안' in self.buttons.buttons:
            self.buttons.buttons['도/라디안'].config(text=new_text)

    def _bind_keyboard(self) -> None:
        """키보드 이벤트 바인딩"""
        self.root.bind('<Key>', self._handle_key_press)

    def _handle_key_press(self, event) -> None:
        """키보드 입력 처리"""
        key = event.char

        if key.isdigit() or key == '.':
            self._handle_digit(key)
        elif key == '+':
            self._handle_operation(OperationType.ADD)
        elif key == '-':
            self._handle_operation(OperationType.SUBTRACT)
        elif key == '*':
            self._handle_operation(OperationType.MULTIPLY)
        elif key == '/':
            self._handle_operation(OperationType.DIVIDE)
        elif event.keysym == 'Return':
            self._handle_calculate()
        elif event.keysym == 'Escape':
            self._handle_clear()
        elif event.keysym == 'BackSpace':
            self._handle_backspace()
