package com.mist.discordbot.listeners;

import org.javacord.api.entity.channel.Channel;
import org.javacord.api.entity.channel.ServerTextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.listener.message.MessageCreateListener;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DeleteRecruitChannelListener implements MessageCreateListener {

    @Override
    public void onMessageCreate(MessageCreateEvent messageCreateEvent) {
        String message = messageCreateEvent.getMessageContent();
        ServerTextChannel channel = (ServerTextChannel) messageCreateEvent.getChannel();

        if (message.equals("!endtrial")) {
            if (channel.getName().matches("\\d+-trial-.+")) {

            }
        }
    }
}
