import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore, QtWidgets
from qt_material import apply_stylesheet


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.history = []

        self.expression1 = ''
        self.expression2 = ''
        self.operation = ''
        self.result = ''

        self.setWindowTitle("Калькулятор")
        self.resize(500, 600)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.label = QLabel('')
        self.label.setSizeIncrement(100, 100)
        self.label.setStyleSheet("width: 100%; height: 100%; color: white;")
        self.history = QtWidgets.QListWidget(self)
        self.history.move(20, 100)
        self.history.setStyleSheet("width: 100%; height: 100%; color: white; font-size: 12pt;")
        self.history.setFixedSize(500, 70)
        self.display = QLineEdit()
        self.display.setFixedSize(500, 100)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Arial", 20))
        self.display.setStyleSheet("width: 100%; height: 100%; color: white; font-size: 24pt;")
        self.display.setAlignment(QtCore.Qt.AlignRight)

        self.buttons = [
            QPushButton('CE'), QPushButton('C'), QPushButton('⌫'),QPushButton('/'),
            QPushButton('7'), QPushButton('8'), QPushButton('9'), QPushButton('*'),
            QPushButton('4'), QPushButton('5'), QPushButton('6'), QPushButton('-'),
            QPushButton('1'), QPushButton('2'), QPushButton('3'), QPushButton('+'),
            QPushButton('.'), QPushButton('0'), QPushButton('=')
        ]
        self.grid.addWidget(self.history, 0, 0, 1, 4, alignment=QtCore.Qt.AlignmentFlag.AlignTop |
                                                                QtCore.Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.label, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop |
                            QtCore.Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.display, 1, 0, 1, 0)

        row = 2
        column = 0
        for button in self.buttons[:-1]:  # Добавляем все кнопки, кроме '='
            button.setFixedSize(120, 80)
            button.setStyleSheet("width: 50%; height: 65%; font-size: 12pt;")
            self.grid.addWidget(button, row, column, 1, 1)
            column += 1
            if column == 4:
                row += 1
                column = 0

        # Добавление кнопки "=" на две ячейки
        equals_button = self.buttons[-1]  # Кнопка "="
        equals_button.setFixedSize(245, 80)  # Задаем размер для кнопки "="
        self.grid.addWidget(equals_button, 6, 2, 1, 2)  # Позиция (4, 2), размер (1, 2)

        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    def button_clicked(self) -> None:
        dct = {'+': self.plus, '-': self.minus, '*': self.multy, '/': self.div, 'C': self.c,
               '⌫': self.reverse, 'CE': self.ce}

        if self.display.text() in ['Ошибка деления на 0', '∞', '0', 'Корень меньше 0', '-']:
            self.ce()

        button_text = self.sender().text()
        if (self.operation == "" and button_text == '0' and not self.expression1) or (
                self.operation != "" and button_text == '0' and not self.expression2):
            return
        if self.operation == '' and button_text == '.' and not self.expression1:
            button_text = '0.'
        elif self.operation != '' and button_text == '.' and not self.expression2:
            button_text = '0.'
        if button_text in ['0.', '.'] and '.' in self.display.text():
            return
        expression = self.define_current_expression()
        if button_text == '.' and expression == '-':
            return

        if button_text == "=":
            self.evaluate("")
            return

        if button_text in dct:
            dct[button_text]()
            return

        if self.operation == '':
            self.expression1 += button_text
            self.display.setText(self.expression1)
        else:
            self.expression2 += button_text
            self.display.setText(self.expression2)

    def define_operation(self, operation: str) -> None:
        operations = {"plus": '+', "minus": "-", "multy": "*", "div": '/'}
        if self.expression2 != '':
            return
        if self.expression1 != '':
            self.operation = operations[operation]
            self.display.setText('')

    def define_current_expression(self) -> str:
        if self.operation == '':
            expression = self.expression1
        else:
            expression = self.expression2
        return expression

    def save_expression(self, expression: str) -> None:
        if self.operation == '':
            self.expression1 = expression
        else:
            self.expression2 = expression

    def plus(self) -> None:
        if not self.expression2 == "":
            self.evaluate("+")
            return
        self.define_operation('plus')

    def minus(self) -> None:
        if not self.expression2 == "":
            self.evaluate("-")
            return
        self.define_operation('minus')

    def multy(self) -> None:
        if not self.expression2 == "":
            self.evaluate("*")
            return
        self.define_operation('multy')

    def div(self) -> None:
        if not self.expression2 == "":
            self.evaluate("/")
            return
        self.define_operation('div')

    def c(self) -> None:
        self.display.setText('')
        self.expression1 = ''
        self.expression2 = ''
        self.operation = ''

    def reverse(self) -> None:
        text = self.display.text()
        if self.operation == '':
            self.expression1 = text[:-1]
        else:
            self.expression2 = text[:-1]
        new_text = text[:-1]
        self.display.setText(str(new_text))

    def ce(self) -> None:
        if self.operation == '':
            self.expression1 = ""
            self.display.setText(self.expression1)
        else:
            self.expression2 = ""
            self.display.setText(self.expression2)

    def evaluate(self, operation) -> None:
        if self.expression2 != '' and self.operation == "/" and float(self.expression2) <= 0:
            self.display.setText("Ошибка деления на 0")
            return

        if self.expression2 != '':
            if self.operation == '+':
                result = float(self.expression1) + float(self.expression2)
            elif self.operation == '-':
                result = float(self.expression1) - float(self.expression2)
            elif self.operation == '*':
                result = float(self.expression1) * float(self.expression2)
            elif self.operation == '/':
                result = float(self.expression1) / float(self.expression2)

            example = f"{self.expression1} {self.operation} {self.expression2}"
            self.display.setText(str(result))
            self.expression1 = str(result)
            self.expression2 = ''
            self.operation = operation
            self.history.addItem(f"{example} = {result}")


if __name__ == '__main__':
    app = QApplication([])
    apply_stylesheet(app, theme='dark_teal.xml')
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())

