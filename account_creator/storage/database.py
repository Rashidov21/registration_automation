import sqlite3
import threading
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'data.db'

class Status:
    PENDING = 'pending'
    REGISTERED = 'registered'
    VERIFIED = 'verified'
    COMPLETED = 'completed'
    FAILED = 'failed'
    BANNED = 'banned'
    SKIPPED = 'skipped'

class Database:
    def __init__(self, path: str = None):
        self.db_path = Path(path) if path else DB_PATH
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        self.init()

    def init(self):
        with self.lock, self.conn:
            self.conn.execute(
                '''CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                status TEXT,
                retries INTEGER DEFAULT 0,
                worker TEXT,
                error TEXT
                )'''
            )
            self.conn.execute(
                '''CREATE TABLE IF NOT EXISTS action_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                action TEXT,
                result TEXT,
                details TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )'''
            )

    def add_account(self, email, password, first_name='', last_name=''):
        with self.lock, self.conn:
            self.conn.execute(
                'INSERT OR IGNORE INTO accounts (email, password, first_name, last_name, status) VALUES (?, ?, ?, ?, ?)',
                (email, password, first_name, last_name, Status.PENDING),
            )

    def update_status(self, account_id, status, error_message=None):
        with self.lock, self.conn:
            self.conn.execute(
                'UPDATE accounts SET status=?, error=? WHERE id=?',
                (status, error_message, account_id),
            )

    def update_profile(self, account_id, **kwargs):
        if not kwargs:
            return
        keys = ','.join(f'{k}=?' for k in kwargs)
        values = list(kwargs.values())
        with self.lock, self.conn:
            self.conn.execute(f'UPDATE accounts SET {keys} WHERE id=?', (*values, account_id))

    def increment_retry(self, account_id):
        with self.lock, self.conn:
            self.conn.execute('UPDATE accounts SET retries=retries+1 WHERE id=?', (account_id,))

    def set_worker(self, account_id, worker_id):
        with self.lock, self.conn:
            self.conn.execute('UPDATE accounts SET worker=? WHERE id=?', (str(worker_id), account_id))

    def get_pending(self, limit=100):
        with self.lock:
            cur = self.conn.execute('SELECT * FROM accounts WHERE status=? ORDER BY id ASC LIMIT ?', (Status.PENDING, limit))
            return [dict(row) for row in cur.fetchall()]

    def get_stats(self):
        with self.lock:
            cur = self.conn.execute('SELECT status, COUNT(*) as cnt FROM accounts GROUP BY status')
            return {row['status']: row['cnt'] for row in cur.fetchall()}

    def get_account(self, account_id):
        with self.lock:
            cur = self.conn.execute('SELECT * FROM accounts WHERE id=?', (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def export_completed(self):
        with self.lock:
            cur = self.conn.execute('SELECT * FROM accounts WHERE status=?', (Status.COMPLETED,))
            return [dict(row) for row in cur.fetchall()]

    def log_action(self, account_id, action, result, details=''):
        with self.lock, self.conn:
            self.conn.execute(
                'INSERT INTO action_logs (account_id, action, result, details) VALUES (?, ?, ?, ?)',
                (account_id, action, result, details),
            )

    def get_logs(self, account_id):
        with self.lock:
            cur = self.conn.execute('SELECT * FROM action_logs WHERE account_id=? ORDER BY id ASC', (account_id,))
            return [dict(row) for row in cur.fetchall()]
