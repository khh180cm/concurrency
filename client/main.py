"""
통합 클라이언트

서버 API를 호출하고 다양한 데이터 처리 작업을 수행합니다.
"""

import asyncio
import os
import random
import time
from typing import Callable

import aiohttp

API_BASE_URL = os.getenv("API_BASE_URL", "http://api-server:8000")

# 시나리오별 호출 횟수 상수
MINIMUM_CALL_COUNT = 5
MODERATE_CALL_COUNT = 50
MAXIMUM_CALL_COUNT = 1000


def simple_computation() -> int:
    """즉시 완료 - 단순 덧셈"""
    return 1 + 1


async def io_bound_async() -> dict:
    """non-blocking I/O Bound 작업 (0-3초)"""
    delay = random.uniform(0, 3.0)
    await asyncio.sleep(delay)
    return {"type": "non-blocking I/O Bound", "delay": round(delay, 3)}


def cpu_bound() -> dict:
    """CPU Bound 작업 (0-3초)"""
    start = time.time()
    n = random.randint(25, 32)

    def fibonacci(num):
        if num <= 1:
            return num
        return fibonacci(num - 1) + fibonacci(num - 2)

    _ = fibonacci(n)
    elapsed = time.time() - start

    return {"type": "CPU Bound", "fib_input": n, "time": round(elapsed, 3)}


async def call_api(session: aiohttp.ClientSession, endpoint: str) -> dict:
    """
    API 호출

    Args:
        session: aiohttp 세션
        endpoint: API 엔드포인트

    Returns:
        dict: API 응답
    """
    url = f"{API_BASE_URL}{endpoint}"

    try:
        async with session.get(url) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}


async def execute_scenario(
    api_endpoint: str, count: int, processing_func: Callable, description: str
) -> None:
    """
    시나리오 실행

    선택한 시나리오에 따라 서버에 API 요청을 보내고 클라이언트 작업을 수행합니다.

    Args:
        api_endpoint: API 엔드포인트
        count: 호출 횟수
        processing_func: 클라이언트 측 데이터 처리 함수
        description: 시나리오 설명
    """
    print(f"\n{'='*70}")
    print(f"시나리오: {description}")
    print(f"API: {api_endpoint}, 호출 횟수: {count}")
    print(f"{'='*70}\n")

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(count):
            task = process_request(session, api_endpoint, processing_func, i + 1)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

    total_time = time.time() - start_time

    success_count = sum(
        1 for r in results if not isinstance(r, Exception) and "error" not in r
    )

    print(f"\n{'='*70}")
    print(f"= 🍺 시나리오 완료")
    print(f"{'='*70}")
    print(f"= 시나리오: {description}")
    print(f"= 총 실행 시간: {total_time:.3f}초")
    print(f"= 성공: {success_count}/{count}")
    print(f"= 평균 시간: {total_time/count:.3f}초/요청")
    print(f"{'='*70}\n")


async def process_request(
    session: aiohttp.ClientSession,
    endpoint: str,
    processing_func: Callable,
    request_num: int,
) -> dict:
    """
    단일 요청 처리

    서버에 API 요청을 보내고, 응답을 받은 후 클라이언트 후속 작업 계속 진행

    Args:
        session: aiohttp 세션
        endpoint: API 엔드포인트
        processing_func: 클라이언트 측 데이터 처리 함수
        request_num: 요청 번호

    Returns:
        dict: 처리 결과
    """
    request_start = time.time()

    _ = await call_api(session, endpoint)
    api_time = time.time() - request_start

    processing_start = time.time()

    if asyncio.iscoroutinefunction(processing_func):
        processing_result = await processing_func()
    else:
        processing_result = processing_func()

    processing_time = time.time() - processing_start
    total_time = time.time() - request_start

    result = {
        "request_num": request_num,
        "api_time": round(api_time, 3),
        "processing_time": round(processing_time, 3),
        "total_time": round(total_time, 3),
        "processing_result": processing_result,
    }

    print(
        f"요청 #{request_num:3d} | API: {api_time:5.3f}초 | 처리: {processing_time:5.3f}초 | 전체: {total_time:5.3f}초"
    )

    return result


