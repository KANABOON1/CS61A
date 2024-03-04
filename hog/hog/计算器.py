"""This is for calculating this turn's score,
 including pig_out,free_bacon rules"""
from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact
GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
FIRST_101_DIGITS_OF_PI = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
def roll_dice(num_rolls, dice=six_sided):
    """掷色子，num_rolls:掷的次数;dice:提供色子模型"""
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    def make_up(times):
        """补全因提早return导致的dice()调用次数减少"""
        while times<num_rolls:
            dice()
            times+=1
    i,score_turn,counter=0,0,0
    while i<num_rolls:
        sc=dice()
        i, score_turn = i + 1, score_turn + sc
        if sc==1:
            make_up(i)
            return 1
    return score_turn
    # END PROBLEM 1
"""dice=make_test_dice(1,2,3)
#注：1.仅仅调用一次make_test_dice()中的主部分,从而实现每次调用的次序的继承
#   2.每次不能都调用主函数make_test_dice()，否则主函数每次都会执行,则index不能继承
point1=roll_dice(1,dice)
point2=dice()
#dice()的返回值是继承的
print(point1,point2)"""
def free_bacon(score):
    """free_bacon:若不抛掷色子，则根据opponent_score计算本轮该player的得分"""
    assert score < 100, 'The game should be over.'
    pi = FIRST_101_DIGITS_OF_PI

    # Trim pi to only (score + 1) digit(s)
    # BEGIN PROBLEM 2
    pi=pi//pow(10,101-score-1)
    # END PROBLEM 2

    return pi % 10 + 3


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """根据num_rolls分为两种情况:1.num_rolls==0:按照free_bacon rule calculate score
                              2.num_rolls!=0:按照roll_dice rule正常计算本轮得分"""
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls==0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls,dice)
    # END PROBLEM 3

def extra_turn(player_score, opponent_score):
    """判断是否需要进行一次extra_turn"""
    return (pig_pass(player_score, opponent_score) or
            swine_align(player_score, opponent_score))

def swine_align(player_score, opponent_score):
    """检测函数:在当前player的得分计算完毕后,判断当前两名选手的score的gcd,若gcd>10,则current player再抛掷一次:another turn
    """
    # BEGIN PROBLEM 4a
    def judge():
        gcd = 1
        for i in range(2, min(player_score, opponent_score) + 1):
            if not player_score % i and not opponent_score % i:
                gcd = i
            i += 1
        return gcd

    if judge() >= 10:
        return True
    else:
        return False
    # END PROBLEM 4a
def pig_pass(player_score, opponent_score):
    """检测函数:pig_pass:if the current player's score is less than his opponent and the different between them is less than three,do another turn
    """
    # BEGIN PROBLEM 4b
    if player_score<opponent_score and player_score>opponent_score-3:
        return True
    else:
        return False

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1."""
    return 1 - who
def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence

def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """统筹整个游戏，最后返回score0,score1
    """
    who = 0
    def cal(score):
        if who == 0:
            return take_turn(strategy0(score, score1), score1, dice)
        else:
            return take_turn(strategy1(score, score0), score0, dice)
    def this_turn(score):
        if who == 0:
            return extra_turn(score, score1)
        else:
            return extra_turn(score, score0)
    def get():
        nonlocal who
        if who==0:
            score=score0
        else:
            score=score1
        score+=cal(score)
        if score >= goal:
            return score
        while this_turn(score):
            score+=cal(score)
            if score>=goal:
                return score
        who=other(who)
        return score
    while 1:
        score0=get()
        if score0>=goal:
            break
        score1=get()
        if score1>=goal:
            break
    return score0,score1
