from flask import Flask, request, render_template, send_from_directory
from flask_caching import Cache
import time
import redis
import re
from redis.exceptions import ConnectionError

app = Flask(__name__)

cache_config = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": "6379",
    "CACHE_REDIS_DB": "0",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
}
app.config.from_mapping(cache_config)
cache = Cache(app)


def connect():
    r = redis.Redis(host="localhost", port=6379, db=0)
    while True:
        try:
            if r.ping():
                print("Connected to Redis server")
                return r
        except ConnectionError:
            print("Can't connect to Redis server. Retrying in 5 seconds...")
            time.sleep(5)


def process_stream(r, stream_name):
    last_id = "0-0"  # Start reading from the beginning of the stream
    while True:
        try:
            messages = r.xread({stream_name: last_id}, block=0)
            for message in messages:
                stream, data = message
                for message_id, value in data:
                    print(f"Received: {value} from {stream}")
                    last_id = message_id  # Update last_id to continue where we left off
        except redis.exceptions.ConnectionError:
            print("Connection lost. Reconnecting...")
            time.sleep(5)  # Wait for 5 seconds before attempting to reconnect
            r = connect()  # Attempt to reconnect


def get_message_count(r, stream_name):
    return r.xlen(stream_name)


def get_last_messages(r, stream_name, count):
    return r.xrevrange(stream_name, count=count)


def get_oldest_message(r, stream_name):
    messages = r.xrange(stream_name, count=1)
    if messages:
        return messages[0]
    else:
        return None


def get_time_difference(r, stream_name):
    # Get the oldest and newest messages
    oldest_message = get_oldest_message(r, stream_name)
    newest_message = get_last_messages(r, stream_name, 1)

    if oldest_message and newest_message:
        # Extract the timestamps from the message IDs
        oldest_timestamp = int(oldest_message[0][0].decode().split("-")[0])
        newest_timestamp = int(newest_message[0][0].decode().split("-")[0])

        # Calculate the time difference in milliseconds
        time_difference = newest_timestamp - oldest_timestamp

        # Convert the time difference to seconds
        time_difference_seconds = time_difference / 1000

        return time_difference_seconds
    else:
        return None


def get_messages_in_time_range(r, stream_name, start_time, end_time):
    # Convert the start and end times to milliseconds
    start_time_ms = int(start_time * 1000)
    end_time_ms = int(end_time * 1000)

    # Create the start and end IDs
    start_id = f"{start_time_ms}-0"
    end_id = f"{end_time_ms}-0"

    # Get the messages in the time range
    messages = r.xrange(stream_name, min=start_id, max=end_id)

    return messages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/raw_data/<int:page>")
def funct(page=1):
    r = connect()
    start_time = time.time() - 24 * 60 * 60  # 24 hours ago
    end_time = time.time()  # Now
    messages = get_messages_in_time_range(r, "sensor_data", start_time, end_time)
    query = request.args.get("q", "")  # Get the query parameter
    messages = [msg for msg in messages if query in str(msg)]  # Filter the messages
    per_page = 100  # Number of messages per page
    start = (page - 1) * per_page
    end = start + per_page
    messages = messages[start:end]  # Get only the messages for this page
    return str(messages)


@app.route("/data/<int:page>")
def all_data(page=1):
    r = connect()
    per_page = 100  # Number of messages per page
    start = (page - 1) * per_page
    end = start + per_page - 1

    # Get the query from the URL parameters
    query = request.args.get("q")
    if query is None:
        query = request.args.get("query", "")

    # Get the messages from the stream
    messages = list(r.xrange("sensor_data"))

    # Filter the messages based on the query
    filtered_messages = [msg for msg in messages if query in str(msg)]

    # Calculate the total number of pages
    total_pages = (len(filtered_messages) + per_page - 1) // per_page

    # Paginate the filtered messages
    start = (page - 1) * per_page
    end = start + per_page
    paginated_messages = filtered_messages[start:end]

    return render_template(
        "data.html",
        messages=paginated_messages,
        page=page,
        query=query,
        total_pages=total_pages,
        is_filtered=bool(query),
    )


"""
@app.before_request
def before_request():
    if request.path.startswith("/data/"):
        try:
            with open("./templates/data.html", "r") as f:
                content = f.read()

            # Check if the HTML file contains a link to a CSS file
            css_file = re.search(r'href="([^"]*.css)"', content)
            if css_file:
                css_file = css_file.group(1)

                # Cache the CSS file
                @cache.cached(timeout=50)
                def cached_css():
                    return send_from_directory("static", css_file)

                cached_css()
        except FileNotFoundError:
            print("Cannot cache: File not found")
"""

"""
@app.teardown_appcontext
def close_redis():
    r = connect()

    if redis is not None:
        r.close()
"""

if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
