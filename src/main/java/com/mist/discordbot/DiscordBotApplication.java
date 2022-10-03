package com.mist.discordbot;

import com.mist.discordbot.listeners.CreateRecruitChannelListener;
import com.mist.discordbot.listeners.DeleteListener;
import com.mist.discordbot.listeners.DeleteRecruitChannelListener;
import com.mist.discordbot.listeners.RecruitWebhookListener;
import org.javacord.api.DiscordApi;
import org.javacord.api.DiscordApiBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.core.env.Environment;


@SpringBootApplication
public class DiscordBotApplication {

	private static final String DISCORD_LOGIN_TOKEN = System.getenv("DISCORD_TOKEN");

	@Autowired
	private Environment env;

	@Autowired
	RecruitWebhookListener recruitWebhookListener;
	@Autowired
	CreateRecruitChannelListener createRecruitChannelListener;
	@Autowired
	DeleteListener deleteListener;
	@Autowired
	DeleteRecruitChannelListener deleteRecruitChannelListener;


	public static void main(String[] args) {
		SpringApplication.run(DiscordBotApplication.class, args);
	}

	@Bean
	@ConfigurationProperties(value = "discord-api")
	public DiscordApi discordApi() {
		//String token = env.getProperty("TOKEN");
		DiscordApi api = new DiscordApiBuilder().setToken(DISCORD_LOGIN_TOKEN)
				.setAllNonPrivilegedIntents()
				.login()
				.join();

		api.addMessageCreateListener(recruitWebhookListener);
		api.addMessageCreateListener(createRecruitChannelListener);
		api.addReactionAddListener(deleteListener);
		api.addMessageCreateListener(deleteRecruitChannelListener);

		return api;
	}

}
