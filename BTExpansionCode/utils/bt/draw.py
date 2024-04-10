
##############################################################################
# Imports
##############################################################################

import os
import typing
import uuid

import pydot
from py_trees import behaviour
from py_trees import blackboard
from py_trees import common
from py_trees import composites
from py_trees import decorators
from py_trees import utilities

COMPOSITE_NODE_SIZE = 0.01


def dot_tree(
        root: behaviour.Behaviour,
        visibility_level: common.VisibilityLevel = common.VisibilityLevel.DETAIL,
        collapse_decorators: bool = False,
        with_blackboard_variables: bool = False,
        with_qualified_names: bool = False):
    """
    Paint your tree on a pydot graph.

    .. seealso:: :py:func:`render_dot_tree`.

    Args:
        root (:class:`~py_trees.behaviour.Behaviour`): the root of a tree, or subtree
        visibility_level (optional): collapse subtrees at or under this level
        collapse_decorators (optional): only show the decorator (not the child), defaults to False
        with_blackboard_variables (optional): add nodes for the blackboard variables
        with_qualified_names (optional): print the class information for each behaviour in each node, defaults to False

    Returns:
        pydot.Dot: graph

    Examples:

        .. code-block:: python

            # convert the pydot graph to a string object
            print("{}".format(py_trees.display.dot_graph(root).to_string()))
    """

    def get_node_attributes(node):
        blackbox_font_colours = {common.BlackBoxLevel.DETAIL: "dodgerblue",
                                 common.BlackBoxLevel.COMPONENT: "lawngreen",
                                 common.BlackBoxLevel.BIG_PICTURE: "white"
                                 }
        if node.type =="Selector":
            attributes = ('box', '#B0FFFF', 'black')  # octagon
        elif node.type =="Sequence":
            attributes = ('box', '#FF8080', 'black')
        elif isinstance(node, composites.Parallel):
            attributes = ('parallelogram', 'lightgold', 'black')
        elif isinstance(node, decorators.Decorator):
            attributes = ('diamond', 'orange', 'black')
            # attributes = ('ellipse', 'ghostwhite', 'black')
        elif node.type =="Act":
            attributes = ('box', 'lightgreen', 'black')
        # elif node.type =="Inverter":
        #     attributes = ('diamond', 'lightred', 'black')
        else:
            attributes = ('ellipse', '#FFFF80', 'black')

        try:
            if node.blackbox_level != common.BlackBoxLevel.NOT_A_BLACKBOX:
                attributes = (attributes[0], 'gray20', blackbox_font_colours[node.blackbox_level])
        except AttributeError:
            # it's a blackboard client, not a behaviour, just pass
            pass
        return attributes

    def get_node_label(node_name, behaviour):
        """
        This extracts a more detailed string (when applicable) to append to
        that which will be used for the node name.
        """
        # Custom handling of composites provided by this library. Not currently
        # providing a generic mechanism for others to customise visualisations
        # for their derived composites.
        # prefix = ""
        # policy = ""
        '''
        if isinstance(behaviour, composites.Composite):
            try:
                if behaviour.memory:
                    prefix += console.circled_m
            except AttributeError:
                pass
            try:
                if behaviour.policy.synchronise:
                    prefix += console.lightning_bolt
            except AttributeError:
                pass
            try:
                policy = behaviour.policy.__class__.__name__
            except AttributeError:
                pass
            try:
                indices = [str(behaviour.children.index(child)) for child in behaviour.policy.children]
                policy += "({})".format(', '.join(sorted(indices)))
            except AttributeError:
                pass

        node_label = f"{prefix} {node_name}" if prefix else node_name
        if policy:
            node_label += f"\n{str(policy)}"
        if with_qualified_names:
            node_label += f"\n({utilities.get_fully_qualified_name(behaviour)})"
        '''
        if node_name == "Sequence":
            node_name = "&rarr;"
        if node_name == "Selector":
            node_name = "?"
        if node_name == "Inverter":
            node_name = "!"
        return node_name

    fontsize = 20
    blackboard_colour = "blue"  # "dimgray"
    graph = pydot.Dot(graph_type='digraph', ordering="out")
    graph.set_name("pastafarianism")  # consider making this unique to the tree sometime, e.g. based on the root name
    # fonts: helvetica, times-bold, arial (times-roman is the default, but this helps some viewers, like kgraphviewer)
    graph.set_graph_defaults(fontname='times-roman')  # splines='curved' is buggy on 16.04, but would be nice to have
    graph.set_node_defaults(fontname='times-roman')
    graph.set_edge_defaults(fontname='times-roman')
    (node_shape, node_colour, node_font_colour) = get_node_attributes(root)
    root_name = str(root.id)
    node_root = pydot.Node(
        name=root_name,
        label=get_node_label(root.ins_name, root),
        shape=node_shape,
        style="filled",
        fillcolor=node_colour,
        fontsize=fontsize,
        fontcolor=node_font_colour,
    )
    if isinstance(root, composites.Composite):
        node_root.set_height(COMPOSITE_NODE_SIZE)
        node_root.set_width(COMPOSITE_NODE_SIZE)
    graph.add_node(node_root)
    behaviour_id_name_map = {root.id: str(root.id)}

    def add_children_and_edges(root, root_node, root_dot_name, visibility_level, collapse_decorators):
        if isinstance(root, decorators.Decorator) and collapse_decorators:
            return
        if visibility_level < root.blackbox_level:
            node_names = []
            for c in root.children:
                (node_shape, node_colour, node_font_colour) = get_node_attributes(c)
                node_name = str(c.id)
                # while node_name in behaviour_id_name_map.values():
                #     node_name += ""
                behaviour_id_name_map[c.id] = node_name
                # Node attributes can be found on page 5 of
                #    https://graphviz.gitlab.io/_pages/pdf/dot.1.pdf
                # Attributes that may be useful: tooltip, xlabel
                node = pydot.Node(
                    name=str(c.id),
                    label=get_node_label(c.name, c),
                    shape=node_shape,
                    style="filled",
                    fillcolor=node_colour,
                    fontsize=fontsize,
                    fontcolor=node_font_colour,
                )
                if isinstance(c, composites.Composite):
                    node.set_height(COMPOSITE_NODE_SIZE)
                    node.set_width(COMPOSITE_NODE_SIZE)
                node_names.append(node_name)
                graph.add_node(node)
                edge = pydot.Edge(root_dot_name, node_name)
                graph.add_edge(edge)
                if c.children != []:
                    add_children_and_edges(c, node, node_name, visibility_level, collapse_decorators)

    add_children_and_edges(root, node_root, root_name, visibility_level, collapse_decorators)

    def create_blackboard_client_node(blackboard_client_name: str):
        return pydot.Node(
            name=blackboard_client_name,
            label=blackboard_client_name,
            shape="ellipse",
            style="filled",
            color=blackboard_colour,
            fillcolor="gray",
            fontsize=fontsize - 2,
            fontcolor=blackboard_colour,
        )

    def add_blackboard_nodes(blackboard_id_name_map: typing.Dict[uuid.UUID, str]):
        data = blackboard.Blackboard.storage
        metadata = blackboard.Blackboard.metadata
        clients = blackboard.Blackboard.clients
        # add client (that are not behaviour) nodes
        subgraph = pydot.Subgraph(
            graph_name="Blackboard",
            id="Blackboard",
            label="Blackboard",
            rank="sink",
        )

        for unique_identifier, client_name in clients.items():
            if unique_identifier not in blackboard_id_name_map:
                subgraph.add_node(
                    create_blackboard_client_node(client_name)
                )
        # add key nodes
        for key in blackboard.Blackboard.keys():
            try:
                value = utilities.truncate(str(data[key]), 20)
                label = key + ": " + "{}".format(value)
            except KeyError:
                label = key + ": " + "-"
            blackboard_node = pydot.Node(
                key,
                label=label,
                shape='box',
                style="filled",
                color=blackboard_colour,
                fillcolor='white',
                fontsize=fontsize - 1,
                fontcolor=blackboard_colour,
                width=0, height=0, fixedsize=False,  # only big enough to fit text
            )
            subgraph.add_node(blackboard_node)
            for unique_identifier in metadata[key].read:
                try:
                    edge = pydot.Edge(
                        blackboard_node,
                        blackboard_id_name_map[unique_identifier],
                        color="green",
                        constraint=False,
                        weight=0,
                    )
                except KeyError:
                    edge = pydot.Edge(
                        blackboard_node,
                        clients[unique_identifier].__getattribute__("name"),
                        color="green",
                        constraint=False,
                        weight=0,
                    )
                graph.add_edge(edge)
            for unique_identifier in metadata[key].write:
                try:
                    edge = pydot.Edge(
                        blackboard_id_name_map[unique_identifier],
                        blackboard_node,
                        color=blackboard_colour,
                        constraint=False,
                        weight=0,
                    )
                except KeyError:
                    edge = pydot.Edge(
                        clients[unique_identifier].__getattribute__("name"),
                        blackboard_node,
                        color=blackboard_colour,
                        constraint=False,
                        weight=0,
                    )
                graph.add_edge(edge)
        graph.add_subgraph(subgraph)

    if with_blackboard_variables:
        blackboard_id_name_map = {}
        for b in root.iterate():
            for bb in b.blackboards:
                blackboard_id_name_map[bb.id()] = behaviour_id_name_map[b.id]
        add_blackboard_nodes(blackboard_id_name_map)

    return graph


