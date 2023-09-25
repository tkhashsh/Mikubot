import logging
from typing import Literal

import aiohttp

from .object import Event

calender_2023_id = "yJojmgmD7kt9"  # 2023


class Client:
    def __init__(self, api_key: str, calendar_id: str) -> None:
        self.api_key: str = api_key
        self.calendar_id: str = calendar_id
        self.logger = logging.getLogger(__name__)

    async def get_upcoming_events(self, days: Literal[1, 2, 3, 4, 5, 6, 7] = 1) -> list[Event]:
        # https://developers.timetreeapp.com/ja/docs/api/oauth-app#list-upcoming-events
        upcoming_url = (
            f"https://timetreeapis.com/calendars/{self.calendar_id}/upcoming_events?days={days!s}&timezone=Asia/Tokyo"
        )
        headers = {
            "Accept": "application/vnd.timetree.v1+json",
            "Authorization": f"Bearer {self.api_key}",
        }
        async with aiohttp.ClientSession() as session, session.get(upcoming_url, headers=headers) as res:
            data = await res.json(encoding="utf-8")
            self.logger.debug(res.status)
            self.logger.debug(data)

            try:
                events = [
                    Event(
                        event_id=elm["id"],
                        event_type=elm["type"],
                        **elm["attributes"],
                        raw_data=elm,
                    )
                    for elm in data["data"]
                ]
            except Exception:
                self.logger.exception("Error occurred while parsing json")
                return []
            else:
                return events


# def getTodaysEventsJson(title):
#     data = getEventFromAPI()
#     todaysEvents = ""
#     # 予定の件数を取得
#     todaysEventsTop = "{}月{}日の予定は{}件だよ!\n\n".format(
#         datetime.date.today().month, datetime.date.today().day, len(data["data"])
#     )
#     embed = discord.Embed(title=title, description=todaysEventsTop, color=0x5EFCEB)

#     # 予定のタイトルを取得し表示
#     for content in data["data"]:
#         emName = getEventTitle(content)
#         emValue = ""
#         if content["attributes"]["all_day"]:
#             emValue = "終日\n"
#         else:
#             emValue = getEventStartAt(content) + "〜" + getEventEndAt(content) + "\n"
#         embed.add_field(name=emName, value=emValue, inline=False)
#     return embed
