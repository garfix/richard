from richard.entity.ParseTreeNode import ParseTreeNode


def get_trees_with_least_amount_of_regexps(trees: list[ParseTreeNode]):
    kept_trees = []
    least_regexp_count = None

    for tree in trees:
        regexp_count = tree.reg_exp_count
        if least_regexp_count == None or regexp_count < least_regexp_count:
            least_regexp_count = regexp_count
            kept_trees = [tree]
        elif regexp_count == least_regexp_count:
            kept_trees.append(tree)

    return kept_trees
