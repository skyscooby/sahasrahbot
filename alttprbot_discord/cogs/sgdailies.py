import dateutil.parser
import discord
from discord.commands import Option
from discord.ext import commands
from alttprbot.util import speedgaming
import os

ALTTP_RANDOMIZER_SERVERS = list(map(int, os.environ.get("ALTTP_RANDOMIZER_SERVERS", "").split(',')))


class SgDaily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sgdaily")
    async def sgdaily_oldcmd(self, ctx: commands.Context):
        await ctx.reply("Please use the /sgdaily command instead.")

    @commands.slash_command(name="sgdaily", guild_ids=ALTTP_RANDOMIZER_SERVERS)
    async def sgdaily_cmd(
        self,
        ctx: discord.ApplicationContext,
        number_of_days: Option(int, description="Number of days to lookup.", default=1)
    ):
        """
        Retrieves the next SG daily race.
        """
        sg_schedule = await speedgaming.get_upcoming_episodes_by_event("alttprdaily", hours_past=0, hours_future=192)
        if len(sg_schedule) == 0:
            await ctx.respond("There are no currently SpeedGaming ALTTPR Daily Races scheduled within the next 8 days.")
            return

        if number_of_days == 1:
            embed = discord.Embed(
                title=sg_schedule[0]['event']['name'],
                description=f"**Mode:** {'*TBD*' if sg_schedule[0]['match1']['title'] == '' else sg_schedule[0]['match1']['title']}\n[Full Schedule](http://speedgaming.org/alttprdaily)"
            )
        else:
            embed = discord.Embed(
                title="ALTTP Randomizer SG Daily Schedule",
                description="[Full Schedule](http://speedgaming.org/alttprdaily)"
            )

        for episode in sg_schedule[0:number_of_days]:
            when = dateutil.parser.parse(episode['when'])
            if number_of_days == 1:
                embed.add_field(
                    name='Time', value=f"{discord.utils.format_dt(when, 'f')} ({discord.utils.format_dt(when, 'R')})", inline=False)
                broadcast_channels = [a['slug'] for a in episode['channels'] if not " " in a['name']]
                if broadcast_channels:
                    embed.add_field(name="Twitch Channels", value=', '.join(
                        [f"[{a}](https://twitch.tv/{a})" for a in broadcast_channels]), inline=False)
            else:
                embed.add_field(
                    name='TBD' if episode['match1']['title'] == '' else episode['match1']['title'],
                    value=discord.utils.format_dt(when, 'f'),
                    inline=False
                )
        embed.set_footer()

        embed.set_thumbnail(
            url='https://pbs.twimg.com/profile_images/1185422684190105600/3jiXIf5Y_400x400.jpg')
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(SgDaily(bot))
