from config.config import settings

from anti_captcha import solve_anti_captcha
from monster_captcha import solve_monster_captcha
from two_captcha import solve_2captcha

async def solve_captcha(params=None):
    if params is None:
        params = {
            "websiteURL": settings["CAPTCHA_URL"],
            "websiteKey": settings["WEBSITE_KEY"],
        }
    if settings["TYPE_CAPTCHA"] == "2captcha":
        return await solve_2captcha(params)
    elif settings["TYPE_CAPTCHA"] == "anticaptcha":
        return await solve_anti_captcha(params)
    elif settings["TYPE_CAPTCHA"] == "monstercaptcha":
        return await solve_monster_captcha(params)
    print("Invalid type captcha")
    return None