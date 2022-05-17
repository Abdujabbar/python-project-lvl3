import logging
from page_loader.cli import get_cmd_args
from page_loader.html import download


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        args = get_cmd_args()

        download(args.url, args.output)
    except Exception as ex:
        logging.error(f"Trouble: {ex}")
        raise ex


if __name__ == '__main__':
    main()
