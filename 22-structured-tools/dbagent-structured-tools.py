from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import sqlite3

# ============================================================
# DB SETUP
# ============================================================

def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        authenticated INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    users = [
        ("ML001", "Raj", 1),
        ("ML002", "Ram", 0),
        ("ML003", "Sham", 1)
    ]

    cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

    conn.commit()
    conn.close()


# ============================================================
# TOOLS (STRUCTURED)
# ============================================================

@tool("add_user", description="Use this tool to add a user to the database. Provide name and id as input.")
def add_user(name: str, user_id: str) -> str:
    """Add a user to the database"""
    # print(f"Adding user with name={name} and id={user_id}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (id, name, authenticated) VALUES (?, ?, ?)",
            (user_id, name, 1)
        )
        conn.commit()
        conn.close()
        return f"User {name} added with ID {user_id}"
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}"
        
@tool
def list_users() -> str:
    """List all users"""
    # print("[Tool] Listing all users...")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, authenticated FROM users")
    rows = cursor.fetchall()
    conn.close()

    response = "\n".join([str(r) for r in rows]) or "No users found"
    # print("[Tool] List of users:\n", response)
    return response


# ============================================================
# MAIN
# ============================================================

f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt")
groq_api_key = f.read()
f.close()

if __name__ == "__main__":

    setup_db()
    seed_data()

    # Groq via OpenAI-compatible API
    llm = ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

    tools = [add_user, list_users]

    # ---------------- Demo: change prompt to show how system prompt can be used to steer agent behavior ----------------

    prompt = """

"""

    prompt2 = """

"""

    agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=prompt2,
            # debug=True,
        )

    # Invoke
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "Add a user named Sunil with id ML508"}
        ]
    })

    print(response["messages"][-1].content)

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "Give me a list of all users"}
        ]
    })

    print(response["messages"][-1].content)


    