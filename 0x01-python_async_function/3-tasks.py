#!/usr/bin/env python3
''' Even tasks have a type '''

import asyncio
Task = asyncio.Task

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> Task:
    ''' returns a task '''
    return asyncio.create_task(wait_random(max_delay))
