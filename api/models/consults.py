from multiprocessing import Queue, Process

from crawler.jus_crawler.spiders.spider_jus import search_justice
from crawler.jus_crawler.spiders.spider_jus_2 import search_justice_second_instance


def consult_process(number: str) -> dict:
    """
    Builds the process in order to run two consults in parallel
    """

    code = 200

    process_details_first_instance = Queue()
    process_details_second_instance = Queue()

    process1 = Process(target=search_justice, args=(
        number, process_details_first_instance))
    process2 = Process(target=search_justice_second_instance,
                       args=(number, process_details_second_instance))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    result = {
        "Primeira Instancia": process_details_first_instance.get(),
        "Segunda Instancia": process_details_second_instance.get(),
    }

    return result, code
