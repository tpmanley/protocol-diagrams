from flask import Flask, request
import parsers

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
	
@app.route('/protocol', methods=['POST'])
def protocol():
	api_version = request.form["api_version"]
	message = request.form["message"]
	messages = parsers.parse_string(message)
	return "Found %d messages" % len(messages)

def main():
	app.run()
	
if __name__ == '__main__':
    main()