import discord
from discord.ext import commands
from discord import app_commands

# Canal donde se anunciarán los eventos
CANAL_EVENTOS_ID = 1373406824547745839

class Evento(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="evento", description="Crea un evento con anuncio para todos")
    async def evento(self, interaction: discord.Interaction, titulo: str, descripcion: str):
        # Embed del evento
        embed = discord.Embed(
            title=f"📢 Evento: {titulo}",
            description=descripcion,
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Organizado por {interaction.user.display_name}")

        # Canal destino
        canal = self.bot.get_channel(CANAL_EVENTOS_ID)
        if canal:
            await canal.send(
                content="@everyone 🚨 ¡Nuevo evento programado!",
                embed=embed
            )

        # Confirmación al usuario
        await interaction.response.send_message(
            f"✅ Evento **{titulo}** enviado en {canal.mention} con ping a @everyone.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Evento(bot))
