from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# SQLiteはデフォルトで「接続を作ったスレッドからしか使えない」という制約がある。
# FastAPIはリクエストごとに別スレッドで処理することがあるため、
# SQLiteの場合だけこの制約を緩める設定を追加する（他のDBでは不要なので空の辞書）。
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# --- Engine ---
# EngineはDB全体への「接続口」そのもの。
# settings.database_url（例: "sqlite:///./book_shelf.db"）を見て、
# どのDB(SQLite/PostgreSQLなど)にどう繋ぐかを管理するオブジェクト。
# アプリ起動時に1つだけ作成し、アプリ全体で共有する（リクエストごとに作り直さない）。
engine = create_engine(settings.database_url, connect_args=connect_args)

# --- SessionLocal ---
# SessionはDBとの「1回のやりとり単位」（会話のようなもの）。
# SessionLocalはSessionを作るための「工場（ファクトリ）」で、
# 呼び出すたびに新しいSessionインスタンスを生成する。
# - autocommit=False: クエリを実行しても自動でコミットしない（明示的にcommit()するまで確定しない）
# - autoflush=False:  クエリ実行前に自動でDBへ変更を送信(flush)しない（明示的に呼ぶまで保留される）
# - bind=engine:      どのEngine（DB接続口）を使ってSessionを作るかを指定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- get_db ---
# FastAPIの依存性注入(Depends)で使うための関数。
# リクエストが来るたびにこの関数が呼ばれ、
#   1. SessionLocal()で新しいSession（DBとのやりとり用オブジェクト）を作る
#   2. yieldでそのSessionをAPIの処理側に渡す（この間にDB操作が行われる）
#   3. 処理が終わったら（エラーが起きても）finallyでdb.close()し、接続を返却する
# というライフサイクルを管理する。
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
