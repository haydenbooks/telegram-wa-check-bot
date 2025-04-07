import logging
import os
import time
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "7670708763:AAFVlc5d_AfnT0m_uH6lyCyizJzHpfq0TVA"
WAIT_TIME = 30

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def check_number_on_whatsapp(number: str) -> str:
    try:
        driver = start_driver()
        driver.get(f"https://wa.me/{number}")
        time.sleep(5)
        page = driver.page_source
        driver.quit()

        if "<title>WhatsApp</title>" in page and "Continue to Chat" in page:
            return f"✅ {number} is available on WhatsApp."
        else:
            return f"❌ {number} is not available on WhatsApp."
    except Exception as e:
        return f"⚠️ Error checking number: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a phone number (with country code) to check if it's on WhatsApp.")

async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    if not number.isdigit():
        await update.message.reply_text("❌ Please send a valid number with country code. Example: 15551234567")
        return

    await update.message.reply_text("⏳ Checking number, please wait...")
    result = check_number_on_whatsapp(number)
    await update.message.reply_text(result)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))
    print("Bot running...")
    app.run_polling()
