from tables.schemas import TwitterUserTable


def clean(data: dict, cls=TwitterUserTable) -> dict:
    """Parse user fields from a CSV (as dict) row and recast/clean the data.

    Param:
    data (dict): CSV row as a dictionary

    Return:
    selected_user_data (dict): Key-value pairs of column names and values
    """
    # Select the user data fields from the CSV dict row
    selected_user_data = {}
    for k, v in data.items():
        if k in [f"user_{col.name}" for col in cls.columns]:
            k = k[5:]
            selected_user_data.update({k: v})
        elif k == "user_name":
            k = "display_name"
            selected_user_data.update({k: v})
        elif k == "collection_time":
            selected_user_data.update({k: v})
    # Clean the selected data fields
    for column in cls.columns:
        if selected_user_data[column.name] == "":
            selected_user_data.update({column.name: None})
        # Cast booleans as booleans
        if column.type == "BOOLEAN":
            b = selected_user_data[column.name]
            if b == "0":
                selected_user_data.update({column.name: False})
            elif b == "1":
                selected_user_data.update({column.name: True})
    return selected_user_data
