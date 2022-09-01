from insert import start_insert

from traitement import start_traitement

from multiprocessing import Process

if __name__ == "__main__":
    p1 = Process(target=start_traitement)
    p2 = Process(target=start_insert)
    p1.start()
    p2.start()
