from app import create_app

app = create_app()

# 54.191.253.12
# 44.226.122.3

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
