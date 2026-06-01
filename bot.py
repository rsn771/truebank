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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Оплата 100 звёзд",
        description="Нажмите кнопку ниже, чтобы оплатить 100 Telegram Stars",
        payload="pay_100_stars",
        provider_token="",          # пустой токен — для Stars
        currency="XTR",             # XTR = Telegram Stars
        prices=[LabeledPrice("100 Stars", 100)],
    )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Спасибо! Оплата 100 звёзд прошла успешно.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
