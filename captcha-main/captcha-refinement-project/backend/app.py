

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

captcha_store = {}

def generate_captcha_text(length=6):
    """Generates a random alphanumeric CAPTCHA string"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/')
def index():
    """Serve the frontend HTML file"""
    return send_from_directory("../frontend", "index.html")

@app.route('/get_captcha', methods=['GET'])
def get_captcha():
    """Generates a new CAPTCHA image"""
    captcha_text = generate_captcha_text()
    captcha_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  
    captcha_store[captcha_id] = captcha_text

    return jsonify({"image_url": f"/captcha/{captcha_id}", "captcha_id": captcha_id})

@app.route('/captcha/<captcha_id>', methods=['GET'])
def serve_captcha_image(captcha_id):
    """Serves the CAPTCHA image"""
    if captcha_id in captcha_store:
        image_buffer = generate_captcha_image(captcha_store[captcha_id])
        return send_file(image_buffer, mimetype='image/png')
    return "Invalid CAPTCHA ID", 404

@app.route('/validate_captcha', methods=['POST'])
def validate_captcha():
    """Validates user input against stored CAPTCHA"""
    data = request.get_json()
    user_input = data.get("captcha_text", "").strip()
    captcha_id = data.get("captcha_id")

    if not captcha_id or captcha_id not in captcha_store:
        return jsonify({"success": False, "message": "Invalid CAPTCHA ID"}), 400

    if user_input == captcha_store[captcha_id]:
        del captcha_store[captcha_id]
        return jsonify({"success": True, "message": "CAPTCHA validated successfully"})
    
    return jsonify({"success": False, "message": "Incorrect CAPTCHA"}), 400

if __name__ == "__main__":
    app.run(debug=True)
