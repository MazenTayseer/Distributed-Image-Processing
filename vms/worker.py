from WorkerThread import WorkerThread
import queue
import json


def matches_filename(data, image_path):
    if data.split("/")[-1] == image_path.split("/")[-1]:
        return True
    return False


def worker(comm, images_list):
    CPU_NUM = comm.Get_size() - 1

    threads = []
    integerPartPerPart = len(images_list) // CPU_NUM
    remainder = len(images_list) % CPU_NUM

    result = [integerPartPerPart] * CPU_NUM

    for i in range(remainder):
        result[i] += 1

    number_of_threads = result[comm.Get_rank() - 1]

    with open("/home/mazen/gui/image_data.json") as f:
        image_data = json.load(f)

    task_queue = queue.Queue()
    starting_index = (comm.Get_rank() - 1) * number_of_threads

    for i in range(starting_index, starting_index + number_of_threads):
        for d in image_data:
            if matches_filename(d["file_path"], images_list[i]):
                task_queue.put((images_list[i], d["operation"], i))
                break

    for i in range(number_of_threads):
        task_queue.put(None)

    for i in range(number_of_threads):
        thread = WorkerThread(task_queue, comm)
        thread.start()
        # print(f"Thread {i+1} started on node", comm.Get_rank())
        threads.append(thread)

    for thread in threads:
        thread.join()
