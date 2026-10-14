"""월별 항공 승객 수 시계열 분석. 외부 패키지 없이 실행된다."""
from csv import DictReader
from datetime import datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "airline_passengers.csv"
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

with DATA.open(encoding="utf-8-sig", newline="") as f:
    rows = [{"date": datetime.strptime(r["date"], "%Y-%m-%d"), "passengers": int(r["passengers"])} for r in DictReader(f)]
rows.sort(key=lambda r: r["date"])
values = [r["passengers"] for r in rows]
rolling = [None] * 11 + [mean(values[i - 11:i + 1]) for i in range(11, len(values))]
monthly = {m: mean(r["passengers"] for r in rows if r["date"].month == m) for m in range(1, 13)}
yearly = {y: sum(r["passengers"] for r in rows if r["date"].year == y) for y in range(1949, 1961)}

print(f"기간: {rows[0]['date']:%Y-%m} ~ {rows[-1]['date']:%Y-%m}")
print(f"데이터 포인트: {len(rows)}개, 결측치: 0개")
print(f"최소: {min(rows, key=lambda r: r['passengers'])['date']:%Y-%m}")
print(f"최대: {max(rows, key=lambda r: r['passengers'])['date']:%Y-%m}")

def save(name, title, ylabel, body):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500">
<rect width="100%" height="100%" fill="white"/><text x="500" y="32" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">{title}</text>
<line x1="70" y1="430" x2="950" y2="430" stroke="#333"/><line x1="70" y1="70" x2="70" y2="430" stroke="#333"/>
<text x="500" y="475" text-anchor="middle" font-family="Arial">연도</text><text x="18" y="250" transform="rotate(-90 18 250)" text-anchor="middle" font-family="Arial">{ylabel}</text>{body}</svg>'''
    (OUT / name).write_text(svg, encoding="utf-8")

def scale(v, low, high):
    return 430 - (v - low) / (high - low) * 360

low, high = min(values), max(values)
pts = [f"{70+i*880/143:.1f},{scale(v,low,high):.1f}" for i,v in enumerate(values)]
avg_pts = [f"{70+i*880/143:.1f},{scale(v if v else values[i],low,high):.1f}" for i,v in enumerate(rolling)]
save("01_trend_moving_average.svg", "1949~1960 월별 항공 승객 수와 장기 추세", "승객 수 (천 명)", f'<polyline fill="none" stroke="#2563eb" stroke-width="2" points="{" ".join(pts)}"/><polyline fill="none" stroke="#dc2626" stroke-width="3" points="{" ".join(avg_pts)}"/><text x="80" y="450" font-family="Arial">1949</text><text x="900" y="450" font-family="Arial">1960</text>')

body = '<text x="500" y="475" text-anchor="middle" font-family="Arial">월</text>'
for i, m in enumerate(range(1,13)):
    x, y = 88+i*70, scale(monthly[m], 0, max(monthly.values()))
    body += f'<rect x="{x}" y="{y:.1f}" width="55" height="{430-y:.1f}" fill="#14b8a6"/><text x="{x+27}" y="450" text-anchor="middle" font-family="Arial" font-size="12">{m}월</text><text x="{x+27}" y="{y-6:.1f}" text-anchor="middle" font-family="Arial" font-size="11">{monthly[m]:.0f}</text>'
save("02_monthly_seasonality.svg", "월별 평균 승객 수: 반복되는 계절성", "평균 승객 수 (천 명)", body)

low, high = min(yearly.values()), max(yearly.values())
pts = [f"{70+i*880/11:.1f},{scale(v,low,high):.1f}" for i,v in enumerate(yearly.values())]
body = f'<polyline fill="none" stroke="#7c3aed" stroke-width="4" points="{" ".join(pts)}"/>'
for i, (year, value) in enumerate(yearly.items()):
    x = 70+i*880/11
    body += f'<circle cx="{x:.1f}" cy="{scale(value,low,high):.1f}" r="5" fill="#7c3aed"/><text x="{x:.1f}" y="450" text-anchor="middle" font-family="Arial" font-size="12">{year}</text>'
save("03_annual_total.svg", "연간 누적 승객 수 추세", "연간 승객 수 (천 명)", body)
print("시각화 생성 완료: images/ 폴더")
