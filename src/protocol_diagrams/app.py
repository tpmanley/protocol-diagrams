from flask import Flask, render_template, request, redirect, url_for

import parsers, pd

app = Flask(__name__)

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
@app.route('/protocol', methods=['POST'])
def protocol():
    api_version = request.form["api_version"]
    message = request.form["message"]
    messages = parsers.parse_string(message)
    pd.process(messages[0], "tom.png")
    return "Found %d messages" % len(messages)

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

    
def main():
    app.run(debug=True)
    
if __name__ == '__main__':
    main()