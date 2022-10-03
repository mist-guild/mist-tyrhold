package com.mist.discordbot.listeners;

import com.mist.discordbot.Services.MessagingService;
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
            if (split.length != 2) return;


            System.out.println(split[0]);
            System.out.println(split[1]);
            System.out.println(split.length);


        }
    }
}
