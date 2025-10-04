"""
계산기 애플리케이션 진입점
Calculator application entry point
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.calculator import Calculator
from src.ui.main_window import MainWindow


def main():
    """메인 함수"""
    # Calculator 인스턴스 생성
    calc = Calculator()

    # MainWindow 생성 및 실행
    window = MainWindow(calc)
    window.run()


if __name__ == "__main__":
    main()
