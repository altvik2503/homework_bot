from typing import Tuple


class Position():
    """Определяет положение пользователя в точке."""

    class WrongData(Exception):
        """Ошибка в инициализирующих данных."""

        def __init__(self, *args: object) -> None:
            self._msg = 'Список не может быть пустым.'

        def __str__(self) -> str:
            return self._msg

    def __init__(self, directions: Tuple['Direction']) -> None:
        """Принимает кортеж Direction.
        Предполагает, что кортеж не пустой.
        """
        if not len(directions):
            raise self.WrongData
        self._directions: tuple = directions
        self._active =  0

    @property
    def image(self) -> str:
        """Возвращает текущую картинку."""
        return self._directions[self._active].image

    @property
    def next(self) -> 'Position':
        """ Возвращает ссылку на следующую Position"""
        return self._directions[self._active].next

    def _move(self, step: int) -> None:
        """Смещает активное напрвление до следующего.
        Пропускает направления без изображений.
        """
        for _ in range(len(self._directions)):
            self._active = (self._active + step) % len(self._directions)
            if self.image:
                break

    def left(self):
        """Смещает активное направление влево."""
        self._move(-1)

    def right(self):
        """Смещает активное направление вправо."""
        self._move(1)


class Direction():
    """Описывает одно напрвление."""

    def __init__(self, view: str = '', next: Position = None) -> None:
        self._view: str = view
        self._next: Position = next

    @property
    def show(self) -> str:
        return self._view

    @property
    def next(self):
        return self._next


class Map():
    """Управление действиями пользователя на карте."""

    def __init__(self, head: Position) -> None:
        """Принимает позицию начала перемещений."""
        self._active = head

    def update(self) -> None:
        """Обновляет изображение позиции у пользователя."""
        pass

    def step(self) -> None:
        """Сдвигает позицию на шаг."""
        next = self._active.next
        if next:
            self._active = next
            self.update()

    def left(self):
        """Смещает активное направление влево."""
        self._active.left()
        self.update()

    def right(self):
        """Смещает активное направление вправо."""
        self._active.right()
        self.update()