def render_dot_tree(root: behaviour.Behaviour,
                    visibility_level: common.VisibilityLevel = common.VisibilityLevel.DETAIL,
                    collapse_decorators: bool = False,
                    name: str = None,
                    target_directory: str = os.getcwd(),
                    with_blackboard_variables: bool = False,
                    with_qualified_names: bool = False,
                    png_only = True):
    """
    Render the dot tree to .dot, .svg, .png. files in the current
    working directory. These will be named with the root behaviour name.

    Args:
        root: the root of a tree, or subtree
        visibility_level: collapse subtrees at or under this level
        collapse_decorators: only show the decorator (not the child)
        name: name to use for the created files (defaults to the root behaviour name)
        target_directory: default is to use the current working directory, set this to redirect elsewhere
        with_blackboard_variables: add nodes for the blackboard variables
        with_qualified_names: print the class names of each behaviour in the dot node

    Example:

        Render a simple tree to dot/svg/png file:

        .. graphviz:: dot/sequence.dot

        .. code-block:: python

            root = py_trees.composites.Sequence("Sequence")
            for job in ["Action 1", "Action 2", "Action 3"]:
                success_after_two = py_trees.behaviours.Count(name=job,
                                                              fail_until=0,
                                                              running_until=1,
                                                              success_until=10)
                root.add_child(success_after_two)
            py_trees.display.render_dot_tree(root)

    .. tip::

        A good practice is to provide a command line argument for optional rendering of a program so users
        can quickly visualise what tree the program will execute.
    """
    graph = dot_tree(
        root, visibility_level, collapse_decorators,
        with_blackboard_variables=with_blackboard_variables,
        with_qualified_names=with_qualified_names)
    filename_wo_extension_to_convert = root.ins_name if name is None else name
    filename_wo_extension = utilities.get_valid_filename(filename_wo_extension_to_convert)
    filenames = {}

    if png_only:
        write_dict = {"png": graph.write_png}
    else:
        write_dict = {"dot": graph.write, "png": graph.write_png, "svg": graph.write_svg}

    for extension, writer in write_dict.items():
        filename = filename_wo_extension + '.' + extension
        pathname = os.path.join(target_directory, filename)
        print("Writing {}".format(pathname))
        writer(pathname)
        filenames[extension] = pathname
    return filenames["png"]
