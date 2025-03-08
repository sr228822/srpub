import argparse
import time
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from terminal_grid_screensaver import GridScreensaver

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

start_time = None
screensaver = None


@app.route("/content")
def get_content():
    # Extract width and height with defaults if not provided
    width = int(request.args.get("width", 800))
    height = int(request.args.get("height", 600))

    # Generate dynamic content
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = screensaver.run_once_html(width=width, height=height)
    content = f"""
    <div class="content">
        {html}
        <p>Current server time: {current_time}</p>
        <p>Server has been running for {time.time() - start_time:.2f} seconds.</p>
    </div>
    """
    return jsonify({"html": content})


def run_server(port=8000):
    global start_time
    start_time = time.time()

    print(f"Starting Flask server on port {port}...")
    app.run(host="0.0.0.0", port=port)
    print("Server stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a Flask server that serves dynamic HTML content"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)",
    )
    args = parser.parse_args()

    screensaver = GridScreensaver()

    run_server(args.port)
