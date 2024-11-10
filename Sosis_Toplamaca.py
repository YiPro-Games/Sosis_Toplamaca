import pygame
import random

pygame.init()

g_y = (1000, 520)
w = pygame.display.set_mode(g_y)
FPS = 60
saat = pygame.time.Clock()


font = pygame.font.SysFont("comicsans", 16)
puan = 0


baslama_ekrani = True
oyun_aktif = False
kazandin_ekrani = False
siyah_ekran = False


def yeni_sosis_olustur():
    sosis_x = random.randint(100, 900)
    return pygame.Rect(sosis_x, 325, 64, 64)

def yeni_bok_olustur():
    bok_x = random.randint(880, 900)  
    return bok_x

sosis_koordinat = yeni_sosis_olustur()
bok_x = yeni_bok_olustur()

# NESNELER ve ARKAPLAN
arkaplan = pygame.image.load("Arkaplan.png")
arkaplan_koordinat = arkaplan.get_rect()
arkaplan_koordinat.topleft = (0, 0)
baldiback = pygame.image.load("Baldiback1.png")
baldiback_koordinat = baldiback.get_rect()
baldiback_koordinat.topleft = (250, 205)
sosis_resmi = pygame.image.load("sosis.png")
baslama_ekrani_resmi = pygame.image.load("başlama ekranı.png")
baslama_ekrani_koordinat = baslama_ekrani_resmi.get_rect(center=(500, 300))
buton_resmi = pygame.image.load("buton.png")
buton_koordinat = buton_resmi.get_rect(center=(500, 350))


bok = pygame.image.load("bok.png")
bok_koordinat = bok.get_rect()
bok_koordinat.y = 325
bok_koordinat.x = bok_x
bok_hareket_yonu = 1
bok_hareket_hizi = 4

# ZIPLAMA 
ziplama = False
ziplama_hizi = 15
yercekimi = 1

durum = True
while durum:
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            durum = False
        if etkinlik.type == pygame.MOUSEBUTTONDOWN:
            if baslama_ekrani and buton_koordinat.collidepoint(etkinlik.pos):
                baslama_ekrani = False
                oyun_aktif = True
        if etkinlik.type == pygame.KEYDOWN:
            if siyah_ekran and etkinlik.key == pygame.K_SPACE:
                siyah_ekran = False
                oyun_aktif = True
                puan = 0
                baldiback_koordinat.topleft = (250, 205)
                bok_koordinat.x = yeni_bok_olustur()
                bok_hareket_hizi = 4
    # Kontroller
    if baslama_ekrani:
        w.fill((0, 0, 0))
        w.blit(baslama_ekrani_resmi, baslama_ekrani_koordinat)
        w.blit(buton_resmi, buton_koordinat)
    elif oyun_aktif and not siyah_ekran:
        tus = pygame.key.get_pressed()
        baldiback = pygame.image.load("Baldiback1.png")
        if tus[pygame.K_d] and baldiback_koordinat.x < 890:
            baldiback_koordinat.x += 7
        elif tus[pygame.K_a] and baldiback_koordinat.x > 20:
            baldiback = pygame.image.load("Baldiback2.png")
            baldiback_koordinat.x -= 7

        # Zıplama KONTROL
        if not ziplama:
            if tus[pygame.K_w]:
                ziplama = True
                ziplama_hizi = 20
        else:
            baldiback_koordinat.y -= ziplama_hizi
            ziplama_hizi -= yercekimi
            if baldiback_koordinat.y >= 205:
                baldiback_koordinat.y = 205
                ziplama = False

        
        if baldiback_koordinat.colliderect(sosis_koordinat):
            puan += 1
            sosis_koordinat = yeni_sosis_olustur()

        if puan in [15, 30, 45, 60]:  
            bok_hareket_hizi += 0.03

        if puan < 60:
            bok_koordinat.x += bok_hareket_yonu * bok_hareket_hizi
            if bok_koordinat.x <= 50 or bok_koordinat.x >= 900:
                bok_hareket_yonu *= -1

        if bok_koordinat.colliderect(baldiback_koordinat) or puan >= 100:
            siyah_ekran = True

        w.blit(arkaplan, arkaplan_koordinat)
        w.blit(baldiback, baldiback_koordinat)
        w.blit(sosis_resmi, sosis_koordinat)
        w.blit(bok, bok_koordinat)
        puan_yazi = font.render(f"PUAN: {puan}", True, (0, 0, 0))
        w.blit(puan_yazi, (900, 10))

    elif siyah_ekran:
        w.fill((0, 0, 0))
        bitis_mesaji = "Kazandın!" if puan >= 60 else "Boka basıp geberdin!"
        bitis_yazisi = font.render(bitis_mesaji, True, (250, 250, 250))
        puan_yazisi_bitis = font.render(f"Puan: {puan}", True, (250, 250, 250))
        w.blit(bitis_yazisi, (400, 240))
        w.blit(puan_yazisi_bitis, (400, 280))

    pygame.display.update()
    saat.tick(FPS)

pygame.quit()
