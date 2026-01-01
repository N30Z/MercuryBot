import asyncio, os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from stores._store import Store
from utils import makejson
from datetime import datetime


def _parse_emoji_env(env_var):
    """Parse emoji environment variable to int or None"""
    value = os.getenv(env_var)
    if value and value.isdigit():
        return int(value)
    return None


class Main(Store):
    """
    psplus store
    """
    def __init__(self):
        self.base_url = 'https://www.playstation.com'
        super().__init__(
            name = 'psplus',
            id = '4',
            discord_emoji = _parse_emoji_env('DISCORD_PSPLUS_EMOJI') or 0,
            service_name = 'PlayStation Plus',
            url = 'https://www.playstation.com/en-gr/ps-plus/whats-new/'
        )


    async def process_data(self):
        """
        get data for psplus
        """
        data = await self.request_data(self.url, mode="html")
        monthly_games_section = data.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " cmp-experiencefragment--wn-latest-monthly-games-content ")]')[0]
        games= monthly_games_section.xpath('.//div[starts-with(@class, "box")]')
        json_data = []

        if not games: return self.logger.critical('PSplus isn\'t returning any deals!')

        for i, game in enumerate(games):
            try:
                title_el = game.xpath('.//h3[contains(@class, "txt-style-medium-title") and contains(@class, "txt-block-paragraph__title")]')
                title = title_el[0].text_content().strip()
                game_button = game.xpath('.//a[@role="button"]')

                if game_button and 'href' in game_button[0].attrib:
                    game_url = self.base_url + game_button[0].attrib['href']
                else:
                    game_url = 'https://store.playstation.com'

                # Try to get game image from source tags with proper bounds checking
                sources = game.xpath('.//source')
                if len(sources) >= 3:
                    game_image = sources[2].attrib.get('srcset')
                elif len(sources) >= 1:
                    # Fallback to first available source
                    game_image = sources[0].attrib.get('srcset')
                elif i > 0:
                    # Fallback to previous game's image if available
                    prev_sources = games[i-1].xpath('.//source')
                    if len(prev_sources) >= 3:
                        game_image = prev_sources[2].attrib.get('srcset')
                    elif len(prev_sources) >= 1:
                        game_image = prev_sources[0].attrib.get('srcset')
                    else:
                        game_image = 'https://image.api.playstation.com/gs2-sec/appkgo/prod/CUSA02299_00/8/i_d3c3c3dd5cf8e284b68add3958c24353cf2b0c14f72c90cc8e3e98a1e5a6a8db/i/icon0.png'
                else:
                    # Default placeholder image for PlayStation
                    game_image = 'https://image.api.playstation.com/gs2-sec/appkgo/prod/CUSA02299_00/8/i_d3c3c3dd5cf8e284b68add3958c24353cf2b0c14f72c90cc8e3e98a1e5a6a8db/i/icon0.png'

                offer_from  = datetime.now()
                json_data = makejson.data(json_data, title, 1, game_url, game_image, offer_from)
            except Exception as e:
                self.logger.warning("Failed to parse game data at index %d: %s", i, e)

        return await self.compare(json_data)


    async def get(self):
        """
        psplus get
        """
        if await self.process_data():
            return 1
        return 0


if __name__ == "__main__":
    from utils import environment
    from utils.database import Database
    Database.connect(environment.DB)

    a = Main()
    asyncio.run(a.get())
    print(a.data)
