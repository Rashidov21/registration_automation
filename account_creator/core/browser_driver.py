import asyncio
import random
from playwright.async_api import async_playwright

class BrowserDriver:
    def __init__(self, worker_id, proxy=None, settings=None):
        self.worker_id = worker_id
        self.proxy = proxy
        self.settings = settings
        self.playwright = None
        self.browser = None
        self.page = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        launch_kwargs = {
            'headless': self.settings.BROWSER_HEADLESS,
            'slow_mo': self.settings.BROWSER_SLOW_MO,
        }
        if self.proxy:
            launch_kwargs['proxy'] = {'server': self.proxy}

        self.browser = await self.playwright.chromium.launch(**launch_kwargs)
        self.page = await self.browser.new_page(viewport={'width': self.settings.BROWSER_VIEWPORT[0], 'height': self.settings.BROWSER_VIEWPORT[1]})
        await self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def goto(self, url, wait_until='networkidle'):
        await self.page.goto(url, wait_until=wait_until, timeout=self.settings.BROWSER_TIMEOUT)

    async def type_human(self, selector, text):
        for char in text:
            await self.page.type(selector, char, delay=random.randint(self.settings.TYPING_DELAY_MIN, self.settings.TYPING_DELAY_MAX))

    async def click(self, selector):
        await self.page.click(selector)

    async def select_option(self, selector, value=None, label=None):
        await self.page.select_option(selector, value=value, label=label)

    async def execute_js(self, script, *args):
        return await self.page.evaluate(script, *args)

    async def element_exists(self, selector, timeout=2000):
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception:
            return False

    async def get_options_count(self, selector):
        elems = await self.page.query_selector_all(f'{selector} option')
        return len(elems)

    async def wait_for_options_change(self, selector, prev_count, timeout=20):
        end = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < end:
            current = await self.get_options_count(selector)
            if current != prev_count:
                return True
            await asyncio.sleep(0.3)
        return False

    async def screenshot_on_error(self, filename):
        await self.page.screenshot(path=filename)
