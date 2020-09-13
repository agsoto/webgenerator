from random import choice, choices
#Global
class RandomHelper:
    binary_choice = [True, False]

    @staticmethod
    def flip_coin(true_probability=None):
        if true_probability is not None:
            return choices(RandomHelper.binary_choice, [true_probability, 1-true_probability])[0]
        else:
            return choice(RandomHelper.binary_choice)