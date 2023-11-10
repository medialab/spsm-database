from typing import Dict

from psycopg2.extensions import connection as Connection

from csv_to_table_classes.base_table import TableBase


class TweetTable(TableBase):
    def __init__(self, connection: Connection, yaml_stem="tweet.yml") -> None:
        super().__init__(yaml_stem)
        self.connection = connection

    def create(self, reset: bool) -> None:
        self._create_table(connection=self.connection, reset=reset)

    def clean(self, row: Dict) -> Dict:
        clean_row = self._clean_csv_row(row)
        clean_row.update(
            {
                "is_retweet": bool(clean_row["retweeted_id"]),
                "is_quote_tweet": bool(clean_row["quoted_id"]),
            }
        )
        if not clean_row["retweeted_id"] and not clean_row["quoted_id"]:
            clean_row.update({"is_original_tweet": True})
        else:
            clean_row.update({"is_original_Tweet": False})
        return clean_row

    def insert_row(self, row: Dict) -> None:
        clean_row = self.clean(row)
        conflict_epilogue = (
            f"WHERE ({self.name}.collection_time) > EXCLUDED.collection_time"
        )
        conflict = self._compose_on_conflict() + conflict_epilogue
        self._insert(connection=self.connection, clean_row=clean_row, conflict=conflict)


class TwitterUserTable(TableBase):
    prefix = "user_"

    def __init__(self, connection: Connection, yaml_stem="twitter_user.yml") -> None:
        super().__init__(yaml_stem)
        self.connection = connection

    def create(self, reset: bool) -> None:
        self._create_table(connection=self.connection, reset=reset)

    def clean(self, row: Dict) -> Dict:
        clean_row = self._clean_csv_row(row, prefix=self.prefix)
        clean_row.update({"collection_time": row["collection_time"]})
        clean_row.update({"display_name": row["user_name"]})
        clean_row.update({"handle": row["user_screen_name"]})
        return clean_row

    def insert_row(self, row: Dict) -> None:
        clean_row = self.clean(row)
        conflict_epilogue = (
            f"WHERE ({self.name}.collection_time) < EXCLUDED.collection_time"
        )
        conflict = self._compose_on_conflict() + conflict_epilogue
        self._insert(connection=self.connection, clean_row=clean_row, conflict=conflict)


class TweetQueryTable(TableBase):
    def __init__(self, connection: Connection, yaml_stem="tweet_query.yml") -> None:
        super().__init__(yaml_stem)
        self.connection = connection

    def create(self, reset: bool) -> None:
        self._create_table(connection=self.connection, reset=reset)

    def clean(self, row: Dict) -> Dict:
        clean_row = {"tweet_id": row["id"], "query": row["query"]}
        return clean_row

    def insert_row(self, row: Dict) -> None:
        clean_row = self.clean(row)
        conflict = "ON CONFLICT (tweet_id,query) DO NOTHING"
        self._insert(connection=self.connection, clean_row=clean_row, conflict=conflict)
