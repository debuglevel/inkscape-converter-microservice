import logging
import os
from subprocess import call

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

conversions: int = 0


def convert(input_format: str, output_format: str, input_file, output_file):
    global conversions
    conversions = conversions + 1

    logger.debug(
        f"Converting {input_file.name} from {input_format} to {output_format}, named {output_file.name}..."
    )

    process_arguments = [
        "inkscape",
        f"{input_file.name}",
        f"--export-filename={output_file.name}",
    ]
    logger.debug(f"Calling inkscape: {process_arguments}")
    call(process_arguments)
    logger.debug(f"Called inkscape")

    output_size = os.path.getsize(output_file.name)
    logger.debug(f"Inkscape destination file {output_file.name}: {output_size} bytes")
