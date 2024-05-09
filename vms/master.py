import cv2  # OpenCV for image processing
from mpi4py import MPI
import os
import paramiko

SERVER_NODE_HOST = "server"
NODE_PORT = 22
NODE_USERNAME = "mazen"
NODE_PASSWORD = "MazenAzure2002"

SERVER_NODE_REMOTE_PATH = "/home/mazen/flask/static/results"

UPLOADS_DIR = "/home/mazen/gui/uploads"
RESULTS_DIR = "/home/mazen/gui/results"


def master(comm, images_list):
    # Create worker threads

    def save_image(image, filepath):
        cv2.imwrite(filepath, image)

    for i in range(len(images_list)):
        received_data = comm.recv(source=MPI.ANY_SOURCE, tag=i)
        processed_image = received_data

        image_name = images_list[i].split("/")[-1]

        results_local_path = os.path.join(RESULTS_DIR, image_name)

        save_image(processed_image, results_local_path)

        remote_path = os.path.join(SERVER_NODE_REMOTE_PATH, image_name)
        upload_to_node(
            results_local_path,
            remote_path,
            SERVER_NODE_HOST,
            NODE_PORT,
            NODE_USERNAME,
            NODE_PASSWORD,
        )

        uploads_local_path = os.path.join(UPLOADS_DIR, image_name)

        os.remove(results_local_path)
        os.remove(uploads_local_path)

        print(image_name)

    # print("Copied All Images")

    os.remove("/home/mazen/gui/image_data.json")


def upload_to_node(local_path, remote_path, host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    # SCPClient takes a paramiko transport as its only argument
    scp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    scp.put(local_path, remote_path)

    scp.close()
    ssh.close()
