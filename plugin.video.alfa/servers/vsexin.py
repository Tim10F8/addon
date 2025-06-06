# -*- coding: utf-8 -*-
from core import httptools
from core import scrapertools
from core import servertools
from platformcode import logger
from platformcode import platformtools
from bs4 import BeautifulSoup

forced_proxy_opt = 'ProxySSL'

kwargs = {'set_tls': True, 'set_tls_min': True, 'retries_cloudflare': 0, 'forced_proxy_ifnot_assistant': forced_proxy_opt, 'ignore_response_code': True, 'cf_assistant': False}


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    global data
    response = httptools.downloadpage(page_url, **kwargs)
    data = response.data
    # https://69x.online/e/RktydXFBWVNKYUZIUDRKenNlenN4dz09  NETU
    if response.code == 404 or "<h2>WE ARE SORRY</h2>" in data or '<title>404 Not Found</title>' in data:
        return False, "[vsexin] El fichero no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, video_password):
    logger.info("(page_url='%s')" % page_url)
    soup = create_soup(page_url)
    data = create_soup(soup.iframe['src'])
    url = data.meta['content']
    url = scrapertools.find_single_match(url, 'url=([^"]+)')
    # if '69x.' in url:
        # return False, "[vsexin] Servidor no soportado"
    # server = servertools.get_server_from_url(url)
    
    devuelve = servertools.findvideos(url, True)
    if devuelve:
        url = devuelve[0][1]
        server = devuelve[0][2]
    
    video_url = servertools.resolve_video_urls_for_playing(server, url)
    if not video_url:
        platformtools.dialog_ok("sdefxcloud: Error", "Error en el servidor: %s" %server)
    return video_url[0]


def create_soup(url):
    logger.info()
    data = httptools.downloadpage(url, **kwargs).data
    soup = BeautifulSoup(data, "html5lib", from_encoding="utf-8")
    return soup
