# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import os, tempfile, time, sys, logging
logger = logging.getLogger(__name__)

import dryscrape
import pytesseract
from PIL import Image

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class ThreatDefenceRedirectMiddleware(RedirectMiddleware):
    def __init__(self, settings):
        super().__init__(settings)

        # start xvfb to support headless scraping
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        self.dryscrape_session = dryscrape.Session(base_url='https://yoururl.com')
        for key, value in settings['DEFAULT_REQUEST_HEADERS'].items():
            # seems to be a bug with how webkit-server handles accept-encoding
            if key.lower() != 'accept-encoding':
                self.dryscrape_session.set_header(key, value)
    def _redirect(self, redirected, request, spider, reason):
        # act normally if this isn't a threat defense redirect
        if not self.is_threat_defense_url(redirected.url):
            return super()._redirect(redirected, request, spider, reason)

        logger.debug(f'ari threat defense triggered for {request.url}')
        request.cookies = self.bypass_threat_defense(redirected.url)
        request.dont_filter = True # prevents the original link being marked a dupe
        return request
