import argparse
import asyncio
from account_creator.config.settings import settings
from account_creator.storage.database import Database
from account_creator.workers.task_queue import TaskQueueManager


def seed_accounts(db, count):
    for i in range(count):
        db.add_account(f'user{i}@example.com', 'P@ssw0rd123!', 'Auto', 'User')


async def run_engine(args):
    db = Database()

    if args.count > 0:
        seed_accounts(db, args.count)

    if args.stats:
        print(db.get_stats())
        return

    manager = TaskQueueManager(db, settings)
    await manager.run(args.workers)

    if args.export:
        import csv

        with open('export.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'status'])
            writer.writeheader()
            for row in db.export_completed():
                writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description='Account Creator Automation')
    parser.add_argument('--count', type=int, default=0)
    parser.add_argument('--workers', type=int, default=settings.MAX_WORKERS)
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--stats', action='store_true')
    parser.add_argument('--export', action='store_true')
    args = parser.parse_args()

    settings.BROWSER_HEADLESS = args.headless
    asyncio.run(run_engine(args))


if __name__ == '__main__':
    main()