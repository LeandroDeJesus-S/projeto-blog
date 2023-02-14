from django import template

register = template.Library()


@register.filter('plural_comments')
def plural_coments(coment_nums):
    try:
        coment_nums = int(coment_nums)
        if coment_nums == 0:
            return 'Nenhum comentário'
        elif coment_nums == 1:
            return f'{coment_nums} comentário'
        else:
            return f'{coment_nums} comentários'
    except Exception as error:
        return f'{coment_nums} comentário(s)'
    