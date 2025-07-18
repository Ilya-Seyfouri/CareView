import os
import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_psycopg2_connection():
    """Test direct psycopg2 connection"""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "careview"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "MySecurePass123")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Direct psycopg2 connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Direct psycopg2 connection failed: {e}")
        return False


def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "careview")
        DB_USER = os.getenv("DB_USER", "admin")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "MySecurePass123")

        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Connection string: {DATABASE_URL}")

        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ SQLAlchemy connection successful!")
            return True
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False


def check_env_variables():
    """Check if environment variables are loaded correctly"""
    print("Environment variables:")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', ''))}")
    print()


if __name__ == "__main__":
    print("=== Database Connection Test ===")
    print()

    check_env_variables()

    print("1. Testing direct psycopg2 connection...")
    psycopg2_success = test_psycopg2_connection()
    print()

    print("2. Testing SQLAlchemy connection...")
    sqlalchemy_success = test_sqlalchemy_connection()
    print()

    if psycopg2_success and sqlalchemy_success:
        print("🎉 All tests passed! Ready to create models.")
    else:
        print("❌ Some tests failed. Please check database setup.")