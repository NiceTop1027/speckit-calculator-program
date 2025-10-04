"""
Integration test: Scenario 2 - Division by Zero
통합 테스트: 시나리오 2 - 0으로 나누기 에러 처리
"""
import pytest
from src.core.calculator import Calculator
from src.core.enums import OperationType


def test_division_by_zero_scenario():
    """10 ÷ 0 에러 처리 시나리오 테스트"""
    calc = Calculator()

    # 10 입력
    calc.input_digit('1')
    assert calc.input_digit('0') == "10"

    # ÷ 연산자
    assert calc.input_operation(OperationType.DIVIDE) == "10"

    # 0 입력
    assert calc.input_digit('0') == "0"

    # = 계산 시 에러 발생
    with pytest.raises(ZeroDivisionError, match="0으로 나눌 수 없습니다"):
        calc.calculate()
