import os
from app import create_app

host = os.environ['APP_HOST']
port = os.environ['APP_PORT']

app = create_app()

# 54.191.253.12
# 44.226.122.3

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
