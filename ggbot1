import json
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# === НАСТРОЙКИ ===
BOT_TOKEN = "7890915663:AAG_VLDpMLMNr8YCuhnx61PxQdAPNXxxPg8"
GROUP_CHAT_ID = "@r2wrfq"  # ← теперь как username
ADMIN_ID = 6040186314

DB_FILE = "orders.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:#
        json.dump({}, f)

def load_orders():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_orders(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n"
        "Это *официальный бот GGPoint*.\n"
        "Здесь вы можете следить за статусом своих заказов.\n\n"
        "Введите команду:\n"
        "`/status [номер_заказа]` — чтобы узнать последний статус.",
        parse_mode="Markdown"
    )

# === /status ===
async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = load_orders()
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("❗ Используйте команду так: /status [номер_заказа]")
        return

    order_id = context.args[0]
    user_id = update.message.from_user.id

    if order_id in orders:
        orders[order_id]["users"].append(user_id)
        orders[order_id]["users"] = list(set(orders[order_id]["users"]))
        save_orders(orders)
        status = orders[order_id]["status"]
        await update.message.reply_text(f"📦 Статус заказа #{order_id}: {status}")
    else:
        orders[order_id] = {"status": "Нет данных", "users": [user_id]}
        save_orders(orders)
        await update.message.reply_text(f"📦 Статус заказа #{order_id}: Нет данных")

# === Обработка сообщений в группе ===
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.username != GROUP_CHAT_ID.lstrip("@"):
        return

    text = update.message.text.strip()
    if not text.startswith("#"):
        return

    parts = text[1:].split(" ", 1)
    if len(parts) != 2 or not parts[0].isdigit():
        return

    order_id, new_status = parts
    orders = load_orders()

    if new_status.lower().strip() == "товар отдан":
        if order_id in orders:
            del orders[order_id]
            save_orders(orders)
            await update.message.reply_text(f"🗑 Заказ #{order_id} удалён (товар отдан)")
        return

    if order_id not in orders:
        orders[order_id] = {"status": "", "users": []}

    orders[order_id]["status"] = new_status
    save_orders(orders)

    for user_id in orders[order_id]["users"]:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🔔 Новый статус для заказа #{order_id}:\n{new_status}"
            )
        except Exception as e:
            print(f"❌ Ошибка при отправке пользователю {user_id}: {e}")

    await update.message.reply_text(f"✅ Статус заказа #{order_id} сохранён")

# === ЗАПУСК ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", check_status))

    # Обработка сообщений в любом чате, но фильтруем по username в коде
    app.add_handler(MessageHandler(filters.TEXT, handle_group_message))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
