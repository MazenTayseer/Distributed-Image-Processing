from mpi4py import MPI  # MPI for distributed computing
import os

from master import master
from worker import worker

comm = MPI.COMM_WORLD

TEST_CASES_DIR = "/home/mazen/gui/uploads"
RESULTS_DIR = "/home/mazen/gui/results"

def main():
    for directory in [TEST_CASES_DIR, RESULTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    images_list = [
        os.path.join(TEST_CASES_DIR, filename)
        for filename in os.listdir(TEST_CASES_DIR)
        if any(
            filename.lower().endswith(ext)
            for ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]
        )
    ]

    if comm.Get_rank() == 0:
        master(comm, images_list)
    else:
        worker(comm, images_list)


main()
