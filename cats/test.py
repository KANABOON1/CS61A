from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime

def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    paragraphs=[paragraph for paragraph in paragraphs if select(paragraph)]
    if k<len(paragraphs):
        return paragraphs[k]
    else:
        return ''

"""ps = ['short', 'really long', 'tiny']
select=lambda p: len(p) <= 5
print(choose(ps,select,1))"""

def about(topic):
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph):
        paragraph=remove_punctuation(paragraph)
        paragraph = lower(paragraph)
        words_in_paragraph=split(paragraph)
        for word in topic:
            if word in words_in_paragraph:
                return True
        return False
    return select
"""about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
print(choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 0))"""
def accuracy(typed, reference):
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    sum = 0
    accurate = 0.0
    for index in range(min(len(typed_words), len(reference_words))):
        if typed_words[index] == reference_words[index]:
            sum += 1
    if len(typed_words):
        accurate = sum / len(typed_words) * 100
    return accurate
    # END PROBLEM 3

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    else:
        diff_index=[diff_function(user_word,eva,limit) for eva in valid_words]
        min_diff=min(diff_index)
        if min_diff>limit:
            return user_word
        min_index=diff_index.index(min_diff)
        return valid_words[min_index]
def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit == -1:  # 有关 limit的 base case,当差异>limit时,返回值比limit大1
        return 0
    if len(start) == 0 or len(goal) == 0:  # base case
        return abs(len(start) - len(goal))
    elif start[0] == goal[0]:
        return shifty_shifts(start[1:], goal[1:], limit)
    else:  # note:需要考虑参数limit,返回值比limit大1
        return shifty_shifts(start[1:], goal[1:], limit - 1) + 1
def pawssible_patches(start, goal, limit):
    """
    A diff function that computes the edit distance from START to GOAL.
    cases:start[i]!=goal[i]:
    1.start[i] not in goal:remove
    2.start[i] in goal:add
    caiteus=>kittens:kiteus(remove)=>kitteus(add)=>kittens(sub) eus<=>tens
    """

    if limit < 0:
        return 0
    elif start=='' or goal=='':
        return len(start)+len(goal)
    elif start[0]==goal[0]:
        return pawssible_patches(start[1:],goal[1:],limit)
    else:
        add_diff=1+pawssible_patches(start,goal[1:],limit-1)
        remove_diff=1+pawssible_patches(start[1:],goal,limit-1)
        substitue_diff=1+pawssible_patches(start[1:],goal[1:],limit-1)
        return min(add_diff,remove_diff,substitue_diff)
def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    index=0
    for index in range(len(typed)):
        if typed[index]!=prompt[index]:
            break
    progress=index/len(prompt)
    disc_progress={'id':user_id,'progress':progress}
    send(disc_progress)
    return progress
prompt = ['I', 'have', 'begun', 'to', 'type']
print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
print(report_progress(['I', 'begun'], prompt, 2, print_progress))