import discord
from discord import app_commands
from discord.ext import commands
import datetime

# Diccionario en memoria para guardar registros de móviles
registros_moviles = {}

class RegistroMoviles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="registro_movil", description="Registrar un servicio con la móvil")
    @app_commands.describe(
        nombre="Tu nombre completo",
        placa="Placa de la móvil",
        motivo="Motivo del servicio",
        fecha_hora="Fecha y hora del servicio",
        foto="Sube una foto de la móvil"
    )
    async def registro_movil(
        self,
        interaction: discord.Interaction,
        nombre: str,
        placa: str,
        motivo: str,
        fecha_hora: str,
        foto: discord.Attachment
    ):
        if not foto.content_type.startswith("image/"):
            return await interaction.response.send_message("❌ Solo se permiten imágenes en el campo de foto.", ephemeral=True)

        user_id = str(interaction.user.id)

        if user_id not in registros_moviles:
            registros_moviles[user_id] = []

        registro_data = {
            "nombre": interaction.user.mention,
            "placa": placa,
            "motivo": motivo,
            "fecha_hora": fecha_hora,
            "foto": foto.url
        }

        registros_moviles[user_id].append(registro_data)

        # Embed público
        embed = discord.Embed(
            title="🚓 Nuevo Registro de Móvil",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="👤 Nombre", value=registro_data["nombre"], inline=False)
        embed.add_field(name="🚓 Placa", value=registro_data["placa"], inline=False)
        embed.add_field(name="📅 Fecha y hora", value=registro_data["fecha_hora"], inline=False)
        embed.add_field(name="📝 Motivo", value=registro_data["motivo"], inline=False)
        embed.set_image(url=registro_data["foto"])

        await interaction.response.send_message(embed=embed)  # 🔥 Público

    @app_commands.command(name="registro_de_moviles", description="Ver los registros de móviles de un usuario")
    @app_commands.describe(usuario="Menciona a un usuario para ver sus registros de móviles (opcional)")
    async def registro_de_moviles(self, interaction: discord.Interaction, usuario: discord.User = None):
        user = usuario or interaction.user
        user_id = str(user.id)

        if user_id not in registros_moviles or not registros_moviles[user_id]:
            return await interaction.response.send_message(f"📭 {user.mention} no tiene registros de móviles.", ephemeral=True)

        embed = discord.Embed(
            title=f"📑 Registros de móviles de {user.display_name}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )

        for i, r in enumerate(registros_moviles[user_id], start=1):
            embed.add_field(
                name=f"Registro #{i}",
                value=(
                    f"👤 **Nombre:** {r['nombre']}\n"
                    f"🚓 **Placa:** {r['placa']}\n"
                    f"📅 **Fecha y hora:** {r['fecha_hora']}\n"
                    f"📝 **Motivo:** {r['motivo']}\n"
                    f"📷 **Foto:** [Ver imagen]({r['foto']})"
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="borrar_registros_moviles", description="Borra todos los registros de móviles")
    async def borrar_registros_moviles(self, interaction: discord.Interaction):
        global registros_moviles
        registros_moviles = {}
        await interaction.response.send_message("🗑️ Todos los **registros de móviles** han sido borrados.", ephemeral=False)


async def setup(bot):
    await bot.add_cog(RegistroMoviles(bot))
