import re
from multiprocessing import Process, Queue
import html

from scrapy.spiders import CrawlSpider 
from scrapy.http import Request, TextResponse
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from ..consult.crawler_second import Crawler_2_Instance 


class JusCrawler(CrawlSpider):

    def __init__(self, number:str):
        super().__init__()
        # self.number = '0710802-55.2018.8.02.0001'
        self.number = number

    # # set a name for referecing the spider
    name = "transparency_spider_second_instance"
    scraped_data = []

    # # restrict and define the intended domains 
    allowed_domains = ["www2.tjal.jus.br", "esaj.tjce.jus.br"]

    def start_requests(self):
        to_crawl = Crawler_2_Instance(self.number)

        response = to_crawl.consult()
        
        if response == "Couldn't find the process":
            yield Request(url='https://www2.tjal.jus.br/', callback=self.finish_spider)
        else:
            yield Request(url=response, callback=self.scrape) 


    def finish_spider(self, response):
        data = {"data": "Process not found"}
        self.scraped_data.append(data)
        self.crawler.engine.close_spider(self, "Process not found")
        return data

    def scrape(self, response): #( todas essas funções podem ser colocadas numa pasta de helpers hein)
        
        def format_scape_char(value: str) -> str:
            '''
            strips the excedent spaces in the value field
            '''
            try:
                value = re.sub(r'(\s)+', r' ', value)
                return value
            except:
                value = 'não consta'
                return value 
        
            
        def remove_nbsp(text):
            return re.sub(r'&amp;nbsp', '', text)

        def extract_parties(html):
            """
            extract all the parties in the process
            """
            selector = Selector(text=html)
            parties = []

            # autor_type = selector.css('').get()

            autor_name = selector.css('tr.fundoClaro:nth-child(1) td.nomeParteEAdvogado::text').get().replace('\xa0', ' ').strip()
            autor_lawyers = re.findall(r'Advogad[oa]:\s*(.*?)\s*(?=(?:Advogad[oa]:|$))', selector.css('tr.fundoClaro:nth-child(1) td.nomeParteEAdvogado').get(), flags=re.DOTALL)

            re_name = selector.css('tr.fundoClaro:nth-child(2) td.nomeParteEAdvogado::text').get().replace('\xa0', ' ').strip()
            re_lawyers = re.findall(r'Advogad[oa]:\s*(.*?)\s*(?=(?:Advogad[oa]:|$))', selector.css('tr.fundoClaro:nth-child(2) td.nomeParteEAdvogado').get(), flags=re.DOTALL)

            # Remove unwanted characters from lawyer names
            autor_lawyers = [re.sub(r'<.*?>', '', lawyer).strip() for lawyer in autor_lawyers]
            re_lawyers = [re.sub(r'<.*?>', '', lawyer).strip() for lawyer in re_lawyers]

            parties.append({
                'Autor': autor_name,
                'Advogado(s)': list(map(remove_nbsp, list(map(format_scape_char, autor_lawyers))))
            })
            parties.append({
                'Ré': re_name,
                'Advogado(s)': list(map(remove_nbsp, list(map(format_scape_char, re_lawyers))))
            })

            return parties


        def extract_movimentacoes(html):
            response = TextResponse(url='', body=html, encoding='utf-8')

            movimentacoes = []

            for tr in response.css('#tabelaUltimasMovimentacoes'):
                data_movimentacao = tr.css('tr.fundoClaro.movimentacaoProcesso .dataMovimentacaoProcesso::text').get().strip()
                descricao_movimentacao = tr.css('tr.fundoClaro.movimentacaoProcesso .descricaoMovimentacaoProcesso::text').get().strip()

                movimentacoes.append({
                    'Data Movimentacao': data_movimentacao,
                    'Descricao Movimentacao': descricao_movimentacao
                })

            return movimentacoes
        

        data = {
            "classe": response.css('#classeProcesso span::text').get(),
            "area": response.css('#areaProcesso span::text').get(),
            "assunto": response.css('#assuntoProcesso span::text').get(),
            "data_distribuicao": response.css('#dataHoraDistribuicaoProcesso::text').get(),
            "juiz": response.css('#juizProcesso::text').get(),
            "valor_da_acao": format_scape_char(response.css('#valorAcaoProcesso span::text').get()),
            "partes_do_processo": extract_parties(response.css('#tablePartesPrincipais').get()),
            'lista_das_movimentacoes': extract_movimentacoes(response.css('#tabelaUltimasMovimentacoes').get())
        }

        self.scraped_data.append(data)

        return {"data": data}


def search_justice_second_instance(number: str, queue):
    settings = Settings()
    settings.setmodule("scrapy.settings.default_settings")

    process = CrawlerProcess(settings)

    crawler = process.create_crawler(JusCrawler)

    JusCrawler.scraped_data = []  # Clear the class attribute before starting

    process.crawl(crawler, number=number)

    scraped_data = JusCrawler.scraped_data
    process.start(stop_after_crawl=True,install_signal_handlers=False)

    queue.put(scraped_data)

# def search_justice_second_instance(number: str):
#     queue = Queue()
#     p = Process(target=begin, args=(number, queue))
#     p.start()
#     p.join()
#     process_data = queue.get()
#     return process_data
