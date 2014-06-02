---
layout: post
---
I think it's safe to say that NodeJS modules like [Gulp](http://gulpjs.com) and [Grunt](http://gruntjs.com/) have revolutionized the way the frontend workflows... well... work. There is one notable effort to integrate frontend workflows into your Java build. Namely [JHipster](http://jhipster.github.io/). Setting aside the J-prefix, I dislike the name. It seems to suggest that using AngularJS or Yeoman puts you ahead of the curve or on the bleeding edge of something. How can you expect it to ever be taken seriously when you call your project J__Hipster__ for keeping up with the normal evolution of technology. Java has an image of stable, but boring and old-fashioned. Names like JHipster make me think that it is in no small part thanks to the Java community itself.

The way JHipster does the integration is by using the [yeoman-maven-plugin](https://github.com/trecloux/yeoman-maven-plugin). However, I have an alternative that I like better: [frontend-maven-plugin](https://github.com/eirslett/frontend-maven-plugin). Using the frontend plugin, you don't need to install node+npm yourself. You can specify the version of node you want to use, which is great for having repeatable results in CI. It also lets you choose between Gulp and Grunt. Thanks to certain Gulp plugins ([gulp-cached](https://www.npmjs.org/package/gulp-cached) and [gulp-remember](https://www.npmjs.org/package/gulp-remember)) the rebuild times when watching sources are extremely fast, so this is what I went with myself. Together with Jetty I can serve up my dev-backend with my dev-frontend in one server instance. 

This is how you do it. **Step 1**, add the frontend plugin.

	<plugin>
		<groupId>com.github.eirslett</groupId>
		<artifactId>frontend-maven-plugin</artifactId>
		<version>0.0.14</version>
		<executions>
			<execution>
				<id>install node and npm</id>
				<goals>
					<goal>install-node-and-npm</goal>
				</goals>
				<phase>generate-resources</phase>
				<configuration>
					<nodeVersion>v0.10.26</nodeVersion>
					<npmVersion>1.4.3</npmVersion>
				</configuration>
			</execution>
			<execution>
				<id>npm install</id>
				<goals>
					<goal>npm</goal>
				</goals>
				<phase>generate-resources</phase>
			</execution>
			<execution>
				<id>gulp build</id>
				<goals>
					<goal>gulp</goal>
				</goals>
				<phase>generate-resources</phase>
			</execution>
		</executions>
	</plugin>

The phase you bind your executions to is important! If you want to automatically build your resources __each time__ before Jetty starts, then add it somewhere before `test-compile` like I did in the example. HOWEVER, if you're continuously working on the frontend code, and are starting something like `gulp watch` in parallel, then you don't need to let Maven do it at all and you can comment it out completely until you need it again. This will speed up your Jetty restarts by a lot during development. Your rebuilt html/js/css will be available anyway, because (**Step 2**) you're adding extra resource locations to Jetty. Assuming your `gulpfile.js` is writing to the target directory `target/assets`, you can do it like so:

	<plugin>
		<groupId>org.eclipse.jetty</groupId>
		<artifactId>jetty-maven-plugin</artifactId>
		...
		<configuration>
			...
			<webApp>
				<resourceBases>
					<resourceBase>src/main/webapp</resourceBase>
					<resourceBase>target/assets</resourceBase>
				</resourceBases>
			</webApp>
		</configuration>
	</plugin>

**Step 3** has to do with your templates. I use [Thymeleaf](http://www.thymeleaf.org/) templates which get processed and minified by my Gulp build. I have Gulp put them in `target/assets/WEB-INF/templates` which Jetty will add to the context classpath. You have to turn off all the caching so your changes are immediately visible. Since I use Spring, my view resolver config looks like this:

	@Bean
	public ThymeleafViewResolver thymeleafViewResolver(WebApplicationContext wac) {
		ThymeleafViewResolver resolver = new ThymeleafViewResolver();
		SpringTemplateEngine templateEngine = new SpringTemplateEngine();
		ServletContextTemplateResolver templateResolver = new ServletContextTemplateResolver();
		templateResolver.setPrefix("/WEB-INF/templates/");
		templateResolver.setSuffix(".html");
		templateResolver.setTemplateMode("HTML5");
		templateResolver.setCharacterEncoding("UTF-8");
		templateEngine.setTemplateResolver(templateResolver);
		resolver.setTemplateEngine(templateEngine);
		resolver.setOrder(2);
		resolver.setApplicationContext(wac);
		resolver.setCharacterEncoding("UTF-8");
		// caching
		String[] activeProfiles = environment.getActiveProfiles();
		System.err.println("profiles : " + activeProfiles);
		if (Arrays.asList(activeProfiles).contains("dev")) {
			System.err.println("IMPORTANT: ==DEV== PROFILE IS ON!!!");
			templateResolver.setCacheable(false);
			templateEngine.setCacheManager(null);
			resolver.setCache(false);
		}
		return resolver;
	}

Notice how I use the active profile to determine whether or not to turn off caching, this way I cannot forget to turn it back on in production. Please ignore `System.err.println`. I do actually use proper SLF4J logging in most places!

**Step 4** is do your development thing! Start Jetty and assuming you have a auto-rebuild Gulp task defined with the name `watch`, run both:

	(mvn jetty:run &); (gulp watch &)

###Is this worth the trouble?
IMO: absolutely. JHipster is a great way to get a workflow started with a powerful stack. However, I like understanding the tech better before I adopt it so I made my own. In the end I like my solution better, because I was free to choose my own stack (Gulp and **no** Bower modules) and I now understand the inner workings of the tools much better. I can recommend anyone that considers themselves to be a java-based full-stack developer learn to use these tools.
