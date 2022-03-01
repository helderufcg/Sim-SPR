from numpy import *
import matplotlib.pyplot as plt
import os

print("\n------------------------------------------ Bem vindo ao Sim-SPR --------------------------------------------\n"
      "\n------------------------------------------------------------------------------------------------------------\n"
      "     Esta atualização do Sim-SPR consiste na reestruturação da plataforma de código-aberto utilizada para a\n"
      "analise e projeto de biosensores ópticos baseados no efeito de Ressonancia de Plasmons de Superficie(SPR) já\n"
      "existente. A extensão foi implementada em linguagem Python e traz a nova funcionalidade de interrogação pelo \n"
      "comprimento de onda (WIM).\n"
      "     De forma simples e intuitiva, o Sim-SPR oferece um suporte para calcular os pontos de ressonancia e a \n"
      "sensibilidade, tanto no modo de interrogação angular (AIM) como no modo de interrogação por comprimento de \n"
      "onda (WIM) considerando o acoplamento óptico com prisma em estruturas planas (configurações de Krestchmann \n"
      "e Otto). A modelagem numérica da reflectância em função do ângulo incidente ou do comprimento de onda tem \n"
      "como base o método da matriz de transferência característica obtida a partir das equações de Fresnel. \n"
      "\nAo fim da simulação, o código fornece resultados em termos de: \n"
      "         (1) Ponto de ressonância na primeira interação \n"
      "         (2) Reflectancia mínima na primeira interação\n"
      "         (3) Sensibilidade Angular ou Espectral\n"
      "         (4) FWHM da curva na priemira interação\n"
      "         (5) Variação do ângulo ou comprimento de onda de ressonância após as 'n' interações\n"
      "         (6) Detecção de acurácia (DA) e \n"
      "         (7) Fator de qualidade (QF).\n"
      "E ainda respostas gráficas com: \n"
      "         (1) Curva de ressonancia\n"
      "         (2) Deslocamentos da curva de ressonancia em função da variação do indice de refração\n"
      "         (3) Curva de Sensibilidade e \n"
      "         (4) Curva com a variação dos pontos de ressonância.\n"
      "\nOs resultados obtidos foram validados através de outras ferramentas computacionais disponível na literatura."
      
      "\n-----------------------------------------------------------------------------------------------------------\n")
x = input("Enter para continuar... \n>>>")
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

