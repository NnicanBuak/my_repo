# class ExerciseManager:

class Exercise():
  last_used_id = 1
  def __init__(self, name):
    self.id = Exercise.last_used_id
    Exercise.last_used_id += 1

exercise1 = Exercise()