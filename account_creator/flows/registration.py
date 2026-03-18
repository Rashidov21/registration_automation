import random
from .base_flow import BaseFlow

SEL = {
    'email': "input[name='email']",
    'password': "input[name='password']",
    'password2': "input[name='password_confirm']",
    'first_name': "input[name='first_name']",
    'last_name': "input[name='last_name']",
    'phone': "input[name='phone']",
    'country': "select[name='country']",
    'submit': "button[type='submit']",
    'success': "text=Registration successful",
    'error': "text=Error",
    'captcha_img': "img.captcha",
    'captcha_input': "input[name='captcha']",
}

class RegistrationFlow(BaseFlow):
    async def run(self, email, password, first_name, last_name):
        await self.driver.goto(self.driver.settings.REGISTER_URL)

        await self.driver.type_human(SEL['email'], email)
        await self.driver.type_human(SEL['password'], password)

        if await self.driver.element_exists(SEL['password2'], timeout=1000):
            await self.driver.type_human(SEL['password2'], password)

        if first_name and await self.driver.element_exists(SEL['first_name'], timeout=1000):
            await self.driver.type_human(SEL['first_name'], first_name)

        if last_name and await self.driver.element_exists(SEL['last_name'], timeout=1000):
            await self.driver.type_human(SEL['last_name'], last_name)

        await self.driver.click(SEL['submit'])

        if await self.driver.element_exists(SEL['success'], timeout=10000):
            return True

        return False
