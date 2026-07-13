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

#Child class for HTML Nodes, representing HTMLNodes that do not have a child or are the tip of the HTML node tree.
class LeafNode(HTMLNode):
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
        
