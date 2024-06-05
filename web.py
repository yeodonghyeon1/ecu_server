from flask import Flask, send_from_directory, jsonify

import os



app = Flask(__name__)



VIDEO_DIRECTORIES = {

    "org_video": "../camera/org_video",

    "composit": "../camera/cv_video"

}



@app.route('/')

def index():

    return app.send_static_file('index.html')



@app.route('/videos/<category>/<path:filename>')

def download_file(category, filename):

    directory = VIDEO_DIRECTORIES.get(category)

    if directory:

        return send_from_directory(directory, filename)

    return 'File not found', 404



@app.route('/video-list')

def video_list():

    directory = VIDEO_DIRECTORIES.get("org_video")

    if directory:

        videos = os.listdir(directory)

        return jsonify(videos)

    return jsonify([])



if __name__ == '__main__':

    app.run(debug=True, host='192.168.0.108', port=6060)