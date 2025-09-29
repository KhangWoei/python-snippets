import core as c

def main_poops(capfd):
    c.main()

    out, _ = capfd.readouterr()
    assert out == "poop"
