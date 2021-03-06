from flask import Flask, request, jsonify, abort
import numpy as np
import cv2
from scipy.misc import toimage

from cena.recognition import FaceRecognizer
from cena.utils import decode_image, encode_image
from cena.settings import DEV, ANNOTATE_FRAME

RECOGNIZER = FaceRecognizer()
app = Flask(__name__)


@app.route('/recognize', methods=['POST'])
def recognize():
    if not request.json:
        abort(400)
    if 'frame' not in request.json:
        abort(400)
    if 'list_o_faces' not in request.json:
        abort(400)
    if 'shape' not in request.json:
        abort(400)

    # frame = cv2.imdecode(np.array(request.json['frame']), None)
    # frame = np.array(request.json['frame'])
    # frame = frame.astype('uint8')
    # frame = toimage(np.array(request.json['frame']))
    # frame = cv2.(np.array(request.json['frame']))
    # print(frame[0][0].dtype)
    encoded_frame = request.json['frame']
    shape = request.json['shape']
    return_frame = request.json.get('return_frame', False)
    frame = decode_image(encoded_frame, shape)
    list_o_faces = request.json['list_o_faces']

    frame, people_list, time = RECOGNIZER.recognize_faces(frame, list_o_faces)
    # if ANNOTATE_FRAME:
    #     frame, people_list, time = RECOGNIZER.recognize_faces(frame, list_o_faces)
    # else:
    #     people_list, time = RECOGNIZER.recognize_faces(frame, list_o_faces)

    response = {
        'people_list': people_list,
        'time': time
    }

    if return_frame:
        response.update({'frame': encode_image(frame)})
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
