import discord
from discord.ext import commands


class ExamCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.command(name='react')
	@commands.has_permissions(manage_messages=True)  # We can change that later so every student can use that function
	async def add_reactions(self, ctx):
		keyword = 'kolokwium'  # we can use regex later on to do some advanced search
		channel = self.client.get_channel('PASS THE CHANNEL ID HERE')
		messages = await channel.history(limit=200).flatten()

		for message in messages:
			if message.attachments and keyword in message.content:
				await message.add_reaction("✅")

		print('Done!')

def setup(client):
	client.add_cog(ExamCommands(client))
