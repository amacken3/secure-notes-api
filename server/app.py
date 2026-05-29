from config import app


@app.route("/")
def index():
    return {"message": "Secure Notes API"}, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)