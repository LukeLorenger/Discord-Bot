from discord.ext import commands

# Inherit from commands.Cog
class ExtensionAlpha(commands.Cog):

    # allows us to reference client, passing into cog
    def __init__(self, client):
        # allows accessing
        self.client = client
    # function decorator for event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print('ExtensionAlpha-cog is ready.')

    # cog commands
    @commands.command()
    async def pingAlpha(self, ctx):
        await ctx.send(f'Pong from ExtensionAlpha! {round(self.client.latency * 1000)}ms')

# setup function, allowing cog to connect to bot
def setup(client):
    # running add_cog method of client, passing in instance of Example class
    client.add_cog(ExtensionAlpha(client))