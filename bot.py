import asyncio
import random
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# 🔑 Replace with your bot details
TOKEN = "901945986:AAHBuiG4IrYSzStp9lHhVhmPBZNpVI-GoAk"
CHAT_ID = "575671651"   # use @userinfobot to find your ID

bot = Bot(token=TOKEN)

# 🌐 Official URLs
URLS = {
    "FC Kairat (official site)": "https://fckairat.com/view/ticket-selling/",
    "Ticketon": "https://ticketon.kz/sports/futbolniy-klub-kairat",
    "Kassir.kz": "https://kassir.kz/",
}

# 🔎 Ticket-related keywords
KEYWORDS = [
    "Купить билет",
    "Билеты",
    "В продаже",
    "Tickets",
    "Buy tickets",
    "Реал",
    "Real Madrid",
]


async def send_alert(msg: str):
    """Send alert to Telegram chat"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        logging.error("Telegram send error: %s", e)


def check_site(name: str, url: str):
    """Check if tickets are mentioned on a site"""
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        for kw in KEYWORDS:
            if kw.lower() in text.lower():
                return True, kw
        return False, None
    except Exception as e:
        logging.error("Error checking %s: %s", url, e)
        return False, None


async def monitor():
    """Main loop: check sites every 5–20 min"""
    while True:
        for name, url in URLS.items():
            found, kw = check_site(name, url)
            if found:
                await send_alert(f"🎟 Tickets update found! '{kw}' on {name} → {url}")
            else:
                print(f"❌ No tickets yet on {name}")

        # Random delay between 5–20 minutes
        delay = random.randint(300, 1200)
        print(f"⏳ Next check in {delay // 60} minutes.")
        await asyncio.sleep(delay)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(monitor())
