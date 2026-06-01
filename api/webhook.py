from http.server import BaseHTTPRequestHandler
import json
import asyncio
from telegram import Update, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = "8338386090:AAG14TDq3H5kMuVpW3BFEbzy56K0hmQ3CMU"

# Фото берётся напрямую с GitHub (локальные файлы на Vercel недоступны)
PROMO_PHOTO_URL = "https://raw.githubusercontent.com/rsn771/truebank/main/promo_bot.png"

PROMO_TEXT = (
    "Оплата мануала для абуза фп\n\n"
    "что входит: файл с нужными скриптами и обучение-запись экрана со скриншотами\n\n"
    "Все наглядно и понято, но если есть вопросы по части доков на фп в поддержке пишите @r18sn"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=PROMO_PHOTO_URL,
        caption=PROMO_TEXT,
    )
    await context.bot.send_invoice(
        chat_id=chat_id,
        title="Оплата 100 звёзд",
        description="Нажмите кнопку ниже, чтобы оплатить 100 Telegram Stars",
        payload="pay_100_stars",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice("100 Stars", 100)],
    )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Спасибо! Оплата 100 звёзд прошла успешно.")


async def handle_update(update_json: dict):
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    async with app:
        update = Update.de_json(update_json, app.bot)
        await app.process_update(update)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length", 0))
        body = json.loads(self.rfile.read(length))
        asyncio.run(handle_update(body))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Webhook active!")
