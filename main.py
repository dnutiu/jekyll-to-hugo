import logging
import sys

from app.converter import Converter


def main():
    # Logging configuration
    logging.basicConfig(
        format="%(asctime)s %(process)d %(levelname)s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    if len(sys.argv) != 3:
        logger.error(
            "Usage: python main.py <source path to jekyll posts> <output path to hugo posts>"
        )
        sys.exit(1)

    # Converter
    converter = Converter(sys.argv[1], sys.argv[2])
    converter.convert()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
