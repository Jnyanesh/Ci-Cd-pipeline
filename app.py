from flask import Flask

# Initialize the app
app = Flask(__name__)

# Define what happens when a user visits the home page
@app.route('/')
def home():
    return "<h1>Hello, Flask!</h1><p>Your simple app is running successfully.</p>"

if __name__ == '__main__':
    # Run the app in debug mode (auto-reloads on changes)
    app.run(debug=True)
