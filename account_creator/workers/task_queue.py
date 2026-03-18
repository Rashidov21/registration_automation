import asyncio
from .worker import Worker

class TaskQueueManager:
    def __init__(self, db, settings):
        self.db = db
        self.settings = settings

    def prepare_queue(self):
        pending = self.db.get_pending(1000)
        q = asyncio.Queue()
        for account in pending:
            q.put_nowait(account)
        return q

    async def run(self, num_workers=None):
        num_workers = num_workers or self.settings.MAX_WORKERS
        queue = self.prepare_queue()
        tasks = []
        for i in range(num_workers):
            tasks.append(asyncio.create_task(Worker(i, queue, self.db, self.settings).run()))

        await queue.join()

        for task in tasks:
            task.cancel()
