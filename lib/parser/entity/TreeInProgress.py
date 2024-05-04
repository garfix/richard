from dataclasses import dataclass

from lib.entity.ParseTreeNode import ParseTreeNode
from lib.parser.entity.WorkingStep import WorkingStep


@dataclass()
class TreeInProgress:
    root: ParseTreeNode
    path: list[WorkingStep]


    def treeInProgress(self):

        newRoot, aMap = self.cloneTree(self.root)

        newSteps = []
        for step in self.path:
            newNodes = []
            for node in step.nodes:
                newNode = aMap[node]
                newNodes.append(newNodes, newNode)

            newStep = WorkingStep(
                step.states,
                newNodes,
                step.stateIndex,
            )
            newSteps.append(newStep)

        newStack = TreeInProgress(
            newRoot,
            newSteps,
        )

        return newStack


    def cloneTree(self, tree: ParseTreeNode):

        aMap = {}
        newTree = self.cloneNodeWithMap(tree, aMap)

        return newTree, aMap


    def cloneNodeWithMap(self, node, aMap):

        children = []
        for constituent in node.children:
            clone = self.cloneNodeWithMap(constituent, aMap)
            children.append( clone)

        newNode = ParseTreeNode(
            node.category,
            children,
            node.form,
            node.rule,
        )

        aMap[node] = newNode

        return newNode


    def advance(self):

        newTip = self
        done = True

        if len(newTip.path) > 0:
            step = newTip.path[len(newTip.path)-1]
            if step.stateIndex < len(step.states):
                step.stateIndex += 1
            else:
                return newTip.pop().advance()
            done = False

        return newTip, done


    def peek(self):
        if len(self.path) == 0:
            raise Exception("empty stack!")
        else:
            return self.path[len(self.path)-1]


    def push(self, step):
        newStack = self
        newStack.path.append(step)
        return newStack


    def pop(self):
        newStack = self
        newStack.path = newStack.path[0 : len(newStack.path)-1]
        return newStack


