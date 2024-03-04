"""
CS 61A presents Ants Vs. SomeBees.
调用并实现各种method(接口),实现类的封装性
"""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################

class Place:
    """A Place holds insects and has an exit to another Place."""

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        if exit:    # 注:采用分开设置的方法设置exit && entrance,将不同的place关联起来
            exit.entrance=self
        # END Problem 2

    def add_insect(self, insect):
        """
        将insects与place关联起来的核心方法在Place中,以后只要对于place调用add_insect就可以了
        Asks the insect to add itself to the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """
        Asks the insect to remove itself from the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has armor and a Place."""
    damage = 0
    # ADD CLASS ATTRIBUTES HERE
    is_watersafe=False   # default

    def __init__(self, armor, place=None):
        """Create an Insect with an ARMOR amount and a starting PLACE."""
        self.armor = armor
        self.place = place  # set by Place.add_insect and Place.remove_insect,place是Insect属性,一只昆虫只有一个地点.lm,llll...

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the insect from its place if it
        has no armor remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_armor(2)
        >>> test_insect.armor
        3
        """
        self.armor -= amount
        if self.armor <= 0:
            self.place.remove_insect(self)
            self.death_callback()

    def action(self, gamestate):
        """The action performed each turn.

        gamestate -- The GameState, used to access game state information.
        """

    def death_callback(self):
        # overriden by the gui
        pass

    def add_to(self, place):
        """Add this Insect to the given Place
        By default just sets the place attribute, but this should be overriden in the subclasses
            to manipulate the relevant attributes of Place
        """
        self.place = place  # 能用超类表示的部分就用超类表示 !

    def remove_from(self, place):
        self.place = None


    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    # ADD CLASS ATTRIBUTES HERE
    double_damage=False
    blocks_path=True
    def __init__(self, armor=1):
        """Create an Ant with an ARMOR quantity."""
        Insect.__init__(self, armor)

    def can_contain(self, other):   # 为了对应containerAnt的can_contain()方法
        return False

    def contain_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):   # 通过add_to将place\ant\container关联
        if place.ant is None:
            place.ant = self    # 先在place中添加self
        else:
            # BEGIN Problem Optional 2
            if place.ant.can_contain(self):
                place.ant.contain_ant(self)
            elif self.can_contain(place.ant):
                self.contain_ant(place.ant)
                place.ant=self   # place.ant must be the container !
            else: # cannot contain each other
                assert place.ant is None, 'Two ants in {0}'.format(place)
            # END Problem Optional 2
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            # queen or container (optional) or other situation
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 2
    def action(self, gamestate):
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN Problem 1
        "*** YOUR CODE HERE ***"
        gamestate.food+=1       # 每一轮 HaversterAnt都会收集一个食物
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 3
    # 对于任意类型的ThrowerAnt,都定义了max_range以及min_range
    max_range=float('inf')    # 每一类都定义最大距离
    min_range=0               # 每一类都定义最小距离,便于nearest_bee()编写
    def nearest_bee(self, beehive):
        """Return the nearest Bee in a Place that is not the HIVE (beehive), connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN Problem 3 and 4
        def check_the_distance(place1,place2):  # 认为 place2-place1 > 0
            """ 计算place1与place2的距离 """
            distance=0
            while True:
                if place1==place2:
                    return distance
                distance,place1=distance+1,place1.entrance

        place = self.place
        while place!=beehive:
            if place.bees:
                if self.min_range<=check_the_distance(self.place,place)<=self.max_range:
                    return rANTdom_else_none(place.bees)
            place=place.entrance
        return None                                   # 如果都没有找到 bee,则返回 None
        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the TARGET Bee, reducing its armor."""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee(gamestate.beehive))

def rANTdom_else_none(s):
    """Return a random element of sequence S, or return None if S is empty."""
    assert isinstance(s, list), "rANTdom_else_none's argument should be a list but was a %s" % type(s).__name__
    if s:
        return random.choice(s)

##############
# Extensions #
##############

class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    max_range=3
    min_range=0
    # BEGIN Problem 4
    implemented =True   # Change to True to view in the GUI

    # END Problem 4

