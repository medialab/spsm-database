This source code was designed to replace the code in `src/build-database`. In contrast to the former, whose tables are hard coded as classes, the goal of this code was to build PostgreSQL tables using schemas defined in a human-readable YAML file. The code was used belatedly in the database's modeling and only to create the `twitter_user` table.

However, this code was never fully developed and was never used to fully replace the earlier code base `src/build-database`.
