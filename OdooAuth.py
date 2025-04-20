from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/odoo/session', methods=['POST'])
def get_odoo_session():
    try:
        data = request.json
        odoo_url = data.get("url")  # e.g., https://yourcompany.odoo.sh
        db = data.get("db")
        login = data.get("login")
        password = data.get("password")

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": db,
                "login": login,
                "password": password
            },
            "id": 1
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Send POST request
        resp = requests.post(f"{odoo_url}/web/session/authenticate", json=payload, headers=headers)

        # Debug prints
        print("Status Code:", resp.status_code)
        print("Response Headers:", resp.headers)
        print("Response Cookies:", resp.cookies)
        print("Response Body:", resp.text)

        # Check for session_id in cookies
        session_id = resp.cookies.get("session_id")
        if not session_id:
            return jsonify({
                "error": "Session ID not found",
                "debug_response": resp.json()
            }), 400

        return jsonify({"session_id": session_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

