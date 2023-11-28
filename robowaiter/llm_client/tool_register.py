import inspect
import traceback
from copy import deepcopy
from pprint import pformat
from types import GenericAlias
from typing import get_origin, Annotated
import robowaiter.llm_client.find_obj_utils as find_obj_utils
import random
# import spacy

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = {}
# nlp = spacy.load('en_core_web_lg')


def register_tool(func: callable):
    tool_name = func.__name__
    tool_description = inspect.getdoc(func).strip()
    python_params = inspect.signature(func).parameters
    tool_params = []
    for name, param in python_params.items():
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            raise TypeError(f"Parameter `{name}` missing type annotation")
        if get_origin(annotation) != Annotated:
            raise TypeError(f"Annotation type for `{name}` must be typing.Annotated")

        typ, (description, required) = annotation.__origin__, annotation.__metadata__
        typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
        if not isinstance(description, str):
            raise TypeError(f"Description for `{name}` must be a string")
        if not isinstance(required, bool):
            raise TypeError(f"Required for `{name}` must be a bool")

        tool_params.append({
            "name": name,
            "description": description,
            "type": typ,
            "required": required
        })
    tool_def = {
        "name": tool_name,
        "description": tool_description,
        "params": tool_params
    }

    # print("[registered tool] " + pformat(tool_def))
    _TOOL_HOOKS[tool_name] = func
    _TOOL_DESCRIPTIONS[tool_name] = tool_def

    return func


def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = _TOOL_HOOKS[tool_name]
    try:
        ret = tool_call(**tool_params)
    except:
        ret = traceback.format_exc()
    return str(ret)


def get_tools() -> dict:
    return deepcopy(_TOOL_DESCRIPTIONS)


# Tool Definitions

# @register_tool
# def random_number_generator(
#         seed: Annotated[int, 'The random seed used by the generator', True],
#         range: Annotated[tuple[int, int], 'The range of the generated numbers', True],
# ) -> int:
#     """
#     Generates a random number x, s.t. range[0] <= x < range[1]
#     """
#     if not isinstance(seed, int):
#         raise TypeError("Seed must be an integer")
#     if not isinstance(range, tuple):
#         raise TypeError("Range must be a tuple")
#     if not isinstance(range[0], int) or not isinstance(range[1], int):
#         raise TypeError("Range must be a tuple of integers")
#
#     import random
#     return random.Random(seed).randint(*range)


# @register_tool
# def get_weather(
#         city_name: Annotated[str, 'The name of the city to be queried', True],
# ) -> str:
#     """
#     Get the current weather for `city_name`
#     """
#
#     if not isinstance(city_name, str):
#         raise TypeError("City name must be a string")
#
#     key_selection = {
#         "current_condition": ["temp_C", "FeelsLikeC", "humidity", "weatherDesc", "observation_time"],
#     }
#     import requests
#     try:
#         resp = requests.get(f"https://wttr.in/{city_name}?format=j1")
#         resp.raise_for_status()
#         resp = resp.json()
#         ret = {k: {_v: resp[k][0][_v] for _v in v} for k, v in key_selection.items()}
#     except:
#         import traceback
#         ret = "Error encountered while fetching weather data!\n" + traceback.format_exc()
#
#     return str(ret)


# @register_tool
# def add(
#         a: Annotated[int, '需要相加的第1个数', True],
#         b: Annotated[int, '需要相加的第2个数', True]
# ) -> int:
#     """
#     获取 `a` + `b` 的值
#     """
#
#     if (not isinstance(a, int)) or (not isinstance(b, int)):
#         raise TypeError("相加的数必须为整数")
#
#     return int(a+b)

