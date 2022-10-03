package com.mist.discordbot.listeners;

import com.mist.discordbot.Services.MessagingService;
import org.javacord.api.entity.channel.*;
import org.javacord.api.entity.message.Message;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.listener.message.MessageCreateListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.swing.text.html.Option;
import java.util.Optional;

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
            if (split.length != 3) return;

            String id = split[1];
            String name = split[2];

            Optional<ChannelCategory> category = messageCreateEvent.getServer()
                    .get()
                    .getChannelCategoryById("992720873528246294");
            if (category.isPresent()) {
                messageCreateEvent.getServer()
                        .get()
                        .createTextChannelBuilder()
                        .setName(String.format("%s-trial-%s", id, name))
                        .setCategory(category.get())
                        .create();
            }
        }
    }
}
