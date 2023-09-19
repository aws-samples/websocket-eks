from flask import Flask, render_template,request
import json
import os
import sys
import boto3


app = Flask(__name__)

@app.before_request
def log_request_info():
    #info to see that we are receiving the request.
    print(request)
    sys.stdout.flush()

@app.route('/', methods = ['GET'])
def get_request():
    return "get"

@app.route('/connect', methods = ['POST'])
def websocket_connect_request():
    #implement your business logic..
    # we are returning ok here but actually you would need to respond back to the api gateway.
    print("in connect")
    return "connect"

@app.route('/', methods = ['POST'])
def websocket_default_request():
    #implement your business logic..
    # we are returning the message sent 
    try:
        print("in default")
        b= request.get_data()
        b = b.decode('utf8').replace("'", '"')
        body = json.loads(b)
        if ("myConnectionIdProperty" in body):
            conn_id = body["myConnectionIdProperty"]
            domain= body['domain']
            stage= body["stage"]

            my_msg = body["myBody"]
            message = "Got message:"+my_msg
            endpoint_url = "https://"+domain+"/"+stage
            apig_management_client = boto3.client(
                              'apigatewaymanagementapi', endpoint_url=endpoint_url)
            send_response = apig_management_client.post_to_connection(
                                     Data=message, ConnectionId=conn_id)
    except Exception as e:
        print(e)
    sys.stdout.flush()
    return "default"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8501))
    app.run(debug=True, host='0.0.0.0', port=port)
