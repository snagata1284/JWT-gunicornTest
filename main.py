from fastapi import FastAPI
# このほか、python-multipart、bcryptをインポート
# 自作モジュールのインポート
from routers import index
from routers import auth

app = FastAPI()
# メイン
app.include_router(index.router)
# APIKey認証
app.include_router(auth.router)

# 本番環境でgunicornを使う場合は不要
if __name__ == '__main__':
    app.run()