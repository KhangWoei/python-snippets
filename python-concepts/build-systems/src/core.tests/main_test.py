import core.main as c

def test_main_poops(capfd):
    c.main()

    out, _ = capfd.readouterr()
    assert out == "poop\n"

