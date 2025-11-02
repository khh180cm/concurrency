"""
asyncio는 async/await 구문을 사용하여 동시성 코드를 작성하는 라이브러리입니다.

asyncio는 고성능 네트워크 및 웹 서버, 데이터베이스 연결 라이브러리, 분산 작업 큐 등을 제공하는 여러 파이썬 비동기 프레임워크의 기반으로 사용됩니다.

asyncio는 종종 IO 병목이면서 고수준의 구조화된 네트워크 코드에 가장 적합합니다.

asyncio는 async/await 구문을 사용하여 동시성 코드를 작성할 수 있게 해주는 모듈로, asyncio를 사용하면 단일 스레드 작업을 병렬로 처리할 수 있다.

파이썬 3.7 버전 이상부터 사용할 수 있다.
"""

import asyncio


async def main():
    print("Hello, ")
    await asyncio.sleep(2)
    print("World!")


# if __name__ == "__main__":
#     asyncio.run(main())


"""
문제 1.
다음은 서로 다른 입력 값으로 sum() 함수를 2번 수행하여 결괏값을 출력하는 파이썬 프로그램이다.
"""

# async def sum_numbers(a:int, b: int) -> int:
#     return a + b

# async def main():
#     tasks = [sum_numbers(1, 2), sum_numbers(3, 4),]
#     results = await asyncio.gather(*tasks)
#     print(results)


# if __name__ == "__main__":
#     asyncio.run(main())

# import time


# def sleep(seconds: int | None = None) -> None:
#     if seconds:
#         time.sleep(seconds)
#     else:
#         time.sleep(1)


# def sum_numbers(name: str, numbers):
#     start = time.time()
#     total = 0
#     for number in numbers:
#         sleep()
#         total += number
#         print(f'작업중={name}, number={number}, total={total}')
#     end = time.time()
#     print(f'작업명={name}, 걸린시간={end-start}')
#     return total


# def main():
#     start = time.time()

#     result1 = sum_numbers("A", [1, 2])
#     result2 = sum_numbers("B", [1, 2, 3])

#     end = time.time()
#     print(f'총합={result1+result2}, 총시간={end-start}')


# if __name__ == "__main__":
#     main()

import asyncio
import time


async def sleeping():
    asyncio.sleep(1)


async def sum_numbers(name: str, numbers: list) -> int:
    start = time.time()
    total = 0
    for number in numbers:
        total += number
        print(f"작업중={name}, number={number}, total={total}")
    end = time.time()
    print(f"작업명={name}, 걸린시간={end-start}")
    return total


"""
함수를 비동기로 호출하려면 이렇게 def 앞에 async라는 키워드를 넣으면 된다. 
그러면 이제 이 함수는 비동기 함수가 된다. 
이때 async를 적용한 비동기 함수를 코루틴이라 부른다.

또한, 코루틴 안에서 다른 코루틴을 호출할 때는 await sleep()과 같이 await를 함수명 앞에 붙여 호출해야 한다. 
코루틴 수행 중 await 코루틴을 만나면 await로 호출한 코루틴이 종료될 때까지 기다리지 않고 
제어권을 메인 스레드나 다른 코루틴으로 넘긴다. 
이러한 방식을 non-blocking이라 한다. 
그리고 호출한 코루틴이 종료되면 이벤트에 의해 다시 그 이후 작업이 수행된다.
"""


async def main():
    start = time.time()
    """
    asyncio.create_task()는 수행할 코루틴 작업(태스크)을 생성한다. 
    여기서는 작업을 생성할 뿐이지 실제로 코루틴이 수행되는 것은 아니다. 
    실제 코루틴 실행은 await 태스크가 담당한다. 
    그리고 실행 태스크의 결괏값은 태스크.result()로 얻을 수 있다.
    """
    task1 = asyncio.create_task(sum_numbers("A", [1, 2]))
    task2 = asyncio.create_task(sum_numbers("B", [1, 2, 3]))

    await task1
    await task2

    result1 = task1.result()
    result2 = task2.result()

    end = time.time()
    print(f"총합={result1+result2}, 총시간={end-start}")


if __name__ == "__main__":
    """
    asyncio.run(main())은 런 루프를 생성하여 main() 코루틴을 실행한다.
    코루틴을 실행하려면 런 루프가 반드시 필요하다.
    코루틴이 모두 비동기적으로 실행되기 때문에 그 시작과 종료를 감지할 수 있는 이벤트 루프가 반드시 필요하기 때문이다.
    """
    asyncio.run(main())
