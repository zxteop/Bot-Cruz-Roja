import discord
from discord.ext import commands
from discord import app_commands

# Canal de dudas
CANAL_DUDAS_ID = 1406467387745894520  

class Duda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duda", description="Envía tu duda y recibe soporte")
    async def duda(self, interaction: discord.Interaction, texto: str):
        # 1️⃣ Respuesta al usuario
        await interaction.response.send_message(
            f"❓ Tu duda fue registrada:\n> {texto}\n\n"
            f"📌 El tiempo de respuesta varia un poco:\n"
            f" ⏰ Ten paciencia!",
            ephemeral=False  # 🔹 visible para todos, no solo el usuario
        )

        # 2️⃣ Enviar al canal de dudas con ping a everyone
        canal = self.bot.get_channel(CANAL_DUDAS_ID)
        if canal:
            embed = discord.Embed(
                title="📩 Nueva duda recibida",
                description=f"**Usuario:** {interaction.user.mention}\n\n**Duda:**\n{texto}",
                color=discord.Color.blue()
            )
            await canal.send(
                content="@everyone 🚨 ¡Nueva duda recibida!",
                embed=embed
            )

async def setup(bot):
    await bot.add_cog(Duda(bot))
