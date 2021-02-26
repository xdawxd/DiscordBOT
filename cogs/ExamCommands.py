import os
import random
import discord
from discord.ext import commands


class ExamCommands(commands.Cog):
	groups = {}
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

	def edit_messages(self, channel):  # TODO
		pass

	def edit_data(self, file, id, emoji):
		content = self.read_data(file)
		content[id][1] = emoji

		file.truncate(0)
		self.write_data(content, file)

	@commands.Cog.listener()
	async def on_message(self, msg):
		channel = self.client.get_channel(812498438699614209)  # id of an channel the message is send to
		author_id = msg.author.id
		guild = msg.guild

		if msg.attachments and len(msg.content) > 0:
			emoji = random.choice(self.emojis)
			data = {author_id: [msg.content, emoji]}
			role_name = f'Grupa: {msg.content}'
			role_names = [gn.name for gn in guild.roles]

			self.emojis.remove(emoji)
			await msg.add_reaction(emoji)

			if role_name not in role_names:
				await guild.create_role(name=role_name)
				role = discord.utils.get(guild.roles, name=role_name)
				await msg.author.add_roles(role)
			else:
				role = discord.utils.get(guild.roles, name=role_name)
				await msg.author.add_roles(role)

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
							self.edit_data(file, str(author_id), value[1])

					users = [user for (user, group) in self.groups.items()]
					message = ''
					for user in users:
						message += f'<@{user}>, '

					await channel.send(f'{message} sa w \'{role_name}\'')

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.emoji and user != self.client.user:
			msg = reaction.message
			role_name = f'Grupa: {msg.content}'
			role = discord.utils.get(msg.guild.roles, name=role_name)
			await user.add_roles(role)

	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction, user):
		if reaction.emoji:
			msg = reaction.message
			role_name = f'Grupa: {msg.content}'
			role = discord.utils.get(msg.guild.roles, name=role_name)
			await user.remove_roles(role)

	@commands.has_permissions(manage_roles=True, ban_members=True)
	@commands.command()
	async def delete_roles(self, ctx):
		guild = ctx.message.guild
		roles = [role.name for role in ctx.message.guild.roles]
		for role_name in roles:
			if role_name.startswith('Grupa: '):
				role = discord.utils.get(guild.roles, name=role_name)
				await role.delete()
		await ctx.message.channel.send('Usunieto wszystkie grupy.')


def setup(client):
	client.add_cog(ExamCommands(client))
