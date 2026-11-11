from pyparsing import infixNotation, opAssoc, Keyword, Word, alphas, ParserElement

# 启用忽略大小写的关键字
ParserElement.enablePackrat()

# 定义基础元素
variable = Word(alphas)
predicate = variable + '(' + variable + ',' + variable + ')'

# 定义逻辑运算符
and_ = Keyword("And")
or_ = Keyword("Or")
not_ = Keyword("Not")

# 由于你的表达式使用 "&" 和 "|"
and_sym = Word("&", exact=1)
or_sym = Word("|", exact=1)

# 定义逻辑表达式的语法
expr = infixNotation(predicate,
                     [
                         (not_, 1, opAssoc.RIGHT),
                         (and_sym, 2, opAssoc.LEFT, and_),
                         (or_sym, 2, opAssoc.LEFT, or_),
                     ])

# 解析示例表达式
goal = "Not(On(Yogurt,Table1)) & (On(Coffee,Table1) | On(ADMilk,Table1)) & At(Robot,Bar)"
parsed_expr = expr.parseString(goal)

# 打印解析结果
print(parsed_expr.asList())
