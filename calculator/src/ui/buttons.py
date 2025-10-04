"""
계산기 버튼 레이아웃
Calculator button layout
"""
import tkinter as tk
from typing import Callable, Dict
from ..core.enums import CalculatorMode


class ButtonLayout:
    """버튼 레이아웃 관리"""

    def __init__(self, parent):
        self.parent = parent
        self.buttons: Dict[str, tk.Button] = {}
        self.button_frame = None

    def create_standard_buttons(self, handlers: Dict[str, Callable]) -> None:
        """표준 모드 버튼 생성"""
        if self.button_frame:
            self.button_frame.destroy()

        self.button_frame = tk.Frame(self.parent, bg='#F0F0F0')
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 버튼 레이아웃 정의 (5x6 그리드)
        layout = [
            ['MC', 'MR', 'M+', 'M-', 'MS'],
            ['C', 'CE', '←', '%', '√'],
            ['7', '8', '9', '÷', 'x²'],
            ['4', '5', '6', '×', '1/x'],
            ['1', '2', '3', '-', '+/-'],
            ['0', '.', '=', '+', '']
        ]

        # 버튼 생성
        for row_idx, row in enumerate(layout):
            for col_idx, text in enumerate(row):
                if not text:
                    continue

                # 버튼 스타일
                if text in '0123456789.':
                    bg = '#FAFAFA'  # 숫자 버튼
                elif text in ['=']:
                    bg = '#0078D4'  # = 버튼
                    fg = 'white'
                elif text in ['+', '-', '×', '÷']:
                    bg = '#E0E0E0'  # 연산자 버튼
                elif text in ['C', 'CE', '←']:
                    bg = '#D0D0D0'  # 기능 버튼
                else:
                    bg = '#E8E8E8'  # 기타

                btn = tk.Button(
                    self.button_frame,
                    text=text,
                    font=("맑은 고딕", 12),
                    width=7,
                    height=2,
                    bg=bg if text != '=' else bg,
                    fg='white' if text == '=' else 'black'
                )
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')

                # 핸들러를 나중에 바인딩
                if text in handlers:
                    btn.config(command=handlers[text])

                self.buttons[text] = btn

        # 그리드 가중치 설정
        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)

    def create_scientific_buttons(self, handlers: Dict[str, Callable]) -> None:
        """공학용 모드 확장 버튼 생성"""
        # 표준 버튼 먼저 생성
        self.create_standard_buttons(handlers)

        # 공학용 확장 버튼 프레임
        sci_frame = tk.Frame(self.parent)
        sci_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 공학용 버튼 레이아웃
        sci_layout = [
            ['π', 'e', 'sin', 'cos', 'tan'],
            ['asin', 'acos', 'atan', 'log', 'ln'],
            ['eˣ', '10ˣ', 'n!', '(', ')'],
            ['도/라디안', '', '', '', '']
        ]

        for row_idx, row in enumerate(sci_layout):
            for col_idx, text in enumerate(row):
                if not text:
                    continue

                btn = tk.Button(
                    sci_frame,
                    text=text,
                    font=("맑은 고딕", 10),
                    width=7,
                    height=1,
                    bg='#F0F0F0'
                )
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')

                if text in handlers:
                    btn.config(command=handlers[text])

                self.buttons[text] = btn

        for i in range(4):
            sci_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            sci_frame.grid_columnconfigure(i, weight=1)

    def bind_button(self, button_id: str, handler: Callable) -> None:
        """버튼 이벤트 핸들러 바인딩"""
        if button_id in self.buttons:
            self.buttons[button_id].config(command=handler)
