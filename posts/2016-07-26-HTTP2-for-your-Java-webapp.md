---
title: Simple and free HTTP/2
teaser: LetsEncrypt, HAProxy, and Jetty
---

If you're wondering about [the what and why of HTTP/2](https://http2.github.io/faq/), then maybe this article isn't for you. However, if you you're interested in an overview of the steps required to set it up quickly and safely, then it just might be. One thing I will say in case there is any doubt in your mind about the value: it promotes the use of HTTPS (which means a safer internet) while also improving performance.

### The Stack
I'll be going through the creation of a web server stack comprised of (most notably) [HAProxy](http://www.haproxy.org/), [Jetty](http://www.eclipse.org/jetty/) and [Let’s Encrypt](https://letsencrypt.org/). I'll explain these choices briefly...

When [I wrote about SPDY](http://positor.nl/2014/09/20/spdy-in-your-webapp.html "An older article about SPDY") the clear winner on Java server side implementations was Jetty. You have a lot of [Java servers with HTTP/2 support](https://github.com/http2/http2-spec/wiki/Implementations) to choose from, but I'm a fan of Jetty's innovative tendencies, so it's my go to project.

The aim is to set up a 2-tiered web server with HAProxy in front of Jetty doing TLS offloading. HAProxy has a tcp mode allowing it to send the cleartext HTTP/2 requests to Jetty but not parsing or processing any of the content, letting the Server PUSH and all other features work transparently. Why not let Jetty do everything? For one, HAProxy can do TLS faster than Java can. I've never tested this myself, but it seems commonly accepted. Secondly, having a quasi-permanent reverse proxy in front of the application allows for smoother deployment scenarios.

TLS is a requirement to use HTTP/2 and that's where "Let's Encrypt" comes in. Being a free Certificate Authority, it has brought the potential of TLS and HTTP/2 to the masses.

### The Steps
TL;DR

1. Compile HAProxy with a version of OpenSSL that supports ALPN (protocol negotiation, required). *Skip this if you're reading from the future where your Linux distro's prepackaged HAProxy is already up-to-date.*
2. Configure Jetty's HTTP/2 connector.
3. Run the "Let's Encrypt" bot
4. Configure HAProxy with A-rated security features (rated by SSLLabs)
5. Configure HAProxy + Let's Encrypt bot for automatic certificate renewal

#### 1. Compile HAProxy
According to Wikipedia 

> "OpenSSL [supports ALPN] since version 1.0.2 released in January 2015". 

Yet, at the time of this writing many Linux distributions haven't updated their OpenSSL versions yet. We need to compile and statically link a newer version. [Here is a script that does it for you](https://gist.githubusercontent.com/arienkock/72ef8d5607dea00022041838b839d392/raw/provide-haproxy.sh) (made for and tested on Debian Jessie). I also made [a Docker image for HAProxy with ALPN support](https://hub.docker.com/r/arienkock/haproxy-alpn/). Pretty simple.

#### 2. Configure Jetty's HTTP/2 connector
If you're using Jetty's official distribution package, then enabling the right modules takes care of everything. No need to edit XML or anything like that. Here's what the command would look like using the official Jetty Docker image:

```sh
/usr/bin/docker run --name my-jetty \
  -p 8080:8080 \
  -v /path/to/your/webapps/:/var/lib/jetty/webapps/ \
  jetty --module=http2c,deploy,servlet
```

#### 3. Run the "Let's Encrypt" bot

I hate to be all RTFM on you, but it's really as simple as running:

```sh
curl -sO https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
./certbot-auto certonly -n --agree-tos --standalone \
  --email your@emailaddress.com -d "www.example.org"
# a dir to store your combined certificates
mkdir -p /etc/haproxy/certs/
cat /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
  /etc/letsencrypt/live/$DOMAIN/privkey.pem > /etc/haproxy/certs/$DOMAIN.pem
```

#### 4. Configure HAProxy with A-rated security features

After setting these config values, you should be able to get this little (very satisfying) report:

<img src="/images/ssllabs_report_thumb.png" alt="A-rated recurity report" title="ssllabs report: A-rating" style="margin: auto; display: block"/>

Add the following lines to your listener or global sections of haproxy.cfg (for a complete example config look at step 5)

```text
tune.ssl.default-dh-param 2048
ssl-default-bind-ciphers EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
```

and in your frontend section, make sure you use these (the location of your cert file may differ, of course):

```text
bind :443 ssl no-sslv3 no-tls-tickets crt /usr/local/etc/haproxy/haproxy-cert.pem alpn h2,http/1.1
```

#### 5. Automatic certificate renewal

Few things feel as good as automating menial tasks. What you're doing in this step is allowing the "Let's Encrypt" service get its challenge response (a file needed to prove that you own the domain) be served through HAProxy. This is something that is supported out of the box for many other proxies/servers, but requires some extra effort for us. Here is [a full haproxy.cfg example](https://gist.githubusercontent.com/arienkock/aedc48b2d44acf4e06bd13840100fdee/raw/haproxy.cfg) that includes a special `backend letsencrypt` section and `acl` rule for exactly this purpose. Lastly, you can run the following script (which makes certain assumptions, so make sure you read it before use) from cron to ensure your certificate never expires:

```sh
#!/usr/bin/env bash
set -x -e
MD5_BEFORE=`md5sum /etc/letsencrypt/live/your.domain.com/fullchain.pem`
certbot-auto --agree-tos --noninteractive --standalone --standalone-supported-challenges http-01 --http-01-port 9999 renew
MD5_AFTER=`md5sum /etc/letsencrypt/live/your.domain.com/fullchain.pem`

# concatenate the certificates and only restart on change
if [ "$MD5_BEFORE" != "$MD5_AFTER" ]; then
  cat /etc/letsencrypt/live/your.domain.com/{fullchain.pem,privkey.pem} > /home/uitguru/haproxy/haproxy-cert.pem
  systemctl restart haproxy
fi
```

### Conclusion

HTTP/2 is faster and requires TLS, promoting security while improving the user experience. There are plenty of OSS projects to choose from and the only reasons for not using it are laziness and unfamiliarity. If you think anyone needs convincing, link them to this article. Everyone wins.
