

class DiscordUtility:
    @staticmethod
    def get_applicant_id_from_channel_name(channel_name):
        channel_split = channel_name.split("-")
        return channel_split[len(channel_split) - 1]
