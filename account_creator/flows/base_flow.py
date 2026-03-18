from abc import ABC, abstractmethod

class BaseFlow(ABC):
    def __init__(self, driver, db, account_id):
        self.driver = driver
        self.db = db
        self.account_id = account_id

    @abstractmethod
    async def run(self, *args, **kwargs):
        raise NotImplementedError

    def log(self, message):
        print(f'[Flow {self.__class__.__name__}][{self.account_id}] {message}')

    def save_step(self, key, value):
        self.db.update_profile(self.account_id, **{key: value})
