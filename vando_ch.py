# 공정 조건: 공정명 → (최소 온도, 최대 온도, 최소 시간)
process_conditions = {
    "산화": (1000, 1200, 30),     # 단위: °C, 분
    "식각": (300, 600, 10),
    "증착": (500, 700, 20),
    "이온주입": (25, 300, 5)
}

# 수율 계산 함수
def calculate_yield(process, temp, time):
    min_temp, max_temp, min_time = process_conditions[process]
    yield_rate = 100.0

    if temp < min_temp:
        yield_rate -= (min_temp - temp) * 1.5
    elif temp > max_temp:
        yield_rate -= (temp - max_temp) * 1.5

    if time < min_time:
        yield_rate -= (min_time - time) * 2.0

    return max(0.0, round(yield_rate, 1))

# 프로그램 실행
print("=== 반도체 공정 시뮬레이터: 수율 기반 모델 ===")
print("가능한 공정: 산화, 식각, 증착, 이온주입")

# 공정 개수 입력 (예외 처리 포함)
while True:
    try:
        n = int(input("수행할 공정 개수 입력 (1~4): "))
        if 1 <= n <= 4:
            break
        else:
            print("⚠️ 1~4 사이의 정수를 입력하세요.")
    except ValueError:
        print("⚠️ 숫자만 입력하세요. 예: 2")

results = []

for i in range(n):
    print(f"\n[{i+1}번째 공정]")
    process = input("공정명 입력: ").strip()

    if process not in process_conditions:
        print("⚠️ 유효하지 않은 공정입니다. 건너뜁니다.")
        continue

    min_temp, max_temp, min_time = process_conditions[process]
    print(f"ℹ️ {process} 공정 조건 → 온도: {min_temp}~{max_temp}°C, 시간: {min_time}분 이상")

    # 온도 입력 (현실적 범위 검사)
    try:
        temp = int(input("온도 입력(°C): "))
        if not (0 <= temp <= 1500):
            print("⚠️ 온도는 0~1500°C 사이여야 합니다. 공정 스킵합니다.")
            continue
    except ValueError:
        print("⚠️ 숫자를 입력해야 합니다. 공정 스킵합니다.")
        continue

    # 시간 입력 (현실적 범위 검사)
    try:
        time = int(input("처리 시간 입력(분): "))
        if not (0 <= time <= 300):
            print("⚠️ 시간은 0~300분 사이여야 합니다. 공정 스킵합니다.")
            continue
    except ValueError:
        print("⚠️ 숫자를 입력해야 합니다. 공정 스킵합니다.")
        continue

    # 수율 계산
    yield_rate = calculate_yield(process, temp, time)

    # 수율 평가 기준
    if yield_rate >= 90:
        status = "정상 생산 (우수)"
    elif yield_rate >= 80:
        status = "정상 생산"
    elif yield_rate >= 60:
        status = "부분 불량 발생"
    else:
        status = "생산 실패"

    results.append((process, temp, time, yield_rate, status))

# 결과 출력
print("\n📋 [공정 결과 요약]")
for idx, (proc, temp, time, rate, status) in enumerate(results):
    print(f"{idx+1}. {proc} | 온도: {temp}°C | 시간: {time}분 → 수율: {rate}% → {status}")
