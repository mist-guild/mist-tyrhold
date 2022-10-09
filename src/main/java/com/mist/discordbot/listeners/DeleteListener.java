package com.mist.discordbot.listeners;

import org.javacord.api.event.message.reaction.ReactionAddEvent;
import org.javacord.api.listener.message.reaction.ReactionAddListener;
import org.springframework.stereotype.Component;

@Component
public class DeleteListener implements ReactionAddListener {

    @Override
    public void onReactionAdd(ReactionAddEvent reactionAddEvent) {
        if (reactionAddEvent.getEmoji().equalsEmoji("❌")) {
            reactionAddEvent.deleteMessage();
        }
    }
}
