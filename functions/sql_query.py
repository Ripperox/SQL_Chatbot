from sqlalchemy import create_engine, inspect
import pandas as pd
import ast
import re
from logger import logger
from database import database_uri

engine = create_engine(database_uri)

def create_dataframe(data,query):
    if not data:
        return pd.DataFrame()  

    data_str = str(data)
   
    try:
        data_list = ast.literal_eval(data_str)
    except (SyntaxError, ValueError) as e:
        logger.error(f"Error parsing data: {e}")
        return pd.DataFrame()
    
    df = pd.DataFrame(data_list, columns=create_columns(query))
    return df

# def create_columns(query):
#     select_pattern = r"SELECT\s+(.*?)\s+FROM\s+`?(\w+)`?"
#     from_pattern = r"FROM\s+`?(\w+)`?"

#     select_match = re.search(select_pattern, query, re.IGNORECASE)
#     from_match = re.search(from_pattern, query, re.IGNORECASE)

#     if select_match and from_match:
#         columns_part = select_match.group(1).strip()
#         table_name = from_match.group(1)

#         if columns_part == "*":
#             table_columns = get_column_names(table_name)
#             return table_columns
#         else:
#             columns = columns_part.split(',')
#             extracted_columns = []
#             for col in columns: 
#                 col = col.strip().replace('`', '')
#                 if ' AS ' in col.upper():
#                     col = col.upper().split(' AS ')[-1].strip()
#                 col=col.lower()
#                 extracted_columns.append(col)
#             return extracted_columns
#     else:
#         return

def create_columns(query):
    select_pattern = r"SELECT\s+(.*?)\s+FROM\s+`?(\w+)`?"
    from_pattern = r"FROM\s+`?(\w+)`?"

    select_match = re.search(select_pattern, query, re.IGNORECASE)
    from_match = re.search(from_pattern, query, re.IGNORECASE)

    if select_match and from_match:
        columns_part = select_match.group(1).strip()
        table_name = from_match.group(1)

        if columns_part == "*":
            table_columns = get_column_names(table_name)
            return [remove_underscore(col) for col in table_columns]
        else:
            columns = columns_part.split(',')
            extracted_columns = []
            for col in columns: 
                col = col.strip().replace('`', '')
                if ' AS ' in col.upper():
                    col = col.upper().split(' AS ')[-1].strip()
                col = remove_underscore(col)
                extracted_columns.append(col)
            return extracted_columns
    else:
        return

def remove_underscore(column):
    print(column)
    column = column.lower()
    business_dict = {
    'num_traders': 'number of traders',
    'share_price': 'price of each share',
    'trader_id': 'trader identifier',
    'transaction_id':'transaction identifier',
    }
    column = business_dict.get(column, column)
    column=column.replace('_', ' ')
    return column.title()


def get_column_names(table_name,engine):
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        column_names = [col['name'].lower() for col in columns]
        return column_names