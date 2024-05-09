import os
import paramiko
import json

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

MASTER_NODE_HOST = "master001"
NODE001_NODE_HOST = "node001"

NODE_PORT = 22
NODE_USERNAME = "mazen"
NODE_PASSWORD = "MazenAzure2002"

VMS = [MASTER_NODE_HOST]

REMOTE_PATH_TEST_CASES = "/home/mazen/gui/uploads"
REMOTE_PATH = "/home/mazen/gui"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def upload_to_node(local_path, remote_path, host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, NODE_PORT, NODE_USERNAME, NODE_PASSWORD)

    # SCPCLient takes a paramiko transport as its only argument
    scp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    scp.put(local_path, remote_path)

    scp.close()
    ssh.close()


def process_images():
    # Command to execute
    command = "mpirun -np 2 -machinefile /home/mazen/gui/machinefile python3 /home/mazen/gui/run.py"

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(MASTER_NODE_HOST, NODE_PORT, NODE_USERNAME, NODE_PASSWORD)

    # Execute the command on the remote VM
    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode()
    error = stderr.read().decode()

    # Close the SSH connection
    ssh.close()

    # Create JSON response
    response = {"output": output, "error": error}

    return response





@app.route("/upload", methods=["POST"])
def upload_images():
    images = request.files.getlist("images")
    operations = request.form.getlist("operations")

    image_data = []
    for image, op in zip(images, operations):
        local_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(local_path)

        image_info = {"operation": op, "file_path": local_path}
        image_data.append(image_info)

        remote_path = os.path.join(REMOTE_PATH_TEST_CASES, image.filename)
        for host in VMS:
            upload_to_node(local_path, remote_path, host)

    json_local_path = "image_data.json"
    with open(json_local_path, "w") as json_file:
        json.dump(image_data, json_file, indent=4)

    remote_path = os.path.join(REMOTE_PATH, json_local_path)
    for host in VMS:
        upload_to_node(json_local_path, remote_path, host)

    for image in images:
        os.remove(os.path.join(UPLOAD_FOLDER, image.filename))
    os.remove(json_local_path)

    vms_response = process_images()
    images = vms_response["output"].split("\n")

    return (
        jsonify(
            {
                "message": "Successful Processing",
                "Virtual Machines Output": vms_response,
                "images": images,
            }
        ),
        200,
    )


@app.route("/results/<path:filename>")
def static_results(filename):
    return send_from_directory("static/results", filename)


@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete_file(filename):
    file_path = os.path.join("static/results", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"File '{filename}' deleted successfully."}), 200
    return jsonify({"error": f"File '{filename}' not found."}), 404


@app.route("/check_ssh/<host>")
def check_connection(host):
    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            host, 22, "mazen", "MazenAzure2002", timeout=10
        )  # Adding timeout for connection attempt

        # Execute a simple command to check for response
        stdin, stdout, stderr = ssh.exec_command('echo "Successful"')

        # Check for response
        response = stdout.read().decode().strip()

        # Close the SSH connection
        ssh.close()

        return {"message": response}, 200
    except Exception as e:
        return {"message": "Failed to connect"}, 200


@app.route("/upload_test", methods=["POST"])
def upload_test():
    images = ["cat.jpg", "dog.jpg"]

    return (
        jsonify({"message": "Successful Processing", "images": images}),
        200,
    )


@app.route("/ping")
def ping():
    return (jsonify({"message": "pong"}), 200)


@app.route("/")
def index():
    return render_template("./index.html")


app.run(host="0.0.0.0", port=80, debug=True)
