from flask import Flask, request, render_template, make_response
from flask_bootstrap import Bootstrap

import os
import uuid
import base64

from PIL import Image
import warnings
warnings.simplefilter('error', Image.DecompressionBombWarning)

# app = Flask(__name__)
app = Flask(__name__, static_folder='imgs')

bootstrap = Bootstrap(app)


@app.route('/')
def do_get():
    return render_template('index.html')

# 追加
@app.route('/saveimage', methods=['POST'])
def saveimage():
    event = request.form.to_dict()

    dir_name = 'imgs'
    img_name = uuid.uuid4().hex

    # Saving image in the 'imgs' folder temporarily. Should be deleted after a certain period of time
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(os.path.join(dir_name, '{}.png'.format(img_name)), 'wb') as img:
        img.write(base64.b64decode(event['image'].split(",")[1]))

    original = Image.open(os.path.join(dir_name, '{}.png'.format(img_name)))
    # Needs simple validation of format for security since Pillow supports various type of Images
    if(original.format != 'PNG'):
        return make_response('Unsupported image type.', 400)

    original.thumbnail((240, 240), Image.ANTIALIAS)
    original.save(os.path.join(dir_name, '{}_240.png'.format(img_name)), 'PNG')
    print(make_response)
    return make_response(img_name, 200)


if __name__ == '__main__':
    server_port = int(os.environ.get('PORT', 4998))
    app.run(debug=True, port=server_port)
    # app.run(host='0.0.0.0', port=server_port)