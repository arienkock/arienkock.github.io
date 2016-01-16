---
title: Blocking Similar Requests
---


When regular users can cause serious contention issues in your web-application (that make the whole thing unresponsive) simply by refreshing a specific page, it's probably a sign that something needs to be re-thought. Faced with just such an issue, I tried optimizing the requests, but some requests are still just really slow and cannot be easily cached. The ACTUAL solution is re-designing the interaction, possibly splitting it up into smaller steps, but until then! Rate limiting to the rescue!

Using Guava's cache and custom collections I made this [SimilarRequestLimitingFilter](https://gist.github.com/arienkock/3fc5e06db51f5b1eb04a). Incoming requests are remembered until they complete, and if the number of 'similar' requests exceeds a certain number, BAM! HTTP error 429! You don't know status code 429? It means ["slow your roll"](http://httpstatusdogs.com/429-too-many-requests).

To make sure this thing can actually withstand the high frequency of requests without itself becoming the point of contention, I did some measurements with JMeter and optimized the part where I do some logging. The most interesting part of that class is perhaps this:

		if (loggedKeysSet.getIfPresent(key) == null) {
			// lock on cache to do atomic putIfNotPresent
			synchronized (loggedKeysSet) {
				// must re-check if key exists once we have the lock
				// as some other thread may have gone before is 
				if (loggedKeysSet.getIfPresent(key) == null) {
					loggedKeysSet.put(key, key);
					// and continue
				} else {
					return;
				}
			}
		} else {
			return;
		}

It's interesting because it has a synchronization block which is used to perform an atomic operation. However, blocking is slow. So what I did was do the "should I do X?" check before getting a lock, then after acquiring the lock I do a "should I _still_ do X?" check to make sure nothing's changed between the first and second checks. Doing double the work may seem wasteful, but locking tends to be slow and the idea is that most code will NOT do double work, but back off after the first check fails.
