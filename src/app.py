from .create_app import create_app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    app.run(host="0.0.0.0", port=port, debug=True)
