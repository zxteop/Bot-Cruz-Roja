import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🦶 Expulsar usuario
    @app_commands.command(name="kick", description="Expulsar a un usuario del servidor")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, miembro: discord.Member, razon: str = "Sin razón"):
        try:
            await miembro.kick(reason=razon)
            await interaction.response.send_message(
                f"✅ {miembro.mention} fue expulsado. Razón: {razon}", ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ No se pudo expulsar a {miembro.mention}. Error: {e}", ephemeral=True
            )

    # 🔨 Banear usuario
    @app_commands.command(name="ban", description="Banear a un usuario del servidor")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, miembro: discord.Member, razon: str = "Sin razón"):
        try:
            await miembro.ban(reason=razon)
            await interaction.response.send_message(
                f"✅ {miembro.mention} fue baneado. Razón: {razon}", ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ No se pudo banear a {miembro.mention}. Error: {e}", ephemeral=True
            )

    # 🧹 Borrar mensajes
    @app_commands.command(name="clear", description="Borrar mensajes de un canal")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, cantidad: int):
        await interaction.response.defer(ephemeral=True)
        borrados = await interaction.channel.purge(limit=cantidad)
        await interaction.followup.send(
            f"🧹 Se borraron {len(borrados)} mensajes en {interaction.channel.mention}.", ephemeral=False
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))
