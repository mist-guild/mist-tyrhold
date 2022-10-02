package com.mist.discordbot;

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
		return api;
	}

}
