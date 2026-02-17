import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy import create_engine
import pandas as pd

TOKEN = os.environ.get("TOKEN")

engine = create_engine("sqlite:///asistencia.db")

def inicializar_db():
    with engine.connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS grupos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        )
        """)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Bot Académico Activo\n\n"
        "/crear_grupo nombre\n"
        "/ver_grupos"
    )

async def crear_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = " ".join(context.args)
    if not nombre:
        await update.message.reply_text("Escribe nombre del grupo.")
        return

    df = pd.DataFrame([[nombre]], columns=["nombre"])
    df.to_sql("grupos", engine, if_exists="append", index=False)

    await update.message.reply_text(f"✅ Grupo '{nombre}' creado.")

async def ver_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df = pd.read_sql("SELECT * FROM grupos", engine)
    if df.empty:
        await update.message.reply_text("No hay grupos.")
        return

    texto = "\n".join([f"{row.id} - {row.nombre}" for row in df.itertuples()])
    await update.message.reply_text("📋 Grupos:\n" + texto)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("crear_grupo", crear_grupo))
app.add_handler(CommandHandler("ver_grupos", ver_grupos))

inicializar_db()
app.run_polling()
