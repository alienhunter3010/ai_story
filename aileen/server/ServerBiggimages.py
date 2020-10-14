import logging

from google_images_search import GoogleImagesSearch

from aileen.Answer import Answer
from aileen.Config import Keys
from aileen.Handlers import Handlers
from aileen.server.ServerViewer import ServerViewer


class ServerBiggimages(ServerViewer):
    value = 30

    def __init__(self, setup=None):
        super().__init__(setup=setup);
        # define search params:
        self._search_params = {
            'q': 'Nemo',
            'num': 15,
            'safe': 'off',
            'fileType': 'jpg|gif|png',
            'imgType': 'imgTypeUndefined',
            'imgSize': 'imgSizeUndefined',
            'imgDominantColor': 'imgDominantColorUndefined'
        }
        Keys.load()
        gcs = Keys.get('GoogleSearchImages')
        self.gis = GoogleImagesSearch(gcs['apiKey'], gcs['cx'])

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('show', self.show)\
            .add_control('greetings', self.greetings)

    def greetings(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "\t<code>BigGImages</code> uses the Custom Search Engine's API by <b>Google</b>. And <code>Viewer</code> from render"
        ])

    def show(self, source, question=None, answer=Answer()):
        logging.info("Searching for: {}".format(source))
        self._search_params['q'] = source
        self.gis.search(search_params=self._search_params)
        for image in self.gis.results():
            return self.binary(image.url, answer)
