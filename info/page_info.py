import logging
import time
import os
import errno


logger = logging.getLogger('ogame_bot.info.page_info')


class Page(object):
    def __init__(self, session, url, data=None):
        self.logger = logger
        self._url = url

        if data is None:
            self._data = {}
        else:
            self._data = data

        self._session = session
        self._content = ''
        self.last_refresh_time = 0
        self.refresh_content()

    def refresh_content(self, force_refresh=False):
        current_time = time.time()
        time_delta = current_time - self.last_refresh_time
        if force_refresh or time_delta > 5:
            self.logger.debug("Refreshing site info for site: " + self._url)
            self.content = str(self._session.get(self._url, data=self._data).content)
            self.last_refresh_time = current_time
        else:
            self.logger.debug("Last refresh of site " + self._url + " was only " + str(time_delta) + " seconds before. Skipping refresh!")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        try:
            os.makedirs("page_contents")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        file_name = self._url.split("=")[-1] + ".txt"
        with open(os.path.join("page_contents", file_name), 'w') as file:
            file.write(content)
        self._content = content
