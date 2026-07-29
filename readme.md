# Available Markdown blocks that can be parsed:
- paragraphs ("pragraph" - > <p>)
- heading ("# " -> <h1> - <h6>)
- code ("```\n" -> <code>)
- quote (">" -> <blockquote>)
- unordered_list ("- " -> <ul>)
- ordered_list blocks ("1. " -> <ol>)

# Available markdown lines that can be parsed:
- text (plain text -> plain text)
- bold ("**" -> <b>)
- italic ("_" -> <i>)
- code ("`" -> <code>) 
- link ("[{alt}]({url})") 
- images ("![{alt}]({url})")


Issues: Single and triple backticks without closing raises an error, double backticks will just result in an empty space