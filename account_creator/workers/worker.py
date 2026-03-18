import asyncio
from loguru import logger
from ..core.email_service import EmailService
from ..flows.registration import RegistrationFlow
from ..flows.verification import VerificationFlow
from ..flows.profile import ProfileFlow

class Worker:
    def __init__(self, worker_id, queue, db, settings, proxy=None):
        self.worker_id = worker_id
        self.queue = queue
        self.db = db
        self.settings = settings
        self.proxy = proxy

    async def run(self):
        from ..core.browser_driver import BrowserDriver

        while not self.queue.empty():
            account = self.queue.get_nowait()
            account_id = account['id']
            self.db.set_worker(account_id, self.worker_id)
            try:
                email = account['email']
                password = account['password']
                first_name = account['first_name']
                last_name = account['last_name']

                email_service = EmailService(self.settings)

                async with BrowserDriver(self.worker_id, self.proxy, self.settings) as driver:
                    reg = RegistrationFlow(driver, self.db, account_id)
                    ok = await reg.run(email, password, first_name, last_name)
                    if not ok:
                        raise RuntimeError('registration failed')
                    self.db.update_status(account_id, 'registered')

                    verification = VerificationFlow(driver, self.db, account_id)
                    # placeholder: in real scenario, you'd wait for email and fill code
                    success = await verification.run(code='0000')
                    if not success:
                        raise RuntimeError('verification failed')
                    self.db.update_status(account_id, 'verified')

                    profile = ProfileFlow(driver, self.db, account_id)
                    profile_ok = await profile.run(first_name, last_name)
                    if not profile_ok:
                        raise RuntimeError('profile update failed')

                    self.db.update_status(account_id, 'completed')

            except Exception as e:
                logger.error(f'Worker {self.worker_id} account {account_id} failed: {e}')
                self.db.increment_retry(account_id)
                self.db.update_status(account_id, 'failed', str(e))
            finally:
                self.queue.task_done()
