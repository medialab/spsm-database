import csv
import sys
from typing import Optional

import casanova
import click
from sqlalchemy import (DateTime, Float, ForeignKey, Integer, MetaData, String,
                        create_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, mapped_column,
                            relationship)


@click.group()
@click.pass_context
def cli(ctx) -> None:
    engine = create_engine("sqlite:///spsm.db", echo=True)
    with Session(engine) as session:
        ctx.obj["SESSION"] = session
        ctx.obj["ENGINE"] = engine


class Base(DeclarativeBase):
    pass


class Links(Base):
    __tablename__ = "links"

    id: Mapped[int] =  mapped_column(primary_key=True, autoincrement=True)
    hash: Mapped[str] = mapped_column(String(50))
    archive_url: Mapped[str]  = mapped_column(String(255))
    archive_time: Mapped[Optional[str]] = mapped_column(String(50))
    domain: Mapped[Optional[str]] = mapped_column(String(50))
    normalized_url: Mapped[Optional[str]] = mapped_column(String(255))
    fetch_date: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[int]] = mapped_column(Integer)
    webpage_title: Mapped[Optional[str]] = mapped_column(String(255))
    webpage_text: Mapped[Optional[str]] = mapped_column(String())
    webpage_lang: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Links(id={self.id!r}, archive_url={self.archive_url!r}, domain={self.domain!r}, archive_date={self.archive_time!r}, status={self.status!r})"


class Condor(Base):
    __tablename__ = "condor"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url_hash: Mapped[str] = mapped_column(ForeignKey("links.hash"))
    url_rid: Mapped[str] = mapped_column(String(50))
    clean_url: Mapped[str] = mapped_column(String(255))
    first_post_time: Mapped[Optional[str]] = mapped_column(String(50))
    share_title: Mapped[Optional[str]] = mapped_column(String(255))
    tpfc_rating: Mapped[Optional[str]] = mapped_column(String(255))
    tpfc_first_fact_check: Mapped[Optional[str]] = mapped_column(String(50))
    public_shares_top_country: Mapped[Optional[str]] = mapped_column(String(10))

    def __repr__(self) -> str:
        return f"Condor(id={self.id!r}, hash={self.url_hash!r}, url_rid={self.url_rid!r}, clean_url={self.clean_url!r}, first_post_time={self.first_post_time!r}, share_title={self.share_title!r}, tpfc_rating={self.tpfc_rating!r}, tpfc_first_fact_check={self.tpfc_first_fact_check!r}, public_shares_top_country={self.public_shares_top_country!r})"


class ScienceFeedback(Base):
    __tablename__ = "sciencefeedback"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    appearance_id: Mapped[str] = mapped_column(String(5))
    url_hash: Mapped[str] = mapped_column(ForeignKey("links.hash"))
    url_content_id: Mapped[str] = mapped_column(String(5))
    url: Mapped[str] = mapped_column(String(255))
    claimreviewed: Mapped[str] = mapped_column(String(255))
    publisheddate: Mapped[str] = mapped_column(String(50))
    publisher: Mapped[str] = mapped_column(String(100))
    reviews_author: Mapped[str] = mapped_column(String(100))
    reviews_reviewratings_ratingvalue: Mapped[float] = mapped_column(Float)
    reviews_reviewratings_standardform: Mapped[str] = mapped_column(String(50))
    urlreviews_reviewratings_alternatename: Mapped[str] = mapped_column(String(50))
    urlreviews_reviewratings_ratingvalue: Mapped[float] = mapped_column(Float)


@click.command()
@click.argument('file')
@click.pass_context
def create_condor(ctx, file):
    session = ctx.obj["SESSION"]
    engine = ctx.obj["ENGINE"]

    Base.metadata.create_all(bind=engine, checkfirst=True)

    with open(file) as f:
        reader = casanova.reader(f)
        url_rid_pos = reader.headers['url_rid']
        url_hash_pos = reader.headers['hash']
        clean_url_pos = reader.headers['clean_url']
        first_post_time_pos = reader.headers['first_post_time']
        share_title_pos = reader.headers['share_title']
        tpfc_rating_pos = reader.headers['tpfc_rating']
        tpfc_first_fact_check_pos = reader.headers['tpfc_first_fact_check']
        public_shares_top_country_pos = reader.headers['public_shares_top_country']

        condor_insert = list()
        for row in reader:
            condor_insert.append(Condor(
                url_rid=row[url_rid_pos],
                url_hash=row[url_hash_pos],
                clean_url=row[clean_url_pos],
                first_post_time=row[first_post_time_pos],
                share_title=row[share_title_pos],
                tpfc_rating=row[tpfc_rating_pos],
                tpfc_first_fact_check=row[tpfc_first_fact_check_pos],
                public_shares_top_country=row[public_shares_top_country_pos],
            ))

    session.add_all(condor_insert)
    session.commit()


@click.command()
@click.argument('file')
@click.pass_context
def create_links(ctx, file):
    session = ctx.obj["SESSION"]
    engine = ctx.obj["ENGINE"]

    Base.metadata.create_all(bind=engine, checkfirst=True)

    with open(file) as f:
        csv.field_size_limit(sys.maxsize)
        reader = casanova.reader(f)
        url_hash_pos = reader.headers['url_id']
        archive_url_pos = reader.headers['archive_url']
        archive_date_pos = reader.headers['archive_timestamp']
        domain_pos = reader.headers['domain']
        normalized_url_pos = reader.headers['resolved_url']
        fetch_date_pos = reader.headers['fetch_date']
        status_pos = reader.headers['status']
        webpage_title_pos = reader.headers['webpage_title']
        webpage_text_pos = reader.headers['webpage_text']
        webpage_lang_pos = reader.headers['webpage_lang']

        links_insert = list()
        for row in reader:
            links_insert.append(Links(
                    hash=row[url_hash_pos],
                    archive_url=row[archive_url_pos],
                    archive_time=row[archive_date_pos],
                    domain=row[domain_pos],
                    normalized_url=row[normalized_url_pos],
                    fetch_date=row[fetch_date_pos],
                    status=row[status_pos],
                    webpage_title=row[webpage_title_pos],
                    webpage_text=row[webpage_text_pos],
                    webpage_lang=row[webpage_lang_pos],
                ))

    session.add_all(links_insert)
    session.commit()


@click.command()
@click.argument('file')
@click.pass_context
def create_science_feedback(ctx, file):
    session = ctx.obj["SESSION"]
    engine = ctx.obj["ENGINE"]

    print("coming soon.")


if __name__ == '__main__':
    cli.add_command(create_links)
    cli.add_command(create_condor)
    cli.add_command(create_science_feedback)
    cli(obj={})
