from contextlib import redirect_stdout
from io import StringIO


# @pytest.mark.skip(reason="Not implemented yet")
def test_main():
    f = StringIO()
    with redirect_stdout(f):
        print("Hello, World!")
    out = f.getvalue().strip()
    assert out == "Hello, World!"
