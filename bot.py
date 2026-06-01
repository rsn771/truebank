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
PROMO_PHOTO = "promo_bot.png"

PROMO_TEXT = (
    "Оплата мануала для абуза фп\n\n"
    "что входит: файл с нужными скриптами и обучение-запись экрана со скриншотами\n\n"
    "Все наглядно и понято, но если есть вопросы по части доков на фп в поддержке пишите @r18sn"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Отправляем фото с текстом
    with open(PROMO_PHOTO, "rb") as photo:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=PROMO_TEXT,
        )

    # Отправляем инвойс
    await context.bot.send_invoice(
        chat_id=chat_id,
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
