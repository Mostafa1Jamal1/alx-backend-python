#!/usr/bin/env python3
''' Let's execute multiple coroutines at the same time with async '''

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    ''' return the list of all the delays '''
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = []
    for task in asyncio.as_completed(tasks):
        delays.append(await task)
    return delays
