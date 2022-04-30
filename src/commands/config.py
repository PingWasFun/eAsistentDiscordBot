import logging
import typing

import discord
from discord import Embed, app_commands
from discord.ext import commands

from src.ui import ConfigView, Confirm
from src.formatter import format_config_user_embed, \
    format_config_guild_embed, no_permission_embed
from src.database.db_api import set_user_data, set_guild_data, reset_user_data


class ConfigurationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.debug(f"commands.config (ConfigurationCog) started")

    # @commands.command(name="nastavitve",
    #                   aliases=["settings", "uconfig", "uc"])
    # async def user_config(self, ctx: discord.Message):
    #     embed_description = "test"
    #     embed = Embed(color=0x9141ac, description=embed_description)
    #
    #     if ctx.author.guild_permissions.administrator:
    #         view = ConfigView(ctx, administrator=True)
    #     else:
    #         view = ConfigView(ctx)
    #
    #     view.message = await ctx.send(embed=embed, view=view)

    @app_commands.command(name="ponastavi", description="Ponastavi svoje podatke")
    async def reset_user_data(self, interaction: discord.Interaction) -> None:
        view = Confirm()

        await interaction.response.send_message(
            "Ali želite ponastavi svoje podatke?",
            view=view,
            ephemeral=True)

    @app_commands.command(name="nastavitve",
                          description="Nastavite svoje podatke")
    async def user_settings(
            self,
            interaction: discord.Interaction,
            school_id: str = None,
            class_id: str = None,
            # alerts_enabled: typing.Literal["Ja", "Ne"] = None,
            # alert_time: typing.Literal[
            #     '0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00',
            #     '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00',
            #     '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00',
            #     '22:00', '23:00'] = None,
    ) -> None:
        alert_time = None
        alerts_enabled = None

        user_id = interaction.user.id
        # if alerts_enabled is None:
        #     pass
        # elif alerts_enabled.lower() == "ja":
        #     alerts_enabled = True
        # elif alerts_enabled.lower() == "ne":
        #     alerts_enabled = False
        # else:
        #     alerts_enabled = None
        # if alert_time is not None:
        #     alert_time = alert_time.split(":")[0]

        set_user_data(
            user_id,
            school_id=school_id,
            class_id=class_id,
            alerts_enabled=alerts_enabled,
            alert_time=alert_time,
        )

        config_embed = format_config_user_embed(user_id)

        await interaction.response.send_message(ephemeral=True,
                                                embed=config_embed)

    @app_commands.command(
        name="nastavitve_serverja", description="Nastavite podatke serverja"
    )
    async def guild_settings(
            self,
            interaction: discord.Interaction,
            school_id: str = None,
            class_id: str = None,
            # schedule_channel_id: str = None,
            # alerts_enabled: typing.Literal["Ja", "Ne"] = None,
            # alert_time: typing.Literal[
            #     '0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00',
            #     '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00',
            #     '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00',
            #     '22:00', '23:00'] = None,
            # alert_role_id: str = None
    ) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(ephemeral=True,
                                                    embed=no_permission_embed(
                                                        "Administrator"))
            return

        alert_role_id = None
        alerts_enabled = None
        alert_time = None
        schedule_channel_id = None

        guild_id = interaction.guild.id
        # if alerts_enabled is None:
        #     pass
        # elif alerts_enabled.lower() == "ja":
        #     alerts_enabled = True
        # elif alerts_enabled.lower() == "ne":
        #     alerts_enabled = False
        # else:
        #     alerts_enabled = None
        # if alert_time is not None:
        #     alert_time = alert_time.split(":")[0]

        set_guild_data(
            guild_id,
            school_id=school_id,
            class_id=class_id,
            schedule_channel_id=schedule_channel_id,
            alerts_enabled=alerts_enabled,
            alert_time=alert_time,
            alert_role_id=alert_role_id,
        )

        config_embed = format_config_guild_embed(guild_id)

        await interaction.response.send_message(ephemeral=True,
                                                embed=config_embed)


async def setup(bot) -> None:
    await bot.add_cog(
        ConfigurationCog(bot), guilds=[discord.Object(id=882993496141729792)]
    )
