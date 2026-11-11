

from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, Not, Or, And, to_dnf


# goal = "(On_Coffee_Bar | On_Yogur_Bar) & At_Robot_Bar"
# goal = "On(Coffee,WaterTable),On(Coffee,BrightTable6)"
goal = "~ (On_Coffee_Bar | On_Yogur_Bar) & At_Robot_Bar"

goal_dnf = str(to_dnf(goal, simplify=True))
# print(goal_dnf)
goal_set=[]
if '|' in goal or '&' in goal or 'Not' in goal:
    goal_ls = goal_dnf.split("|")
    for g in goal_ls:
        g_set = set()
        g = g.replace(" ", "").replace("(", "").replace(")", "")
        g = g.split("&")
        for literal in g:
            if '_' in literal:
                first_part, rest = literal.split('_', 1)
                literal = first_part + '(' + rest
                # 添加 ')' 到末尾
                literal += ')'
                # 替换剩余的 '_' 为 ','
                literal = literal.replace('_', ',')
            g_set.add(literal)
        goal_set.append(g_set)
else:
    g_set = set()
    w = goal.split(")")
    g_set.add(w[0] + ")")
    if len(w) > 1:
        for x in w[1:]:
            if x != "":
                g_set.add(x[1:] + ")")
    goal_set.append(g_set)

# goal_set = [set(["On(Coffee,Bar)", "At(Robot,Bar)"]), set(["On(Yogurt,Bar)", "At(Robot,Bar)"])]
print(goal_set)