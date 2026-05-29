"""
Core Text-to-SQL sequential chain.
Takes a natural language question -> generates SQL -> executes it -> returns a plain-English answer.
"""
import os
from operator import itemgetter

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool  # Updated from deprecated import path (latest as of 2025)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq  # Updated from deprecated langchain_openai.ChatOpenAI -> ChatGroq (latest as of 2025)
from langchain.chains import create_sql_query_chain  # Updated from deprecated langchain_classic.chains -> langchain.chains (latest as of 2025)

load_dotenv()

_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comic_store.db")

if not os.path.exists(_DB_PATH):
    raise FileNotFoundError(
        "comic_store.db not found. Run 'python setup_db.py' first."
    )

# Database connection
db = SQLDatabase.from_uri(f"sqlite:///{_DB_PATH}")

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

# SQL generation prompt — must contain {input}, {table_info}, {top_k}
SQL_PROMPT_TEMPLATE = """You are a SQLite expert. Given an input question, create a
syntactically correct SQLite query to run.

Unless the user specifies a number of results, query for at most {top_k} results
using the LIMIT clause. Order results to return the most informative data.

Never query for all columns (SELECT *) unless explicitly needed.
Only query columns that are needed. Wrap column names in double quotes.
Pay attention to column names in the schema below - do NOT invent column names.
Pay attention to which column belongs to which table.
Use JOINs when you need human-readable names from related tables.

IMPORTANT: Return ONLY the raw SQL query as plain text.
Do NOT wrap it in ```sql ... ``` code blocks.
Do NOT explain the query. Do NOT add any extra text.

The output format must be exactly:
SQLQuery: <your sql query here>

Schema and sample rows for relevant tables:
{table_info}

Question: {input}"""

sql_prompt = PromptTemplate.from_template(SQL_PROMPT_TEMPLATE)

# Answer generation prompt
answer_prompt = PromptTemplate.from_template(
    """Given the user question, the SQL query that was run, and the SQL result,
generate a helpful, clear, and concise answer in plain English.

If results contain dollar amounts, format them nicely (e.g., $1,234.56).
If the result is a list, present it as a numbered list.

Question: {question}
SQL Query: {query}
SQL Result: {result}

Answer: """
)


def _clean_sql(text: str) -> str:
    """Strip LLM formatting artifacts so only a plain SQL string remains."""
    if "SQLQuery:" in text:
        text = text.split("SQLQuery:")[-1]
    if "```sql" in text:
        text = text.split("```sql")[-1].split("```")[0]
    return text.strip()


_query_write_chain = create_sql_query_chain(
    llm=llm,
    db=db,
    prompt=sql_prompt,
    k=10,
)

_execute_query = QuerySQLDataBaseTool(db=db)

# Full pipeline: question -> SQL -> execute -> plain English answer
full_chain = (
    RunnablePassthrough.assign(
        query=_query_write_chain | StrOutputParser() | _clean_sql
    )
    .assign(result=itemgetter("query") | _execute_query)
    | answer_prompt
    | llm
    | StrOutputParser()
)


def ask(question: str) -> str:
    """
    Ask a natural language question about the comic store database.
    Returns a plain English answer.
    """
    return full_chain.invoke({"question": question})
