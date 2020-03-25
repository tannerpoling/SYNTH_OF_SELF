class SynthIter:
    # an interator that continually returns a value, which can be updated

    def __init__(self, curValue = 0.15):
        self.curValue = curValue

    def __iter__(self):
        return self

    def changeCur(value):
        self.curValue = value

    def __next__(self):
        num = self.curValue
        return num
