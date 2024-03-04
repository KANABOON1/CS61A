"""Typing test implementation"""
"""
cats:一个关于打字的project.
"""
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########
"""
项目Part A:
基础功能的实现
1.choose():按照select()选择paragraphs中符合要求的paragraph,并构建一个列表.
2.about():返回的实际上是一个含有topic的select()函数,并给到choose()中作为select()函数参数,选择含有topic中词汇的paragraph.
3.accuracy():比较输入句子的精准度.
4.wpm():计算每次每分钟输入的单词数量,以每个单词为5个字符作为估算,并且其中包含了空格.
5.在GUI中的作用:a.choose()与about()返回的select()配合,筛选出含有核心词(topics)的paragraphs.
              b.accuracy()用于计算敲单词的精准度,每打一个空格调用一次.
              c.wpm()用于计算wpm(每分钟敲出的单词数),每打一个空格调用一次.
"""

def choose(paragraphs, select, k):
    """
    Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    paragraphs=[paragraph for paragraph in paragraphs if select(paragraph)]
    #列表推导式：简洁.
    if k<len(paragraphs):
        return paragraphs[k]
    else:
        return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph):#paragraph仅仅是传值.
        """
        该select()函数判断某一段paragraph是否符合要求,适用于choose()中的select()函数
        判断paragraph是否有topic中的单词.
        """
        paragraph=remove_punctuation(paragraph)#将paragraph中的标点符号全部去掉.
        paragraph=lower(paragraph)#将paragraph中的单词全部转为小写.
        words_in_paragraph=split(paragraph)#将paragraph中的单词依次存入words_in_paragraph列表.
        for word in topic:
            if word in words_in_paragraph:
                return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """
    计算打出的单词的精准度,以空格为分隔符,每敲完一个空格计算调用一次.
    Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    sum=0
    accurate=0.0
    for index in range(min(len(typed_words),len(reference_words))):
        if typed_words[index]==reference_words[index]:
            sum+=1
    if len(typed_words):
        accurate=sum/len(typed_words)*100
    return accurate
    # END PROBLEM 3


def wpm(typed, elapsed):
    """
    计算每分钟敲出的words数量.
    Return the words-per-minute (WPM) of the TYPED string.
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed)/5)*(60/elapsed)
    # END PROBLEM 4

###########
# Phase 2 #
###########
"""
项目Part B:
增加autocorrect功能
1.先建立general的autocorrect()函数,返回的是valid_words列表中的与user_word差异最小(根据diff_function判定)的单词.
2.shifty_shifts():从index==0开始计算有多少字符需要被替换=>用于autocorrect中的diff_function.
3.pawssible_patches():计算最小的改正步骤.
4.在GUI中的作用:autocorrect()会依据shifty_shifts()/pawssible_patches()自动改正单词.
"""
def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    else:
        diff_index=[diff_function(user_word,eva,limit) for eva in valid_words]#量化valid_word中每个单词与user_word的差异
        min_diff=min(diff_index)#列表聚合:min(返回的是最先的一个
        if min_diff>limit:
            return user_word
        min_index=diff_index.index(min_diff)
        #注:列表聚合:列表的索引元素下标的操作:list.index()即可返回列表中相应的最前的元素的下标.
        return valid_words[min_index]
    # END PROBLEM 5

def shifty_shifts(start, goal, limit):
    """
    递归中limit的处理,让limit也参与递归.
    基本的处理思路还是 recursive faith of leap.
    A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit < 0: # base case
        # 有关 limit的 base case,当差异>limit时,返回值比limit大
        # minimize the computation to do:如果差异已经大于limit,则不需要继续做下去.
        return 0
    if len(start) == 0 or len(goal) == 0:  # base case
        return abs(len(start) - len(goal))
    elif start[0] == goal[0]:
        return shifty_shifts(start[1:], goal[1:], limit)
    else:  # note:需要考虑参数limit,返回值比limit大1
        return shifty_shifts(start[1:], goal[1:], limit - 1) + 1
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """
    A diff function that computes the edit distance from START to GOAL.
    注:1.不局限与关注这一位应该如何处理，而是通过依次计算每一种处理办法对应的步数,然后取得最小值.
      2.递归一定要弄清主函数的用途,因为递归时还需再次调用主函数.
    """
    if limit < 0: # base case1
        return 0
    elif start == '' or goal == '': # base case2
        return len(start) + len(goal)
    elif start[0] == goal[0]:
        return pawssible_patches(start[1:], goal[1:], limit)
    else:
        #枚举三种计算方法所需要的步骤,不局限于讨论哪一步是正确的.
        add_diff = 1 + pawssible_patches(start, goal[1:], limit - 1)
        remove_diff = 1 + pawssible_patches(start[1:], goal, limit - 1)
        substitue_diff = 1 + pawssible_patches(start[1:], goal[1:], limit - 1)
        return min(add_diff, remove_diff, substitue_diff)

def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########
"""
项目 Part C:
1.report_progress():玩家每次敲完一个单词就会调用该函数,传给multiplayer_server.
2.time_per_word():计算每一个player敲完每一个words中的单词所用的时间,并且返回一个数据类型game(words,times)
3.fastest_words():计算每一个玩家最快敲的单词,并返回一个list of lists形式的单词集合.
4.在GUI中的作用:实现多人游戏
"""
def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    lenth=0
    for i in range(len(typed)):
        if typed[i]==prompt[i]:
            lenth+=1
        else:
            break
    progress = lenth / len(prompt)
    dic_progress = {'id': user_id, 'progress': progress} #dic_progress 是一个字典,
    send(dic_progress) #send a program report to the multiplayer server
    return progress
    # END PROBLEM 8

def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """
    构造已有数据类型game需要的参数times:嵌套的列表推导式.
    Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    build=lambda member:[times_per_player[member][i+1]-times_per_player[member][i] for i in range(len(words))]
    times=[build(member) for member in range(len(times_per_player))]
    #嵌套的列表推导式,本质上还是将member带入前面的函数Build中
    return game(words,times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10

    fastest=[[] for member in range(len(all_times(game)))]#构建长度为len(all_times(game))的列表.
    words,times=all_words(game),all_times(game)
    for i in range(len(words)):
        #使用二重循环分别计算每一个单词对应的最短时间.
        mem,min_time=0,time(game,0,i)
        for j in range(1,len(times)):
            if time(game,j,i) < min_time:
                mem,min_time=j,time(game,j,i)
        fastest[mem].append(word_at(game,i))
    return fastest

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)