class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    min_range=5
    max_range=float('inf')
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI

    # END Problem 4

class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI
    # END Problem 5

    def __init__(self, armor=3):   # 默认缺省参数
        """Create an Ant with an ARMOR quantity."""
        Ant.__init__(self, armor)

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the FireAnt from its place if it
        has no armor remaining.

        Make sure to damage each bee in the current place, and apply the bonus
        if the fire ant dies.
        """
        # BEGIN Problem 5
        "*** YOUR CODE HERE ***"
        list_of_bees=self.place.bees.copy()
        for bee in list_of_bees:      # 在循环的时候尽量不要改变可变对象,否则有可能会跳过某些元素,因此需要copy()一份
            bee.reduce_armor(amount)  # 注:只要调用该接口即可,reduce_armor()中包含有

        if self.armor-amount <= 0:
            list_of_bees=self.place.bees.copy()
            for bee in list_of_bees:
                bee.reduce_armor(self.damage)
        # 为了保持self与place的关系,智能最后再删除self
        Ant.reduce_armor(self, amount)
        # END Problem 5

class HungryAnt(Ant):
    """HungryAnt will take three turns to digest a Bee in its place.
    While digesting, the HungryAnt can't eat another Bee.
    """
    name = 'Hungry'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 6
    implemented = True   # Change to True to view in the GUI
    time_to_digest=3             # 需要消化的轮数
    # END Problem 6
    def __init__(self, armor=1):
        # BEGIN Problem 6
        "*** YOUR CODE HERE ***"
        self.digesting = 0  # default is 0,since it haven't eaten anything at the beginning
        Ant.__init__(self,armor)
        # END Problem 6

    def eat_bee(self, bee):
        """ 吃掉一个bee """
        # BEGIN Problem 6
        "*** YOUR CODE HERE ***"
        bee.reduce_armor(bee.armor)
        self.digesting=self.time_to_digest
        # END Problem 6

    def action(self, gamestate):   # 为了保持调用action时的一致性
        # BEGIN Problem 6
        "*** YOUR CODE HERE ***"
        if self.digesting:
            self.digesting-=1
        else:
            bee=rANTdom_else_none(self.place.bees)  # 从当前格子中随机选择一个bee
            if bee:
                self.eat_bee(bee)
        # END Problem 6



# BEGIN Problem 7
class WallAnt(Ant):
    """ 实现单纯用来防御的墙蚁 """
    name='Wall'     # The WallAnt class
    food_cost = 4   # 类属性
    implemented = True
    def __init__(self,armor=4):     # armor为实例属性,因为每一个实例的armor会各有不同
        Ant.__init__(self,armor)    # 调用Ant的__init__()接口

# END Problem 7


class Water(Place):
    """
    继 hive,place后的第三种地方:Water
    Water is a place that can only hold watersafe insects.
    """
    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not watersafe, reduce
        its armor to 0."""
        # BEGIN Problem 8
        "*** YOUR CODE HERE ***"
        Place.add_insect(self,insect)  # 对于Place类来说,add_insect()相当于是函数,不是Method=>故不会自动传入self
        if not insect.is_watersafe:    # 如果该类怕水,则先add再移除
            insect.reduce_armor(insect.armor)
        # END Problem 8

# BEGIN Problem 9
class ScubaThrower(ThrowerAnt):
    """ A kind of ant that is water safe ! """
    name='Scuba'
    food_cost = 6
    is_watersafe = True
    implemented = True
# The ScubaThrower class
# END Problem 9


