
from flask import Flask, request, jsonify
from scrapy import scrap_upwork  # Import your function from the module where it's defined

app = Flask(__name__)


@app.route('/automate_upwork', methods=['POST'])
def automate():
    try:
        # Get the link from the request body
        data = request.get_json()
        upwork_job_link = data.get('upwork_job_link','')

        if not upwork_job_link:
            return jsonify({"error": "No Upwork job link provided"}), 400

        # Call the automate_firsthalf function with the provided link
        result = scrap_upwork(upwork_job_link)

        return jsonify({"result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
