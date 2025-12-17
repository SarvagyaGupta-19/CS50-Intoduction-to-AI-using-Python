from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A's statement
    Or(
        And(AKnight, And(AKnight, AKnave)),
        And(AKnave, Not(And(AKnight, AKnave)))
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
     # A and B are each either knight or knave, but not both
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # A's statement
    Or(
        And(AKnight, And(AKnave, BKnave)),
        And(AKnave, Not(And(AKnave, BKnave)))
    )
)
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
same_kind = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
)

different_kind = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # A and B are each either knight or knave, but not both
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # A's statement
    Or(
        And(AKnight, same_kind),
        And(AKnave, Not(same_kind))
    ),

    # B's statement
    Or(
        And(BKnight, different_kind),
        And(BKnave, Not(different_kind))
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # A, B, C are each either knight or knave, but not both
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # A did NOT say "I am a knave"
    Not(AKnave),

    # B says: "C is a knave"
    Or(
        And(BKnight, CKnave),
        And(BKnave, Not(CKnave))
    ),

    # C says: "A is a knight"
    Or(
        And(CKnight, AKnight),
        And(CKnave, Not(AKnight))
    )
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
