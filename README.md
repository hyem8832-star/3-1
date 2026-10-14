# 월별 항공 승객 수 시계열 분석

## 실행 방법

```bash
python analysis.py
```

외부 패키지를 설치할 필요 없이 Python 표준 라이브러리만으로 실행됩니다.

실행하면 `images/`에 분석 그래프 3개가 생성됩니다. 자세한 분석은 [REPORT.md](REPORT.md)를 참고하세요.

## 데이터 출처

`data/airline_passengers.csv`는 Box and Jenkins의 월별 국제 항공 승객 수 데이터(AirPassengers)를 분석용 CSV로 정리한 것입니다. 기간은 1949년 1월부터 1960년 12월까지이며 단위는 천 명입니다. 교육 및 분석 목적으로 사용했습니다.
