package com.mist.discordbot.listeners;

import com.mist.discordbot.Services.MessagingService;
import org.javacord.api.entity.channel.ChannelCategory;
import org.javacord.api.entity.channel.ServerTextChannel;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.listener.message.MessageCreateListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Optional;
import java.util.concurrent.CompletableFuture;

@Component
public class CreateRecruitChannelListener implements MessageCreateListener {

    @Autowired
    private MessagingService messagingService;

    @Override
    public void onMessageCreate(MessageCreateEvent messageCreateEvent) {
        Long channelId = messageCreateEvent.getChannel().getId();
        String message = messageCreateEvent.getMessageContent();

        if (channelId.equals(1026048915688140800L) && message.startsWith("!trial")) {
            String[] split = message.split(" ");
            if (split.length != 3) {
                messagingService.sendMessage(
                        messageCreateEvent.getMessageAuthor(),
                        null,
                        "Please ensure your command follows this skeleton: !trial id name",
                        "This message will delete itself in 1 minute. 💣",
                        null,
                        messageCreateEvent.getChannel(),
                        true
                );
                return;
            }

            String id = split[1];
            String name = split[2];

            Optional<ChannelCategory> category = messageCreateEvent.getServer()
                    .get()
                    .getChannelCategoryById("992720873528246294");
            if (category.isPresent()) {
                CompletableFuture<ServerTextChannel> newChannel = messageCreateEvent.getServer()
                        .get()
                        .createTextChannelBuilder()
                        .setName(String.format("%s-trial-%s", id, name))
                        .setCategory(category.get())
                        .create();
                }
        }
    }
}
