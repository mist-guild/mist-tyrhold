package com.mist.discordbot.listeners;

import com.mist.discordbot.Services.MessagingService;
import org.javacord.api.event.message.MessageCreateEvent;
import org.javacord.api.listener.message.MessageCreateListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RecruitWebhookListener implements MessageCreateListener {

    @Autowired
    private MessagingService messagingService;

    @Override
    public void onMessageCreate(MessageCreateEvent messageCreateEvent) {
        try {
            Long id = messageCreateEvent.getMessageAuthor().getId();
            if (id.equals(1026049033439023155L)) {
                messageCreateEvent.getMessage().addReaction("\uD83D\uDC4D");
                messageCreateEvent.getMessage().addReaction("\uD83D\uDC4E");
                messageCreateEvent.getMessage().addReaction("\uD83D\uDDE3");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }

    }
}
