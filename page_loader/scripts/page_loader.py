from page_loader.cli import get_cmd_args
from page_loader.html import download


def main():
    args = get_cmd_args()

    download(args.url, args.output)


if __name__ == '__main__':
    main()
