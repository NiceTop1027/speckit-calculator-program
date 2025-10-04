"""
Integration test: Scenario 4 - Memory Functions
통합 테스트: 시나리오 4 - 메모리 기능
"""
from src.core.calculator import Calculator


def test_memory_functions_scenario():
    """MS, M+, MR, MC 메모리 기능 전체 시나리오 테스트"""
    calc = Calculator()

    # 25 입력 후 MS (메모리 저장)
    calc.input_digit('2')
    calc.input_digit('5')
    calc.memory_store()
    assert calc.memory_state.is_empty is False

    # 100 입력 후 M+ (메모리에 더하기)
    calc.input_digit('1')
    calc.input_digit('0')
    calc.input_digit('0')
    calc.memory_add()

    # CE (전체 지우기)
    calc.clear_all()
    assert calc.get_display() == "0"

    # MR (메모리 불러오기) → 25 + 100 = 125
    result = calc.memory_recall()
    assert result == "125"

    # MC (메모리 지우기)
    calc.memory_clear()
    assert calc.memory_state.is_empty is True
