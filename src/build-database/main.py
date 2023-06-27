# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for creating tables and inserting data from CSV files
#
import click
from connection.create_connection import connect
from connection.parse_args import parse_config
from insert_data.data_sources import insert_data_sources
from insert_data.twitter import insert_tweets


@click.group()
@click.argument("config")
@click.pass_context
def cli(ctx, config):
    connection_config, info = parse_config(file=config)
    connection = connect(config=connection_config)
    ctx.ensure_object(dict)
    ctx.obj["connection"] = connection
    ctx.obj["files"] = info["data sources"]


@cli.command()
@click.pass_context
def sources(ctx):
    connection = ctx.obj["connection"]
    insert_data_sources(
        connection=connection,
    )


@cli.command()
@click.argument("file")
@click.pass_context
def tweets(ctx, file):
    connection = ctx.obj["connection"]
    insert_tweets(connection=connection, file=file)


if __name__ == "__main__":
    cli(obj={})
