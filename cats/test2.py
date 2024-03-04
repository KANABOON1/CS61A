from cats import game, game_string, all_words, all_times, word_at, time
def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if len(start) == 0 or len(goal) == 0:  # base case
        return abs(len(start) - len(goal))
    else:
        return int(start[0]!=goal[0])+shifty_shifts(start[1:],goal[1:],limit)

def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    times=[[times_per_player[member][i+1]-times_per_player[member][i] for i in range(len(words))]
           for member in range(len(times_per_player))]
    return game(words,times)
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
    words, times = all_words(game), all_times(game)
    build=lambda word_index:[time(game,mem,word_index) for mem in range(len(times))]
    compare=[build(index) for index in range(len(words))]
    for element in range(len(compare)):
        min_ele=min(compare[element])
        position=compare[element].index(min_ele)
        fastest[position].append(word_at(game,element))
    return fastest