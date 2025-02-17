import logging
from modules.tui import options
from services.dazn import dazn
from services.disney import disney
from services.hbo import hbo
from services.espn import espn
from services.paramount import paramount_ as paramount
from services.direct import direct

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.CRITICAL)
    service = options()
    match service:
        case 1:
            dazn()
        case 2:
            disney()
        case 3:
            hbo()
        case 4:
            espn()
        case 5:
            paramount()
        case 6:
            print("Soon..")
            exit()
        case 7:
            exit()

