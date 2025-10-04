"""
Integration test: Scenario 1 - Basic Arithmetic
통합 테스트: 시나리오 1 - 기본 사칙연산
"""
from src.core.calculator import Calculator
from src.core.enums import OperationType


def test_basic_addition_scenario():
    """5 + 3 = 8 전체 시나리오 테스트"""
    calc = Calculator()

    # 5 입력
    assert calc.input_digit('5') == "5"

    # + 연산자
    assert calc.input_operation(OperationType.ADD) == "5"

    # 3 입력
    assert calc.input_digit('3') == "3"

    # = 계산
    result = calc.calculate()
    assert result == "8"

    # 히스토리 확인
    history = calc.get_history()
    assert len(history) == 1
    assert history[0].expression == "5 + 3"
    assert str(history[0].result) == "8"
