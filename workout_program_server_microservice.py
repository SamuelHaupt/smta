
from multiprocessing import Process
import zmq


def calculate_one_rep_max(weight):
    one_rep_max = weight * (1 + 0.0333 * 5)
    return one_rep_max


def one_rep_max_microservice():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:49152")
    results = []
    while True:
        # Wait for incoming request
        weights = socket.recv_pyobj()
        print(weights)
        results = []
        # Calculate the results

        for i in weights:
            results.append(calculate_one_rep_max(i))

        # Send the results back to the client
        print(results)
        socket.send_pyobj(results)


def calculate_five_three_one(max):
    max_weight = max * 0.9

    return max_weight


def five_three_one_microservice():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:49153")
    results = []
    while True:
        # Wait for incoming request
        maxes = socket.recv_pyobj()
        print(maxes)
        # Calculate the results
        results = []
        for i in maxes:
            results.append(calculate_five_three_one(i))

        # Send the results back to the client
        print(results)
        socket.send_pyobj(results)


if __name__ == "__main__":
    Process(target=one_rep_max_microservice).start()
    Process(target=five_three_one_microservice).start()
