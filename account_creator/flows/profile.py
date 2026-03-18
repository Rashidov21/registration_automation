from .base_flow import BaseFlow

SEL = {
    'first_name': "input[name='first_name']",
    'last_name': "input[name='last_name']",
    'country': "select[name='country']",
    'region': "select[name='region']",
    'district': "select[name='district']",
    'mahalla': "select[name='mahalla']",
    'save_btn': "button[type='submit']",
    'success': "text=Profile updated",
    'error': "text=Error",
}

class ProfileFlow(BaseFlow):
    async def run(self, first_name, last_name):
        await self.driver.goto(self.driver.settings.PROFILE_URL)
        if first_name:
            await self.driver.type_human(SEL['first_name'], first_name)
        if last_name:
            await self.driver.type_human(SEL['last_name'], last_name)
        await self.driver.click(SEL['save_btn'])
        return await self.driver.element_exists(SEL['success'], timeout=10000)
