import os

from alttprbot.alttprgen.randomizer import roll_z1r
from alttprbot.tournament.core import TournamentConfig
from alttprbot_discord.bot import discordbot
from .sglcore import SGLRandomizerTournamentRace


class Z1R(SGLRandomizerTournamentRace):
    async def configuration(self):
        guild = discordbot.get_guild(590331405624410116)
        return TournamentConfig(
            guild=guild,
            racetime_category='sgl',
            racetime_goal="Zelda 1 Randomizer",
            event_slug="sgl21z1r",
            audit_channel=discordbot.get_channel(772351829022474260),
            commentary_channel=discordbot.get_channel(631564559018098698),
            stream_delay=15,
            coop=False,
            gsheet_id=os.environ.get("SGL_RESULTS_SHEET"),
            auto_record=True
        )

    async def roll(self):
        self.seed_id, self.flags = roll_z1r('gLMg3JukA0S9sq8tnMpPiZS5CtQHWW')

    @property
    def seed_info(self):
        return f"Seed: {self.seed_id} - Flags: {self.flags}"
