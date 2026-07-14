class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None or "":
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        
        return result
    
    def __repr__(self):
        return f"tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"

class LeafNode(HTMLNode):
    """Child class of an HTML parent node"""
    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"tag:{self.tag}, value:{self.value}, props:{self.props}"
        
class ParentNode(HTMLNode):
    """Parent class of an HTML parent node, requires a child node"""
    def __init__(self, tag: str, children: list,  props: dict | None = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node is missing a tag parameter")

        if not self.children:
            raise ValueError("Parent node is missing child nodes in children list")
        
        result = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            result = result + child.to_html()

        return f"{result}</{self.tag}>"

