def run_server():
    import os

    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("APP_ENV", "development") == "development"

    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_server()