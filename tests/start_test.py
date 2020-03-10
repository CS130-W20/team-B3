import os, time
from multiprocessing import Process, Queue

Q = Queue()

def start_server():
    os.system("python3 backend/manage.py runserver")
def start_testing():
    cmd = os.system("cd tests && python3 test.py")
    Q.put(os.WEXITSTATUS(cmd))

def main():
    p1 = Process(target=start_server)
    p2 = Process(target=start_testing)

    p1.start()
    time.sleep(10)
    p2.start()
    p2.join()
    p1.terminate()
    exit(Q.get())

if __name__ == "__main__":
    main()