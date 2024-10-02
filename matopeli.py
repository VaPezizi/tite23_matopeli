
import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PySide6.QtCore import Qt, QTimer

# Vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        # starting game by button
        self.game_started = False
        self.init_screen()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

    def init_screen(self):
        start_text = self.scene().addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    def keyPressEvent(self, event):
        key = event.key()
        # starting game by button
        if not self.game_started:
            self.game_started = True
            self.scene().clear()
            self.start_game()
            return

        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # Päivitetään suunta vain, jos se ei ole vastakkainen valitulle suunnalle
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # Tarkistetaan törmäys pelikentän reunoihin
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            self.timer.stop()  # Pysäytetään peli, jos törmätään reunaan
            return

        # Tarkistetaan törmäys itseensä
        if new_head in self.snake:
            self.timer.stop()  # Pysäytetään peli, jos käärme törmää itseensä
            return

        self.snake.insert(0, new_head)

        # Tarkista, onko ruoka syöty
        if self.food in self.snake:
            self.score += 1
            self.food = self.spawn_food()
            self.addPiece()
        else:
            self.snake.pop()

        self.print_game()

    def addPiece(self):
        if self.direction == Qt.Key_Left:
            new_tail = (self.snake[-1][0] + 1, self.snake[-1][1])
        elif self.direction == Qt.Key_Right:
            new_tail = (self.snake[-1][0] - 1, self.snake[-1][1])
        elif self.direction == Qt.Key_Up:
            new_tail = (self.snake[-1][0], self.snake[-1][1] + 1)
        elif self.direction == Qt.Key_Down:
            new_tail = (self.snake[-1][0], self.snake[-1][1] - 1)

        self.snake.append(new_tail)

    def rainbow(self):  # Lisätty RGB
        r = random.randrange(0, 255 + 1)
        g = random.randrange(0, 255 + 1)
        b = random.randrange(0, 255 + 1)

        self.pen.setColor(QColor(r, g, b, 255))
        self.brush.setColor(QColor(r, g, b, 255))

    def draw_grid(self):
        pen = QPen(QColor(150, 150, 150))  # Harmaa väri ruudukolle
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            self.scene().addLine(x, 0, x, GRID_HEIGHT * CELL_SIZE, pen)
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            self.scene().addLine(0, y, GRID_WIDTH * CELL_SIZE, y, pen)

    def print_game(self):
        self.scene().clear()

        # Piirrä ruudukko
        self.draw_grid()

        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.pen, self.brush)

        self.scene().addText(f"Points: {self.score}", QFont("Arial", 10))  # pistelaskun piirto -JH
        self.rainbow()

        # print food
        fx, fy = self.food
        self.scene().addRect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.red))

    def start_game(self):
        self.score = 0  # Pistelaskun muuttuja
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.timer.start(300)
        self.pen = QPen(Qt.green)  # RGB
        self.brush = QBrush(Qt.red)  # RGB
        self.food = self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()