def show_menu() -> None:
    """메뉴 출력"""
    print("\n" + "=" * 70)
    print("동시성 API 학습 클라이언트")
    print("=" * 70)
    print(
        f"1. 클라이언트: 즉시 완료 ({MODERATE_CALL_COUNT}회), 서버: API 1 (즉시 응답)"
    )
    print(
        f"2. 클라이언트: Non-blocking I/O ({MODERATE_CALL_COUNT}회), 서버: API 1 (즉시 응답)"
    )
    print(f"3. 클라이언트: CPU 작업 ({MINIMUM_CALL_COUNT}회), 서버: API 1 (즉시 응답)")
    print(f"4. 클라이언트: CPU 작업 ({MAXIMUM_CALL_COUNT}회), 서버: API 1 (즉시 응답)")
    print(
        f"5. 클라이언트: 즉시 완료 ({MODERATE_CALL_COUNT}회), 서버: API 2 (비동기 I/O)"
    )
    print(
        f"6. 클라이언트: Non-blocking I/O ({MODERATE_CALL_COUNT}회), 서버: API 2 (비동기 I/O)"
    )
    print(f"7. 클라이언트: CPU 작업 ({MINIMUM_CALL_COUNT}회), 서버: API 2 (비동기 I/O)")
    print(f"8. 클라이언트: CPU 작업 ({MAXIMUM_CALL_COUNT}회), 서버: API 2 (비동기 I/O)")
    print("0. 종료")
    print("=" * 70)


async def run_selected_case(choice: str) -> None:
    """
    선택한 시나리오 실행

    Args:
        choice: 메뉴 선택
    """
    scenarios = {
        "1": (
            "/api1",
            MODERATE_CALL_COUNT,
            simple_computation,
            f"클라이언트: 즉시 완료 ({MODERATE_CALL_COUNT}회), 서버: API 1",
        ),
        "2": (
            "/api1",
            MODERATE_CALL_COUNT,
            io_bound_async,
            f"클라이언트: I/O Bound ({MODERATE_CALL_COUNT}회), 서버: API 1",
        ),
        "3": (
            "/api1",
            MINIMUM_CALL_COUNT,
            cpu_bound,
            f"클라이언트: CPU Bound ({MINIMUM_CALL_COUNT}회), 서버: API 1",
        ),
        "4": (
            "/api1",
            MAXIMUM_CALL_COUNT,
            cpu_bound,
            f"클라이언트: CPU Bound ({MAXIMUM_CALL_COUNT}회), 서버: API 1",
        ),
        "5": (
            "/api2",
            MODERATE_CALL_COUNT,
            simple_computation,
            f"클라이언트: 즉시 완료 ({MODERATE_CALL_COUNT}회), 서버: API 2",
        ),
        "6": (
            "/api2",
            MODERATE_CALL_COUNT,
            io_bound_async,
            f"클라이언트: I/O Bound ({MODERATE_CALL_COUNT}회), 서버: API 2",
        ),
        "7": (
            "/api2",
            MINIMUM_CALL_COUNT,
            cpu_bound,
            f"클라이언트: CPU Bound ({MINIMUM_CALL_COUNT}회), 서버: API 2",
        ),
        "8": (
            "/api2",
            MAXIMUM_CALL_COUNT,
            cpu_bound,
            f"클라이언트: CPU Bound (무제한={MAXIMUM_CALL_COUNT}회), 서버: API 2",
        ),
    }

    if choice in scenarios:
        endpoint, count, func, desc = scenarios[choice]
        await execute_scenario(endpoint, count, func, desc)
    else:
        print("\n❌ 잘못된 선택입니다. 0-8 사이의 숫자를 입력하세요.\n")


async def main():
    """메인 함수"""
    while True:
        show_menu()
        choice = input("\n선택 (0-8): ").strip()

        if choice == "0":
            print("\n종료합니다.\n")
            break

        await run_selected_case(choice)


if __name__ == "__main__":
    asyncio.run(main())
