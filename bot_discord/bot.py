import discord
from discord.ext import commands
import os
import config
import asyncio

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix="/", intents=intents)

# ID de tu servidor
GUILD_ID = config.GUILD_ID


@bot.event
async def on_ready():
    print("=======================================")
    print(f"✅ Bot conectado como {bot.user}")
    print("✅ ID:", bot.user.id)
    print("✅ Servidores:", [g.name for g in bot.guilds])
    print("=======================================")

    # Sincronizar slash commands
    guild = discord.Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} comandos sincronizados en el servidor {GUILD_ID}")
    except Exception as e:
        print(f"❌ Error al sincronizar: {e}")


async def load_cogs():
    """Carga todos los cogs en ./cogs"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📂 Cargado: {filename}")
            except Exception as e:
                print(f"❌ Error cargando {filename}: {e}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
