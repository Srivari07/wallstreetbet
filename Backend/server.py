from webAPI import app, dataExists


def main():
    dataExists()
    app.run(debug=True)


if __name__ == '__main__':
    main()
