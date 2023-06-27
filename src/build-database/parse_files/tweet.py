from tables.schemas import TweetTable
from datetime import datetime
import ast


def clean(data: dict, cls=TweetTable) -> dict:
    """Parse user fields from a CSV (as dict) row and recast/clean the data.

    Param:
    data (dict): CSV row as a dictionary

    Return:
    selected_user_data (dict): Key-value pairs of column names and values
    """
    # Select the user data fields from the CSV dict row
    selected_tweet_data = {
        k: v for k, v in data.items() if k in [col.name for col in cls.columns]
    }
    additional_fields = [cls.is_quote_tweet, cls.is_retweet]
    for field in additional_fields:
        selected_tweet_data.update({field.name: None})
    # Clean the select data fields
    for column in cls.columns:
        # Clean up empty strings with null value
        if selected_tweet_data[column.name] == "":
            selected_tweet_data.update({column.name: None})
        # Clean boolean fields
        if column.type == "BOOLEAN":
            if selected_tweet_data[column.name] == "1":
                selected_tweet_data.update({column.name: True})
            else:
                selected_tweet_data.update({column.name: False})
        # Parse timestamp integer
        elif column.name.endswith("timestamp_utc") and column.type == "TIMESTAMP":
            s = None
            try:
                s = str(datetime.fromtimestamp(int(selected_tweet_data[column.name])))
            except TypeError:
                pass
            selected_tweet_data.update({column.name: s})
        # Parse array data
        elif column.type == "TEXT[]":
            parsed_column = selected_tweet_data[column.name]
            array = ""
            # If the data is written as a list (i.e. coordinates), read it literally
            if (
                parsed_column
                and parsed_column.startswith("[")
                and parsed_column.endswith("]")
            ):
                try:
                    array = ast.literal_eval(parsed_column)
                except Exception:
                    pass
            # Otherwise, try to unnest the data on the | delimiter
            elif parsed_column:
                array = parsed_column.split("|")
            else:
                array = None
            selected_tweet_data.update({column.name: array})
        # Create additional "is retweet" column
        if column.name == "is_retweet":
            if selected_tweet_data["retweeted_id"]:
                selected_tweet_data.update({column.name: True})
            else:
                selected_tweet_data.update({column.name: False})
        # Create additional "is quote tweet" column
        elif column.name == "is_quote_tweet":
            if selected_tweet_data["quoted_id"]:
                selected_tweet_data.update({column.name: True})
            else:
                selected_tweet_data.update({column.name: False})
    return selected_tweet_data
