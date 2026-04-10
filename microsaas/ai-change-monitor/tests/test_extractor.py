from app.services.extractor import extract_visible_text, normalize_text


def test_extract_visible_text_skips_script_and_style():
    html = """
    <html>
      <head><title>Ignored</title><style>.x { color: red; }</style></head>
      <body>
        <h1>Hello</h1>
        <script>console.log("ignore")</script>
        <p>World</p>
      </body>
    </html>
    """

    text = extract_visible_text(html)

    assert "Hello" in text
    assert "World" in text
    assert "console.log" not in text
    assert "Ignored" not in text


def test_normalize_text_collapses_spacing():
    text = "  Alpha   beta \n\n\n Gamma  "

    assert normalize_text(text) == "Alpha beta\nGamma"

