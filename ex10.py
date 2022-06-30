phrase = input("Set a phrase: ")


class TestCheckLong:
    def test_check_long(self):
        assert len(phrase) < 15, "The phrase are longer or equal 15 symbols length"
