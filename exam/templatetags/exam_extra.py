
from django import template
register = template.Library()

@register.filter()
def your_choice(choice, ques):
    c = choice.get(ques=ques)

    if str(c) == ques.correct_answer:
        return "Correct"
    else:
        return c

@register.filter()
def sum(score_card):
    x = 0
    for score_card in score_card:
        x += score_card.score
        print(score_card.score)
        return str(x)
