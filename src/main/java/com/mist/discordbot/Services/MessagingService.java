package com.mist.discordbot.Services;

import com.mist.discordbot.listeners.DeleteListener;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.MessageAuthor;
import org.javacord.api.entity.message.MessageBuilder;
import org.javacord.api.entity.message.embed.EmbedBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.awt.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

@Component
public class MessagingService {

    @Autowired
    private DeleteListener deleteListener;

    public CompletableFuture<Message> sendMessage(MessageAuthor author, String title, String description, String footer, String thumbnail, TextChannel textChannel) {
        return new MessageBuilder().setEmbed(new EmbedBuilder()
                .setAuthor(author)
                .setTitle(title)
                .setDescription(description)
                .setFooter(footer)
                .setThumbnail(thumbnail)
                .setColor(generateColor()))
                .send(textChannel);
    }

    public void sendMessage(MessageAuthor author, String title, String description, String footer, String thumbnail, TextChannel textChannel, boolean withDelete) {
        this.sendMessage(author, title, description, footer, thumbnail, textChannel).thenAccept(
                message -> message.addReactionAddListener(deleteListener)
                        .removeAfter(1, TimeUnit.MINUTES)
        );
    }

    private Color generateColor() {
        int red = (int) Math.floor(Math.random() * 255);
        int green = (int) Math.floor(Math.random() * 255);
        int blue = (int) Math.floor(Math.random() * 255);

        return new Color(red, green, blue);
    }
}
