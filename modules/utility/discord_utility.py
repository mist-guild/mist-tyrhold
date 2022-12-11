import os
import discord


class DiscordUtility:
    @staticmethod
    def get_applicant_id_from_recruit_channel_name(channel_name):
        channel_split = channel_name.split("-")
        return channel_split[len(channel_split) - 1]

    @staticmethod
    def get_applicant_id_from_archive_channel_name(channel_name):
        channel_split = channel_name.split("-")
        return channel_split[len(channel_split) - 2]
    
    @staticmethod
    def get_category_by_id(guild, category_id):
        return discord.utils.get(guild.categories, id=category_id)
    
    @staticmethod
    async def create_text_channel(guild, channel_name, category):
        channel = await guild.create_text_channel(name=channel_name, category=category)
        return channel

    @staticmethod
    async def get_role_by_id(guild, role_id):
        return discord.utils.get(guild.roles, id=role_id)

    @staticmethod
    async def get_users_by_role(guild, role_id):
        return get_role_by_id(guild, role_id).members