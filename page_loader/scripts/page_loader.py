import logging
import sys
from page_loader.cli import get_cmd_args
from page_loader import download


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        args = get_cmd_args()

        html_path = download(args.url, args.output)

        print(f"page: {args.url}, finished download and saved in {html_path}")

    except Exception as ex:
        logging.error(ex)
        sys.exit(1)


if __name__ == '__main__':
    main()
