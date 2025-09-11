# Простое приложение "Крестики-нолики" на Tkinter.
# В этом файле показаны основные приёмы работы с Tkinter:
# - создание окна и виджетов
# - обработка событий (нажатия кнопок)
# - хранение и изменение состояния игры


import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple, Optional


WIN_COMBINATIONS: List[Tuple[int, int, int]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Три горизонтали
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Три вертикали
    (0, 4, 8), (2, 4, 6),  # Две диагонали
]


class TicTacToeApp:
    """
    Класс приложения "Крестики-нолики" на Tkinter.

    Здесь мы инкапсулируем всё состояние и логику в один класс:
    - окно `self.root`
    - состояние доски `self.game_board`
    - текущий игрок `self.current_player`
    - кнопки-клетки `self.buttons`
    - флаг окончания партии `self.game_over`
    - строка статуса `self.status_text`
    """

    def __init__(self) -> None:
        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)  # фиксированный размер окна

        # Инициализация состояния игры
        self.current_player: str = "X"  # Кто ходит сейчас
        self.game_board: List[str] = [""] * 9  # Пустая доска из 9 клеток
        self.buttons: List[tk.Button] = []  # сюда сохраним кнопки, чтобы к ним обращаться по индексу
        self.game_over: bool = False

        # Строка статуса для отображения, кто ходит
        self.status_text = tk.StringVar(value=f"Ход игрока {self.current_player}")

        # Строим интерфейс: поле и строку статуса
        self._build_board()
        self._build_status()

    def _build_board(self) -> None:
        """Создание 9 кнопок (3х3), каждая представляет клетку поля."""
        for i in range(9):
            # Для кнопки задаем команду с замыканием индекса i
            btn = tk.Button(
                self.root,
                text="",
                font=("Arial", 24),
                height=2,
                width=5,
                command=lambda i=i: self.handle_click(i),  # при нажатии передаём индекс клетки
            )
            # Выкладываем кнопки в сетку 3х3
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)

    def _build_status(self) -> None:
        """Добавление текстовой строки статуса под полем."""
        status_label = tk.Label(self.root, textvariable=self.status_text)
        status_label.grid(row=3, column=0, columnspan=3, pady=(6, 0))

    def check_winner(self) -> Optional[str]:
        """Проверка результата партии.
        Возращает:
        - 'X' или 'O' если есть победитель
        - 'Tie' если все клетки заполнены и победителя нет (ничья)
        - None если игра продолжается
        """
        for a, b, c in WIN_COMBINATIONS:
            # Если в трёх клетках одинаковый символ (и не пустой), значит есть победитель
            if self.game_board[a] and self.game_board[a] == self.game_board[b] == self.game_board[c]:
                return self.game_board[a]
        # Если пустых клеток не осталось, объявляем ничью
        return "Tie" if "" not in self.game_board else None
    
    def reset_game(self) -> None:
        """Полный сброс состояния игры и интерфейса."""
        self.game_board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="", state="normal")  # Очищаем текст и включаем кнопки
        self.game_over = False
        self.status_text.set(f"Ход игрока {self.current_player}")

    def handle_click(self, index: int) -> None:
        """Обработчик нажатия на клетку с индексом 'index'."""
        # Если партия уже завершена - игнорим нажатие
        if self.game_over:
            return
        # Запрещаем ходить на занятую клетку
        if self.game_board[index]:
            messagebox.showwarning("Недопустимый ход", "Эта клетка уже занята.")
            return

        # Записываем ход текущего игрока
        self.game_board[index] = self.current_player
        self.buttons[index].config(text=self.current_player)

        # Проверяем исход после хода
        result = self.check_winner()
        if result in ("X", "O"):
            self.game_over = True
            messagebox.showinfo("Игра окончена", f"Победил игрок {result}!")
            self.reset_game()
            return
        if result == "Tie":
            self.game_over = True
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.reset_game()
            return

        # Переход хода к другому игроку
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_text.set(f"Ход игрока {self.current_player}")
    
    def run(self) -> None:
        """Запуск главного цикла приложения Tkinter."""
        self.root.mainloop()


def main() -> None:
    """Создаем приложение и запускаем его."""
    app = TicTacToeApp()
    app.run()
