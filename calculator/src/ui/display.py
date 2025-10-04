"""
계산기 디스플레이 위젯
Calculator display widget
"""
import tkinter as tk
from decimal import Decimal


class DisplayWidget:
    """디스플레이 위젯"""

    def __init__(self, parent):
        self._text = tk.StringVar(value="0")
        self.display = tk.Entry(
            parent,
            textvariable=self._text,
            font=("맑은 고딕", 24),
            justify='right',
            bd=2,
            relief='sunken',
            bg='white',
            fg='black',
            state='normal'
        )
        self.display.pack(fill=tk.BOTH, padx=10, pady=10)
        self.display.config(state='readonly')

    @property
    def text(self) -> str:
        """현재 표시 중인 텍스트"""
        return self._text.get()

    @text.setter
    def text(self, value: str) -> None:
        """텍스트 설정"""
        self._text.set(value)

    def format_number(self, value: Decimal) -> str:
        """숫자를 디스플레이 형식으로 변환"""
        # 정수면 소수점 없이
        if value == int(value):
            result = str(int(value))
        else:
            # 불필요한 trailing 0 제거
            result = str(value)
            if '.' in result:
                result = result.rstrip('0').rstrip('.')

        # 천 단위 구분 쉼표 (정수만)
        if '.' not in result and 'e' not in result.lower():
            try:
                num = int(result)
                result = f"{num:,}"
            except:
                pass

        # 과학적 표기법 (너무 크거나 작은 수)
        abs_value = abs(value)
        if abs_value > 1e10 or (abs_value < 1e-10 and abs_value != 0):
            result = f"{float(value):.10e}"

        # 최대 15자리 유효숫자
        if len(result) > 15 and ',' not in result:
            result = result[:15]

        return result
