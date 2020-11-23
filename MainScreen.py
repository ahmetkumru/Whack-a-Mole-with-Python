#Kullanılcak kütüphaneleri import etme işlemleri.
import random
import time as t
import pygame
from pygame import *



#Oyunumuzun ana hatlarının bulunduğu class'ın oluşturması işlemleri.
class WhackAMole:
    def __init__(self):

        self.FPS = 60

        #Kullanacağımız renkleri tanımlama işlemleri.
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.RED = (188, 0, 0)
        self.BROWN = (115, 74, 18)


        self.leftMouseHit = True #Sol tık kontrol işlemi.
        pygame.display.set_caption('Whack A Mole') #Oyunumuzun başlığını ayarlama işlemi.

       #Skor, Hatalı Tıklama ve Level Bilgisi sayaçlarının oluşturulması işlemleri.
        self.scoreCounter = 0
        self.missCounter = 0
        self.levelCounter = 1

       #Ekranımızın oluşturma ve  boyutlandırma işlemleri.
        self.frame = pygame.display.set_mode((1000, 900), 0, 32)

        #Yazı fontunun ayarlanması işlemi
        self.font = pygame.font.SysFont('Hursheys', 50)
        #Arka plan resminin projeye eklenmesi işlemi.
        self.background = pygame.image.load("background.png")


        #Backgroundumuzdaki deliklerin yerini belirlemek amacıyla doğru dikdörtgenlerin çizilmesi işlemleri.
        pygame.draw.circle(self.frame, self.WHITE, (100, 298), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (100, 548), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (100, 798), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (350, 298), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (350, 548), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (350, 798), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (600, 298), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (600, 548), 85, 0)
        pygame.draw.circle(self.frame, self.WHITE, (600, 798), 85, 0)


        #Tasarladığımız "mole.png" resmini animasyonumuzda kullanmak üzere parçalara ayırarak listeye kaydetme işlemleri.
        molesImage = pygame.image.load("mole.png")
        self.moles = []
        self.moles.append(molesImage.subsurface(149, 0, 130, 120))
        self.moles.append(molesImage.subsurface(289, 0, 130, 120))
        self.moles.append(molesImage.subsurface(429, 0, 130, 120))
        self.moles.append(molesImage.subsurface(555, 0, 150, 120))
        self.moles.append(molesImage.subsurface(699, 0, 150, 120))
        self.moles.append(molesImage.subsurface(833, 0, 150, 120))


        #Köstebek deliklerimizi, konumlarını verip listeye kaydetme işlemleri.
        self.holes = []
        self.holes.append((30, 108))
        self.holes.append((30, 368))
        self.holes.append((30, 618))
        self.holes.append((280, 108))
        self.holes.append((280, 368))
        self.holes.append((280, 618))
        self.holes.append((530, 108))
        self.holes.append((530, 368))
        self.holes.append((530, 618))

    #Level bilgilerimizi güncelleyip yeni araklıkları belirlediğimiz fonksiyon.
    def lvlUpUpdate(self, initInterval):
        currentInterval = initInterval - self.levelCounter * 0.13
        if currentInterval > 0:
            return currentInterval
        else:
            return 0.05
            # Level bilgisini aldığımız fonksiyon.

    def lvlInfo(self):
            newLevelInfo = 1 + int(self.scoreCounter / 4)
            return newLevelInfo
            # Sol tık yaptığımız zaman mjolniri gösteren fonksiyon.

    def showMjolnir(self):
        image3 = pygame.image.load("mjolnir.png")
        x, y = pygame.mouse.get_pos()

        self.frame.blit(image3, [x - 20, y - 20])
        pygame.display.update()
    #Köstebeklerimize vurulup vurulmadığını kontrol eden fonksiyon / metod.
    def moleHit(self, holePosition):
        x, y = pygame.mouse.get_pos()
        holeX = holePosition[0]
        holeY = holePosition[1]
        if (x > holeX) and (x < holeX + 150) and (
                y > holeY) and (y < holeY + 150):
            return True
        else:
            return False



    #Skor, Kaçırılan Vuruş ve Level bilgilerini güncel olarak bastıran fonksiyon.
    def printStats(self):

        scoreTxt = self.font.render(str(self.scoreCounter), True, self.WHITE)
        self.frame.blit(scoreTxt, [930, 25])

        missTxt = self.font.render(str(self.missCounter), True, self.WHITE)
        self.frame.blit( missTxt, [930, 140])

        lvlTxt = self.font.render(str(self.levelCounter), True, self.WHITE)
        self.frame.blit(lvlTxt, [930, 248])

        pygame.display.update()

    #Kaçırılan vuruş bilgisini kontrol edip oyunu sonlandıran fonksiyon.
    def ShutDownOrContinue(self, missNumber):

        if missNumber == 5:
            self.font = pygame.font.SysFont('Hursheys', 150)
            gameOverTxt = self.font.render("Game Over", True, self.RED)
            self.frame.blit(gameOverTxt, [100, 375])
            pygame.display.update()
            t.sleep(3)
            pygame.quit()


    #Başlangıç değerlerinin belirlenip oyunun başlatılması işlemleri.
    def initialValues(self):
        gameLoopTimer = 0 #Loop zaman sayacı
        animationNumber = -1 #Köstebeğin animasyon numarası
        gameLoop = True
        isMoleDown = False #Köstebeğin aşşağıda olup olmamasının kontrolü.
        plusInterval = 0.1  #Level arttıkça köstebeklerin ne kadar daha hızlı geleceğini belirleyen değişken.
        initialInterval = 1 #Başlangıç için köstebeklerin çıkış aralğını belirten değer.
        holeNumber = 0 #Delik numarasını belirten değişken.

        #Zaman tutan değişken.
        timer = pygame.time.Clock()


        #Oyun döngüsünü başlatma işlemi.
        while gameLoop:
            self.ShutDownOrContinue(self.missCounter)
            self.printStats()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameLoop = False

                if event.type == MOUSEBUTTONDOWN and event.button == self.leftMouseHit:
                    #Doğru köstebek deliğine tıklanıp tıklanmadığının kontrolü işlemi.

                    if self.moleHit(self.holes[holeNumber]) and animationNumber > 0 :
                        #Mjolnir'ın anlık gösterilmesi sebebiyle gösterim süresinin artması amacıyla for döngüsünün içine sokma işlemi.
                        for i in range(150):
                            self.showMjolnir()
                        animationNumber = 3
                        isMoleDown = False
                        plusInterval = 0
                        self.scoreCounter += 1
                        self.levelCounter = self.lvlInfo()

                    else:
                        self.missCounter += 1
                        for i in range(150):
                            self.showMjolnir()

            if animationNumber == -1:
                self.frame.blit(self.background, (0, 0))
                animationNumber = 0
                isMoleDown = False
                plusInterval = 0.5
                holeNumber = random.randint(0, 8)

            mil = timer.tick(self.FPS)
            sec = mil / 1000.0
            gameLoopTimer += sec

            if animationNumber > 5:
                self.frame.blit(self.background, (0, 0))
                animationNumber = -1



            if gameLoopTimer > plusInterval:
                pic = self.moles[animationNumber]
                self.frame.blit(self.background, (0, 0))
                self.frame.blit(pic, (self.holes[holeNumber][0] +5 , self.holes[holeNumber][1]  ))

                if isMoleDown is False:
                    animationNumber += 1

                else:
                    animationNumber -= 1

                if animationNumber == 4:
                    plusInterval = 0.3

                elif animationNumber == 3:
                    animationNumber -= 1
                    isMoleDown = True
                    plusInterval = self.lvlUpUpdate(initialInterval)

                else:
                    plusInterval = 0.1
                gameLoopTimer = 0

            pygame.display.flip()


#Oyunun çalıştırılmasının başlatılma işlemleri.
pygame.init()

try:
    runGame = WhackAMole()
    runGame.initialValues()

except:
    print("GAME OVER")

pygame.quit()