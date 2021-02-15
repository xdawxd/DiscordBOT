import discord
from discord.ext import commands


class BotStart(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):

		game = discord.Game("Type .help for the list of commands.")
		await self.client.change_presence(activity=game)

		print('Bot is ready.')
		

def setup(client):
	client.add_cog(BotStart(client))
