import discord
from discord import app_commands
from discord.ext import commands
import datetime

# Diccionario en memoria para guardar reportes
reportes = {}

class Reporte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================================
    # Slash Command para crear reporte
    # ================================
    @app_commands.command(name="reporte", description="Registrar un reporte de incidente")
    @app_commands.describe(
        nombre="Tu nombre completo",
        fecha_hora="Fecha y hora del incidente",
        incidente="Describe el incidente",
        numero_reporte="Número de reporte",
        companeros="Compañeros involucrados",
        emergencias="Número de emergencias atendidas",
        foto="Sube una imagen del incidente"
    )
    async def reporte(
        self,
        interaction: discord.Interaction,
        nombre: str,
        fecha_hora: str,
        incidente: str,
        numero_reporte: str,
        companeros: str,
        emergencias: int,
        foto: discord.Attachment
    ):
        if not foto.content_type.startswith("image/"):
            return await interaction.response.send_message("❌ Solo se permiten imágenes en el campo de foto.", ephemeral=True)

        user_id = str(interaction.user.id)

        if user_id not in reportes:
            reportes[user_id] = []

        reporte_data = {
            "nombre": interaction.user.mention,
            "fecha_hora": fecha_hora,
            "incidente": incidente,
            "numero_reporte": numero_reporte,
            "companeros": companeros,
            "emergencias": emergencias,
            "foto": foto.url
        }

        reportes[user_id].append(reporte_data)

        # Embed público
        embed = discord.Embed(
            title="📑 Nuevo Reporte de Emergencia",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="👤 Nombre", value=reporte_data["nombre"], inline=False)
        embed.add_field(name="📅 Fecha y hora", value=reporte_data["fecha_hora"], inline=False)
        embed.add_field(name="⚠️ Incidente", value=reporte_data["incidente"], inline=False)
        embed.add_field(name="🔢 Número de reporte", value=reporte_data["numero_reporte"], inline=False)
        embed.add_field(name="👥 Compañeros", value=reporte_data["companeros"], inline=False)
        embed.add_field(name="🚑 Emergencias atendidas", value=str(reporte_data["emergencias"]), inline=False)
        embed.set_image(url=reporte_data["foto"])

        await interaction.response.send_message(embed=embed)  # 🔥 Público

    # Ver reportes
    @app_commands.command(name="registro_de_reportes", description="Ver los reportes de un usuario")
    @app_commands.describe(usuario="Menciona a un usuario para ver sus reportes (opcional)")
    async def registro_de_reportes(self, interaction: discord.Interaction, usuario: discord.User = None):
        user = usuario or interaction.user
        user_id = str(user.id)

        if user_id not in reportes or not reportes[user_id]:
            return await interaction.response.send_message(f"📭 {user.mention} no tiene reportes.", ephemeral=True)

        embed = discord.Embed(
            title=f"📑 Reportes de {user.display_name}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )

        for i, r in enumerate(reportes[user_id], start=1):
            embed.add_field(
                name=f"Reporte #{i}",
                value=(
                    f"👤 **Nombre:** {r['nombre']}\n"
                    f"📅 **Fecha y hora:** {r['fecha_hora']}\n"
                    f"⚠️ **Incidente:** {r['incidente']}\n"
                    f"🔢 **Número de reporte:** {r['numero_reporte']}\n"
                    f"👥 **Compañeros:** {r['companeros']}\n"
                    f"🚑 **Emergencias atendidas:** {r['emergencias']}\n"
                    f"📷 **Foto:** [Ver imagen]({r['foto']})"
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="borrar_reportes", description="Borra todos los reportes registrados")
    async def borrar_reportes(self, interaction: discord.Interaction):
        global reportes
        reportes = {}
        await interaction.response.send_message("🗑️ Todos los **reportes de emergencia** han sido borrados.", ephemeral=False)


async def setup(bot):
    await bot.add_cog(Reporte(bot))