# BEGIN Problem EC
class QueenAnt(ScubaThrower):  # You should change this line
# END Problem EC
    """The Queen of the colony. The game is over if a bee enters her place."""

    name = 'Queen'
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC
    implemented = True   # Change to True to view in the GUI
    num_of_queens = 0    # 记录蚁后的数量,只有数量为0时才是真正的蚁后

    def __init__(self, armor=1):
        # BEGIN Problem EC
        "*** YOUR CODE HERE ***"
        if QueenAnt.num_of_queens == 0:
            QueenAnt.num_of_queens+=1
            self.is_queen = True    # 蚁后的属性,True才是真正的 queen
        else:
            self.is_queen = False
        ScubaThrower.__init__(self,armor)
        # END Problem EC

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.

        Impostor queens do only one thing: reduce their own armor to 0.
        """
        # BEGIN Problem EC
        "*** YOUR CODE HERE ***"
        if not self.is_queen:    # 如果是假的蚁后,则在action中将生命值减小至0
            self.reduce_armor(self.armor)
            return

        ScubaThrower.action(self,gamestate)   # 从ThrowerAnt处继承
        # 将queen后的ant的damage都翻成2倍
        place=self.place.exit
        while place!=None:
            if place.ant:
                if place.ant.double_damage==False:
                    place.ant.double_damage,place.ant.damage=True,2*place.ant.damage
            place=place.exit
        # END Problem EC

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and if the True QueenAnt has no armor
        remaining, signal the end of the game.
        """
        # BEGIN Problem EC
        "*** YOUR CODE HERE ***"
        # inheit from the class Insect
        ScubaThrower.reduce_armor(self,amount)
        # if the queen is killed, then the bees win
        if self.armor<=0 and self.is_queen:
            bees_win()
        # END Problem EC
    def remove_from(self, place):
        if self.is_queen:      # queen不能被remove
            return
        else:
            ScubaThrower.remove_from(self,place)

class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = False

    def __init__(self):
        Ant.__init__(self, 0)

