import os, time, multiprocessing

def start_server():
    os.system("python3 backend/manage.py runserver")
def start_testing():
    os.system("cd tests && python3 test.py")

def main():
    p1 = multiprocessing.Process(target=start_server)
    p2 = multiprocessing.Process(target=start_testing)

    p1.start()
    time.sleep(10)
    p2.start()
    p2.join()
    p1.terminate()

if __name__ == "__main__":
    main()