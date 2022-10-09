package com.mist.discordbot.listeners;

import com.mist.discordbot.Services.MessagingService;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.event.channel.server.ServerChannelCreateEvent;
import org.javacord.api.listener.channel.server.ServerChannelCreateListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;

@Configuration
public class TrialChannelCreationListener implements ServerChannelCreateListener {

    @Autowired
    private MessagingService messagingService;
    @Autowired
    Environment env;

    @Override
    public void onServerChannelCreate(ServerChannelCreateEvent serverChannelCreateEvent) {
        String channelName = serverChannelCreateEvent.getChannel().getName();
        if (channelName.matches("\\d+-trial-.+")) {
            String id = channelName.split("-")[0];
            String name = channelName.split("-")[2];
            messagingService.sendMessage(
                    "Application for " + name,
                    env.getProperty("URL") + "/" + id,
                    String.format("Click on the title to re-review the application. Good luck to %s on their trial!", name),
                    null,
                    null,
                    (TextChannel) serverChannelCreateEvent.getChannel()
            );
        }
    }
}
