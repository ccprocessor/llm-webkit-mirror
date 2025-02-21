from unstructured.partition.html import partition_html


def eval_unstructured(html: str, title: str) -> str:
    elements = partition_html(text=html)
    return '\n\n'.join([str(el) for el in elements])


if __name__ == '__main__':
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta http-equiv="x-ua-compatible" content="ie=edge">
      <meta name="viewport" content="width=device-width">
      <title>MathJax v3 with MathML input and HTML output</title>
      <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/mml-chtml.js"></script>
    </head>
    <body>
        <h1>MathJax v3 beta: MathML input, HTML output test</h1>
        <p> $$ x^2 + 2x + 1 = 0 $$ </p>
    </body>
    </html>
    """
    title = 'test'
    print(eval_unstructured(html, title))
