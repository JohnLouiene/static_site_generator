# Available Markdown blocks that can be parsed:
- paragraphs ("pragraph" - > <p>)
- heading ("# " -> <h1> - <h6>)
- code ("```\n" -> <code>)
- quote (">" -> <blockquote>)
- unordered_list ("- " -> <ul>)
- ordered_list blocks ("1. " -> <ol>)

# Available markdown symbols that can be parsed:
- text (plain text -> plain text)
- bold ("**" -> <b>)
- italic ("_" -> <i>)
- code ("`" -> <code>) 
- link ("[{alt}]({url})") 
- images ("![{alt}]({url})")


Notes: 
- Incomplete markdown symbols will raise an error
- Requires an h1 header at the beginning of the markdown