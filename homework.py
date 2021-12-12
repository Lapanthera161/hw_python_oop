from typing import List, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Я честно гуглила эту формулу и нет там расшифровки этих просто чисел.
       Поэтому названия такие."""
    RATIO_CAL_1: int = 18
    RATIO_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.RATIO_CAL_1 * self.get_mean_speed() - self.RATIO_CAL_2)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_H)


class SportsWalking(Training):
    RATIO_CAL_3: float = 0.035
    RATIO_CAL_4: float = 0.029
    RATIO_SPEED: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.RATIO_CAL_3 * self.weight
                + (self.get_mean_speed() ** self.RATIO_SPEED // self.height)
                * self.RATIO_CAL_4 * self.weight) * self.duration * self.MIN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    RATIO_CAL_5: float = 1.1
    RATIO_W: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.RATIO_CAL_5)
                * self.RATIO_W * self.weight)


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Здесь не совсем поняла про полную аннотацию аргумента."""

    action_type = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming}
    if workout_type in action_type:
        return action_type[workout_type](*data)
    else:
        raise ValueError('Error 404')


def main(training: Training) -> None:
    """Главная функция."""

    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