class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    is_watersafe=True
    scared=False
    change_direction=False
    def sting(self, ant):
        """Attack an ANT, reducing its armor by 1."""
        ant.reduce_armor(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        # BEGIN Problem Optional
        if self.place.ant is not None:   # if Ant -> NinjaAnt
            return self.place.ant.blocks_path
        return False
        # END Problem Optional

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        destination = self.place.exit
        # Extra credit: Special handling for bee direction
        # BEGIN EC
        "*** YOUR CODE HERE ***"
        if self.change_direction:
            destination=self.place.entrance
        # END EC
        if self.blocked():
            self.sting(self.place.ant)
        elif self.armor > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        Insect.add_to(self, place)

    def remove_from(self, place):
        place.bees.remove(self)     # 从place的bees列表中删除self
        Insect.remove_from(self, place)

############
# Optional #
############

class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place.
    This class is optional.
    """

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    blocks_path = False
    # BEGIN Problem Optional 1
    implemented = True   # Change to True to view in the GUI
    # END Problem Optional 1

    def action(self, gamestate):
        # BEGIN Problem Optional 1
        "*** YOUR CODE HERE ***"
        place=self.place
        bees=place.bees.copy()
        for bee in bees:
            bee.reduce_armor(self.damage)   # 注:只会在place.bees[]中删除bee对象,故在bees中遍历不会漏掉任何对象

        # END Problem Optional 1

class ContainerAnt(Ant):    # BodyguardAnt以及 TankAnt的超类
    def __init__(self, *args, **kwargs):
        Ant.__init__(self, *args, **kwargs)   # 同时支持位置参数(1,2,3)以及关键字参数{'1':1,'2':2}
        self.contained_ant = None

    def can_contain(self, other):
        """ juedge whether the containerAnt can contain another ant """
        # BEGIN Problem Optional 2
        "*** YOUR CODE HERE ***"
        return not self.contained_ant and not isinstance(other,ContainerAnt)  # 注:利用isinstance()判断类别
        # END Problem Optional 2

    def contain_ant(self, ant):
        """ pass the argu to set the contained_ant attribute """
        # BEGIN Problem Optional 2
        "*** YOUR CODE HERE ***"
        self.contained_ant=ant
        # END Problem Optional 2

    def remove_ant(self, ant):
        if self.contained_ant is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.contained_ant = None

    def remove_from(self, place):
        # Special handling for container ants (this is optional)
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            place.ant = place.ant.contained_ant
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN Optional 2
        "*** YOUR CODE HERE ***"
        if self.contained_ant:   # if contains ant, then perform the contained ant's action
            self.contained_ant.action(gamestate)
        # END Optional 2

class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants."""

    name = 'Bodyguard'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Optional 2
    implemented = True
    # Change to True to view in the GUI
    def __init__(self,armor=2):
        ContainerAnt.__init__(self,armor)
    # END Optional 2

class TankAnt(ContainerAnt):
    """TankAnt provides both offensive and defensive capabilities."""

    name = 'Tank'
    damage = 1
    food_cost = 6
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem Optional 3
    implemented = True   # Change to True to view in the GUI
    # END Problem Optional 3

    def __init__(self, armor=2):
        ContainerAnt.__init__(self, armor)

    def action(self, gamestate): # 重写了action
        # BEGIN Problem Optional 3
        "*** YOUR CODE HERE ***"
        bees=self.place.bees[:] # 全切片复制
        for bee in bees:
            bee.reduce_armor(self.damage)
        if self.contained_ant:
            self.contained_ant.action(gamestate)
        # END Problem Optional 3
############
# Statuses #
############

def make_slow(action, bee):
    """
    Return a new action method that calls ACTION every other turn.
    action -- An action method of some Bee
    实现了Bee的另一种action
    """
    # BEGIN Problem Optional 4
    "*** YOUR CODE HERE ***"
    def new_action(gamestate):
        if gamestate.time%2==0:  # even
            action(gamestate)
    return new_action            # 返回的是一个action
    # END Problem Optional 4

def make_scare(action, bee):
    """Return a new action method that makes the bee go backwards.
    action -- An action method of some Bee
    实现了Bee的另一种action
    """
    # BEGIN Problem Optional 4
    "*** YOUR CODE HERE ***"
    def new_action(gamestate):
        #注:因为将函数绑定为对象/类的方法时,self参数不会自动绑定,
        #所以为了与原先的bee.action(gamestate)保持一致,参数只设定为一参的gamestate即可
        bee.scared = True  # scared的bee不会再被scared
        bee.change_direction = True
        action(gamestate)

    return new_action
    # END Problem Optional 4

def apply_status(status, bee, length):
    """
    Apply a status to a BEE that lasts for LENGTH turns.
    依据 length 重新绑定到Bee.action上
    注意:函数的绑定不能绑定第一个self参数
    """
    # BEGIN Problem Optional 4
    "*** YOUR CODE HERE ***"
    old_action = bee.action               # old_action可能也是一个replace_action(),故可以实现链式action的传递
    new_action = status(old_action, bee)  # 返回上面构造的new_action

    def replace_action(gamestate):
        nonlocal length
        if length > 0:
            new_action(gamestate)   # 执行一次新方法
            length -= 1
        else:
            if bee.scared:          # 如果已经scared则不会再转向
                bee.change_direction = False
            old_action(gamestate)

    bee.action=replace_action   # core:重新绑定bee的action方法
    # END Problem Optional 4


class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 4
    # BEGIN Problem Optional 4
    implemented = True   # Change to True to view in the GUI
    # END Problem Optional 4

    def throw_at(self, target):    # 从ThrowerAnt.action()处传回throw_at()
        if target:
            apply_status(make_slow, target, 3)   # 只是把 make_slow这个 status(实际上是func)传给 target


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = 'Scary'
    food_cost = 6
    # BEGIN Problem Optional 4
    implemented = True   # Change to True to view in the GUI
    # END Problem Optional 4

    def throw_at(self, target):
        # BEGIN Problem Optional 4
        "*** YOUR CODE HERE ***"
        if target and not target.scared:               # target.scared用于判断该蜜蜂是否有被scare过
            apply_status(make_scare,target,2)   # 先前的throw改变bee的armor,这里的throw改变bee的action=>方法的重新绑定
        # END Problem Optional 4

class LaserAnt(ThrowerAnt):
    # This class is optional. Only one test is provided for this class.

    name = 'Laser'
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem Optional 5
    implemented = True   # Change to True to view in the GUI
    damage = 2
    # END Problem Optional 5

    def __init__(self, armor=1):
        ThrowerAnt.__init__(self, armor)
        self.insects_shot = 0

    def insects_in_front(self, beehive):
        """ 形成每一只昆虫以及LaserAnt到该昆虫之间的距离 """
        # BEGIN Problem Optional 5
        insects_and_distances={}
        place,distance=self.place,0
        while True:
            if place.ant and not isinstance(place.ant,LaserAnt):
                insects_and_distances[place.ant]=distance
            for bee in place.bees:   # None自动不进行
                insects_and_distances[bee]=distance
            if place==beehive:
                break
            place,distance=place.entrance,distance+1
        return insects_and_distances
        # END Problem Optional 5

    def calculate_damage(self, distance):
        # BEGIN Problem Optional 5
        damage=self.damage-0.05*self.insects_shot
        weakened_damage=damage-0.2*distance
        if weakened_damage > 0:
            return weakened_damage
        else:
            return 0
        # END Problem Optional 5

    def action(self, gamestate):  # 每一次行动
        insects_and_distances = self.insects_in_front(gamestate.beehive)   # 首先返回一个insects_and_distances的字典
        for insect, distance in insects_and_distances.items():             # 对于其中每一个昆虫
            damage = self.calculate_damage(distance)                       # 计算laserAnt对其的伤害
            insect.reduce_armor(damage)
            if damage:
                self.insects_shot += 1





##################
# Bees Extension #
##################

class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2

class Hornet(Bee):
    """Class of bee that is capable of taking two actions per turn, although
    its overall damage output is lower. Immune to statuses.
    """
    name = 'Hornet'
    damage = 0.25

    def action(self, gamestate):
        for i in range(2):
            if self.armor > 0:
                super().action(gamestate)

    def __setattr__(self, name, value):
        if name != 'action':
            object.__setattr__(self, name, value)

class NinjaBee(Bee):
    """A Bee that cannot be blocked. Is capable of moving past all defenses to
    assassinate the Queen.
    """
    name = 'NinjaBee'

    def blocked(self):
        return False

class Boss(Wasp, Hornet):
    """The leader of the bees. Combines the high damage of the Wasp along with
    status immunity of Hornets. Damage to the boss is capped up to 8
    damage by a single attack.
    """
    name = 'Boss'
    damage_cap = 8
    action = Wasp.action

    def reduce_armor(self, amount):
        super().reduce_armor(self.damage_modifier(amount))

    def damage_modifier(self, amount):
        return amount * self.damage_cap/(self.damage_cap + amount)

class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)


