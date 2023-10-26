from textx import get_location, TextXSemanticError


def find_stratification(nodes, names):
    stratification = []

    def precondition_satisfiable(step, names):
        if (not hasattr(step.precondition, "referenced_names")):
            return True

        for name in step.precondition.referenced_names.names_fields:
            if not name in names:
                return False
        return True

    def find_path(nodes, names, cnt):
        starting_nodes = set(
            filter(lambda s: precondition_satisfiable(s, names), nodes))

        for starting_node in starting_nodes:
            step_names = {**starting_node.computed_property_names, **starting_node.field_names}
            for name in step_names:
                names.add(name)

        rest = set(nodes) - set(starting_nodes)
        stratification.append(list(map(lambda n: n.name, nodes-rest)))

        if rest == starting_nodes or len(rest) == 0:
            return nodes

        if cnt == 400:  # max recursion depth
            raise TextXSemanticError(
                f"Steps \'{ ' and '.join([n.name for n in rest]) }\' are unreachable due to their preconditions ", **get_location(list(rest)[0].precondition.expressions[0]))

        return find_path(rest, names, cnt + 1)

    find_path(nodes, names, cnt=1)
    return stratification
