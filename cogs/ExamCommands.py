import os
import random
import discord
from discord.ext import commands


class ExamCommands(commands.Cog):
	groups = {}
	# messages = []
	with open('emojis.txt', encoding='utf-8') as file:
		emojis = [i.strip().split(' ')[0].strip('\\')[0] for i in file.readlines()]

	def __init__(self, client):
		self.client = client

	@staticmethod
	def write_data(data, file):
		for key, value in data.items():
			file.write(f'{key}: {str(value[0])} {str(value[1])}\n')

	@staticmethod
	def read_data(file):
		file.seek(0)
		f_formated = [i.strip().split(':') for i in file.readlines()]
		content = {item[0]: item[1].lstrip().split(' ') for item in f_formated}
		return content

	def edit_data(self, file, id, emoji):  # edit the emoji saved in data.txt so its the same as the user in their group
		content = self.read_data(file)
		content[id][1] = emoji

		file.truncate(0)
		self.write_data(content, file)

	@commands.Cog.listener()
	async def on_message(self, msg):
		author_id = msg.author.id
		channel = self.client.get_channel(812498438699614209)  # channel id
		ctx = await self.client.get_context(msg)
		# self.messages = await ctx.channel.history(limit=200).flatten()

		if msg.attachments and len(msg.content) > 0:
			emoji = random.choice(self.emojis)
			data = {author_id: [msg.content, emoji]}

			self.emojis.remove(emoji)
			await msg.add_reaction(emoji)

			with open('data.txt', 'a+', encoding='utf-8') as file:
				if not os.path.getsize('data.txt'):
					self.write_data(data, file)

				else:
					content = self.read_data(file)
					self.write_data(data, file)

					if author_id not in self.groups:
						self.groups[str(author_id)] = msg.content

					for key, value in content.items():
						group = str(value[0])
						if data[author_id][0] == group:
							if key not in self.groups:
								self.groups[key] = group

							await msg.clear_reaction(emoji)
							await msg.add_reaction(value[1])

							# guild = ctx.guild
							# role_name = f'Grupa: {value[0]}.'

							# if role_name not in guild.roles:
							# 	role = discord.utils.get(guild.roles, name=role_name)
							# 	user = msg.author

							# 	await guild.create_role(name=role_name)
							# 	await user.add_roles(role)

							self.edit_data(file, str(author_id), value[1])

					users = [user for (user, group) in self.groups.items()]
					message = ''
					for user in users:
						message += f'<@{user}>, '

					# for mess_d in self.messages:
					# 	if str(msg.author) in mess_d.content:
					# 		self.client.delete_message(mess_d) 	

					await channel.send(f'{message} sa w tej samej grupie.')
							

def setup(client):
	client.add_cog(ExamCommands(client))
