import pygame
import random
import sys

pygame.init()

try:
    robot_img = pygame.image.load("robo.png")
    robot_img = pygame.transform.scale(robot_img, (80, 80))
except pygame.error:
    robot_img = pygame.Surface((80, 80))
    robot_img.fill((0, 150, 255)) 

TAMANHO_CELULA = 100
GRID = 5

LARGURA = GRID * TAMANHO_CELULA
ALTURA = GRID * TAMANHO_CELULA + 80

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Geraldo e o Bug do Milênio")

FONTE = pygame.font.SysFont(None, 30)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 100, 255)
VERDE = (0, 200, 0)
VERMELHO = (255, 0, 0)
CINZA = (180, 180, 180)

def gerar_posicoes():
    proibidas = [(0, 0), (4, 4)]
    usadas = set(proibidas)

    componentes = []
    bugs = []

    while len(componentes) < 3:
        pos = (random.randint(0, 4), random.randint(0, 4))
        if pos not in usadas:
            componentes.append(pos)
            usadas.add(pos)

    while len(bugs) < 5:
        pos = (random.randint(0, 4), random.randint(0, 4))
        if pos not in usadas:
            bugs.append(pos)
            usadas.add(pos)

    return componentes, bugs


def desenhar_texto(texto, cor, x, y):
    img = FONTE.render(texto, True, cor)
    TELA.blit(img, (x, y))


class Jogo:

    def __init__(self):
        self.jogador = [0, 0]
        self.servidor = (4, 4)

        self.componentes, self.bugs = gerar_posicoes()

        self.energia = 5
        self.coletados = 0

        self.mensagem = "Colete 3 componentes."
        self.rodando = True

    def mover(self, dx, dy):
        novo_x = self.jogador[0] + dx
        novo_y = self.jogador[1] + dy

        if novo_x < 0 or novo_x >= GRID or novo_y < 0 or novo_y >= GRID:
            self.mensagem = "Você bateu em uma parede!"
            return

        self.jogador = [novo_x, novo_y]
        self.verificar_eventos()

    def verificar_eventos(self):
        pos = tuple(self.jogador)

        if pos in self.componentes:
            self.componentes.remove(pos)
            self.coletados += 1
            self.mensagem = f"Componente coletado! Total: {self.coletados}"

        elif pos in self.bugs:
            self.bugs.remove(pos)
            self.energia -= 1
            self.mensagem = f"Bug encontrado! Energia: {self.energia}"

        if self.energia <= 0:
            self.mensagem = "Game Over! O Bug corrompeu o Geraldo."
            self.rodando = False

        if pos == self.servidor:
            if self.coletados >= 3:
                self.mensagem = "Vitória! Sistema restaurado."
                self.rodando = False
            else:
                self.mensagem = "Você precisa de 3 componentes!"

    def desenhar(self):
        TELA.fill(BRANCO)

        for linha in range(GRID):
            for coluna in range(GRID):
                rect = pygame.Rect(
                    coluna * TAMANHO_CELULA,
                    linha * TAMANHO_CELULA,
                    TAMANHO_CELULA,
                    TAMANHO_CELULA
                )
                pygame.draw.rect(TELA, CINZA, rect, 1)

        sx, sy = self.servidor
        pygame.draw.rect(
            TELA,
            VERDE,
            (
                sy * TAMANHO_CELULA + 25,
                sx * TAMANHO_CELULA + 25,
                50,
                50
            )
        )

        px, py = self.jogador
        TELA.blit(
            robot_img,
            (
                py * TAMANHO_CELULA + 10,
                px * TAMANHO_CELULA + 10
            )
        )

        pygame.draw.rect(
            TELA,
            PRETO,
            (0, GRID * TAMANHO_CELULA, LARGURA, 80)
        )

        desenhar_texto(
            f"Energia: {self.energia}",
            BRANCO,
            10,
            GRID * TAMANHO_CELULA + 10
        )

        desenhar_texto(
            f"Componentes: {self.coletados}/3",
            BRANCO,
            10,
            GRID * TAMANHO_CELULA + 40
        )

        desenhar_texto(
            self.mensagem,
            BRANCO,
            180,
            GRID * TAMANHO_CELULA + 25
        )

        if not self.rodando:
            desenhar_texto(
        "Pressione R para reiniciar",
        BRANCO,
        180,
        GRID * TAMANHO_CELULA + 50
        )
        
        pygame.display.flip()


def main():
    try:
        clock = pygame.time.Clock()
        jogo = Jogo()

        while True:
            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:

                    # Reiniciar partida
                    if not jogo.rodando:
                        if evento.key == pygame.K_r:
                            jogo = Jogo()

                    else:
                        if evento.key in (pygame.K_w, pygame.K_UP):
                            jogo.mover(-1, 0)

                        elif evento.key in (pygame.K_s, pygame.K_DOWN):
                            jogo.mover(1, 0)

                        elif evento.key in (pygame.K_a, pygame.K_LEFT):
                            jogo.mover(0, -1)

                        elif evento.key in (pygame.K_d, pygame.K_RIGHT):
                            jogo.mover(0, 1)

            jogo.desenhar()
            clock.tick(60)

    except Exception as erro:
        print("Erro durante a execução:")
        print(erro)


if __name__ == "__main__":
    main()
