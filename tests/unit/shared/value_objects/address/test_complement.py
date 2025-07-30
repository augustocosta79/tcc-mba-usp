from apps.shared.value_objects import Complement

class TestComplement:
    def test_should_create_complement_successfully(self):
        complement = Complement("complement")
        assert complement.value == "complement"

    def test_should_return_true_comparing_two_equal_complements(self):
        complement1 = Complement("complement") 
        complement2 = Complement("complement") 
        assert complement1 == complement2

    def test_should_return_false_comparing_two_different_complements(self):
        complement1 = Complement("complement1") 
        complement2 = Complement("complement2") 
        assert complement1 != complement2
