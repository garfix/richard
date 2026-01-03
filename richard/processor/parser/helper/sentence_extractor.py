from richard.entity.ParseTreeNode import ParseTreeNode

def extract_sentences(node: ParseTreeNode, sentence_category: str):
    sentences = []

    if node.category == sentence_category:
        sentences.append(node)
    else:
        for child in node.children:
            sentences.extend(extract_sentences(child, sentence_category))

    return sentences
