from richard.entity.ParseTreeNode import ParseTreeNode

def extract_sentences(node: ParseTreeNode, sentence_categories: list[str]):
    sentences = []

    if node.category in sentence_categories:
        sentences.append(node)
    else:
        for child in node.children:
            sentences.extend(extract_sentences(child, sentence_categories))

    return sentences
