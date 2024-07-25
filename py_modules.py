from fastapi import FastAPI, Request, Form,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from database import db,db_config
from functions.sql_query import create_dataframe,get_column_names
from functions.visualization import visualizer, edit
from logger import logger
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
import ast
import logging