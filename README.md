# Text-to-SQL Chain — LangChain + Groq

A sequential LangChain pipeline that translates natural language questions into SQL queries, runs them against a local SQLite database, and returns plain English answers.

Built while learning LangChain's LCEL (LangChain Expression Language) as part of my transition from .NET development into GenAI engineering.

---

## What It Does

```
User Question
     ↓
[SQL Generation] — Groq LLM reads the DB schema and writes a SQL query
     ↓
[SQL Execution]  — LangChain runs the query against comic_store.db
     ↓
[Answer Generation] — Groq LLM converts raw results into plain English
```

**Example:**

```
❓ Who are the top 5 customers with the most money spent?

💬 The top 5 customers by total spending are:
   1. Tony Stark — $112.92
   2. Peter Parker — $60.95
   3. Kavya Desai — $51.89
   ...
```

---

## Database

The project includes an 8-table SQLite schema for a fictional comic book store:

| Table | Description |
|---|---|
| `comic` | Comics for sale with title, genre, price |
| `publisher` | Marvel, DC, Dark Horse, IDW |
| `customer` | 20 customers |
| `employee` | 4 staff across 2 branches |
| `branch` | Manhattan and Brooklyn locations |
| `inventory` | Stock counts per branch |
| `sale` | Each customer visit / transaction |
| `sale_transaction` | Line items (which comics were in each sale) |

---

## Setup

**1. Clone and create a virtual environment**

```bash
git clone https://github.com/imbhaskarm/text-to-sql-chain.git
cd text-to-sql-chain
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Set up your API key**

```bash
cp .env.example .env
# Edit .env and paste your Groq API key
```

Get a free Groq API key at: https://console.groq.com

**3. Create the database**

```bash
python setup_db.py
```

This creates `comic_store.db` in the project folder with all tables and sample data.

**4. Run the chain**

```bash
python main.py
```

---

## Project Structure

```
text-to-sql-chain/
├── setup_db.py       # Creates and seeds comic_store.db (run once)
├── chain.py          # Full LangChain LCEL pipeline definition
├── main.py           # Entry point — runs 5 sample questions
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Key Concepts

| Concept | Where Used |
|---|---|
| `SQLDatabase.from_uri()` | Wraps SQLite for LangChain tools |
| `create_sql_query_chain()` | LLM + schema → SQL string |
| `QuerySQLDataBaseTool` | Executes SQL, returns results |
| `RunnablePassthrough.assign()` | LCEL step chaining |
| `PromptTemplate` | Structured prompts for SQL + answers |
| `StrOutputParser` | Extracts clean text from LLM response |

---

## Notes

- Uses `langchain==0.2.16` with `langchain-community==0.2.16`
- LLM: `llama-3.3-70b-versatile` via Groq (free tier)
- The DB file (`comic_store.db`) is excluded from version control — always run `setup_db.py` first
- Fixed bug from original notebook: `langchain_classic` does not exist — corrected to `langchain.chains`
