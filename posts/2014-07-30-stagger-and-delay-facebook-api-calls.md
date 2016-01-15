---
layout: post
title: Stagger/Delay Your Facebook API Calls
---
Web API providers like Facebook and Twitter have  guidelines for using their API's and one of them is with regards to [request rate](https://developers.facebook.com/docs/reference/ads-api/api-rate-limiting/). If you get blocked, then you can simply wait for the block to be lifted, but a better way would be to limit your request rate so you **don't** get Facebook's infamous...

> It looks like you were misusing this feature by going too fast. You've been blocked from using it. Learn more about blocks in the Help Center.

My solution to this problem was to use a `HttpRequestInterceptor` to use together with [HttpComponents HttpClient](http://hc.apache.org/). 

<script src="https://gist.github.com/arienkock/58efbc6f0e1426546e41.js"></script>

The next step is to create an HttpClient instance that uses this. In Spring I defined a bean as follows:

	import org.springframework.social.facebook.api.impl.FacebookTemplate;
	import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
	import org.apache.http.impl.client.HttpClients;
	...
	public class AppConfig {
		...
		@Autowired
		private Environment environment;
		...

		@Bean
		public FacebookTemplate  facebookTemplate() {
			FacebookTemplate facebookTemplate = new FacebookTemplate(
					environment.getRequiredProperty("facebook.accessToken"));
			facebookTemplate.setRequestFactory(httpRequestFactory());
			return facebookTemplate;
		}
	
		@Bean
		public HttpComponentsClientHttpRequestFactory httpRequestFactory() {
			HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(httpClient());
			requestFactory.setConnectTimeout(Integer.parseInt(environment
					.getProperty("httpclient.connectTimeout")));
			requestFactory.setReadTimeout(Integer.parseInt(environment
					.getProperty("httpclient.soTimeout")));
			return requestFactory;
		}
	
		@Bean(destroyMethod = "close")
		public HttpClient httpClient() {
			return HttpClients
					.custom()
					.setConnectionManager(new PoolingHttpClientConnectionManager())
					.addInterceptorFirst(
							new FixedRateInterceptor(0.42D, "graph.facebook.com"))
					.build();
		}
	}

Facebook isn't 100% clear about the limits, but slightly less than 1 request every 2 seconds tends to work pretty well in my experience. Twitter is [a bit more clear about it](https://dev.twitter.com/docs/rate-limiting/1.1).
