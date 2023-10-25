from app import create_app

app = create_app()
app.run(port=5000, host = '0.0.0.0', debug=True)