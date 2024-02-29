This source code was designed to replace the code in `src/build-database`. In contrast to the former, whose tables are hard coded as classes, the goal of this code was to build PostgreSQL tables using table schema's declared in a human-readable YAML file. This code was used belatedly in the database's modeling to create the `twitter_user` table and clean/import the relevant data fields from CSV files.

However, this code was never fully developed and was never used to fully replace the earlier code base `src/build-database`.
