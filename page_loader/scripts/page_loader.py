import logging
import sys
from page_loader.cli import get_cmd_args
from page_loader.html import download


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        args = get_cmd_args()

        download(args.url, args.output)

        logging.info(f"page: {args.url}, finished download")
    except Exception as ex:
        logging.error(f"Trouble: {ex}")
        sys.exit(1)


if __name__ == '__main__':
    main()
