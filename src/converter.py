#!/usr/bin/python3
from subprocess import call
from os import remove
import csv
import tempfile
import os
import sys

def convert(input_format: str, output_format: str, input_file, output_file):
    print(f"Converting {input_file.name} from {input_format} to {output_format}, named {output_file.name}...", file=sys.stderr)

    process_arguments = ["inkscape", f"{input_file.name}", f"--export-pdf={output_file.name}"]
    print(f"Calling inkscape: {process_arguments}", file=sys.stderr)
    call(process_arguments)
    print(f"Called inkscape", file=sys.stderr)

    output_size = os.path.getsize(output_file.name)
    print(f'Inkscape destination file {output_file.name}: {output_size} bytes', file=sys.stderr)