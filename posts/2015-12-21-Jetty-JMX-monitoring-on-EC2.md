---
title: Jetty JMX Monitoring on EC2
teaser: If you need this, read this
---


I hope this post will save someone from the frustration I've lived through trying to get this to work.

The RMI JMX ConnectorServer (what a name!) is the component that responds to the client when you try to load your MBeans into Visual VM or JConsole. The RMI documentation is pretty clear that a secondary connection is opened up which serves the actual remote object stub. This is why Jetty comes with a component that makes this slightly easier by unifying the ports. Did I lose you? I think it's likely that most Java devs don't work with RMI very often. Suffice it to say, two connections are required to get your JMX MBeans data. 

It was my grave mistake to assume that: Since, the second connection's endpoint is in the service URL (e.g. `service:jmx:rmi://<TARGET_MACHINE>:<JMX_RMI_SERVER_PORT>/jndi/rmi://<TARGET_MACHINE>:<RMI_REGISTRY_PORT>/jmxrmi`), that must also be the endpoint my client actually uses. Surely that would make sense. However, RMI (rightfully) doesn't know or care about JMX. So, RMI just knows that it needs to respond to the initial request with an IP and a port. That IP address is where things go wrong on EC2. EC2 instances don't know their external IP address. None of the network interfaces have it bound, so it cannot be resolved purely inside the instance. In `/$JETTY_HOME/etc/jetty-jmx-remote.xml` you can set a system property which tells the RMI Registry what its hostname is:

```
  <Call class="java.lang.System" name="setProperty">
    <Arg>java.rmi.server.hostname</Arg>
    <Arg>[ec2_ip].[availability_zone].compute.amazonaws.com</Arg>
  </Call>
```

Now it will respond with something that makes sense to the outside world.

This wouldn't have been a problem if Visual VM or JConsole gave more information than just _"I can't connect, yo"_. Writing a test application finally gave me a hint when I saw the instance's internal IP show up in the exception. RMI is pretty cool, considering how old it is. Cool, "Yes". Intuitive and user friendly, "No".
