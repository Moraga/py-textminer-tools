def number(n):
    if int == type(n):
        return '{:,}'.format(n).replace(',', '.')
    else:
        a, b = '{:,.2f}'.format(n).split('.')
        return '{},{}'.format(a.replace(',', '.'), b)


def money(n):
    return 'R$ ' + number(n + .0)