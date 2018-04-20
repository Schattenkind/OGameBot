import logging


logger = logging.getLogger('ogame_bot.info.page_info')

class Page(object):
    def __init__(self, session, url, data={}):
        self.logger = logger
        self._url = url
        self._data = data
        self._session = session
        self._content = ''
        self.refresh_content()

    def refresh_content(self):
        self.logger.debug("Refreshing site info for site: " + self._url)
        self._content = str(self._session.get(self._url, data=self._data).content)

    @property
    def content(self):
        return self._content
