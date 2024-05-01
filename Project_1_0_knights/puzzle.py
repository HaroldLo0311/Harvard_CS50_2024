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
    # Truth: A is either a knight or a knave:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # if A is knight: what he said is true
    Implication(AKnight, And(AKnight, AKnave)),
    # if A is AKnave: what he said is wrong
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #Truth
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    #A says:
    Implication(AKnight, And(AKnave, BKnave)),
    #B says:
    Implication(AKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #Truth:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    #A says:
    #1 if A is knight, they are the same
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    #2 if A is knave, they are not the same
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    #B says:
    #1 if B is knight, they are not the same
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    #2 if B is knave, they are the same
    Implication(BKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #Truth:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    #B:
    #if B is knight:
    Implication(BKnight, CKnave),
    Implication(BKnight, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    #if B is knave:
    Implication(BKnave, Not(CKnave)),
    Implication(BKnight, Not(Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),
    #C:
    # if C is knight:
    Implication(CKnight, AKnight),
    # if C is knave:
    Implication(CKnave, Not(AKnight))
)
print(type(knowledge1))
print(knowledge0)
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
