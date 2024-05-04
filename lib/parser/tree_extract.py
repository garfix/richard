from lib.constants import GAMMA
from lib.entity.ParseTreeNode import ParseTreeNode
from lib.parser.entity.Chart import Chart
from lib.parser.entity.ChartState import ChartState
from lib.parser.entity.TreeInProgress import TreeInProgress
from lib.parser.entity.WorkingStep import WorkingStep


class TreeExtracter:

    trees: list[ParseTreeNode]

    def extract(self, chart: Chart):

        completedGammaState = chart.buildCompleteGammaState()

        self.trees = []

        rootNode = ParseTreeNode(
            category=GAMMA,
            children=[],
            Form="",
            Rule=completedGammaState.rule,
        )

        self.trees.append(rootNode)

        tree = TreeInProgress(
            root=rootNode,
            path=[WorkingStep(
                states=[completedGammaState],
                nodes=[rootNode],
                stateIndex= 0,
            )])

        self.next(chart, tree)

    def next(self, chart: Chart, tree: TreeInProgress):
        """
        walk through the parse-tree-in-progress, one step at a time
        """

        newTree, done = tree.advance()
        if done:
            return

        self.addChildren(chart, newTree)


    def addChildren(self, chart: Chart, tree: TreeInProgress):

        parentState = tree.peek().getCurrentState()

        form = parentState.basic_form()
        if not form in chart.completed:
            self.next(chart, tree)
        else:
            allChildStates = chart.completed[form]
            newTrees = self.forkTrees(tree, len(allChildStates))

            for i, childStates in enumerate(allChildStates):

                newTree = newTrees[i]
                parentNode = newTree.peek().getCurrentNode()

                childNodes = []
                for childState in childStates :
                    childNodes.append( self.createNode(childState))
                parentNode.children = childNodes

                step = WorkingStep(
                    states=childStates,
                    nodes=childNodes,
                    stateIndex= 0,
                )

                newTree = newTree.push(step)

                self.next(chart, newTree)

    def forkTrees(self, tree: TreeInProgress, count: int):
        """
        create `count` clones of `tree`; the first tree is just the original
        the new trees are registered with the tree extractor
        """

        tips = []

        for i in range(count):
            if i == 0:
                tips.append( tree)
            else:
                newTip = tree.clone()
                tips.append( newTip)

                self.trees.append( newTip.root)

        return tips

    def createNode(self, state: ChartState):
        """
        creates a single parse tree node
        """

        form = ""
        if state.is_terminal():
            form = state.rule.consequents[0].predicate

        return ParseTreeNode(
            category=     state.rule.antecedent.predicate,
            children= [],
            Form=         form,
            Rule=         state.rule,
        )



def extract_tree_roots(chart: Chart):

    extracter = TreeExtracter()

    extracter.extract(chart)

    # the sentence node is the first child
    roots = []
    for root in extracter.trees :
        if len(root.children) > 0:
            roots.append(root.children[0])

    return roots


# Returns the word that could not be parsed (or ""), and the index of the last completed word
def find_unknown_word(chart: Chart):
    """
    Returns the word that could not be parsed (or ""), and the index of the last completed word
    """

    nextWord = ""
    lastUnderstoodIndex = -1

    # for i = len(chart.states) - 1; i >= 0; i -= 1:
    for i in range(len(chart.states) - 1, -1, -1):
        states = chart.states[i]
        for state in states :
            if state.is_complete():
                if state.end_word_index > lastUnderstoodIndex:
                    lastUnderstoodIndex = state.end_word_index - 1

    if lastUnderstoodIndex+1 < len(chart.words):
        nextWord = chart.words[lastUnderstoodIndex+1]
    else:
        nextWord = chart.words.join( " ")

    return nextWord
