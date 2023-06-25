from flask import Flask, jsonify, render_template
import subprocess
import json
import traceback
import seqlog
import logging

app = Flask(__name__)

# Create a GELFHandler instance for sending logs to the GELF server
seqlog.configure_from_file('seq.yml')
# Get the logger
logger = logging.getLogger(__name__)

app.logger.warning("GPS App is running")

def is_device_connected():
    command = ['gpspipe', '-w', '--json', '--seconds', '1']
    try:
        output = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.DEVNULL)
        json_lines = output.strip().split('\n')
        for json_line in json_lines:
            #print(json_line)
            data = json.loads(json_line)
            if data.get('class') == 'DEVICES'and len(data.get('devices', [])) > 0:
                return True
        return False
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        app.logger.exception("An Exception Occurred:", exc_info=e)
        return False


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/gps', methods=['GET'])
def get_gps_data():
    command = ['gpspipe', '--json', '--seconds', '2']
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        json_lines = output.strip().split('\n')
        json_array = '[' + ','.join(json_lines) + ']'
        parsed_data = json.loads(json_array)
        return jsonify(parsed_data)
    except subprocess.CalledProcessError as e:
        error_message = f"Failed to execute gpspipe command: {e}"
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500
    except json.JSONDecodeError as e:
        error_message = f"Failed to parse JSON output: {e}"
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500

@app.route('/health', methods=['GET'])
def check_health():
    device_connected = is_device_connected()
    if device_connected:
        return jsonify({'status': 'OK'})
    else:
        error_message = 'Device not connected'
        app.logger.error(error_message)
        return jsonify({'status': error_message}), 503

# Error handlers for 400 and 500 status codes
@app.errorhandler(400)
def handle_bad_request(e):
    error_message = 'Bad Request'
    app.logger.error(f'{error_message}: {e}')
    return jsonify({'error': error_message}), 400

@app.errorhandler(500)
def handle_internal_server_error(e):
    error_message = 'Internal Server Error'
    app.logger.error(f'{error_message}: {e}')
    return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run()