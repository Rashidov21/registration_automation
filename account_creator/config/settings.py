import os
from dataclasses import dataclass

@dataclass
class Settings:
    TARGET_URL: str = os.getenv('TARGET_URL', 'https://your-site.com')
    REGISTER_URL: str = os.getenv('REGISTER_URL', 'https://your-site.com/register')
    VERIFY_URL: str = os.getenv('VERIFY_URL', 'https://your-site.com/verify')
    PROFILE_URL: str = os.getenv('PROFILE_URL', 'https://your-site.com/profile')

    MAILTM_BASE_URL: str = os.getenv('MAILTM_BASE_URL', 'https://api.mail.tm')
    EMAIL_POLL_INTERVAL: float = float(os.getenv('EMAIL_POLL_INTERVAL', '4'))
    EMAIL_POLL_TIMEOUT: float = float(os.getenv('EMAIL_POLL_TIMEOUT', '90'))

    BROWSER_HEADLESS: bool = os.getenv('BROWSER_HEADLESS', 'False').lower() in ('1', 'true', 'yes')
    BROWSER_SLOW_MO: int = int(os.getenv('BROWSER_SLOW_MO', '50'))
    BROWSER_TIMEOUT: int = int(os.getenv('BROWSER_TIMEOUT', '30000'))
    BROWSER_VIEWPORT: tuple[int, int] = (int(os.getenv('BROWSER_VIEWPORT_WIDTH', '1280')), int(os.getenv('BROWSER_VIEWPORT_HEIGHT', '720')))

    MAX_WORKERS: int = int(os.getenv('MAX_WORKERS', '5'))
    DELAY_BETWEEN_ACTIONS_MIN: float = float(os.getenv('DELAY_BETWEEN_ACTIONS_MIN', '1'))
    DELAY_BETWEEN_ACTIONS_MAX: float = float(os.getenv('DELAY_BETWEEN_ACTIONS_MAX', '3'))
    PAUSE_EVERY_N_ACCOUNTS: int = int(os.getenv('PAUSE_EVERY_N_ACCOUNTS', '10'))
    PAUSE_DURATION_MIN: int = int(os.getenv('PAUSE_DURATION_MIN', '30'))
    PAUSE_DURATION_MAX: int = int(os.getenv('PAUSE_DURATION_MAX', '60'))

    TYPING_DELAY_MIN: int = int(os.getenv('TYPING_DELAY_MIN', '50'))
    TYPING_DELAY_MAX: int = int(os.getenv('TYPING_DELAY_MAX', '150'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))

    TESSERACT_CMD: str = os.getenv('TESSERACT_CMD', 'tesseract')
    OCR_RESIZE_FACTOR: int = int(os.getenv('OCR_RESIZE_FACTOR', '3'))
    USE_PROXY: bool = os.getenv('USE_PROXY', 'False').lower() in ('1', 'true', 'yes')
    PROXY_ROTATION_EVERY: int = int(os.getenv('PROXY_ROTATION_EVERY', '10'))
    FAKER_LOCALES: list[str] = ['uz_UZ', 'ru_RU']

settings = Settings()