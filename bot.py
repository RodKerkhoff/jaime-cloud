import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jaime_core import briefing_restrito, triagem_emails, agenda_restrita, gerar_documento

TOKEN = os.getenv("TELEGRAM_TOKEN", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "JAIME - Assistente Geral ativo (nuvem 24h)\n\n"
        "Modo restrito ligado: minimizacao + falha fechada.\n"
        "Comandos:\n"
        "/briefing - briefing diario\n"
        "/agenda - o que tenho hoje/amanha (ref/data/origem)\n"
        "/triagem - ultimos e-mails\n"
        "/gerar procuracao | contrato\n"
        "\nDigite /briefing para testar."
    )

async def briefing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = briefing_restrito()
    await update.message.reply_text(texto)

async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = agenda_restrita()
    await update.message.reply_text(texto)

async def triagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = triagem_emails()
    for chunk in [texto[i:i+4000] for i in range(0, len(texto), 4000)]:
        await update.message.reply_text(chunk)

async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = " ".join(context.args) if context.args else ""
    texto = gerar_documento(args)
    await update.message.reply_text(texto)

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (update.message.text or "").lower()
    if "briefing" in txt:
        await briefing(update, context)
    elif "agenda" in txt:
        await agenda(update, context)
    elif "triagem" in txt or "email" in txt:
        await triagem(update, context)
    else:
        await update.message.reply_text(
            "Entendi. Use /briefing, /agenda, /triagem ou /gerar procuracao\n"
            "Ex: /gerar procuracao CPF 123"
        )

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN nao definido")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("briefing", briefing))
    app.add_handler(CommandHandler("agenda", agenda))
    app.add_handler(CommandHandler("triagem", triagem))
    app.add_handler(CommandHandler("gerar", gerar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    print("Jaime rodando em polling (nuvem)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
