#!/usr/bin/env python3
''' The basics of async '''

import asyncio
from random import uniform


async def wait_random(max_delay=10):
    ''' waits for a random delay between 0 and max_delay '''
    random_time = uniform(0, max_delay)
    await asyncio.sleep(random_time)
    return random_time
