from flask import Flask, request, jsonify
import os, requests
from bs4 import BeautifulSoup
import pyttsx3

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    topic = request.json.get("prompt")

    os.makedirs("images", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # SCRIPT (long video)
    script = " ".join([topic]*200)

    # VOICE
    engine = pyttsx3.init()
    engine.save_to_file(script, "audio/output.mp3")
    engine.runAndWait()

    # AUTO IMAGES
    url = f"https://www.bing.com/images/search?q={topic}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    count = 1
    for img in soup.find_all("img"):
        try:
            src = img.get("src")
            if src and "http" in src:
                data = requests.get(src).content
                with open(f"images/img{count}.jpg","wb") as f:
                    f.write(data)
                count += 1
            if count > 40:
                break
        except:
            pass

    # ANIMATION
    os.system(
        "ffmpeg -r 0.03 -i images/img%d.jpg "
        "-vf zoompan=z='zoom+0.0015':d=200 "
        "-c:v libx264 output/video.mp4"
    )

    # FINAL VIDEO
    os.system(
        "ffmpeg -i output/video.mp4 -i audio/output.mp3 "
        "-c:v copy -c:a aac output/final.mp4"
    )

    # SHORTS
    os.system(
        "ffmpeg -t 30 -i output/final.mp4 output/shorts.mp4"
    )

    return jsonify({
        "video": "output/final.mp4",
        "shorts": "output/shorts.mp4"
    })

app.run(port=5000)
