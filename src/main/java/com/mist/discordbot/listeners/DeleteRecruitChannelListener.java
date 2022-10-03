package com.mist.discordbot.listeners;

import com.mist.discordbot.Services.MessagingService;
import org.javacord.api.entity.channel.Channel;
import org.javacord.api.entity.channel.ServerTextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.listener.message.MessageCreateListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DeleteRecruitChannelListener implements MessageCreateListener {

    @Autowired
    private MessagingService messagingService;

    @Override
    public void onMessageCreate(MessageCreateEvent messageCreateEvent) {
        String message = messageCreateEvent.getMessageContent();
        ServerTextChannel channel = (ServerTextChannel) messageCreateEvent.getChannel();

        if (message.equals("!endtrial")) {
            if (channel.getName().matches("\\d+-trial-.+")) {
                channel.delete();
            }
            messagingService.sendMessage(
                    null,
                    null,
                    "Please ensure you execute !endtrial in a trial channel! It should follow this naming pattern: id-trial-name.",
                    "This message will delete itself in 1 minute. 💣",
                    null,
                    messageCreateEvent.getChannel(),
                    true
            );
        }
    }
}
