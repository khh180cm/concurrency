import asyncio
import random
import time
from datetime import datetime

from fastapi import FastAPI

app = FastAPI(
    title="동시성 및 병렬성 API 서버",
    description="다양한 실행 패턴을 보여주는 FastAPI 서버",
    version="1.0.0",
)


@app.get("/")
async def root():
    """
    루트 엔드포인트

    Returns:
        dict: 서버 정보 및 사용 가능한 API 목록
    """
    return {
        "message": "동시성 및 병렬성 API 서버",
        "endpoints": {
            "API 1": "/api1 - 즉시 응답 (지연 없음)",
            "API 2": "/api2 - 비동기 I/O (asyncio.sleep, 0-3초)",
            "API 3": "/api3 - 동기 블로킹 I/O (time.sleep, 0-3초)",
            "API 4": "/api4 - CPU 집약적 연산 (약 0-3초)",
        },
    }


@app.get("/api1")
async def api1_instant():
    """
    API 1: 즉시 응답

    지연 없이 즉시 응답을 반환합니다.

    Returns:
        dict: API 정보 및 타임스탬프
    """
    return {
        "api": "API 1",
        "type": "instant",
        "description": "즉시 응답",
        "timestamp": datetime.now().isoformat(),
        "delay_seconds": 0,
        "message": "Success",
    }


@app.get("/api2")
async def api2_nonblocking():
    """
    API 2: 비동기 I/O (Non-blocking)

    asyncio.sleep()을 사용하여 non-blocking 방식으로 지연을 발생시킵니다.
    0-3초 사이의 랜덤한 지연 시간 동안 CPU를 다른 작업에 양보합니다.

    Returns:
        dict: API 정보, 지연 시간, 타임스탬프
    """
    delay = random.uniform(0, 3.0)
    start_time = datetime.now()

    await asyncio.sleep(delay)

    end_time = datetime.now()

    return {
        "api": "API 2",
        "type": "non-blocking I/O",
        "description": "비동기 I/O (asyncio.sleep)",
        "method": "asyncio.sleep()",
        "delay_seconds": round(delay, 3),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "message": "Success",
    }


@app.get("/api3")
def api3_blocking():
    """
    API 3: 동기 블로킹 I/O (Blocking)

    time.sleep()을 사용하여 blocking 방식으로 지연을 발생시킵니다.
    0-3초 사이의 랜덤한 지연 시간 동안 워커 스레드가 완전히 차단됩니다.

    Returns:
        dict: API 정보, 지연 시간, 타임스탬프
    """
    delay = random.uniform(0, 3.0)
    start_time = datetime.now()

    time.sleep(delay)

    end_time = datetime.now()

    return {
        "api": "API 3",
        "type": "blocking I/O",
        "description": "동기 블로킹 I/O (time.sleep)",
        "method": "time.sleep()",
        "delay_seconds": round(delay, 3),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "message": "Success",
    }


def fibonacci(n: int) -> int:
    """
    피보나치 수 계산 (재귀 방식)

    CPU 집약적인 재귀 계산을 수행합니다.

    Args:
        n: 피보나치 수열의 n번째 값

    Returns:
        int: n번째 피보나치 수
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def prime_factors(n: int) -> list:
    """
    소인수분해

    주어진 숫자의 소인수를 찾는 CPU 집약적 작업을 수행합니다.

    Args:
        n: 소인수분해할 정수

    Returns:
        list: 소인수 리스트
    """
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors


@app.get("/api4")
async def api4_cpu_bound():
    """
    API 4: CPU 집약적 연산

    실제 CPU 집약적인 계산을 수행합니다.
    피보나치 계산과 소인수분해를 통해 약 0-3초 정도 소요됩니다.

    Returns:
        dict: API 정보, 연산 결과, 소요 시간
    """
    start_time = datetime.now()

    # 피보나치 입력값 조정으로 연산 시간 제어 (약 0-3초)
    fib_input = random.randint(30, 37)

    # CPU 집약적 연산
    fib_result = fibonacci(fib_input)

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    return {
        "api": "API 4",
        "type": "CPU-bound",
        "description": "CPU 연산 작업",
        "computations": {
            "fibonacci": {
                "input": fib_input,
                "result": fib_result,
                "result_length": len(str(fib_result)),
            }
        },
        "computation_time": round(elapsed, 3),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "message": "Success",
    }
