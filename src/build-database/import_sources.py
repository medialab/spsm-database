# =============================================================================
# SPSM Import SQL Table Data
# =============================================================================
#
# Workflow for importing raw data from CSV files into the database.
#
import click
import parse_files
from connection.create_connection import connect
from connection.parse_args import parse_config


@click.group()
@click.argument("config")
@click.pass_context
def cli(ctx, config):
    connection_config, info = parse_config(file=config)
    connection = connect(config=connection_config)
    ctx.ensure_object(dict)
    ctx.obj["connection"] = connection
    ctx.obj["files"] = info["data sources"]


@cli.command("condor")
@click.pass_context
def condor(ctx):
    connection = ctx.obj["connection"]
    file = ctx.obj["files"]["condor"]
    parse_files.condor.insert(connection=connection, file=file)


@cli.command("de-facto")
@click.pass_context
def defacto(ctx):
    connection = ctx.obj["connection"]
    file = ctx.obj["files"]["de facto"]
    parse_files.de_facto.insert(connection=connection, file=file)


@cli.command("science")
@click.pass_context
def science(ctx):
    connection = ctx.obj["connection"]
    file = ctx.obj["files"]["science feedback"]
    parse_files.science_feedback.insert(connection=connection, file=file)


@cli.command("completed-urls")
@click.pass_context
def completed_urls(ctx):
    connection = ctx.obj["connection"]
    file = ctx.obj["files"]["completed urls"]
    parse_files.completed_urls_dataset.insert(connection=connection, file=file)


@cli.command("enriched-titles")
@click.pass_context
def enriched_titles(ctx):
    connection = ctx.obj["connection"]
    file = ctx.obj["files"]["enriched titles"]
    parse_files.url_with_enriched_titles.insert(connection=connection, file=file)


@cli.command("queried-titles")
@click.pass_context
def queried_titles(ctx):
    connection = ctx.obj["connection"]
    file = ctx.obj["files"]["titles"]
    parse_files.titles.insert(connection=connection, file=file)


if __name__ == "__main__":
    cli(obj={})
