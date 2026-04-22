from flask import Flask, request, jsonify
import os, requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    topic = request.json.get("prompt")

    os.makedirs("images", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # SIMPLE SCRIPT
    script = " ".join([topic]*100)

    # IMAGES DOWNLOAD
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
            if count > 20:
                break
        except:
            pass

    # VIDEO (ONLY if ffmpeg works)
    os.system("ffmpeg -r 0.03 -i images/img%d.jpg -c:v libx264 output/video.mp4")

    return jsonify({
        "message": "Process done",
        "video": "output/video.mp4"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
