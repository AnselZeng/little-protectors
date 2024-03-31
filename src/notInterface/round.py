class Round():
    def __init__(self, roundNum, enemyList) -> None:
        self.roundNum = roundNum
        self.enemyList = enemyList
    
    def nextEnemy(self):
        if self.enemyList:
            yield self.enemyList.pop(0)