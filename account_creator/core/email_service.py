import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup

class TempEmailAccount:
    def __init__(self, email, password, token, account_id):
        self.email = email
        self.password = password
        self.token = token
        self.account_id = account_id

class EmailService:
    def __init__(self, settings):
        self.settings = settings

    async def create_account(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.settings.MAILTM_BASE_URL}/domains') as r:
                data = await r.json()
                domain = data['hydra:member'][0]['domain']

            email = f'user{int(asyncio.get_event_loop().time()*1000)}@{domain}'
            password = 'P@ssw0rd123!'

            await session.post(f'{self.settings.MAILTM_BASE_URL}/accounts', json={'address': email, 'password': password})
            async with session.post(f'{self.settings.MAILTM_BASE_URL}/token', json={'address': email, 'password': password}) as r:
                token = (await r.json()).get('token')

            return TempEmailAccount(email, password, token, None)

    async def wait_for_verification(self, account):
        headers = {'Authorization': f'Bearer {account.token}'}
        elapsed = 0

        while elapsed < self.settings.EMAIL_POLL_TIMEOUT:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(f'{self.settings.MAILTM_BASE_URL}/messages') as r:
                    data = await r.json()
                    msgs = data.get('hydra:member', [])

            for m in msgs:
                text = m.get('text', '')
                code = self.extract_code_from_text(text) or self.extract_code_from_html(m.get('html', ''))
                if code:
                    return {'type': 'code', 'value': code}

            await asyncio.sleep(self.settings.EMAIL_POLL_INTERVAL)
            elapsed += self.settings.EMAIL_POLL_INTERVAL

        return {}

    def extract_code_from_text(self, text):
        m = re.search(r'\b\d{4,8}\b', text or '')
        return m.group(0) if m else None

    def extract_code_from_html(self, html):
        if not html:
            return None

        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all(['strong', 'b']):
            t = tag.get_text(strip=True)
            m = re.search(r'\b\d{4,8}\b', t)
            if m:
                return m.group(0)

        return None

    def extract_verification_link(self, html):
        if not html:
            return None

        soup = BeautifulSoup(html, 'lxml')
        a = soup.select_one('a[href*=\"verify\"]')
        return a['href'] if a else None
