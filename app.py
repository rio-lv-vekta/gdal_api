from flask import Flask
from a_create_pyramid import create_pyramid
# from functions import generate_tiles , clear_output_folder

app = Flask(__name__)


@app.route("/")
def hello_world():
    # Example usage
    # generate_tiles('land_shallow_topo_2048.tif', 'test_tiles', default_ullr=['ulx', 'uly', 'lrx', 'lry'])
    # Usage
    # clear_output_folder("outputs")
    return "Hello, World numero 2!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
