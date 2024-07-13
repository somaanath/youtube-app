import logging
from flask import Flask, render_template, request, send_file
from gunicorn.app.base import BaseApplication
from pytube import YouTube
import os
import tempfile

app = Flask(__name__, static_folder='static')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution='1080p').first()
            if not stream:
                stream = yt.streams.get_highest_resolution()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))
                temp_file_path = temp_file.name

            return send_file(temp_file_path, as_attachment=True, download_name=f"{yt.title}.mp4")
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            return render_template("home.html", error="An error occurred while processing the video. Please try again.")
    
    return render_template("home.html")

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        # Apply configuration to Gunicorn
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        "bind": "0.0.0.0:8080",
        "workers": 4,
        "loglevel": "info",
        "accesslog": "-"
    }
    StandaloneApplication(app, options).run()