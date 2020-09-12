import re
import sys

class Expression:
    def __init__(self, expr, level):
        self.expr = expr
        self.level = level

    def __repr__(self):
        return self.expr + "(" + str(self.level) + ")"

class NumberOp:
    def __init__(self, op, num):
        self.op = op
        self.num = num
    
    def __repr__(self):
        return str(self.num) + "(" + self.op + ")"

def parse(toParse):
    toParse = toParse.replace(" ", "")

    if not re.match("(\d+(\.\d*)?[+\-*/]?)+\Z", toParse):
        print("malformed input!")
        return

    matchesI = re.finditer("\d+([\*/]\d+)+", toParse)

    matches = []

    for match in matchesI:
        matches.append(match)

    parsed = []

    currentIndex = 0

    if len(matches) == 0:
        parsed.append(Expression(toParse, 0))

    for match in matches:
        if currentIndex != match.start():
            parsed.append(Expression(toParse[currentIndex:match.start()], 0))
        parsed.append(Expression(match.group(), 1))
        currentIndex = match.end()

    if matches[-1].end() < len(toParse):
        parsed.append(Expression(toParse[matches[-1].end():], 0))

    print(">> " + str(parsed))

    def calculate(toCalc):
        base = float(toCalc[0].num)
        for to in toCalc:
            if to.op == "+":
                base = base + float(to.num)
            if to.op == "-":
                base = base - float(to.num)
            if to.op == "*":
                base = base * float(to.num)
            if to.op == "/":
                base = base / float(to.num)
        return base

    def prepare(toPrepare):
        prepMatchesI = re.finditer("\d+(\.\d*)?", toPrepare)
        prepMatches = []
        for match in prepMatchesI:
            prepMatches.append(match)

        finished = []
        prepCurrentIndex = 0

        for match in prepMatches:
            op = ""
            if match.start() != 0:
                op = toPrepare[match.start()-1:match.start()]
            num = match.group()
            finished.append(NumberOp(op, num))

        return finished

    finalOut = ""

    for expr in parsed:
        if expr.level == 1:
            finalOut = finalOut + str(calculate(prepare(expr.expr)))
        elif expr.level == 0:
            finalOut = finalOut + expr.expr

    print(">> " + finalOut)

    finalOut = str(calculate(prepare(finalOut)))

    print("> " + finalOut)

while True:
    parse(input())
