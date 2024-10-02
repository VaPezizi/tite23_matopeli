import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QFont, QPen, QColor
from PyQt5.QtCore import Qt, QTimer

GRID_HEIGHT = 20
GRID_WIDTH = 26  # 800 // 30
CELL_SIZE = 30
BACKGROUND_COLOR = QColor(200, 200, 200)  # Harmaa väri taustalle

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setFixedSize(800, 600)
        self.scene.setSceneRect(0, 0, 800, 600)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.game_started = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        self.draw_background()  # Piirretään tausta
        self.draw_grid()  # Piirretään ruudukko
        self.init_screen()

    def draw_background(self):
        """Piirretään harmaa tausta."""
        background = QGraphicsRectItem(0, 0, 800, 600)
        background.setBrush(BACKGROUND_COLOR)
        self.scene.addItem(background)

    def init_screen(self):
        """Näyttää aloitusruudun, jossa lukee 'Press any key to start'."""
        start_text = self.scene.addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    def draw_grid(self):
        """Piirtää ruudukon näkymään."""
        pen = QPen(Qt.blue, 0.5)  # Sininen ohut viiva

        # Piirretään vaaka viivat
        for i in range(GRID_HEIGHT + 1):
            self.scene.addLine(0, i * CELL_SIZE, 800, i * CELL_SIZE, pen)

        # Piirretään pystysuorat viivat
        for i in range(GRID_WIDTH + 1):
            self.scene.addLine(i * CELL_SIZE, 0, i * CELL_SIZE, 600, pen)

    def start_game(self):
        """Tämä metodi aloittaa pelin."""
        print("Peli alkaa!")
        self.timer.start(200)  # Asetetaan aikaväli 200 ms:lle

    def update_game(self):
        """Päivittää pelin tilan."""
        # Tässä voit lisätä muita pelitoimintoja, mutta ei enää käärmettä

    def keyPressEvent(self, event):
        """Tämä metodi käsittelee näppäinten painallukset."""
        key = event.key()

        if not self.game_started:
            if key == event.key():
                self.game_started = True
                self.scene.clear()
                self.draw_background()  # Piirretään tausta ennen pelin aloittamista
                self.draw_grid()  # Piirretään ruudukko ennen pelin aloittamista
                self.start_game()
        # Muut pelitoiminnot voivat olla täällä, mutta ei käärmettä

if __name__ == '__main__':
    app = QApplication(sys.argv)

    game_view = SnakeGame()

    game_view.show()

    sys.exit(app.exec_())
