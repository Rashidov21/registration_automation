import random

class ProxyManager:
    def __init__(self, proxies=None, rotation_every=10):
        self.proxies = proxies or []
        self.rotation_every = rotation_every
        self.index = -1

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.proxies = [line.strip() for line in f if line.strip()]

    def get_proxy(self, account_idx):
        if not self.proxies:
            return None

        if account_idx % self.rotation_every == 0:
            self.index = (self.index + 1) % len(self.proxies)
        return self.proxies[self.index]

    def should_rotate(self, n):
        return n > 0 and n % self.rotation_every == 0
