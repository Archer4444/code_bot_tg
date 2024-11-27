import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация API Together.AI
API_KEY = "7034f23db727899a8a392180dba485526b442c2c957c0dbd701c938eccfc910e"
TOGETHER_API_ENDPOINT = "https://api.together.xyz/v1/chat/completions"
MODEL_NAME = "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"

# Ваш токен Telegram
TELEGRAM_TOKEN = "7569033373:AAE32OhfUJaSthaXzViBEDdWooGC3aOzf8g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-бот. Задай мне любой вопрос, и я постараюсь ответить!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Уведомление пользователя о том, что бот пишет ответ
    await update.message.reply_text("Бот пишет ответ...")

    # Получение ответа от Together.AI
    response_text = get_ai_response(user_message)
    
    # Форматирование ответа с учетом выделения всех блоков кода
    formatted_response = format_code_blocks(response_text)
    
    # Отправка ответа пользователю
    await update.message.reply_text(formatted_response, parse_mode="Markdown")

def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(TOGETHER_API_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        return "Ошибка: Не удалось получить ответ от Together.AI."

def format_code_blocks(text):
    lines = text.splitlines()
    formatted_text = []
    in_code_block = False

    for line in lines:
        if "```" in line:
            in_code_block = not in_code_block
        formatted_text.append(line)

    # Закрываем открытый блок, если он остался
    if in_code_block:
        formatted_text.append("```")

    return "\n".join(formatted_text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен!")
    app.run_polling()
