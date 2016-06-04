class Page(object):
    def __init__(self, session, url, data={}):
        self._url = url
        self._data = data
        self._session = session
        self._content = ''
        self.refresh_content()

    def refresh_content(self):
        self._content = str(self._session.get(self._url, data=self._data).content)

    @property
    def content(self):
        return self._content
