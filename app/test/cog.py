import asyncio
import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from components.ui.common.button import Button
from components.ui.send import ViewSender
from components.ui.state import use_state
from components.ui.status import StatusUI
from components.ui.view import View, ViewObject
from const.enums import Color, Status

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class TestCog(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.command(name="try-status", description="StatusUIのテストコマンド")
    async def try_status(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        ui = StatusUI(color=Color.MIKU)
        ui.add(key="STATUS_1", message="ステータス1")
        ui.add(key="STATUS_2", message="ステータス2")

        # msg = await interaction.followup.send(embed=status.to_embed(), wait=True)
        # status.set_message(msg)
        await ui.send(interaction.followup, ephemeral=False)
        ui.update(
            key="STATUS_1",
            status=Status.IN_PROGRESS,
            message="ステータス1を実行中",
        )
        await ui.sync()
        # await msg.edit(embed=status.to_embed())

        await asyncio.sleep(5)
        ui.update(key="STATUS_1", status=Status.SUCCESS, message="ステータス1を完了")
        ui.update(key="STATUS_2", status=Status.IN_PROGRESS, message="ステータス2を実行中")
        await ui.sync()

        await asyncio.sleep(5)
        ui.update(key="STATUS_2", status=Status.FAILED, message="ステータス2でエラーが発生")
        await ui.sync()

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.command(name="try-state", description="Stateのテストコマンド")
    async def try_state(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        view = ViewSender(TestView())
        await view.send(target=interaction.followup, ephemeral=False)


class TestView(View):
    def __init__(self) -> None:
        self.count, self.set_count = use_state(0, self)
        super().__init__()

    def increment(self) -> None:
        self.set_count(lambda x: x + 1)

    def decrement(self) -> None:
        self.set_count(lambda x: x - 1)

    def export(self) -> ViewObject:
        async def callback_increment(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.increment()

        async def callback_decrement(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.decrement()

        return ViewObject(
            embeds=[
                discord.Embed(
                    title="Count",
                    description=f"Count: {self.count()}",
                ),
            ],
            children=[
                Button("+1", style={"color": "green"}, on_click=callback_increment),
                Button("-1", style={"color": "red"}, on_click=callback_decrement),
            ],
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(TestCog(bot))
