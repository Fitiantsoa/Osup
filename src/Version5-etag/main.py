import time as tm
from general import General

if __name__ == "__main__":
    start_time = tm.time()
    general = General()
    general.run()

    print("--- %s seconds ---" % (tm.time() - start_time))
