#!/bin/usr/python3
from flask import Flask
from flask import send_file
from flask import request
from flask import send_from_directory
import sys
import tempfile
import uuid
import os
from . import converter
import shutil
import base64

app = Flask(__name__)

counter = 0
print('Starting up Inkscape Converter microservice...', file=sys.stderr)

@app.route("/health")
def health():
    print('Received GET request on /health', file=sys.stderr)
    return { "status": "up", "counter": counter }

@app.route('/images/', methods=['POST'])
def convert_image():
    print('Received POST request on /images/', file=sys.stderr)

    global counter
    counter = counter + 1

    if (request.content_type.startswith('application/json')):
        print("Received a JSON request", file=sys.stderr)

        json = request.get_json()
        input_base64_string = str(json['base64']) if 'base64' in json else ''
        input_format = str(json['inputformat']) if 'inputformat' in json else ''
        output_format = str(json['outputformat']) if 'outputformat' in json else ''

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.svg') as input_file:
            print('Converting Base64 input...', file=sys.stderr)
            input_base64_bytes = input_base64_string.encode('ascii')
            input_bytes = base64.b64decode(input_base64_bytes)

            print(f'Writing input to {input_file.name}...', file=sys.stderr)
            input_file.write(input_bytes)
            input_file.flush()
            input_size = os.path.getsize(input_file.name)
            print(f'Wrote input to {input_file.name}: {input_size} bytes', file=sys.stderr)

            with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf') as output_file:
                converter.convert(input_format, output_format, input_file, output_file)

                print("Sending PDF file...", file=sys.stderr)
                return send_file(output_file.name, attachment_filename=f"image.pdf", mimetype='application/pdf')

    else:
        print(f"Received not a JSON request ({request.content_type}); aborting...", file=sys.stderr)
        return 'Content-Type for POST request must be application/json', 400

