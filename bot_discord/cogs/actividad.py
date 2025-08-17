import discord
from discord.ext import commands
from discord import app_commands

class Actividad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="actividad", description="Verificar actividad de los miembros")
    async def actividad(self, interaction: discord.Interaction):
        mensaje = (
            "🚨 **Verificación de actividad** 🚨\n\n"
            "Reacciona con ✅ en las próximas **24 horas** para confirmar actividad.\n"
            "De lo contrario, serás expulsado."
        )
        await interaction.response.send_message(mensaje)  # 👈 visible para todos

        # Añadir reacción automática ✅
        canal = interaction.channel
        msg_obj = await canal.fetch_message((await interaction.original_response()).id)
        await msg_obj.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(Actividad(bot))
