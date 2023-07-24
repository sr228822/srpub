#!/usr/bin/env python

import asyncio
import time
import random
import contextvars
import functools


async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()

    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

class Transformer:
    def __init__(self):
        self.last_status = None
        self.work_task = None

        self.loop = asyncio.get_running_loop()

    def _heavy_io(self):
        delay = 4 + int(random.random() * 3)
        print(f"starting simulated-blocking-IO sleep {delay}")
        time.sleep(delay)
        print(f"finished simulated-blocking-IO")
        self.last_status = "foo-status"
        return "foo-model"

    def stream_transform(self):
        if self.work_task is None:
            print('creating task')
            self.work_task = self.loop.create_task(to_thread(self._heavy_io))
            return
        elif not self.work_task.done():
            print(f'task {self.work_task.__class__} not-done')
            return
        else:
            # do something with self.work_task.result()
            print(f'task {self.work_task.__class__} done!')
            result = self.work_task.result()
            print('result is ', result)
            self.work_task = None




async def main():

    t = Transformer()

    # Poll status
    while True:
        res = t.stream_transform()
        print(f"stream_transform res {res} last_status {t.last_status}")
        await asyncio.sleep(0.5)

asyncio.run(main())
