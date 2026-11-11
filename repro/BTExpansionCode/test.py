
# goal = "AND[NOT[On(Yogurt,Table1)],[(On(Coffee,Table1))OR(On(ADMilk,Table1))]]"
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, Not, Or, And, to_dnf
# 定义逻辑变量
# YogurtOnTable1 = symbols('On(Yogurt,Table1)')
# CoffeeOnTable1 = symbols('On(Coffee,Table1)')
# ADMilkOnTable1 = symbols('On(ADMilk,Table1)')

On_Yogurt_Table1, On_Coffee_Table1, On_ADMilk_Table1 = symbols('On_Yogurt_Table1 On_Coffee_Table1 On_ADMilk_Table1')
# YogurtOnTable1, CoffeeOnTable1, ADMilkOnTable1 = symbols('YogurtOnTable1 CoffeeOnTable1 ADMilkOnTable1')
# YogurtOnTable1 = symbols('On[Yogurt,Table1]')
# CoffeeOnTable1 = symbols('On(Coffee,Table1)')
# ADMilkOnTable1 = symbols('On(ADMilk,Table1)')

# 构造原始表达式
# expression = (And(Not(YogurtOnTable1), Or(CoffeeOnTable1, ADMilkOnTable1)))
# 定义字符串形式的逻辑表达式
# goal = "Not(On[Yogurt,Table1]) & (On]Coffee,Table1) | On(ADMilk,Table1))"
# expr_str = "Not(YogurtOnTable1) & (CoffeeOnTable1 | ADMilkOnTable1)"

# expr_str = "Not(On(Yogurt,Table1)) & (On(Coffee,Table1) | On(ADMilk,Table1))"
expr_str = "Not(On_Yogurt_Table1) & (On_Coffee_Table1 | On_ADMilk_Table1 & At_Robot_Bar)"
# expr_str = "Not(YogurtOnTable1) & (CoffeeOnTable1 | ADMilkOnTable1 & Not(YogurtOnTable1) )"

# 将字符串解析为 SymPy 表达式
expr = parse_expr(expr_str, local_dict={
    'On(Yogurt,Table1)': On_Yogurt_Table1,
    'On(Coffee,Table1)': On_Coffee_Table1,
    'On(ADMilk,Table1)': On_ADMilk_Table1
})


dnf_expr = to_dnf(expr, simplify=True)
print(dnf_expr)
# 转换为析取范式
# dnf_expression = to_dnf(expression, simplify=True)
# print(dnf_expression)
