import shortuuid
import py_trees as ptree

from antlr4 import *

if "." in __name__:
    from .ptmlListener import ptmlListener
    from .ptmlParser import ptmlParser
else:
    from ptmlListener import ptmlListener
    from ptmlParser import ptmlParser

short_uuid = lambda: shortuuid.ShortUUID().random(length=8)


class ptmlTranslator(ptmlListener):
    """Translate the ptml language to BT.

    Args:
        ptmlListener (_type_): _description_
    """

    def __init__(self, scene, behaviour_lib_path) -> None:
        super().__init__()
        self.bt_root = None
        self.stack = []
        self.scene = scene
        self.behaviour_lib_path = behaviour_lib_path

    # Enter a parse tree produced by ptmlParser#root.
    def enterRoot(self, ctx: ptmlParser.RootContext):
        pass

    # Exit a parse tree produced by ptmlParser#root.
    def exitRoot(self, ctx: ptmlParser.RootContext):
        pass

    # Enter a parse tree produced by ptmlParser#tree.
    def enterTree(self, ctx: ptmlParser.TreeContext):
        type = str(ctx.internal_node().children[0])

        match type:
            case "sequence":
                tag = "sequence_" + short_uuid()
                node = ptree.composites.Sequence(name=tag, memory=False)
            case "selector":
                tag = "selector_" + short_uuid()
                node = ptree.composites.Selector(name=tag, memory=False)
            case "parallel":
                tag = "parallel_" + short_uuid()
                # threshold = int(ctx.children[1])
                # default policy, success on all
                node = ptree.composites.Parallel(
                    name=tag, policy=ptree.common.ParallelPolicy.SuccessOnAll
                )
            case _:
                raise TypeError("Unknown Composite Type: {}".format(type))

        self.stack.append(node)

    # Exit a parse tree produced by ptmlParser#tree.
    def exitTree(self, ctx: ptmlParser.TreeContext):
        if len(self.stack) >= 2:
            child = self.stack.pop()
            self.stack[-1].add_child(child)
        else:
            self.bt_root = self.stack[0]

    # Enter a parse tree produced by ptmlParser#internal_node.
    def enterInternal_node(self, ctx: ptmlParser.Internal_nodeContext):
        pass

    # Exit a parse tree produced by ptmlParser#internal_node.
    def exitInternal_node(self, ctx: ptmlParser.Internal_nodeContext):
        pass

    # Enter a parse tree produced by ptmlParser#action_sign.
    def enterAction_sign(self, ctx: ptmlParser.Action_signContext):
        # cond / task
        node_type = str(ctx.children[0])
        name = str(ctx.Names())

        # if have params
        args = []
        if len(ctx.children) > 4:
            params = ctx.action_parm()

            for i in params.children:
                if isinstance(i, ptmlParser.BooleanContext):
                    args.append(str(i.children[0]))
                else:
                    args.append(str(i))

        args = "".join(args)

        import sys

        sys.path.append(self.behaviour_lib_path)

        exec("from {} import {}".format(name, name))
        #
        tag = "cond_" + short_uuid() if node_type == "cond" else "task_" + short_uuid()

        node = eval(
            "{}('{}', scene, {})".format(name, tag, args), {"scene": self.scene, **locals()}
        )

        # connect
        self.stack[-1].add_child(node)

    # Exit a parse tree produced by ptmlParser#action_sign.
    def exitAction_sign(self, ctx: ptmlParser.Action_signContext):
        pass

    # Enter a parse tree produced by ptmlParser#action_parm.
    def enterAction_parm(self, ctx: ptmlParser.Action_parmContext):
        pass

    # Exit a parse tree produced by ptmlParser#action_parm.
    def exitAction_parm(self, ctx: ptmlParser.Action_parmContext):
        pass

    # Enter a parse tree produced by ptmlParser#boolean.
    def enterBoolean(self, ctx: ptmlParser.BooleanContext):
        pass

    # Exit a parse tree produced by ptmlParser#boolean.
    def exitBoolean(self, ctx: ptmlParser.BooleanContext):
        pass