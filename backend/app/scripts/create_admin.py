import argparse
from ..db import get_db_cursor
from ..auth import hash_password


def create_admin(name: str, phone: str, email: str, password: str) -> int:
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,),
        )
        if cur.fetchone():
            raise SystemExit("Admin already exists with this email")
        cur.execute(
            """
            INSERT INTO users (name, phone, email, password, role, status)
            VALUES (%s, %s, %s, %s, 'admin', 'active')
            RETURNING id
            """,
            (name, phone, email, hash_password(password)),
        )
        admin_id = cur.fetchone()[0]
        print(f"Created admin with id: {admin_id}")
        return admin_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--phone", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    create_admin(args.name, args.phone, args.email, args.password)


if __name__ == "__main__":
    main()