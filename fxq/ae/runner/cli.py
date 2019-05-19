import logging

from fxq.ae.runner.ae_runner_application import app

format = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
logging.basicConfig(format=format, level=logging.INFO)


def main():
    app.run()


if __name__ == '__main__':
    main()
