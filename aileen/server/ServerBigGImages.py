from google_images_search import GoogleImagesSearch

from aileen.Answer import Answer
from aileen.Config import Keys
from aileen.Handlers import Handlers
from aileen.server.ServerViewer import ServerViewer


class ServerBigGImages(ServerViewer):
    value = 30

    def __init__(self):
        super().__init__();
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
        h = Handlers.getInstance()\
            .add_control('show', self.show)\
            .add_control('greetings', self.greetings)

    def greetings(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "\t<code>BigGImages</code> uses the Custom Search Engine's API by <b>Google</b>. And <code>Viewer</code> from render"
        ])

    def show(self, source, question=None, answer=Answer()):
        print("Searching for: {}".format(source))
        self._search_params['q'] = source
        self.gis.search(search_params=self._search_params)
        for image in self.gis.results():
            content = self.download_binary(image.url)
            if content is None:
                continue # Try again
            answer.binary = content
            answer.append_rows(["Look at this..."])
            return answer