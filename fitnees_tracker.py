class InfoMessage:
  """Информационное сообщение о тренировке."""
  def __init__(self, 
               training_type: str, 
               duration: float, 
               distance: float, 
               speed: float, 
               calories: float):
    self.training_type = training_type
    self.duration = duration
    self.distance = distance
    self.speed = speed
    self.calories = calories

  def get_message(self):
    return(f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.2f} ч.; Дистанция: {self.distance:.2f} км; Ср. скорость: {self.speed:.2f} км/ч; Потрачено ккал: {self.calories:.2f}')


class Training:
  """Базовый класс тренировки."""
  M_IN_KM: int = 1000
  STEP_LEN: float = 0.65
  MIN_IN_H: int = 60
  
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
    return self.action * self.STEP_LEN / self.M_IN_KM

  def get_mean_speed(self) -> float:
    """Получить среднюю скорость движения."""
    return self.get_distance() / self.duration 

  def get_spent_calories(self) -> int:
    """Получить количество затраченных калорий."""
    return 0

  def show_training_info(self) -> InfoMessage:
    """Вернуть информационное сообщение о выполненной тренировке."""
    return InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
  """Тренировка: бег."""
  CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
  CALORIES_MEAN_SPEED_TERM: float = 1.79
  def get_spent_calories(self) -> float:
    return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_TERM) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)

class SportsWalking(Training):
  """Тренировка: спортивная ходьба."""
  CALORIES_WEIGHT_FIRST_MULTIPLAYER: float = 0.035
  CALORIES_WEIGHT_SECOND_MULRIPLAYER: float = 0.029
  KM_H_IN_M_S: float = 0.278
  CM_IN_M: int = 100
  def __init__(self,
               action: int,
               duration: float,
               weight: float,
               height: float
              ) -> None:
    super().__init__(action, duration, weight)  
    self.height = height
  
  def get_spent_calories(self) -> float:
    avg_speed = (self.get_mean_speed() * self.KM_H_IN_M_S) ** 2
    return ((self.CALORIES_WEIGHT_FIRST_MULTIPLAYER * self.weight + (avg_speed /(self.height / self.CM_IN_M)) * self.CALORIES_WEIGHT_SECOND_MULRIPLAYER * self.weight) * self.duration * self.MIN_IN_H)
    

class Swimming(Training):
  LEN_STEP: float = 1.38 
  CALORIES_MEAN_SPEED_TERM: float = 1.1
  CALORIES_WEIGHT_MULTIPLAYER: int = 2
  """Тренировка: плавание."""
  def __init__(self,
               action: int,
               duration: float,
               weight: float,
               len_pool: float,
               count_pool: int):
    super().__init__(action, duration, weight)
    self.len_pool = len_pool
    self.count_pool = count_pool
 
  def get_mean_speed(self) -> float: 
    return self.len_pool * self.count_pool / self.M_IN_KM / self.duration
  
  def get_spent_calories(self) -> float: 
    return (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_TERM) * self.CALORIES_WEIGHT_MULTIPLAYER * self.weight * self.duration
    
def read_package(workout_type: str, data: list) -> Training:
  """Прочитать данные полученные от датчиков."""
  workouts = {'SWM' : Swimming, 'RUN' : Running, 'WLK' : SportsWalking}
  return workouts[workout_type](*data)

def main(training: Training) -> None:
  """Главная функция."""
  print(training.show_training_info().get_message())


if __name__ == '__main__':
  packages = [
      ('SWM', [720, 1, 80, 25, 40]),
      ('RUN', [15000, 1, 75]),
      ('WLK', [9000, 1, 75, 180]),
    ]

  for workout_type, data in packages:
    training = read_package(workout_type, data)
    main(training)