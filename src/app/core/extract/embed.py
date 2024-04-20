import discord

from src.const.discord import MAX_EMBEDS_PER_MESSAGE
from src.const.enums import Color

from .processor import NotionPage


def process_message_to_embeds(message: discord.Message, color: int = Color.MIKU) -> list[discord.Embed]:
    embeds: list[discord.Embed] = []
    guild = message.guild

    e = discord.Embed(
        description=message.content,
        color=color,
        timestamp=message.created_at,
    )
    e.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar.url or message.author.default_avatar.url,
    )
    e.add_field(
        name="送信した人",
        value=message.author.mention,
    )
    if not isinstance(
        message.channel,
        discord.DMChannel | discord.PartialMessageable | discord.GroupChannel,
    ):
        e.add_field(
            name="チャンネル",
            value=message.channel.mention or "",
        )
    if message.reference is not None:
        e.add_field(
            name="返信先",
            value=message.reference.jump_url,
        )
    if message.attachments and message.attachments[0].url:
        e.set_image(url=message.attachments[0].url)
    if guild is not None:
        e.set_footer(text=f"Sent in {guild.name}")

    embeds.append(e)

    for attachment in message.attachments[1:]:
        if len(embeds) >= MAX_EMBEDS_PER_MESSAGE:
            break
        e = discord.Embed(
            color=color,
        )
        e.set_image(url=attachment.url)
        embeds.append(e)

    for _e in message.embeds:
        if len(embeds) >= MAX_EMBEDS_PER_MESSAGE:
            break
        embeds.append(_e)

    return embeds


def process_notion_page_to_embeds(page: NotionPage) -> discord.Embed:
    e = discord.Embed(
        title=f"{page['emoji']} {page['title']}" if page["emoji"] else page["title"],
        url=page["url"],
        color=Color.MIKU,
        timestamp=page["last_updated"],
    )
    e.set_image(url=page["image"])
    e.set_footer(text="Created on Notion")
    return e
