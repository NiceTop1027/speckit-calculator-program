"""
Integration test: Scenario 3 - Chained Calculation
통합 테스트: 시나리오 3 - 연속 계산
"""
from src.core.calculator import Calculator
from src.core.enums import OperationType


def test_chained_calculation_scenario():
    """5 + 3 = 8, 8 × 2 = 16 연속 계산 시나리오 테스트"""
    calc = Calculator()

    # 첫 번째 계산: 5 + 3 = 8
    calc.input_digit('5')
    calc.input_operation(OperationType.ADD)
    calc.input_digit('3')
    result1 = calc.calculate()
    assert result1 == "8"

    # 두 번째 계산: 8 × 2 = 16 (이전 결과 활용)
    calc.input_operation(OperationType.MULTIPLY)
    calc.input_digit('2')
    result2 = calc.calculate()
    assert result2 == "16"

    # 히스토리 확인
    history = calc.get_history()
    assert len(history) == 2
    assert history[0].expression == "5 + 3"
    assert history[1].expression == "8 × 2"
