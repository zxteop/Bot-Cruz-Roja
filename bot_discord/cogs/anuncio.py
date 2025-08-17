import discord
from discord.ext import commands
from discord import app_commands

class Anuncio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="anuncio", description="Enviar un anuncio en el canal actual")
    async def anuncio(self, interaction: discord.Interaction, mensaje: str):
        embed = discord.Embed(
            title="📢 Anuncio",
            description=mensaje,
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)  # 👈 visible para todos

async def setup(bot):
    await bot.add_cog(Anuncio(bot))

