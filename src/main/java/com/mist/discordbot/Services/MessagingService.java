package com.mist.discordbot.Services;

import com.mist.discordbot.listeners.DeleteListener;
import org.javacord.api.entity.channel.ServerTextChannel;
import org.javacord.api.entity.channel.ServerTextChannelBuilder;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.MessageBuilder;
import org.javacord.api.entity.message.embed.EmbedBuilder;
import org.javacord.api.event.message.MessageCreateEvent;
import org.springframework.beans.factory.annotation.Autowired;

import java.awt.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

public class MessagingService {

    @Autowired
    private DeleteListener deleteListener;

    public CompletableFuture<Message> sendRecruitMessage(String title, String description, String footer) {
        int red = (int) Math.floor(Math.random() * 255);
        int blue = (int) Math.floor(Math.random() * 255);
        int green = (int) Math.floor(Math.random() * 255);

        ServerTextChannelBuilder serverTextChannelBuilder = new ServerTextChannelBuilder()
        TextChannel textChannel = event.getGuild().getTextChannelsByName("CHANNEL_NAME",true).get(0)
        return new MessageBuilder().setEmbed(new EmbedBuilder()
                .setTitle(title)
                .setDescription(description)
                .setFooter(footer)
                .setColor(new Color(red, green, blue)))
                .send();
    }

    public CompletableFuture<Message> sendMessage(MessageCreateEvent event, String title, String description, String footer) {
        int red = (int) Math.floor(Math.random() * 255);
        int blue = (int) Math.floor(Math.random() * 255);
        int green = (int) Math.floor(Math.random() * 255);

        return new MessageBuilder().setEmbed(new EmbedBuilder()
                .setAuthor(event.getMessageAuthor())
                .setTitle(title)
                .setDescription(description)
                .setFooter(footer)
                .setColor(new Color(red, green, blue)))
                .send(event.getChannel());
    }

    public void sendMessage(MessageCreateEvent event, String title, String description, String footer, boolean withDelete) {
        if (withDelete) {
            this.sendMessage(event, title, description, footer)
                .thenAccept(message -> message.addReactionAddListener(deleteListener).removeAfter(5, TimeUnit.MINUTES));
        } else {
            this.sendMessage(event, title, description, footer);
        }
    }
}
