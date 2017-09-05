---
title: Flyway and Hibernate
teaser: Some tips on combinging the two
---

How you use your RDBMS can vary wildly from: "I don't know or care about the specifics". All the way to: "I want to use as much SQL as possible and write my own RowMappers". A great write-up on the subject and accompanying controversy can be found in [The Vietnam of Computer Science](http://blogs.tedneward.com/post/the-vietnam-of-computer-science/). If your project tends to lean anywhere on the former side of that spectrum, you'll likely encounter problems when mis-management of your schema comes back to haunt you. You simply __can not__ ignore the specifics of your database. Enter Flyway. (I'll be up front and say that these tips aren't specific to either Flyway OR Hibernate, but I use these names since they are the tools I've used.)

### Schema Changes

Whether changes are driven by the DB or the application's domain layer doesn't matter much. The solution is making changes explicit. Tip #1

> If your schema changes are driven by changes in your entities, you can **still** use automatic DDL generation.

Simply apply Hibernate DDL generation after changes and use your database's admin tools (in case of MySQL then MySQL Workbench) to `diff` the schema before and after. This beats having to track complex changes manually. Save the difference to a migration script for Flyway to use. Which brings me to Tip #2

> If you can, avoid using an in-memory database as much as possible.

With tools like Docker and Vagrant, setting up multiple local databases for development is a snap. By using the same version of the same RDBMS during development, you have fewer environmental differences to potentially cause problems. More to the point:

1. You're less likely to forget to create a migration script
2. Yes! you **can** use Hibernate/JPA annotations that contain vendor-specific column and table definitions

Expanding on point 1. Tip #3

> Migrate as part of your build/CI

Each time you run your tests, run the migrations to test the scripts. Preferably using your deployment automation scripts. An example benefit: Data inserted by the scripts, meant for use in production will show up in screenshots taken by Selenium. All in the name of improving the confidence in your code and deployment process. To make the tests as realistic as possible and to speed up the CI migrations: Tip #4

> Automate the imaging of your production DB

This process can be a simple `mysqldump`, but you'll probably want to limit the size by cherry-picking tables or doing other custom extraction. Not to mention user data [anonymization](https://en.wikipedia.org/wiki/Data_anonymization). By regularly exporting production data, you will avoid the dev and test environments deviating too much from the "real world". And if you're going to do this regularly, you want to automate it. Or to put it more accurately: If you don't automate it, you're not going to do it regularly.
