from src import create_app
from src.utils.global_response import success_response ,not_found_response

app = create_app()

@app.route('/', methods=["GET"])
def is_health():
    return success_response({}, "Health check")

@app.route('/', defaults={'path': ''}, methods=["GET"])
@app.route('/<path:path>', methods=["GET"])
def is_not_found_api(path):
    return not_found_response(path)

if __name__ == "__main__":
    app.run(debug=True , port=8080)
