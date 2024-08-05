import asyncio
import random


class Fork:
    def __init__(self, id_):
        self.id = id_
        self.lock = asyncio.Lock()


class Philosopher:
    def __init__(self, id_, left_fork, right_fork):
        self.id = id_
        self.left_fork = left_fork
        self.right_fork = right_fork

    async def take_a_dinner(self):
        while True:
            await self.think()
            await self.eat()

    async def think(self):
        print(f'Філософ {self.id} думає.')
        await asyncio.sleep(random.uniform(1, 3))

    async def eat(self):
        async with self.left_fork.lock:
            print(f'Філософ {self.id} взяв ліву вилку {self.left_fork.id}.')
            async with self.right_fork.lock:
                print(f'Філософ {self.id} взяв праву вилку {self.right_fork.id}.')
                print(f'Філософ {self.id} їсть.')
                await asyncio.sleep(random.uniform(1, 3))
                print(f'Філософ {self.id} поклав праву вилку {self.right_fork.id}.')
            print(f'Філософ {self.id} поклав ліву вилку {self.left_fork.id}.')


async def main():
    forks = [Fork(i) for i in range(5)]
    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % 5]) for i in range(5)
    ]

    tasks = [
        asyncio.create_task(philosopher.take_a_dinner()) for philosopher in philosophers
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
