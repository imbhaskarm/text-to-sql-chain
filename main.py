"""
Entry point for the Text-to-SQL chain.

Usage:
    python main.py

Run 'python setup_db.py' first if comic_store.db does not exist.
"""
from chain import ask

SAMPLE_QUESTIONS = [
    "What is the total number of customers?",
    "What are the top 10 most popular comics sold?",
    "Who are the top 5 customers with the most comics purchased?",
    "Who are the top 5 customers with the most money spent?",
    "Who are the top 3 salesmen with the highest revenue?",
]


def main():
    print("=" * 60)
    print("  Comic Store - Text-to-SQL Chain")
    print("=" * 60)

    for question in SAMPLE_QUESTIONS:
        print(f"\n❓ {question}")
        answer = ask(question)
        print(f"💬 {answer}")
        print("-" * 60)


if __name__ == "__main__":
    main()
