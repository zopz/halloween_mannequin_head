"""Components for running the raspberry pi in server mode"""

import os
from flask import Flask, jsonify, request
from servo_controller import ServoController


app = Flask(__name__)
sc = ServoController()


@app.route('/')
def index():
    """API index route"""
    return jsonify({'status': 'ok'})


@app.route('/servo/')
def alarm():
    """Turn on the relay"""
    percentage_x = request.args.get('px')
    percentage_y = request.args.get('py')
    if not percentage_x:
        return jsonify({'status': 'no px'})
    if not percentage_y:
        return jsonify({'status': 'no py'})
    sc.set_servo_percent(float(percentage_x), 'x')
    sc.set_servo_percent(float(percentage_y), 'y')
    return jsonify({'status': {f'px={percentage_x}', f'py={percentage_y}'}})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
