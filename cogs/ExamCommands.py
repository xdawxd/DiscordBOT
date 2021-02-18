import re  # add a regex to the keyword
import discord
from discord.ext import commands

'''
Idea:
try to make a emoji list, and react with one of them to a user photo

if user adds a photo and a comment for e.g '11278' <- group of the exam
the group gets stored in a list or database
so if the group repeats the bot adds the same reaction to the other photo with the same group
and somehow informs the users that they're in the same group.

'''

class ExamCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.command(name='react')
	@commands.has_permissions(manage_messages=True)  # We can change that later so every student can use that function
	async def add_reactions(self, ctx):
		await ctx.send('Command is running.')

		keywords = {'A': '🇦', 'B': '🇧', 'C': '🇨', 'D': '🇩', 'E': '🇪', 'F': '🇫'}
		channel = self.client.get_channel(809235905884979263)

		while True:
			messages = await channel.history(limit=200).flatten()

			for message in messages:
				for keyword in keywords:
					if keyword in message.content and message.attachments:
						await message.add_reaction(keywords[keyword])

		print('Done!')

def setup(client):
	client.add_cog(ExamCommands(client))
