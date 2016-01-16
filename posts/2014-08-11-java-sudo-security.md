---
title: A `sudo` security model for Java
teaser: A more sophisticated solution than Java EE
---
I like the way Unix-like systems deal with security and during the course of my work I've encountered many occasions where such a model would be very useful in my Java code. When setting up a Unix-like OS, the security model often boils down to:

1. Creating users with very limited permissions. Followed by...
2. Allowing them to perform a specific tasks in a specific context using `sudo` rules.

The benefit of a model like this is that it forces you to think about what the user needs to be able to do. That is, if you stick to it. Managing these rules can become a hassle, so you may sometimes just give a user ALL `sudo` permissions. 

Needless to say, this model is a bit more expressive than the [Java EE Security Model](http://docs.oracle.com/javaee/7/tutorial/doc/security-intro.htm), which facilitates application security using abstractions such as realms, groups, and roles. However, this doesn't fit my mental model of user authorization. A user is in a group or it is not, it has a role or it doesn't. In Java EE these are facts and do not change based on context. For example, there is no concept of ownership. A user cannot have the role 'owner', because it would always have no matter what object we were talking about. A user should be able to 'manage' a group of objects, while not always being in the 'managers' user group. The Java EE model may not cover these cases, but it doesn't stop us from implementing such a system ourselves. So, I decided to do a little experiment.

### Substitute User (ie. `su`)
The first step is being able to assume a role. Without much fuss we can write some code that replaces the "current user" with a new one, and putting it back after we're done with our task. The concept of a "current user" here is relative to our own context. We define the rules by which our application and all its components should play, so we may as well define our own security context. The task in the following code sample runs within that security context.

	public class AppSec {
		private static InheritableThreadLocal<Queue<User>> userStack;
		...
		public static <T> T sudo(User user, Callable<T> task) throws Exception {
			userStack.get().add(user);
			try {
				return task.call();
			} finally {
				userStack.get().remove();
			}
		}
		...
	}

Notice I use a stack, because we should be able to nest calls to our Java `sudo`. The `InheritableThreadLocal` is used so that we can spawn new threads from within an `AppSec.sudo` call and retain the security context. The use of `finally` ensures we pop back the correct parent user when we exit our task. Application code needs to be able to inspect the current user at any time.

	public static User currentUser() {
		return userStack.get().peek();
	}

And we may want to know how deep we're nested or exactly who called our code.

	public static List<User> getIdentityChain() {
		// create a copy because no one but us should have access to the actual stack
		return new ArrayList<User>(userStack.get());
	}

For use in multiple threads the sudo call should be synchronized, yes? Not in this case since the ThreadLocal stack is unique for each thread, so there is no concurrent access to the stack itself.

The complete code including unit tests can be found on [my GitHub repo](https://github.com/arienkock/java-sudo-impersonation).

### In Summary
This is a first step in creating a more expressive security model that applies to any Java application. Not just webapps. When you are very strict about which users are allowed to modify your entities, you'll get early warnings during development when your own code tries to delete something it doesn't have permissions for. 

At work I've started creating a similar system and it's already caused us to rethink certain permissions. For example, an anonymous user is allowed to register a new account, but that also means editing the account to add some default info. Anonymous users aren't allowed to edit user accounts. So, during the atomic step of creating the account we should assume (`AppSec.sudo`) the new user's identity before proceeding to the next step of the registration process.
 
The next step is to use this model to introduce the same elements as in a Unix-like `sudo` execution, which are the __task__ and the __context__. The task is some application specific operation and the context is the operand/subject of that operation.
