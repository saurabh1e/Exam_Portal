
from django import template
register = template.Library()
from django.core.exceptions import ObjectDoesNotExist

@register.filter()
def your_choice(choice, ques):
    if choice:
        c = choice.get(ques=ques)
        return str(c.ans)

@register.filter()
def sum(score_card):
    x = 0
    for score_card in score_card:
        x += score_card.score
        print(score_card.score)
        return str(x)