class SPR(object):
    def __init__(self):
        # Atributos:
        self.d = []  # Espessura
        self.material = []  # Lista de materiais que constituem as camadas
        self.indexRef = []  # Indice de refração
        self.index_analit = 0  # Indice de refração da camada sensoriada
        self.index_ref_ana = []  # Lista dos indices de refração do analito

        self.ponto_ressonancia = []  # Angulos de ressonacia ou comprimentos de onda obtidos a partir do grafico
        self.ponto_critico = []  # Angulo de reflexão interna total obtidos a partir da formula

        self.R = []  # Lista de valores da Reflectancia
        self.S = []  # Lista de valores da Sensibilidade calculados a partir do grafico

        self.Fwhm = []  # Lista de valores do FWHM

        # Seleciona o tipo de configuração para acoplamento com prisma: Kretschemann ou Otto.
        while True:
            self.config = int(input("Selecione uma configuração:\n1 - Kretschmann\n2 - Otto\n-> "))
            if self.config < 1 or self.config > 3:
                print("Valor Inválido")
            else:
                t = "\nConfiguração de Kretschmann\n" if self.config == 1 else "\nConfiguração de Otto\n"
                print(t)
                break

        # Seleciona o modo de interrogação : Angular ou Espectral.
        while True:
            self.mod_int = int(
                input("Selecione o modo de interrogação:\n1 - Angular (AIM)\n2 - Espectral (WIM)\n-> "))
            if self.mod_int < 1 or self.mod_int > 2:
                print("Valor Inválido")
            else:
                t = "\nModo de Interrogação Angular\n" if self.mod_int == 1 else "\nModo de Interrogação Espectral\n"
                print(t)
                break

        # Determinação do número de camadas
        # (Especificado para 3 <= N <= 7, mas é possivel alterar no código caso necessário)
        while True:
            self.nLayers = int(input("Número de camadas: "))
            if self.nLayers < 3 or self.nLayers > 7:
                print(f"Valor Inválido:\nTente outro valor (3 < N < {7})")
            else:
                print(f"\nEstrutura de {self.nLayers} camadas\n")
                break

        # Determinação da espessura e material das camadas
        for layer in range(self.nLayers):
            self.setLayers(layer)  # Método que solicita do usuário as caracteristicas das camadas
        self.layer_ssr = int(input("\nCamada a ser sensoriada: ")) - 1  # Camada a ser sensoriada

        # Número de interações na variação do indice de refração do analito.
        while True:
            self.inter = int(input("Analisar sensibilidade em quantas interações?\n-> "))
            if self.inter < 0:
                print("Valor Inválido!")
            else:
                break

        # Passo da variação do indice de refração(ex. Delta_n = 0.005 RIU )
        while True:
            self.passo_int = float(input("Passo Delta n =  "))
            if self.passo_int < 0:
                print("Valor Inválido!")
            else:
                break

        # Modo de Interrogação Angular
        if self.mod_int == 1:
            # Angulo de incidência inicial
            while True:
                self.a1 = float(input("Angulo Inicial (0° - 90°):\n-> ")) * (pi / 180)
                if self.a1 < 0 or self.a1 > (pi / 2) or self.a1 == ' ':
                    if self.a1 == '':
                        print("Insira um valor")
                    else:
                        print("Valor fora do intervalo!")
                else:
                    break

            # Angulo de incidência final
            while True:
                self.a2 = float(input("Angulo Final (0° - 90°):\n-> ")) * (pi / 180)
                if self.a2 < self.a1 or self.a2 > (pi / 2) or self.a2 == ' ':
                    if self.a2 == ' ':
                        print("Insira um valor")
                    else:
                        print("Angulo final inferior ao inicial ou maior que 90°.")
                else:
                    break

            # Passo do angulo de varredura
            while True:
                self.passo_ang = float(input("Passo da varredura angular(°):\n-> ")) * (pi / 180)
                if self.passo_ang < 0:
                    print("Valor Inválido!")
                else:
                    break

            # Comprimento de onda do feixe incidente
            while True:
                self.wavelenght = float(input("Comprimento de onda (nm):\n-> ")) * 1e-9
                if self.wavelenght < 0 or self.wavelenght == ' ':
                    print("Valor Inválido")
                else:
                    break

            self.theta_i = arange(self.a1, self.a2, self.passo_ang)  # Array com os ângulos de incidência

            # Método que calcula a sensibilidade e demais indicadores de qualidade
            self.sensibilidade_analise(self.inter)

            # Método que exibe os gráficos:
            # (1) Curva de ressonancia,
            # (2) Deslocamentos da curva de ressonancia em função da variação do indice de refração
            # (3) Curva de Sesibilidade e (4) Curva dos pontos de ressonancia
            self.plot(self.inter, self.index_ref_ana)

        # Modo de Interrogação Espectral
        else:
            # Comprimento de onda inicial
            while True:
                self.a1 = float(input("Comprimento de onda inicial (nm):\n-> ")) * 1e-9
                if self.a1 < 0 or self.a1 == '':
                    if self.a1 == '':
                        print("Insira um valor")
                    else:
                        print("Valor fora do intervalo!")
                else:
                    break

            # Comprimento de onda final
            while True:
                self.a2 = float(input("Comprimento de onda final (nm):\n-> ")) * 1e-9
                if self.a2 < self.a1 or self.a2 == ' ':
                    if self.a2 == ' ':
                        print("Insira um valor")
                    else:
                        print("Comprimento de onda final inferior ao inicial.")
                else:
                    break

            # Passo de varredura espectral em nm
            while True:
                self.passo_ang = float(input("Passo da varredura(nm):  ")) * 1E-9
                if self.passo_ang < 0:
                    print("Valor Inválido!")
                else:
                    break

            # Angulo do feixe incidente
            while True:
                self.theta_i = float(input("Angulo de incidencia(graus): ")) * (pi / 180)
                if self.theta_i < 0 or self.theta_i > pi / 2:
                    print("Valor Inválido")
                else:
                    break

            self.lambda_i = arange(self.a1, self.a2, self.passo_ang)  # Array com os comprimentos de onda incidentes

            # Método que calcula a sensibilidade e demais indicadores de qualidade
            self.sensibilidade_analise(self.inter)

            # Método que exibe os gráficos:
            # (1) Curva de ressonancia,
            # (2) Deslocamentos da curva de ressonancia em função da variação do indice de refração
            # (3) Curva de Sesibilidade e (4) Curva dos pontos de ressonancia
            self.plot(self.inter, self.index_ref_ana)

    def set_index(self, material, wi):
        Lambda_i = wi * 1e6  # Comprimento de onda de incidência em micrômetros
        j = 0 + 1j
        # Materiais que compõem os prismas modelados pela equação de Sellmeier
        if 0 < material <= 8:
            if material == 1:  # BK7
                B1, B2, B3, C1, C2, C3 = 1.03961212, 2.31792344E-1, 1.01046945, 6.00069867E-3, 2.00179144E-2, 103.560653

            elif material == 2:  # Silica
                B1, B2, B3, C1, C2, C3 = 0.6961663, 0.4079426, 0.8974794, 4.6791E-3, 1.35121E-2, 97.934003

            elif material == 3:  # N-F2
                B1, B2, B3, C1, C2, C3 = 1.39757037, 1.59201403E-1, 1.2686543, 9.95906143E-3, 5.46931752E-2, 119.2483460

            elif material == 4:  # Safira sintética(Al2O3)
                B1, B2, B3, C1, C2, C3 = 1.4313493, 0.65054713, 5.3414021, 0.00527993, 0.0142383, 325.01783

            elif material == 5:  # SF2
                B1, B2, B3, C1, C2, C3 = 1.78922056, 3.28427448E-1, 2.01639441, 1.35163537E-2, 6.22729599E-2, 168.014713

            elif material == 6:  # FK51A
                B1, B2, B3, C1, C2, C3 = 0.971247817, 0.216901417, 0.904651666, 0.00472301995, 0.0153575612, 168.68133

            elif material == 7:  # N-SF14
                B1, B2, B3, C1, C2, C3 = 1.69022361, 0.288870052, 1.704518700, 0.01305121130, 0.0613691880, 149.5176890

            elif material == 8:  # Acrilico SUVT
                B1, B2, B3, C1, C2, C3 = 0.59411, 0.59423, 0, 0.010837, 0.0099968, 0

            # Equação de Sellmeier
            n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                     + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

        # Glicerol e PVA
        elif 8 < material <= 10:
            if material == 9:  # PVA
                B1, B2, B3, C1, C2, C3 = 1.460, 0.00665, 0, 0, 0, 0
            elif material == 10:  # Glicerina/glicerol
                B1, B2, B3, C1, C2, C3 = 1.45797, 0.00598, -0.00036, 0, 0, 0
            # Equação que modela o indice de refração em função do comprimento e onda
            n = B1 + B2 / Lambda_i ** 2 + B3 / Lambda_i ** 4

        # Quartzo
        elif 10 < material <= 11:
            B1, B2, B3, C1, C2, C3 = 2.356764950, -1.139969240E-2, 1.087416560E-2, 3.320669140E-5, 1.086093460E-5, 0
            n = sqrt(B1 + (B2 * Lambda_i ** 2) + (B3 / Lambda_i ** 2) + (C1 / Lambda_i ** 4) + (C2 / Lambda_i ** 6))

        # Metais
        elif 11 < material <= 15:
            # X - Define os comprimentos de onda em micrometro,
            # n - parte real do indice de refração e k - parte imaginária
            # tomando como base Johnson and Christy, 1972)

            if material == 12:  # Aluminio com base no modelo de Drude
                LambdaP, LambdaC = 1.0657E-7, 2.4511E-5
                n = sqrt(1 - (((wi ** 2) * LambdaC) / ((LambdaC + (j * wi)) * (LambdaP ** 2))))
            elif material == 13:  # Ouro
                X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313, 0.2371,
                     0.2426, 0.2490, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107, 0.3204, 0.3315,
                     0.3425, 0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714, 0.4959, 0.5209, 0.5486,
                     0.5821, 0.6168, 0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088, 1.216, 1.393, 1.61, 1.937, 3.5]

                n = [1.28, 1.32, 1.34, 1.33, 1.33, 1.30, 1.30, 1.30, 1.30, 1.31, 1.30, 1.32, 1.32,
                     1.33, 1.33, 1.35, 1.38, 1.43, 1.47, 1.49, 1.53, 1.53, 1.54,
                     1.48, 1.48, 1.50, 1.48, 1.46, 1.47, 1.46, 1.45, 1.38, 1.31, 1.04,
                     0.62, 0.43, 0.29, 0.21, 0.14, 0.13, 0.14, 0.16, 0.17, 0.22, 0.27, 0.35, 0.43, 0.56, 0.92, 1.8]

                k = [1.188, 1.203, 1.226, 1.251, 1.277, 1.304, 1.35, 1.387, 1.427, 1.46, 1.497, 1.536, 1.577, 1.631,
                     1.688, 1.749, 1.803, 1.847, 1.869, 1.878, 1.889, 1.893, 1.898, 1.883, 1.871, 1.866, 1.895, 1.933,
                     1.952, 1.958, 1.948, 1.914, 1.849, 1.833, 2.081, 2.455, 2.863, 3.272, 3.697, 4.103, 4.542, 5.083,
                     5.663, 6.35, 7.15, 8.145, 9.519, 11.21, 13.78, 25]

            elif material == 14:  # Prata
                X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313,
                     0.2371, 0.2426, 0.249, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107,
                     0.3204, 0.3315, 0.3425, 0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714,
                     0.4959, 0.5209, 0.5486, 0.5821, 0.6168, 0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088,
                     1.216, 1.393, 1.61, 1.937, 5]

                n = [1.07, 1.1, 1.12, 1.14, 1.15, 1.18, 1.2, 1.22, 1.25, 1.26, 1.28, 1.28, 1.3, 1.31, 1.33, 1.35,
                     1.38, 1.41, 1.41, 1.39, 1.34, 1.13, 0.81, 0.17, 0.14, 0.1, 0.07, 0.05, 0.05, 0.05, 0.04, 0.04,
                     0.05, 0.05, 0.05, 0.06, 0.05, 0.06, 0.05, 0.04, 0.03, 0.04, 0.04, 0.04, 0.04, 0.09, 0.13, 0.15,
                     0.24, 2]

                k = [1.212, 1.232, 1.255, 1.277, 1.296, 1.312, 1.325, 1.336, 1.342, 1.344, 1.357, 1.367, 1.378,
                     1.389, 1.393, 1.387, 1.372, 1.331, 1.264, 1.161, 0.964, 0.616, 0.392, 0.829, 1.142, 1.419,
                     1.657, 1.864, 2.07, 2.275, 2.462, 2.657, 2.869, 3.093, 3.324, 3.586, 3.858, 4.152, 4.483, 4.838,
                     5.242, 5.727, 6.312, 6.992, 7.795, 8.828, 10.1, 11.85, 14.08, 35]

            elif material == 15:  # Cobre
                X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313, 0.2371,
                     0.2426, 0.249, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107, 0.3204, 0.3315,
                     0.3425,
                     0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714, 0.4959, 0.5209, 0.5486, 0.5821,
                     0.6168,
                     0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088, 1.216, 1.393, 1.61, 1.937, 5]

                n = [0.94, 0.95, 0.97, 0.98, 0.99, 1.01, 1.04, 1.08, 1.13, 1.18, 1.23, 1.28, 1.34, 1.37, 1.41, 1.41,
                     1.45,
                     1.46, 1.45, 1.42, 1.4, 1.38, 1.38, 1.34, 1.36, 1.37, 1.36, 1.33, 1.32, 1.28, 1.25, 1.24, 1.25,
                     1.22, 1.18,
                     1.02, 0.7, 0.3, 0.22, 0.21, 0.24, 0.26, 0.3, 0.32, 0.36, 0.48, 0.6, 0.76, 1.09, 2.5]

                k = [1.337, 1.388, 1.44, 1.493, 1.55, 1.599, 1.651, 1.699, 1.737, 1.768, 1.792, 1.802, 1.799, 1.783,
                     1.741, 1.691,
                     1.668, 1.646, 1.633, 1.633, 1.679, 1.729, 1.783, 1.821, 1.864, 1.916, 1.975, 2.045, 2.116, 2.207,
                     2.305, 2.397,
                     2.483, 2.564, 2.608, 2.577, 2.704, 3.205, 3.747, 4.205, 4.665, 5.18, 5.768, 6.421, 7.217, 8.245,
                     9.439, 11.12, 13.43, 35]

            # Método que calcula os indices de refração dos metais atrevés de interpolação linear
            # baseado nos pontos contidos em X, n e k descritos anteriormente
            n_interp = interp(Lambda_i, X, n)
            k_interp = interp(Lambda_i, X, k)
            n = complex(n_interp, k_interp)

        elif material == 16:  # Indice de refração da água
            n = 1.33
        elif material == 17:  # Indice de refração do Ar
            n = 1.0000

        n0 = round(real(n), 5)  # Faz o arredondamento para 5 casas decimais
        k0 = round(imag(n), 5)  # Faz o arredondamento para 5 casas decimais

        return n0 + k0 * j  # Retorna o indice de refração complexo do metal com 5 casas decimais

    def setLayers(self, layer):
        # Determinação do material de cada camada
        if layer == 0:
            print("Camada 1 - Prisma")
            self.d.append(1)
            self.material.append((int(input(f"\n1 - BK7   2 - Sílica   3 - N-F2   4 - Safira sintética(Al2O3)"
                                            f"\n5 - SFL6  6 - FK51A    7 - N-SF14 8 - Acrilico SUVT   "
                                            f"\n\nMaterial -> "))))
        else:
            print(f"Camada {(layer + 1)}")
            self.material.append((int(input(f"\n 1 - BK7     2 - Sílica      3 - N-F2       4 - Safira sintética("
                                            f"Al2O3) "
                                            f"\n 5 - SFL6    6 - FK51A       7 - N-SF14     8 - Acrilico SUVT"
                                            f"\n 9 - PVA    10 - Glicerina  11 - Quartzo   12 - Aluminio"
                                            f"\n13 - Ouro   14 - Prata      15 - Cobre     16 - Água "
                                            f"\n17 - Ar    \n\nMaterial -> "))))

            self.d.append(float(input("Espessura (nm): ")) * 1e-9)  # Método que obtem a espessura das camadas

    def Reflectance(self, indice, theta_i, wavelenght):
        j = complex(0, 1)  # Simplificação do numero complexo "j"
        k0 = 2 * pi / wavelenght  # Número de onda

        """ Modelagem para o cálculo da reflectância baseada na forma matricial das equações de Fresnel descritas em: 
            * E. B. Costa, E. P. Rodrigues, and H. A. Pereira, “Sim-spr: An open-source surface plasmon resonance 
            simulator for academic and industrial purposes,” Plasmonics, vol. 14, no. 6, pp. 1699–1709, 2019."""

        self.b = []  # b_j -> Deslocamento de fase em cada camada
        self.q = []  # q_j -> Admitância de cada camada

        self.M = []  # M_j -> Matriz de transferência entre cada camada
        for layer in range(self.nLayers):
            self.b.append(k0 * self.d[layer] * sqrt(
                indice[layer] ** 2 - ((indice[0] * sin(theta_i)) ** 2)))

            self.q.append(
                sqrt(indice[layer] ** 2 - ((indice[0] * sin(theta_i)) ** 2)) /
                indice[layer] ** 2)

            # Calculo da matriz de transferencia entre as N camadas( N-1 interfaces)
            if layer < (self.nLayers - 1):
                self.M.append(array([[cos(self.b[layer]), (-j / self.q[layer]) * sin(self.b[layer])],
                                     [-j * self.q[layer] * sin(self.b[layer]), cos(self.b[layer])]]))

        Mt = self.M[0]  # M_total -> Matriz de transferência total do sistema
        for k in range(self.nLayers - 2):
            Mt = Mt @ self.M[k + 1]

        num = (Mt[0][0] + Mt[0][1] * self.q[self.nLayers - 1]) * self.q[0] - (
                Mt[1][0] + Mt[1][1] * self.q[self.nLayers - 1])
        den = (Mt[0][0] + Mt[0][1] * self.q[self.nLayers - 1]) * self.q[0] + (
                Mt[1][0] + Mt[1][1] * self.q[self.nLayers - 1])

        r = num / den  # 'r'-> Coeficiente de Fresnel

        return abs(r) ** 2  # Retorna a reflectância

    def ReflectanceAng(self, mod_int, s):
        self.Ri = []  # Armazena o valor de reflectância para cada ângulo de incidência e comprimento de onda

        # Se mod_int (modo de interrogação) == 1 -> calcula-se a reflectancia em função do ângulo de incidencia
        # Se mod_int (modo de interrogação) == 2 -> calcula-se a reflectancia em função do comprimento de onda
        if mod_int == 1:
            for t in range(len(self.theta_i)):
                self.Ri.append(self.Reflectance(self.indexRef, self.theta_i[t], self.wavelenght))
            return self.Ri
        else:
            for t in range(len(self.lambda_i)):
                self.indexRef = []  # Indice de refração reinicializado para cada comprimento de onda

                for m in range(self.nLayers):  # Cálculo do novo indice de refração para cada material
                    self.indexRef.append(self.set_index(self.material[m], self.lambda_i[t]))

                # Atualização do indice de refração da camada sensoriada para analise da sensibilidade
                self.index_analit = self.set_index(self.material[self.layer_ssr], self.lambda_i[t])
                self.indexRef[self.layer_ssr] = (
                    complex(round(self.index_analit.real + (self.passo_int * s), 4), 0))

                self.Ri.append(self.Reflectance(self.indexRef, self.theta_i, self.lambda_i[t]))

            return self.Ri  # Retorna a lista com todos os pontos da curva de ressônancia

    def Ponto_SPR(self, refletancia, modo):
        # O método Ponto_SPR retorna o ponto de ressonância da curva, seja angulo de ressonancia em graus
        # ou comprimento do onda de ressonancia em nanômetros

        c = refletancia.index(min(refletancia))  # Recebe a posição do ponto mínimo da curva
        if modo == 1:
            return self.theta_i[c] * (180 / pi)  # Retorna o ângulo em graus
        else:
            return self.lambda_i[c] * 1E9  # Retorna o compriento de onda em nanômetros

    def set_Rmed(self, s):
        if self.mod_int == 1:
            # Angulo de 0° a 90° para abranger uma faixa maior
            self.theta_i = arange(0, pi / 2, self.passo_ang)

            # Reflectancia que abrange toda faixa angular
            self.Rgeral = self.ReflectanceAng(self.mod_int, s)
            tam = len(self.theta_i)
        else:
            # Lambda de 150 nm a 2500 nm para abranger uma faixa maior no espectro
            self.lambda_i = arange(150E-9, 2500E-9, self.passo_ang)

            # Reflectancia que abrange toda faixa delimitada. Sujeita a alteração a depender da necessidade.
            self.Rgeral = self.ReflectanceAng(self.mod_int, s)
            tam = len(self.lambda_i)

        y1 = list(self.Rgeral)  # Lista com os valores da reflectancia
        c = y1.index(min(self.Rgeral))  # Recebe a posição do ponto mínimo da curva
        yleft = self.Rgeral[0:(c + 1)]  # Parte esquerda da curva
        yright = self.Rgeral[c:(tam + 1)]  # Parte direita da curva

        max_left = max(yleft)  # Máximo da parte esquerda
        min_left = min(yleft)  # Mínimo da parte esquerda
        max_right = max(yright)  # Máximo da parte direita
        min_right = min(yright)  # Mínimo da parte direita

        ymed1 = (max_left + min_left) / 2  # Ponto médio da parte esquerda
        ymed2 = (max_right + min_right) / 2  # Ponto médio da parte direita

        ymedf = (ymed2 + ymed1) / 2  # Altura média entre o ponto médio a esquerda e o ponto médio a direita

        return ymedf  # Retorna a altura média

    def fwhm(self, med_y):
        # O método fwhm recebe o valor da meia altura(med_y) calcula a largura total a meia altura da curva (f)

        # Lista do eixo x em graus ou comprimento de onda
        self.xList = self.theta_i if self.mod_int == 1 else self.lambda_i

        self.yList2 = self.Rgeral  # Lista dos valores de reflectancia calculados em uma faixa máxima limitada

        # Cálculo para descobrir os pontos (x1 e x2) que estão à meia altura
        signs = sign(add(self.yList2, -med_y))

        zero_crossings = (signs[0:-2] != signs[1:-1])
        zero_crossings_i = where(zero_crossings)[0]

        # Usa-se uma método de interpolação ( lin_interp() ) para encontrar x1 e x2
        x1 = self.lin_interp(self.xList, self.yList2, zero_crossings_i[0], med_y)  # Ponto x1 da meia altura
        x2 = self.lin_interp(self.xList, self.yList2, zero_crossings_i[1], med_y)  # Ponto x2 da meia altura

        f = abs((x1 * 180 / pi) - (x2 * 180 / pi)) if self.mod_int == 1 else abs(x2 - x1) * 1E9
        return f  # Retorna a diferença |X2 - X1| em graus ou nanômetros

    def lin_interp(self, x, y, i, h):
        # Interpolação linear para calcular os valores de x
        return x[i] + (x[i + 1] - x[i]) * ((h - y[i]) / (y[i + 1] - y[i]))

    def sensibilidade_analise(self, i):
        # O método sensibilidade_analise() recebe o numero (i) de variações do indice de refração do analito,
        # calcula (1) a curva de reflectancia, (2) o ponto de ressonancia, (3) a sensibilidade para cada interação
        # e exibe os resultados pelo método - exibir_resultados()

        for s in range(i):
            if self.mod_int == 1:
                # Atualização dos indices de refração para analise da sensibilidade angular
                for t in range(len(self.theta_i)):
                    self.indexRef = []  # Indice de refração reinicializado para cada uma das 's' interações

                    for m in range(self.nLayers):  # Cálculo do novo indice de refração para cada material
                        self.indexRef.append(self.set_index(self.material[m], self.wavelenght))

                    # Atualização do indice de refração da camada sensoriada para analise da sensibilidade
                    self.index_analit = self.set_index(self.material[self.layer_ssr], self.wavelenght)
                    self.indexRef[self.layer_ssr] = (
                        complex(round(self.index_analit.real + (self.passo_int * s), 4), 0))

            # Variável local que armazena temporariamente os valores de refletancia par acada uma das 's' interações
            reflet = self.ReflectanceAng(self.mod_int, s)

            # Preenchimento do array com os indices de refração do analito para plotagem dos graficos
            self.index_ref_ana.append(self.indexRef[self.layer_ssr])

            # Ponto de ressonância pelo valores fornecidos a partir do grafico em graus ou nanometros
            self.ponto_ressonancia.append(self.Ponto_SPR(reflet, self.mod_int))

            # Faz o calculo do ângulo crítico de reflexão interna para o modo de interrogação angular
            if self.mod_int == 1:
                self.ponto_critico.append(abs(arcsin(self.index_analit / self.indexRef[0]) * (180 / pi)))

            self.R.append(reflet)  # Armazena os arrays com as curvas de reflectancia para cada uma das 's' interações

            # Calcula a sensibilidade pelo valores obtidos a partir do grafico
            delta_angulo = self.ponto_ressonancia[s] - self.ponto_ressonancia[0]  # Variação do ponto de ressonâcia
            delta_indice = self.indexRef[self.layer_ssr].real - self.index_analit.real  # Variação do indice de refração

            # Calcula a Sensibilidade como (Variação do ponto de ressonâcia )/(Variação do indice de refração)
            if s == 0:
                self.S.append(0)  # Inicializa-se em zero a primeira interação pois a razão ficaria 0/0
            else:
                # Apenas a partir da segunda interação a sensibilidade é considerada
                self.S.append(delta_angulo / delta_indice)
                self.S[0] = self.S[1]

            # Calcula o FWHM apenas na primeira curva de reflectância
            if s == 0:
                Rmed = self.set_Rmed(s)
                self.Fwhm.append(self.fwhm(Rmed))

            # Reinicializa os arrays com os ângulos ou comprimentos de onda de incidencia para plotagem dos gráficos
            if self.mod_int == 1:
                self.theta_i = arange(self.a1, self.a2, self.passo_ang)
            else:
                self.lambda_i = arange(self.a1, self.a2, self.passo_ang)

        # Exibe os resultados
        self.exibir_resultados(s, delta_angulo)

    def exibir_resultados(self, s, delta_angulo):
        # O método exibir_resultados mostra no terminal de comando os resultados obtidos após as 's' interações
        # de variação do analito. Os reusltados fornecidos são:
        # (1) Ponto de ressonância na primeira interação (s=0), (2) Reflectancia mínima na primeira interação (s=0)
        # (3) Sensibilidade, (4) FWHM da primeira curva (s=0)
        # (5) Variação do ângulo ou comprimento de onda de ressonância após as 's' interações
        # (6) Detecção de acurácia (DA) e (7) Fator de qualidade (QF), todos em suas respectivas unidades

        c = '°' if self.mod_int == 1 else 'nm'  # Correspondência entre graus ou nanometros
        z = 'Theta' if self.mod_int == 1 else 'Lambda'  # Correspondência entre modo AIM ou WIM

        parametros = f"Ponto_de_ressonancia_SPR({c}) Refletancia_minima" \
                     f" Sensibilidade({c}/RIU) " \
                     f"FWHM({c}) Delta_{z}_SPR({c}) DA QF_(RIU-1) ".split()
        resultado = f"{self.ponto_ressonancia[0]:.5f} {min(self.R[0]):.5f} {self.S[s]:.5f} " \
                    f"{self.Fwhm[0]:.5f} {delta_angulo:.5f} " \
                    f"{(delta_angulo / self.Fwhm[0]):.5f} {(self.S[s] / self.Fwhm[0]):.5f} ".split()

        print(f"\nApós a {s + 1}° interação:\n")
        for i in range(len(parametros)):
            print(f"{parametros[i]:-<30}{resultado[i]:->15}")

    def plot(self, s, ind_ana):
        # O método plot() recebe o numero de interações 's' na variação do analito e o vetor ind_ana com o
        # indice de refração do analito e então apresenta os gráficos:
        # (1) Curva de ressonancia,
        # (2) Deslocamentos da curva de ressonancia em função da variação do indice de refração
        # (3) Curva de Sesibilidade e (4) Curva dos pontos de ressonancia

        # Adaptação para os modos AIM ou WIM
        y = 'Ângulo' if self.mod_int == 1 else 'Comprimento de Onda'
        c = 'graus' if self.mod_int == 1 else 'nm'
        n = chr(952) if self.mod_int == 1 else chr(955)
        x = self.theta_i * (180 / pi) if self.mod_int == 1 else self.lambda_i * 1E9
        z = (180 / pi) if self.mod_int == 1 else 1E9

        legenda = []    # Array que armazena os rótulos da legenda

        font = dict(size=16, family='Times New Roman')  # Definição da fonte e tamanho
        plt.rc('font', **font)

        # Gráfico da curva de reflectância com detalhe para caixa de anotações informando os pontos de ressonância
        fig0, ax0 = plt.subplots(dpi=150)
        ax0.plot(x, (self.R[0]))
        ax0.set(xlabel=f'{y} de Incidência ({c})', ylabel='Reflectância')
        if self.mod_int == 1:   # Modo AIM
            texto = f"{n}$_C$ = {self.ponto_critico[0]:.4f} °" \
                    f"\n{n}$_S$$_P$$_R$ = {self.ponto_ressonancia[0]:.4f}° "
        else:       # Modo WIM
            texto = f"{n}$_S$$_P$$_R$ = {self.ponto_ressonancia[0]:.4f}nm"

        ax0.annotate(texto, (self.ponto_ressonancia[0], min(self.R[0])), xytext=(self.a1 * z, 0.1),
                     arrowprops=dict(color='b', shrink=0.1, width=0.4, headwidth=5, headlength=10),
                     bbox={'facecolor': 'white', 'edgecolor': 'gray'})
        plt.yticks(arange(0, 1.20, 0.20))
        ax0.grid()

        # Gráfico do deslocamento da curva de reflectância dado a variação do indice de refração do analito
        fig, ax = plt.subplots(dpi=150)
        l2 = []  # Armazena os valores no eixo x nos graficos da sensibilidade e ponto de ressonancia
        for i in range(s):
            ax.plot(x, self.R[i])
            legenda.append(fr"$n_a$  = {ind_ana[i].real:.4f}")
            l2.append(f"{ind_ana[i].real:.3f}")

        ax.set(xlabel=f'{y} de Incidência ({c})', ylabel='Reflectância')
        ax.grid(alpha=0.25)
        ax.legend(legenda, bbox_to_anchor=(0, 1, 1, 1), mode='expand', ncol=4, loc='lower center', fontsize=14)
        plt.yticks(arange(0, 1.20, 0.20))

        # Gráfico da Sensibilidade

        # Formatação dos eixos x e y
        plt.rcParams['xtick.color'] = 'b'
        plt.rcParams['ytick.color'] = 'b'

        fig2, ax2 = plt.subplots(dpi=150)
        ax2.plot(real(ind_ana), self.S, '-^', linewidth=0.8, markersize=7, c='b')
        ax2.grid()
        ax2.set_title("Sensibilidade", fontsize=14, loc='center', color='b', pad='6')
        ax2.set_xticks(real(ind_ana))
        ax2.set_xticklabels(l2, rotation=45)
        ax2.set_yticks(self.S)

        # Gráfico da variação dos pontos de ressonância devido a variação do indice de refração
        fig3, ax3 = plt.subplots(dpi=150)
        ax3.plot(real(ind_ana), self.ponto_ressonancia, '-^', linewidth=0.8, markersize=7, c='b')
        ax3.grid()
        ax3.set_title(f"\n{n}$_S$$_P$$_R$", loc='center', color='b', pad='6')
        ax3.set_xticks(real(ind_ana))
        ax3.set_xticklabels(l2, rotation=45)
        ax3.set_yticks(self.ponto_ressonancia)

        plt.show()


simulaca1 = SPR()