@register_tool
def create_sub_task(
        goal: Annotated[str, '子任务需要达到的目标条件集合，例如{On(Coffee,Bar)}，{At(Robot,Table1)}，{Is(AC,Off)}', True]
) -> str:
    """
    当需要完成具身任务（如做咖啡，拿放物体，扫地，前往某位置）时，调用该函数，根据用户的提示进行意图理解，生成子任务的目标状态集合 `goal`（以一阶逻辑的形式表示），用户意图
    做一杯咖啡,则该函数的参数为 "On(Coffee,Bar)",
    前往一号桌,则该函数的参数为 "At(Robot,Table1)",
    前往二号桌,则该函数的参数为 "At(Robot,Table2)",
    打开空调,则该函数的参数为 "Is(AC,On)",
    关空调,则该函数的参数为 "Is(AC,Off)",
    打开窗帘,则该函数的参数为 "Is(Curtain,On)",
    关闭窗帘,则该函数的参数为 "Is(Curtain,Off)",
    拖地,则该函数的参数为 "Is(Floor,Clean)",
    打开大厅灯,则该函数的参数为 "Is(HallLight,On)",
    """

    return goal


@register_tool
def stop_serve(
) -> bool:
    """
    当顾客通过任何形式表示不再需要服务时，调用该函数
    """
    return True



@register_tool
def get_object_info(
        obj: Annotated[str, '需要获取位置的物体名称', True]
) -> str:
    """
    获取场景中`object`的位置信息。在询问物品位置时调用该函数，以辅助场景交互，不执行动作
    例如：
        `object`在哪里？
        哪有`object`
        哪里有`object`？
         `object`在哪里
        哪里有`object`
        `object`放在哪里
        我在哪儿能找到`object`
        你们这儿有`object`吗？
        你们这里有`object`
        你看见`object`了吗？
        `object`在你们这里吗
        `object`，你看见过吗？
    遇到上述问题时，调用该函数，并根据返回的结果回复物体位置信息，例如
    回答：
        `object`在输出的物品附近
        如果`object` 是一个地点，例如洗手间，则输出大门。
        如果`object`是咖啡，输出桌子，则咖啡在桌子上。
        如果`object`是酸奶，输出冰红茶，则酸奶在冰红茶附近。
        如果`object` 是空桌子，则输出一号桌
    """

    # 桌上有
    # `object`
    # 吗？
    # 咖啡厅里哪里有
    # `object`
    # `object`
    # 放在哪里？

    near_object = None
    # if obj == "Table":
    #     near_object = "Bar"
    if obj == "洗手间":
        near_object = "大门"
    # if obj == "空桌子":
    #     near_object = "一号桌"
    if obj in find_obj_utils.all_loc:   # object是一个地点
        mp = list(find_obj_utils.loc_map[obj])
        # near_object = random.choice(mp)
        near_object = mp
    if obj in find_obj_utils.all_obj:   # object是一个物品
        near_ls = find_obj_utils.all_loc + find_obj_utils.all_obj
        near_object = random.choices(near_ls,k=5)
    return near_object

# @register_tool
# def find_location(
#         location: Annotated[str, '客人咨询的地点', True]
# ) -> str:
#     """"
#     获取的location为英文
#     用户想找某个地点
#     """
    # near_location = None
    # query_token = nlp(location)
    # max_similarity = 0
    # similar_word = None
    # for w in find_obj_utils.all_loc_en:
    #     word_token = nlp(w)
    #     similarity = query_token.similarity(word_token)
    #
    #     if similarity > max_similarity:
    #         max_similarity = similarity
    #         similar_word = w
    # print("similarity:", max_similarity, "similar_word:", similar_word)
    # if similar_word:
    #     mp = list(find_obj_utils.loc_map_en[similar_word])
    #     near_location = random.choice(mp)
    # return near_location


@register_tool
def get_number_of_objects(
        obj: Annotated[str, '需要获取数量的物体名称', True]
) -> str:
    """
    当询问场景中的物体数量时，需要调用这个工具。
    例如询问：
        `obj`有多少？
        有多少`obj`
        你们还有`obj`
        '桌子有几张'
        `obj`还有多的吗？
        `obj`有几个
        `obj`有多少个
    这个工具用于获取场景中指定物体 `obj` 的数量，返回一个整数，不涉及到具体的执行任务。
    如果`obj`是咖啡，如果场景中有5杯咖啡，就返回 5
    如果`obj`是桌子，如果场景中有7张桌子，就返回 7
    如果`obj`是行人，如果场景中有10个顾客，就返回 10
    """


if __name__ == "__main__":
    print(dispatch_tool("get_weather", {"city_name": "beijing"}))
    print(get_tools())
