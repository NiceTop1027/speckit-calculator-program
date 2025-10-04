"""
계산 히스토리 관리
Calculation history management
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass
class HistoryEntry:
    """개별 계산 기록"""
    expression: str
    result: Decimal
    timestamp: datetime


class CalculationHistory:
    """세션 내 계산 히스토리 관리"""

    def __init__(self, max_size: int = 100):
        self.entries: List[HistoryEntry] = []
        self.max_size = max_size

    def add_entry(self, expression: str, result: Decimal) -> None:
        """새 계산 추가"""
        entry = HistoryEntry(
            expression=expression,
            result=result,
            timestamp=datetime.now()
        )
        self.entries.append(entry)

        # 최대 개수 초과 시 가장 오래된 항목 삭제
        if len(self.entries) > self.max_size:
            self.entries.pop(0)

    def clear(self) -> None:
        """히스토리 전체 삭제"""
        self.entries.clear()

    def get_recent(self, n: int) -> List[HistoryEntry]:
        """최근 n개 항목 조회"""
        return self.entries[-n:] if n > 0 else []
