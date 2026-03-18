from .base_flow import BaseFlow

SEL = {
    'code_input': "input[name='code']",
    'submit': "button[type='submit']",
    'success': "text=Account verified",
    'error': "text=Invalid code",
}

class VerificationFlow(BaseFlow):
    async def run(self, code=None, link=None):
        if link:
            await self.driver.goto(link)
            return await self.driver.element_exists(SEL['success'], timeout=10000)

        if code:
            await self.driver.type_human(SEL['code_input'], code)
            await self.driver.click(SEL['submit'])
            return await self.driver.element_exists(SEL['success'], timeout=10000)

        return False