class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, strategy, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        beehive -- a Hive full of bees
        ant_types -- a list of ant constructors
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony."""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []
        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place, self.dimensions[0], self.dimensions[1])

    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        num_bees = len(self.bees)
        try:
            while True:
                self.strategy(self)                 # Ants deploy
                self.beehive.strategy(self)         # Bees invade
                for ant in self.ants:               # Ants take actions
                    if ant.armor > 0:
                        ant.action(self)
                for bee in self.active_bees[:]:     # Bees take actions
                    if bee.armor > 0:
                        bee.action(self)
                    if bee.armor <= 0:
                        num_bees -= 1
                        self.active_bees.remove(bee)
                if num_bees == 0:
                    raise AntsWinException()
                self.time += 1
        except AntsWinException:
            print('All bees are vanquished. You win!')
            return True
        except BeesWinException:
            print('The ant queen has perished. Please try again.')
            return False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        constructor = self.ant_types[ant_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + ant_type_name)
        else:
            ant = constructor()
            self.places[place_name].add_insect(ant)
            self.food -= constructor.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status

class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a BeesWinException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise BeesWinException()

def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()

def bees_win():
    """Signal that Bees win."""
    raise BeesWinException()

def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]

class GameOverException(Exception):
    """Base game over Exception."""
    pass

class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass

class BeesWinException(GameOverException):
    """Exception to signal that the bees win."""
    pass

def interactive_strategy(gamestate):
    """A strategy that starts an interactive session and lets the user make
    changes to the gamestate.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking
    gamestate.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('gamestate: ' + str(gamestate))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

###########
# Layouts #
###########

def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)

def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_armor, time, count):
        """Add a wave at time with count Bees that have the specified armor."""
        bees = [bee_type(bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]