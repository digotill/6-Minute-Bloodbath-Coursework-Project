from Code.DataStructures.HashMap import *
from Code.Individuals.Spark import *

class SparkManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, GENERAL["hash_maps"][5])
                    self.spark_pool = set()

          def update(self):
                    if not self.game.changing_settings:
                              for spark in self.grid.items:
                                        spark.move()
                              self.check_if_remove()
                              self.grid.rebuild()

          def create_spark(self, angle, pos, dictionary):
                    for _ in range(dictionary['amount']):
                              spark_angle = math.radians(random.randint(
                                        int(angle) - dictionary['spread'],
                                        int(angle) + dictionary['spread']
                              ))
                              spark_velocity = random.randint(dictionary["min_vel"], dictionary["max_vel"])
                              if len(self.spark_pool) == 0:
                                        self.grid.insert(
                                                  Spark(self.game, pos, spark_angle, spark_velocity,
                                                        dictionary['colour'], dictionary['scale']))
                              else:
                                        spark = self.spark_pool.pop()
                                        spark.reset(pos, spark_angle, spark_velocity, dictionary["colour"],
                                                    dictionary['scale'])
                                        self.grid.insert(spark)

          def check_if_remove(self):
                    for spark in self.grid.items.copy():
                              if not spark.alive:
                                        self.grid.items.remove(spark)
                                        self.spark_pool.add(spark)