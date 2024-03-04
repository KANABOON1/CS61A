# class Bee(Insect):
#     """A Bee moves from place to place, following exits and stinging ants."""
#
#     name = 'Bee'
#     damage = 1
#     # OVERRIDE CLASS ATTRIBUTES HERE
#
#
#     def sting(self, ant):
#         """Attack an ANT, reducing its armor by 1."""
#         ant.reduce_armor(self.damage)
#
#     def move_to(self, place):
#         """Move from the Bee's current Place to a new PLACE."""
#         self.place.remove_insect(self)
#         place.add_insect(self)
#
#     def blocked(self):
#         """Return True if this Bee cannot advance to the next Place."""
#         # Special handling for NinjaAnt
#         # BEGIN Problem Optional
#         return self.place.ant is not None
#         # END Problem Optional
#
#     def action(self, gamestate):
#         """A Bee's action stings the Ant that blocks its exit if it is blocked,
#         or moves to the exit of its current place otherwise.
#
#         gamestate -- The GameState, used to access game state information.
#         """
#         destination = self.place.exit
#         # Extra credit: Special handling for bee direction
#         # BEGIN EC
#         "*** YOUR CODE HERE ***"
#         # END EC
#         if self.blocked():
#             self.sting(self.place.ant)
#         elif self.armor > 0 and destination is not None:
#             self.move_to(destination)
#
#     def add_to(self, place):
#         place.bees.append(self)
#         Insect.add_to(self, place)
#
#     def remove_from(self, place):
#         place.bees.remove(self)     # 从place的bees列表中删除self
#         Insect.remove_from(self, place)
#
# class GameState:
#     """An ant collective that manages global game state and simulates time.
#
#     Attributes:
#     time -- elapsed time
#     food -- the colony's available food total
#     places -- A list of all places in the colony (including a Hive)
#     bee_entrances -- A list of places that bees can enter
#     """
#
#     def __init__(self, strategy, beehive, ant_types, create_places, dimensions, food=2):
#         """Create an GameState for simulating a game.
#
#         Arguments:
#         strategy -- a function to deploy ants to places
#         beehive -- a Hive full of bees
#         ant_types -- a list of ant constructors
#         create_places -- a function that creates the set of places
#         dimensions -- a pair containing the dimensions of the game layout
#         """
#         self.time = 0
#         self.food = food
#         self.strategy = strategy
#         self.beehive = beehive
#         self.ant_types = OrderedDict((a.name, a) for a in ant_types)
#         self.dimensions = dimensions
#         self.active_bees = []
#         self.configure(beehive, create_places)
#
#     def configure(self, beehive, create_places):
#         """Configure the places in the colony."""
#         self.base = AntHomeBase('Ant Home Base')
#         self.places = OrderedDict()
#         self.bee_entrances = []
#         def register_place(place, is_bee_entrance):
#             self.places[place.name] = place
#             if is_bee_entrance:
#                 place.entrance = beehive
#                 self.bee_entrances.append(place)
#         register_place(self.beehive, False)
#         create_places(self.base, register_place, self.dimensions[0], self.dimensions[1])
#
#     def simulate(self):
#         """Simulate an attack on the ant colony (i.e., play the game)."""
#         num_bees = len(self.bees)
#         try:
#             while True:
#                 self.strategy(self)                 # Ants deploy
#                 self.beehive.strategy(self)         # Bees invade
#                 for ant in self.ants:               # Ants take actions
#                     if ant.armor > 0:
#                         ant.action(self)
#                 for bee in self.active_bees[:]:     # Bees take actions
#                     if bee.armor > 0:
#                         bee.action(self)
#                     if bee.armor <= 0:
#                         num_bees -= 1
#                         self.active_bees.remove(bee)
#                 if num_bees == 0:
#                     raise AntsWinException()
#                 self.time += 1
#         except AntsWinException:
#             print('All bees are vanquished. You win!')
#             return True
#         except BeesWinException:
#             print('The ant queen has perished. Please try again.')
#             return False
#
#     def deploy_ant(self, place_name, ant_type_name):
#         """Place an ant if enough food is available.
#
#         This method is called by the current strategy to deploy ants.
#         """
#         constructor = self.ant_types[ant_type_name]
#         if self.food < constructor.food_cost:
#             print('Not enough food remains to place ' + ant_type_name)
#         else:
#             ant = constructor()
#             self.places[place_name].add_insect(ant)
#             self.food -= constructor.food_cost
#             return ant
#
#     def remove_ant(self, place_name):
#         """Remove an Ant from the game."""
#         place = self.places[place_name]
#         if place.ant is not None:
#             place.remove_insect(place.ant)
#
#     @property
#     def ants(self):
#         return [p.ant for p in self.places.values() if p.ant is not None]
#
#     @property
#     def bees(self):
#         return [b for p in self.places.values() for b in p.bees]
#
#     @property
#     def insects(self):
#         return self.ants + self.bees
#
#     def __str__(self):
#         status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
#         return str([str(i) for i in self.ants + self.bees]) + status
# class ThrowerAnt(Ant):
#     """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""
#
#     name = 'Thrower'
#     implemented = True
#     damage = 1
#     # ADD/OVERRIDE CLASS ATTRIBUTES HERE
#     food_cost = 3
#     # 对于任意类型的ThrowerAnt,都定义了max_range以及min_range
#     max_range=float('inf')    # 每一类都定义最大距离
#     min_range=0               # 每一类都定义最小距离,便于nearest_bee()编写
#     def nearest_bee(self, beehive):
#         """Return the nearest Bee in a Place that is not the HIVE (beehive), connected to
#         the ThrowerAnt's Place by following entrances.
#
#         This method returns None if there is no such Bee (or none in range).
#         """
#         # BEGIN Problem 3 and 4
#         def check_the_distance(place1,place2):  # 认为 place2-place1 > 0
#             """ 计算place1与place2的距离 """
#             distance=0
#             while True:
#                 if place1==place2:
#                     return distance
#                 distance,place1=distance+1,place1.entrance
#
#         place = self.place
#         while place!=beehive:
#             if place.bees:
#                 if self.min_range<=check_the_distance(self.place,place)<=self.max_range:
#                     return rANTdom_else_none(place.bees)
#             place=place.entrance
#         return None                                   # 如果都没有找到 bee,则返回 None
#         # END Problem 3 and 4
#
#     def throw_at(self, target):
#         """Throw a leaf at the TARGET Bee, reducing its armor."""
#         if target is not None:
#             target.reduce_armor(self.damage)
#
#     def action(self, gamestate):
#         """Throw a leaf at the nearest Bee in range."""
#         self.throw_at(self.nearest_bee(gamestate.beehive))
