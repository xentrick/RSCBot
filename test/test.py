import discord
import os.path
import os

from .utils.dataIO import dataIO
from discord.ext import commands
from cogs.utils import checks

class Test:
    """My custom cog that does stuff!"""

    DATA_FOLDER = "data/test"
    CONFIG_FILE_PATH = DATA_FOLDER + "/config.json"

    CONFIG_DEFAULT = {}

    def __init__(self, bot):
        self.bot = bot
        self.check_configs()
        self.load_data()     

    @commands.command()
    async def mycom(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff!")

    @commands.command()
    async def punch(self, user : discord.Member):
        """I will punch anyone! >.<"""

        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

    @commands.command(pass_context=True)
    async def draft(self, ctx, user : discord.Member, teamRole : discord.Role):
        server = ctx.message.server
        server_dict = self.config.setdefault(server.id, {})
        channel = server_dict[server.id]

        if channel:
            await self.bot.add_roles(user, teamRole)
            await self.bot.say(server.get_channel(channel), user.mention + " was drafted onto the " + teamRole)
        else:
            await self.bot.say(":X: Transaction log channel not set")

    @commands.command(pass_context=True)
    async def setTransactionLogChannel(self, ctx, tlog : discord.Channel):
        """Sets transaction-log channel"""
        server = ctx.message.server
        server_dict = self.config.setdefault(server.id, {})

        server_dict.setdefault('Transaction Channel', tlog.id)
        await self.save_data()
        await self.bot.say("Transaction Log channel set to " + tlog)

    # Config
    def check_configs(self):
        self.check_folders()
        self.check_files()

    def check_folders(self):
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER, exist_ok=True)

    def check_files(self):
        self.check_file(self.CONFIG_FILE_PATH, self.CONFIG_DEFAULT)

    def check_file(self, file, default):
        if not dataIO.is_valid_json(file):
            dataIO.save_json(file, default)

    def load_data(self):
        self.config = dataIO.load_json(self.CONFIG_FILE_PATH)

    def save_data(self):
        dataIO.save_json(self.CONFIG_FILE_PATH, self.config)

def setup(bot):
    bot.add_cog(Test(bot))