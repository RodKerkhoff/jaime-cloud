import os, json, tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jaime_core import briefing_restrito, triagem_emails, agenda_restrita, gerar_documento

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "").strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "JAIME - Fase 2 com VOZ 🎙️\nModo: restrito | 24h online\n\nComandos texto:\n/briefing - briefing diário\n/agenda - agenda real\n/triagem - e-mails\n/gerar procuracao\n\nComandos por VOZ (manda áudio):\n'me dá o briefing'\n'qual minha agenda hoje'\n'faz triagem'\n'gera procuração'\n\nStatus: " + ("✅ Drive/Gmail conectado" if os.getenv("GOOGLE_TOKEN_JSON") else "⚠️ Mock - falta GOOGLE_TOKEN_JSON") +
        "\n" + ("✅ Voz com transcrição" if OPENAI_KEY else "⚠️ Voz sem transcrição - adicione OPENAI_API_KEY")
    )

async def responder_intencao(texto: str) -> str:
    t = (texto or "").lower()
    if any(x in t for x in ["briefing","resumo","dia","hoje"]):
        return briefing_restrito()
    if any(x in t for x in ["agenda","reuni","compromisso","anivers"]):
        return agenda_restrita()
    if any(x in t for x in ["triagem","email","gmail","outlook","mensagem"]):
        return triagem_emails()
    if "procur" in t:
        return gerar_documento("procuracao " + texto)
    if "contrato" in t or "honor" in t:
        return gerar_documento("contrato " + texto)
    return briefing_restrito()

async def briefing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(responder_intencao("briefing"))
async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(responder_intencao("agenda"))
async def triagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = responder_intencao("triagem")
    for i in range(0, len(txt), 4000):
        await update.message.reply_text(txt[i:i+4000])
async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = " ".join(context.args) if context.args else ""
    await update.message.reply_text(gerar_documento(args))
async def texto_livre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(await responder_intencao(update.message.text or ""))

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice or update.message.audio or update.message.video_note
    if not voice:
        return
    await update.message.reply_text("🎧 Ouvindo...")
    try:
        file = await context.bot.get_file(voice.file_id)
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            await file.download_to_drive(tmp.name)
            tmp_path = tmp.name
        transcricao = ""
        if OPENAI_KEY:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_KEY)
            with open(tmp_path, "rb") as f:
                tr = client.audio.transcriptions.create(model="whisper-1", file=f, language="pt")
                transcricao = tr.text
        if not transcricao:
            await update.message.reply_text("Recebi seu áudio! Mas preciso da OPENAI_API_KEY no Render para transcrever.\nEnquanto isso, manda por texto: briefing, agenda, triagem")
            os.remove(tmp_path)
            return
        await update.message.reply_text(f'Você disse: "{transcricao}"')
        resp = await responder_intencao(transcricao)
        await update.message.reply_text(resp)
        if OPENAI_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_KEY)
                speech = client.audio.speech.create(model="tts-1", voice="onyx", input=resp[:3500])
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as out:
                    out.write(speech.content)
                    out_path = out.name
                await update.message.reply_voice(voice=open(out_path, "rb"))
                os.remove(out_path)
            except:
                pass
        os.remove(tmp_path)
    except Exception as e:
        await update.message.reply_text(f"Erro áudio: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("briefing", briefing))
    app.add_handler(CommandHandler("agenda", agenda))
    app.add_handler(CommandHandler("triagem", triagem))
    app.add_handler(CommandHandler("gerar", gerar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_livre))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO | filters.VIDEO_NOTE, voz))
    print("JAIME Fase 2 - Voz + Google - rodando...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()