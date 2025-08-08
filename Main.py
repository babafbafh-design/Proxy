import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Defaults
import json, os

def load_config():
    if os.path.exists("config.json"):
        with open("config.json","r") as f:
            return json.load(f)
    return {"source":"", "dest":"", "admin":""}
def save_config(cfg):
    with open("config.json","w") as f:
        json.dump(cfg,f)

def start(update, context):
    uid = update.effective_user.id
    cfg = load_config()
    if not cfg.get("admin"):
        cfg["admin"] = str(uid)
        save_config(cfg)
    update.message.reply_text("ربات آماده‌ست! با /setsource و /setdest کانال‌ها رو تنظیم کن.")

def set_source(update, context):
    cfg = load_config()
    if str(update.effective_user.id) != cfg.get("admin"):
        return update.message.reply_text("حق نداری اینو انجام بدی!")
    if context.args:
        cfg["source"] = context.args[0]
        save_config(cfg)
        update.message.reply_text(f"کانال مبدا تنظیم شد: {cfg['source']}")
    else:
        update.message.reply_text("مثال: /setsource BBCFarsi")

def set_dest(update, context):
    cfg = load_config()
    if str(update.effective_user.id) != cfg.get("admin"):
        return update.message.reply_text("حق نداری اینو انجام بدی!")
    if context.args:
        cfg["dest"] = context.args[0]
        save_config(cfg)
        update.message.reply_text(f"کانال مقصد تنظیم شد: {cfg['dest']}")
    else:
        update.message.reply_text("مثال: /setdest @MyChannel")

def forward(update, context):
    cfg = load_config()
    if update.effective_chat.username == cfg.get("source"):
        msg = update.message
        if msg.text:
            context.bot.send_message(chat_id=cfg['dest'], text=msg.text)
        elif msg.photo:
            context.bot.send_photo(chat_id=cfg['dest'], photo=msg.photo[-1].file_id, caption=msg.caption or "")
        elif msg.document:
            context.bot.send_document(chat_id=cfg['dest'], document=msg.document.file_id, caption=msg.caption or "")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    logging.basicConfig(level=logging.INFO)
    updater = Updater(TOKEN, defaults=Defaults(run_async=True))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setsource", set_source))
    dp.add_handler(CommandHandler("setdest", set_dest))
    dp.add_handler(MessageHandler(Filters.all, forward))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
