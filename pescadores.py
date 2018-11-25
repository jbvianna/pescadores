#!/usr/bin/env python3
# -*- coding: utf8 -*-
u""" Pescadores - Jogo de simulação situado em uma colônia de pescadores.

    Copyleft 2018 João Vianna (jvianna@gmail.com) e Ivan Wermelinger
    Este produto é distribuído sob os termos de licenciamento da
      'Apache License, Version 2.0'
    
    __author__ = "João Vianna <jvianna@gmail.com> e Ivan Wermelinger"
    __date__ = "26 Novembro 2018"
    __version__ = "0.95"
    
    History:
    Version 0.50 - Versão Inicial
    Version 0.80 - Estruturas do Jogo montadas
    Version 0.85 - Em testes, implementado o jornal
    Version 0.90 - Internacionalização - Português e Inglês
    Version 0.95 - Transferindo bens
"""
from __future__ import division

import string, os, sys

from os import path
from random import randint

import gettext
# Para desenvolvimento, sem internacionalização
_ = gettext.gettext

# Para ativar traduções em Inglês
# en = gettext.translation('pescadores', localedir='locales', languages=['en'])
# en.install()
# _ = en.gettext

try:
  # This works for Python 3
  import tkinter
  from tkinter import messagebox
except ImportError:
  # For Python 2, ...
  import Tkinter as tkinter
  import tkMessageBox as messagebox

# TODO: Fatorar e separar Jogo e subclasses em biblioteca
# TODO: Diálogos dentro da tela principal


def debug_print(msg):
  u""" Para depuração
  """
  print(msg)

def strtofloat(txt):
  u""" Auxiliar, para converter vírgulas em pontos (l10n)

      Parameters:
        txt:str - Texto a converter
      Returns
        float - Valor correspondente ao texto convertido para ponto flutuante.
  """
  return float(txt.replace(u',', u'.'))

# Estrutura interna do jogo

class Pescador:
  u""" Um personagem do jogo.

      Attributes:
        nome: string - Nome do pescador
        destreza_na_pesca: int - De 0 a 5, aumenta a chance de fazer uma boa pesca.
        destreza_em_navegacao: int - De 0 a 5, aumenta a chance de sucesso em tempestades, etc.
        posses: - bens que o pescador possui (dinheiro, redes, barcos, rações)
  """
  def __init__(self, nome):
    self._nome = nome
    self._destreza_na_pesca = 0
    self._destreza_em_navegacao = 0
    self._dinheiro = 0
    self._redes = 0
    self._racoes = 0
    self._barcos = []
    
  def nome(self):
    return self._nome

  def credite(self, valor):
    u""" Acrescenta um valor ao saldo do pescador.
    """
    self._dinheiro += valor
    
  def debite(self, valor):
    u""" Debita valor do saldo do pescador.

        Returns:
          True - Se o débito foi executado
          False - Se não havia saldo suficiente.
    """
    if self._dinheiro >= valor:
      self._dinheiro -= valor
      return True
    else:
      return False

  def consulte_saldo(self):
    u""" Consulta saldo em dinheiro.

        Returns:
          int - Saldo disponível para compras e transferências.
    """
    return self._dinheiro
    
  def adicione_barco(self, barco):
    u""" Transfere posse de um barco ao pescador.
    """
    self._barcos.append(barco)

  def remova_barco(self, barco):
    u""" Remove barco do pescador.
    """
    self._barcos.remove(barco)
    
  def barcos(self):
    u""" Retorna lista dos barcos que pertencem ao pescador.
    """
    return self._barcos

  def adicione_redes(self, quant):
    u""" Aumenta a quantidade de redes de um pescador.
    """
    self._redes += quant

  def remova_redes(self, quantas = 1):
    u""" Remove uma rede do pescador.
    
        Returns:
          True - Se havia rede para remover.
          False - Caso contrário.
    """
    if self._redes >= quantas:
      self._redes -= quantas
      return True
    else:
      return False
    
  def redes(self):
    u""" Indica quantas redes o pescador possui.

        Returns:
          int - Quantidade de redes
    """
    return self._redes

  def adicione_racoes(self, quant):
    u""" Aumenta quantidade de rações diárias do pescador.

        Nota: A quantidade final está limitada a 12. O excesso é perdido.
    """
    self._racoes += quant

    # Limite para a quantidade de ração que pode ser mantida sem se estragar.
    if self._racoes > 12:
      self._racoes = 12

  def desconte_racao(self):
    u""" Reduz as rações diárias em uma unidade.

        Returns:
          True - Se ainda havia rações disponíveis
          False - Se pescador já estava sem rações
    """
    if (self._racoes > 0):
      self._racoes -= 1
      return True
    else:
      return False
    
  def consulte_racoes(self):
    u""" Informa a quantidade de rações diárias restantes.

        Returns:
          int - Quantidade de rações restantes.
    """
    return self._racoes

  def destreza_em_navegacao(self):
    u""" Indica o nível de destreza em navegação.

         Quanto maior, mais fácil vencer os perigos de navegação.
        Returns:
          int - Nível de destreza
    """
    return self._destreza_em_navegacao
  
  def aumentar_destreza_em_navegacao(self):
    u""" Incrementa a destreza em navegação de 1 nível.
    """
    self._destreza_em_navegacao += 1
  
  def destreza_na_pesca(self):
    u""" Indica o nível de destreza na pesca.

        Returns:
          int - Nível de destreza
                Quanto maior, mais rende um lançamento da rede.
    """
    return self._destreza_na_pesca
  
  def aumentar_destreza_na_pesca(self):
    u""" Incrementa a destreza na pesca de 1 nível.
    """
    self._destreza_na_pesca += 1
  
    
class Barco:
  u""" Um barco que pode sair para a pesca.
  
      Attributes:
        tipo: string - Tipo de barco, conforme fabricante
        nome: string - Nome do barco
        lotacao: int - Quantos pescadores podem estar no barco
        capacidade: int - Quantos quilos de peixe cabem no barco
        resistencia: int - Resistência do casco às intempéries
        
        pescadores: [Pescador, ...] - Pescadores que estão no barco, limitado à lotação
        pescado: int - Quantidade de peixe no barco, em quilos
        atraso: int - Dias de atraso após passar por alguma intempérie
        posicao: Posicao - Posição em que se encontra o barco no mapa
  """
  def __init__(self, tipo, nome, lot, cap, resist):
    self._tipo = tipo
    self._nome = nome
    self._lotacao = lot
    self._capacidade = cap
    self._resistencia = resist
    self._pescadores = []
    self._pescado = 0
    self._atraso = 0
    self._danos = 0
    self._posicao = None
    
  def nome(self):
    return self._nome
  
  def tipo(self):
    return self._tipo

  def carregue(self, carga):
    u""" Transfere para o barco uma carga de peixes, em Kg.

         Nota: A carga final está limitada à capacidade do barco.

        Arguments:
          carga: int - Quantidade de peixes em Kg
    """
    self._pescado += carga
    if (self._pescado > self._capacidade):
      self._pescado = self._capacidade
      
  def descarregue(self):
    u""" Descarrega o pescado do barco.

        Returns:
          int - A quantidade descarregada, em Kg
    """
    quant = self._pescado
    self._pescado = 0
    return quant
  
  def reduza_carga(self):
    u""" Reduz carga do barco, por problemas na pesca ou navegação.
    """
    self._pescado = int(self._pescado / 2)
    
  def carga_livre(self):
    u""" Retorna a quantidade de carga que ainda cabe no barco em kg.
    
        Returns:
          int - Carga livre
    """
    return self._capacidade - self._pescado
  
  def desembarque(self, pescador):
    u""" Registra desembarque de um pescador.
    
        Parameters:
          pescador: Pescador - Quem está desembarcando
        Returns:
          True - Se o pescador estava no barco
          False - Caso contrário
    """
    if (pescador in self._pescadores):
      self._pescadores.remove(pescador)
      return True
    else:
      return False
    
  def embarque(self, pescador):
    u""" Embarca um pescador, se a lotação permite

        Parameters:
          pescador: Pescador - Quem está embarcando
        Returns:
          True - Se houve o embarque
          False - Se não havia espaço, ou pescador já estava embarcado
    """
    if ((self._lotacao <= len(self._pescadores)) or
         pescador in self._pescadores):
      return False
    else:
      self._pescadores.append(pescador)
      return True
    
  def vagas(self):
    u""" Indica quantas vagas para pescadores há no barco
    
      Returns:
        int - Quantidade de vagas
    """
    return self._lotacao - len(self._pescadores)

  def defina_posicao(self, posicao):
    u""" Estabelece posição do barco no mapa.
    
        Parameters:
          posicao: Posicao - Nova posição do barco
    """
    self._posicao = posicao
    
  def posicao(self):
    u""" Devolve posição do barco no mapa.
    
        Returns:
          Posicao - Posição do barco no mapa.
    """
    return self._posicao
  
  def atrase(self, dias):
    u""" Causa atraso para chegada do barco ao destino.
    
      Parameters:
        dias:int - Dias de atraso
    """
    self._atraso += dias
    
  def desconte_atraso(self):
    u""" Desconta um dia no atraso do barco
    
        Returns:
          True - Se conseguiu descontar o atraso
          False - Caso contrário
    """
    if self._atraso > 0:
      self._atraso -= 1
      return True
    return False
  
  def em_atraso(self):
    u""" Indica se o barco está atrasado
    
        Returns:
          True - Se o barco está atrasado
          False - Se o barco chegou ao destino
    """
    return self._atraso > 0
  
  def pescadores(self):
    u""" Devolve lista com os pescadores embarcados
    
        Returns:
        [Pescador, ...] - Lista com os pescadores embarcados.
    """
    return self._pescadores
  
  def caracteristicas(self):
    u"""  Indica características do barco para enfrentar intempéries.
    
        Returns:
          (int, int) - Resistência do casco e danos já sofridos
    """
    return (self._resistencia, self._danos)
  

class Perigo:
  u""" Um perigo, que exige um teste de navegação
      Attributes:
        nome: str - Tipo do perigo. Exemplos: tempestade, ventania, etc.
        descricao: str - pode ser usada nos diálogos que tratam do perigo.
        probabilidade: int - Valor de 0 a 6, que será comparado com um lançamento
          de dado para definir se o perigo se materializou.
          0 nunca acontece, 6 sempre acontece.
        dificuldade: int - Valor que será usado no teste de navegação.
          Quanto maior, mais chances de que os danos sejam grandes.
  """
  def __init__(self, nome, descr, prob, dif):
    self._nome = nome
    self._descricao = descr
    self._probabilidade = prob
    self._dificuldade = dif
    
  def nome(self):
    return self._nome
  
  def descricao(self):
    return self._descricao
    
  def teste(self, destreza, resistencia, danos):
    u""" Realiza um teste de destreza, para decidir se o perigo foi superado ou não.
      Returns:
        int - Valor maior ou igual a zero, para indicar que o perigo foi superado, ou
              negativo, indicando a quantidade de danos ocorridos.
    """
    dado = randint(1, 6)
    
    if dado <= self._probabilidade:
      # O perigo se materializou. Temos que testar a destreza dos navegadores.
      dado = randint(1, 6)

      # Independente da destreza, sempre há uma chance de tudo dar errado.
      if (dado == 1):
        return -1
      else:
        # A destreza dos navegadores e resistência do barco ajudam a superar o perigo.
        # A dificuldade e danos sofridos anteriormente agem no outro sentido.
        return dado + destreza + resistencia - self._dificuldade - danos
    else:
      return 1
    

class Pesca:
  u""" Atributos de pesca de uma posição
 
      Attributes:
        dificuldade: int - Valor que será usado no teste de pesca.
          Quanto maior, menos chances de sucesso na pescaria.
        rendimento: int - Rendimento máximo de pescado por rede lançada
  """
  def __init__(self, dif, rend):
    self._dificuldade = dif
    self._rendimento = rend

  def pesque(self, destreza):
    u""" Realiza um teste de destreza de pesca, para decidir como foi o lançamento de uma rede.
      Returns:
        int - Valor maior ou igual a zero indica a quantidade de pescado resultante, em Kg.
              negativo indica de danos ocorridos nas redes e outro material de pesca.
    """
    dado = randint(1, 6)
    
    # Independente da destreza, sempre há uma chance de tudo dar errado.
    if dado == 1:
      return 0
    else:
      resultado = int(dado + destreza - self._dificuldade)
      
      if resultado <= 0:
        return resultado
      else:
        if resultado > 5: resultado = 5
        return int(self._rendimento * resultado * 0.2)


class Mercado:    
  u""" Regula operações de compra e venda
  
      Attributes:
        preco_*: int - Preços dos diversos produtos
        
      Notes:
        Nos preços de cursos, o valor de cada posição é o custo de fazer um curso 
        para passar do nível anterior para este.
  """
  def __init__(self):
    self._preco_rede = 300
    self._preco_reparo = 200
    self._precos_cursos = [0, 200, 500, 800]

    # Preço de pescado e rações precisa ser calculado antes da operação.
    self._preco_pescado = 0
    self._preco_racao = 100000

  def defina_precos_do_dia(self):
    u""" Calcula os preços que variam diariamente, conforme o mercado.
    """
    self._preco_racao = 8 + 2 * randint(1, 6)
    self._preco_pescado = 3 + 2 * randint(1, 6)
    
  def consulte_precos(self):
    u""" Informa tabela de preços
    
        Returns:
          [(item:str, valor: int), ...] - Pares com nome do ítem e valor no mercado
    """
    precos = [(_(u'rede'), self._preco_rede),
              (_(u'ração'), self._preco_racao),
              (_(u'pescado'), self._preco_pescado),
              (_(u'curso de nível 1'), self._precos_cursos[1]),
              (_(u'curso de nível 2'), self._precos_cursos[2]),
              (_(u'curso de nível 3'), self._precos_cursos[3]),
              (_(u'barco simples'), 1000),
              (_(u'barco reforçado'), 1950)]
    return precos
    
    
  def fabrique_barco(self, tipo, nome):
    u""" Fabrica um novo barco com o tipo e nome dados.

        Returns:
          (barco: Barco, preco: int)
    """
    if (tipo == _(u'reforçado')):
      return (Barco(tipo, nome, 2, 400, 3), 1950)
    else:
      return (Barco(_(u'simples'), nome, 1, 150, 1), 1000)
    
  def venda_barco(self, pescador, barco, preco):
    u""" Vende um barco a um pescador.
    
        Attributes:
          pescador: Pescador - O pescador que está comprando o barco
          barco: Barco: - O barco sendo negociado
          preco: int - O valor do barco
          
        Returns:
          True - O barco foi vendido
          False - Não houve venda, por falta de dinheiro.
    """
    if pescador.debite(preco):
      pescador.adicione_barco(barco)
      return True
    return False
      
  def venda_racoes(self, pescador, quant):
    u""" Vende rações a um pescador.
    
        Attributes:
          pescador: Pescador - O pescador que está comprando as rações
          quant:int - Quantas diárias de ração
          
        Returns:
          True - Venda realidada
          False - Não houve venda, por falta de dinheiro.
    """
    if pescador.debite(quant * self._preco_racao):
      pescador.adicione_racoes(quant)
      return True
    else:
      return False

  def venda_redes(self, pescador, quant):
    u""" Vende redes a um pescador.
    
        Attributes:
          pescador: Pescador - O pescador que está comprando as redes
          quant:int - Quantas redes serão negociadas
          
        Returns:
          True - Venda realidada
          False - Não houve venda, por falta de dinheiro.
    """
    if pescador.debite(quant * self._preco_rede):
      pescador.adicione_redes(quant)
      return True
    else:
      return False
      
  def venda_curso_navegacao(self, pescador):
    u""" Vende um curso de navegação a um pescador.
    
        Attributes:
          pescador: Pescador - O pescador que está comprando o curso
          
        Notes:
          O curso é sempre para aumentar em um nível a destreza do pescador.
          Ver a tabela de cursos na descrição da classe.
          
        Returns:
          True - Venda realidada
          False - Não houve venda, por falta de dinheiro.
    """
    destreza_nova = pescador.destreza_em_navegacao() + 1
    
    if ((destreza_nova < len(self._precos_cursos)) and
        pescador.debite(self._precos_cursos[destreza_nova])):
      pescador.aumentar_destreza_em_navegacao()
      return True
    else:
      return False
    
  def venda_curso_pesca(self, pescador):
    u""" Vende um curso de pesca a um pescador.
    
        Attributes:
          pescador: Pescador - O pescador que está comprando o curso
          
        Notes:
          O curso é sempre para aumentar em um nível a destreza do pescador.
          Ver a tabela de cursos na descrição da classe.
          
        Returns:
          True - Venda realidada
          False - Não houve venda, por falta de dinheiro.
    """
    # TODO: Refatorar - ver venda_curso_navegacao()
    destreza_nova = pescador.destreza_na_pesca() + 1

    if ((destreza_nova < len(self._precos_cursos)) and
        pescador.debite(self._precos_cursos[destreza_nova])):
      pescador.aumentar_destreza_na_pesca()
      return True
    else:
      return False

  def compre_pescado(self, barco):
    u""" Operação de compra de pescado.

        Returns:
          int - Valor de crédito relativo à compra, a ser distribuído aos pescadores de direito.
    """
    return self._preco_pescado * barco.descarregue()

                     
class Porto:
  u""" Operações ligadas à estadia de barcos e pescadores em um porto.
  
      Attributes:
        pescadores_em_terra: [Pescador, ...] - Os pescadores que estão fora dos barcos
        barcos_em_terra: [Barco, ...] - Barcos aportados
        mercado: Mercado - Se este porto negocia bens
  """
  def __init__(self):
    self._pescadores_em_terra = []
    self._barcos_em_terra = []
    self._mercado = None
    
  def crie_mercado(self):
    u""" Associa um mercado a esse porto.
    """
    self._mercado = Mercado()
    
  def mercado(self):
    return self._mercado
  
  def tem_pescador(self, pescador):
    u""" Indica se certo pescador está no porto.
    
        Returns:
          True - se está
          False - se não está
    """
    return pescador in self._pescadores_em_terra
  
  def pescadores_em_terra(self):
    u""" Retorna lista dos pescadores que estão neste porto.
    
        Returns:
          [Pescador, ...]
    """
    return self._pescadores_em_terra

  def retorne_pescador(self, pescador):
    u""" Traz um pescador para este porto, se ele já não estava lá.

        Returns:
          True - Se o pescador foi retornado ao porto nesta operação.
          False - Se o pescador já estava neste porto.
    """
    if (not self.tem_pescador(pescador)):
      self._pescadores_em_terra.append(pescador)
      return True
    else:
      return False

  def remova_pescador(self, pescador):
    u""" Remove um pescador do porto, para que ele 'embarque'.
    
        Returns:
          True - Se o pescador estava no porto, e foi removido.
          False - Caso contrário
    """
    if (self.tem_pescador(pescador)):
      self._pescadores_em_terra.remove(pescador)
      return True
    else:
      return False

  def adicione_barco(self, barco):
    u""" Recebe um barco no porto, para atracação.
    """
    self._barcos_em_terra.append(barco)

  def remova_barco(self, barco):
    u""" Desatraca um barco, que sai para navegar.
    """
    self._barcos_em_terra.remove(barco)


class Posicao:
  u""" Uma posição geográfica que merece destaque
  
      Attributes:
        nome: str - Nome desta posição
        descricao: str - Uma descrição breve do lugar
        coord_*: int - Coordenadas desta posição
        adjacencias: [Posicao, ...] - Lista de posições adjacentes a esta
        perigo: Perigo - Perigo de navegação ao deixar esta posição, se houver
        pesca: Pesca - Características do pesqueiro, se houver
        porto: Porto - Se não nulo, indica que nesta posição existe um porto.
  """
  def __init__(self, nome, descr, coord_x, coord_y):
    self._nome = nome
    self._descricao = descr
    self._coord_x = coord_x
    self._coord_y = coord_y
    self._adjacencias = []
    self._perigo = None
    self._pesqueiro = None
    self._porto = None
    
  def nome(self):
    return self._nome
  
  def coordenadas(self):
    u""" Indicas coordenadas da posição em um par ordenado: (longitude, latitude)
    
        Notes:
          As coordenadas são dadas em graus e frações, relativas ao
          Equador e ao Meridiano de Greenwich
    """
    return (self._coord_x, self._coord_y)
    
  def adicione_adjacencia(self, pos):
    u""" Adiciona posição adjacente a esta em um mapa.
    """
    self._adjacencias.append(pos)
    
  def adjacencias(self):
    u""" Retorna lista de posições adjacentes a esta em um mapa.
    """
    return self._adjacencias
    
  def defina_perigo(self, perigo):
    u""" Associa um perigo a esta posição.
    
        Notes:
          O perigo se manifesta quando um barco deixa a posição.
    """
    self._perigo = perigo
    
  def perigo(self):
    # TODO: Múltiplos perigos?
    return self._perigo

  def defina_pesqueiro(self, pesca):
    u""" Associa características de pesqueiro a esta posição.
    """
    self._pesqueiro = pesca
    
  def pesqueiro(self):
    return self._pesqueiro
  
  def crie_porto(self):
    u""" Associa esta posição a um Porto, onde os barcos podem atracar.
    """
    self._porto = Porto()
    
  def porto(self):
    return self._porto
  

class Mapa:
  u""" Um mapa, com diversas posições e suas adjacências
  
      Attributes:
        arquivo imagem - Arquivo com a imagem correspondente ao mapa.
        se/nw - Coordenadas correspondentes às extremidades do mapa.
        largura/altura - Dimensões do mapa
        porto principal - O porto de onde saem os barcos,
          no início do jogo, e para onde retornam os barcos e pescadores resgatados.
        posicoes - lista de posições formando uma rede interligada
                    por rotas de navegação.
  """
  def __init__(self):
    self._arquivo_imagem = u''
    self._nw = None
    self._se = None
    self._largura = 0
    self._altura = 0
    self._posicoes = {}
    self._porto_principal = None
    
  def arquivo_imagem(self):
    return self._arquivo_imagem
  
  def dimensoes_imagem(self):
    u""" Retorna dimensões (horizontal, vertical) da imagem.
    """
    return (self._largura, self._altura)
  
  def posicao_na_imagem(self, posicao):
    u""" Mapeia coordenadas em graus e frações no mapa para coordenadas na tela.
    """
    nw = self._nw.coordenadas()
    se = self._se.coordenadas()
    coord = posicao.coordenadas()
    
    x = int(((coord[0] - se[0]) / (nw[0] - se[0])) * self._largura)
    y = int(((nw[1] - coord[1]) / (nw[1] - se[1])) * self._altura)
    return (x, y)

  def preencha_mapa(self, nome_arq):
    u""" Preenche o mapa com diversas posições interconectadas.
    
        Parameters:
          nome_arq:str - Arquivo que descreve o mapa.
    
        Notes:
          Pelo menos uma posição deve ter um porto com mercado,
          e uma outra deve ter um pesqueiro.
          O arquivo com a descrição do mapa tem formato .CSV,
          formando diversas tabelas, conforme descrito no corpo deste método.
              
    """
    mensagens = []
    arq_mapa = open(nome_arq, u'rb')
    
    # Estados possíveis: (I)nício, (D)imensões, (P)osições, (R)otas, Pes(Q)eiro,
    #                    Peri(G)o , (F)im
    # Sub-estado 0 - Esperando cabeçalho, Sub-estado 1 - Lendo dados.
    estado = u'I'
    
    for linha in arq_mapa.readlines():
      linha = linha.decode(u'utf-8').strip()
      campos = linha.strip(u'\t').split(u'\t')
      
      if (len(campos) > 0 and len(campos[0]) > 0):
        # Linha tem conteúdo
        if estado == u'I':
          if campos[0] == u'Pescadores – Mapa':
            estado = u'D0'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Falta cabeçalho.'))
            break
        elif estado == u'D0':
          if (linha.strip() == u'Largura\tAltura\tNorte\tSul\tLeste\tOeste\tImagem'):
            estado = u'D1'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Esperava dimensões.'))
            break
        elif estado == u'D1':
          if len(campos) == 7:
            self._largura = int(campos[0])
            self._altura = int(campos[1])
            self._nw = Posicao(u'NW', _(u'Noroeste'),
                               strtofloat(campos[5]), strtofloat(campos[2]))
            self._se = Posicao(u'SE', _(u'Sudeste'),
                               strtofloat(campos[4]), strtofloat(campos[3]))
            self._arquivo_imagem = campos[6]
            estado = u'P0'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Dimensões inválidas.'))
            break
        elif estado == u'P0':
          if (linha.strip() == u'Posição\tPrincipal\tPorto\tMercado\tLatitude\tLongitude\tDescrição'):
            estado = u'P1'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Esperava posições.'))
            break
        elif estado == u'P1':
          if len(campos) == 7:
            posicao = Posicao(campos[0], campos[6],
                              strtofloat(campos[5]), strtofloat(campos[4]))
            if campos[2] == u'S':
              posicao.crie_porto()
              if campos[3] == u'S':
                posicao.porto().crie_mercado()

            if campos[1] == u'S':
              self._porto_principal = posicao
              
            self._posicoes[campos[0]] = posicao
          else:
            estado = u'R0'
        elif estado == u'R1':
          if len(campos) == 2:
            origem = self._posicoes[campos[0]]
            destino = self._posicoes[campos[1]]
            origem.adicione_adjacencia(destino)
          else:
            estado = u'Q0'
        elif estado == u'Q1':
          if len(campos) == 3:
            posicao = self._posicoes[campos[0]]
            dificuldade = int(campos[1])
            rendimento = int(campos[2].strip())
            posicao.defina_pesqueiro(Pesca(dificuldade, rendimento))
          else:
            estado = u'G0'
        elif estado == u'Q1':
          if len(campos) == 3:
            posicao = self._posicoes[campos[0]]
            dificuldade = int(campos[1])
            rendimento = int(campos[2])
            posicao.defina_pesqueiro(Pesca(dificuldade, rendimento))
          else:
            estado = u'G0'
        elif estado == u'G1':
          if len(campos) == 5:
            posicao = self._posicoes[campos[1]]
            probabilidade = int(campos[2])
            dificuldade = int(campos[3])
            descricao = campos[4]
            posicao.defina_perigo(Perigo(campos[0], descricao, probabilidade, dificuldade))
          else:
            estado = u'F'

        # Nota: Aqui, o estado escorre sem ler nova linha. Não usar elif.
        if estado == u'R0':
          if (linha.strip() == u'Origem\tDestino'):
            estado = u'R1'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Esperava rotas.'))
            break
        elif estado == u'Q0':
          if (linha.strip() == u'Pesqueiro\tDificuldade\tRendimento'):
            estado = u'Q1'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Esperava pesqueiros.'))
            break
        elif estado == u'G0':
          if (linha.strip() == u'Perigo\tPosição\tProbabilidade\tDificuldade\tDescrição'):
            estado = u'G1'
          else:
            mensagens.append(_(u'Formato de arquivo inválido. Esperava perigos.'))
            break
        elif estado == u'F':
          mensagens.append(_(u'Formato de arquivo inválido. Linhas desconhecidas.'))
          
    arq_mapa.close()
    
    if self._porto_principal is None:
      mensagens.append(_(u'Mapa não contém um porto principal.'))
    elif self._porto_principal.porto() is None:
      mensagens.append(_(u'Porto principal indicado não é um porto.'))
    elif self._porto_principal.porto().mercado() is None:
      mensagens.append(_(u'Porto principal indicado não é um mercado.'))
      
    return mensagens
      
  def porto_principal(self):
    u""" Indica posição onde está o porto principal, com mercado.
    
        Returns:
          Posicao
    """
    return self._porto_principal
  
  def portos(self):
    u""" Retorna lista com portos neste mapa.
    
        Returns:
          [Porto, ...] - Os portos encontrados no mapa
    """
    l_portos = []
    for (nome, posicao) in self._posicoes.items():
      if posicao.porto() != None:
        l_portos.append(posicao)
        
    return l_portos
  
  def ache_posicao(self, nome):
    u""" Retorna posição associada ao nome dado.
    
        Returns:
          Posicao
    """
    return self._posicoes.get(nome)


class Jogo:
  u""" Mediador do jogo, que controla as sequências de ações entre as classes internas.
  
      Esta classe esconde o modelo interno de implementação do jogo, apresentando
      um protocolo com métodos que podem ser utilizados por diversas
      interfaces homem-máquina para apresentar o jogo ao usuário.
  
      Attributes:
        mapa - Dicionário com posições interconectadas
        pescadores - Dicionário com pescadores
        barcos - Dicionário de barcos
        jornadas_pendentes: [(nome_barco, jornada), ...] -
                            Lista de jornadas ainda não executadas pelos barcos
        preco_jornada:int - Preço do dia de trabalho no porto.
  """
  _mensagens = [_(u'Vocês são pescadores de uma colônia de pesca em uma vila tranquila.'),
    _(u'O pescado é farto, mas nos pontos onde há mais peixes também há perigos no mar.'),
    _(u'Nos pontos onde a pesca é mais frequente, é preciso evitar a sobre-pesca, garantindo que os peixes se reproduzam.'),
    u'',
    _(u'O dia a dia consiste em preparar os barcos para a pesca e sair para o mar.'),
    _(u'Para os pontos mais distantes, ou se a pesca for pouca, o barco pode ficar vários dias no mar.'),
    _(u'Na volta, o peixe é vendido no mercado, e o dinheiro arrecadado pode ser usado para comprar rações, equipamentos ou fazer cursos de aprimoramento.'),
    u'']
  
  def __init__(self):
    self._mapa = Mapa()
    self._pescadores = {}
    self._barcos = {}
    self._jornadas_pendentes = []
    self._preco_jornada = 30
    self._mapa.preencha_mapa(_(u'mapa_parati.csv'))
    
  def arquivo_imagem(self):
    u""" Retorna nome do arquivo com imagem do mapa.
    """
    return self._mapa.arquivo_imagem()
  
  def dimensoes_imagem(self):
    u""" Retorna dimensões do mapa (largura, altura) em pixels.
    """
    return self._mapa.dimensoes_imagem()
    
  def mensagens_iniciais(self):
    u""" Retorna lista de mensagens a serem apresentadas no início do jogo.
    
        Returns:
          [msg: str, ...] - Mensagens de apresentação do jogo
    """
    return self._mensagens
    
  def adicione_pescadores(self, nomes):
    u""" Adiciona jogadores ao jogo.

        Notes:
          Cada pescador inicia o jogo no porto principal, com R$2.000,00 e
          ração para 1 dia.
        Attributes:
          nomes: [str, ...] - Nomes dos jogadores/pescadores
    """
    for nome in nomes:
      if (self._pescadores.get(nome) == None):
        pescador = Pescador(nome)
        if (nome == _(u'Mestre')):
          pescador.credite(10000)     # Mestre é um jogador especial
        else:
          pescador.credite(2000)      # Cada jogador começa o jogo com R$2.000,00
        pescador.adicione_racoes(1)   # Para a primeira manhã

        self._pescadores[nome] = pescador
        self._mapa.porto_principal().porto().retorne_pescador(pescador)

  def prepare_alvorada(self):
    u""" Executa operações necessárias para preparar um novo dia do jogo.
    
        As operações incluem: Definir novos preços para cada mercado,
        publicar tabelas de preços e descontar rações diárias dos pescadores.
        
        Returns:
          [msg:str, ...] - Lista de mensagens geradas pelas operações.
    """
    mensagens = [u'', _(u'Começa um novo dia na vila.')]
    # Definir preços do dia em todos os mercados
    for pos_porto in self._mapa.portos():
      mercado = pos_porto.porto().mercado()
      if mercado != None:
        mercado.defina_precos_do_dia()
        precos = mercado.consulte_precos()
        msg = _(u'Preços no mercado de %s:\n') % pos_porto.nome()
        for (produto, preco) in precos:
          msg += _(u'%s: R$%d,00\n') % (produto, preco)
      mensagens.append(msg)
    
    porto_principal = self._mapa.porto_principal()

    # Descontar uma ração para cada pescador.
    for nome, pescador in self._pescadores.items():
      if ((nome != _(u'Mestre')) and (not pescador.desconte_racao())):
        # Pescador sem ração deve retornar ao porto principal.
        # Nota: O Mestre não consome rações.
        
        if (porto_principal.porto().retorne_pescador(pescador)):
          # O pescador não estava no porto principal.
          mensagens.append(_(u'%s ficou sem ração, e foi resgatado até o porto.') % nome)
          # Remover dos barcos e outros portos.
          for nome_barco, barco in self._barcos.items():
            if (barco.desembarque(pescador)):
              if (len(barco.pescadores()) == 0):
                # Se o barco ficou vazio, tem que voltar ao porto tambem.
                porto_principal.porto().adicione_barco(barco)
                barco.defina_posicao(porto_principal)
                mensagens.append(
                  _(u'Barco %s ficou sem tripulação, e foi rebocado até o porto.' ) %
                  barco.nome())
              achou = True
              break
          if (not achou):
            # Deve estar em algum porto
            for pos_porto in self._mapa.portos():
              if (pos_porto != porto_principal):
                pos_porto.porto().remova_pescador(pescador)
        else:
          mensagens.append(
            _(u'%s ficou sem ração, e teve que comprar uma ao preço do dia.') % nome)
          
          
        # Agora que o pescador está no porto principal,
        # venda para ele compulsoriamente uma ração, e desconte novamente.
        porto_principal.porto().mercado().venda_racoes(pescador, 1)
        pescador.desconte_racao()
        
    return mensagens
  
  def pescadores_nos_mercados(self):
    u""" Devolve nomes dos pescadores que estão em algum porto com mercado.
    
        Estes pescadores poderão fazer compras para obter os equipamentos e
        suprimentos necessários para sua jornada.
 
        Returns:
          [nome:str, ...] - Nomes dos pescadores
    """
    nomes = []
    
    # Encontrar pescadores que estão em portos com mercado.
    for pos_porto in self._mapa.portos():
      porto = pos_porto.porto()
      if porto.mercado() != None:
        pescadores = porto.pescadores_em_terra()
        
        for pescador in pescadores:
          nomes.append(pescador.nome())

    return nomes
  
  def atenda_pescador(self, nome, pedidos):
    u""" Atende aos pedidos de compras de um pescador.
    
        Attributes:
          nome: str - Nome do pescador
          pedidos: [(tipo_de_pedido: str, detalhe, ...), ...]
          
        Notes:
          Para as rotinas que se seguem, envolvendo transações com bens,
          As listas de bens/pedidos contêm tuplas, em que
          o primeiro elemento é o tipo de bem (barco, rações, etc) e
          os demais são detalhes, como quantidade, etc.
          Os tipos de bens incluem: barco, curso, rações, redes e dinheiro.
    """
    pescador = self._pescadores.get(nome)
    if pescador != None:
      for pos_porto in self._mapa.portos():
        porto = pos_porto.porto()
        if (porto.tem_pescador(pescador) and (porto.mercado() != None)):
          mercado = porto.mercado()
          for pedido in pedidos:
            if (pedido[0] == _(u'barco')):
              # TODO: Tabela de barcos no mercado
              nome_barco = pedido[2]
              (barco_novo, preco) = mercado.fabrique_barco(pedido[1], nome_barco)
              if mercado.venda_barco(pescador, barco_novo, preco):
                self._barcos[nome_barco] = barco_novo
                porto.adicione_barco(barco_novo)
                barco_novo.defina_posicao(pos_porto)
                
            elif (pedido[0] == _(u'curso')):
              if (pedido[1] == _(u'navegação')):
                mercado.venda_curso_navegacao(pescador)
              elif (pedido[1] == _(u'pesca')):
                mercado.venda_curso_pesca(pescador)
            elif (pedido[0] == _(u'rações')):
                mercado.venda_racoes(pescador, int(pedido[1]))
            elif (pedido[0] == _(u'redes')):
                mercado.venda_redes(pescador, int(pedido[1]))
            else:
              debug_print(_(u'Jogo::atenda_pescador() - Pedido inválido: ') + pedido[0])
          break
        
  def transfira_bens(self, nome_vendedor, nome_comprador, bens, contrato):
    u""" Transfere bens entre pescadores (também usado com o Mestre).
    
        Attributes:
          nome_*: str - Nome do vendedor e do comprador
          bens: [(tipo_de_bem: str, detalhe, ...), ...] - Bens a transferir, inclusive dinheiro.
          contrato: str - Razão da transferência (doação, compra e venda, etc)
        Returns:
          [msg: str, ...] - Mensagens
    """
    mensagens = []
    comprador = self._pescadores.get(nome_comprador)
    vendedor = self._pescadores.get(nome_vendedor)

    if comprador != None and vendedor != None:
      mensagens.append(_(u'Transação entre %s (comprador) e %s (vendedor) relativa a \n %s') %
                       (nome_comprador, nome_vendedor, contrato))

      # Primeiro passo: Validar a transação (saldo e número de redes.
      transferencia_valida = True
      for bem in bens:
        if (bem[0] == _(u'redes')):
          if vendedor.redes() < int(bem[1]):
            mensagens.append(_(u'O vendedor não tem o número de redes prometido.'))
            transferencia_valida = False
            break
        elif (bem[0] == _(u'dinheiro')):
          if comprador.consulte_saldo() < int(bem[1]):
            mensagens.append(_(u'O comprador não tem saldo para pagar a transação.'))
            transferencia_valida = False
            break
      if transferencia_valida:
         # Agora é pra valer...
        for bem in bens:
          if (bem[0] == _(u'barco')):
            barco = self._barcos[bem[2]]
            vendedor.remova_barco(barco)
            comprador.adicione_barco(barco)
            mensagens.append(_(u'Barco %s de nome %s') % (barco.tipo(), barco.nome()))
          elif (bem[0] == _(u'redes')):
            num_redes = int(bem[1])
            if vendedor.remova_redes(num_redes):
              comprador.adicione_redes(num_redes)
              mensagens.append(_(u'%d redes') % num_redes)
              
          elif (bem[0] == _(u'dinheiro')):
            valor = bem[1]
            if comprador.debite(valor):
              vendedor.credite(valor)
              mensagens.append(_(u'Valor: R$%d,00') % valor)
          else:
            debug_print(_(u'Jogo::transfira_bens() - Bem inválido: ') + bem[0])
    return mensagens
        
  def inventario_pescador(self, nome):
    u""" Retorna bens de um pescador em formato semelhante
        aos pedidos do método atenda_pescador().
        
        Returns:
          bens: [(tipo_de_bem, detalhe, ...), ...]
    """
    bens = []
    pescador = self._pescadores[nome]
    
    bens.append((_(u'rações'), pescador.consulte_racoes()))
    bens.append((_(u'dinheiro'), pescador.consulte_saldo()))
    
    for barco in pescador.barcos():
      bens.append((_(u'barco'), barco.tipo(), barco.nome()))
      
    bens.append((_(u'redes'), pescador.redes()))
    
    bens.append((_(u'curso'), _(u'navegação'), pescador.destreza_em_navegacao()))
    bens.append((_(u'curso'), _(u'pesca'), pescador.destreza_na_pesca()))
    return bens
  
  def estado_barco(self, nome_barco):
    u""" Retorna estado de um barco.
    
      Os dados retornados são aqueles que variam a cada jornada
      e podem ser utilizadas para se tomar decisões sobre a jornada seguinte:
      posição, coordenadas correspondentes, carga que ainda cabe no barco,
      pescadores embarcados e quantidade de redes em bom estado no barco.
    
      Returns:
        [(caracteristica:str, valor), ...]
    """
    barco = self._barcos[nome_barco]
    
    caracteristicas = []
    
    caracteristicas.append((_(u'posição'), barco.posicao().nome()))
    
    (x, y) = self._mapa.posicao_na_imagem(barco.posicao())
    caracteristicas.append((_(u'coordenadas'), u'(%d,%d)' % (x, y)))

    caracteristicas.append((_(u'capacidade restante'), str(barco.carga_livre())))
    
    quantas_redes = 0
    
    for pescador in barco.pescadores():
      caracteristicas.append((_(u'pescador'), pescador.nome()))
      quantas_redes += pescador.redes()
      
    caracteristicas.append((_(u'redes'), str(quantas_redes)))

    return caracteristicas
  
  def barcos_com_vaga(self):
    u""" Retorna os barcos que têm vagas para pescadores.
    
        Returns:
          [(nome_barco:str, vagas:int), ...]
    """
    barcos_vagas = []
    # TODO: Transformar em iterable, porque a cada embarque os pescadores disponíveis mudam.
    for (nome, barco) in self._barcos.items():
      if not barco.em_atraso():
        porto = barco.posicao().porto()
        if ((porto != None) and (barco.vagas() > 0)):
          barcos_vagas.append((nome, barco.vagas()))
    return barcos_vagas
  
  def pescadores_para_barco(self, nome_barco):
    u""" Retorna os pescadores que podem embarcar em um dado barco (no mesmo porto).
    
        Returns:
          [nome_pescador: str, ...]
    """
    nomes_pescadores = []
    barco = self._barcos[nome_barco]
    porto = barco.posicao().porto()
    if ((porto != None) and (barco.vagas() > 0)):
      for pescador in porto.pescadores_em_terra():
        # O Mestre não embarca.
        if (pescador.nome() != _(u'Mestre')):
          nomes_pescadores.append(pescador.nome())
    return nomes_pescadores
  
  def embarque(self, nome_barco, nomes_pescadores):
    u""" Embarca pescadores em um barco
    
        Attributes:
          nome_barco: str - O barco
          nomes_pescadores: [nome:str, ...] - Pescadores a embarcar
          
        Returns:
          [msg:str, ...] - Mensagens relativas às operações realizadas.
    """
    mensagens = []
    barco = self._barcos[nome_barco]
    porto = barco.posicao().porto()
    if porto != None:
      for nome_pescador in nomes_pescadores:
        if barco.vagas() < 1:
          mensagens.append(_(u'Vagas esgotadas no barco %s.') % nome_barco)
          break
        pescador = self._pescadores[nome_pescador]
        if porto.remova_pescador(pescador):
          mensagens.append(_(u'Embarcando %s no barco %s.') % (nome_pescador, nome_barco))
          barco.embarque(pescador)
    return mensagens

  def destrua_rede(self, nome_barco):
    u""" Remover a rede de algum pescador do barco indicado.
    
        Attributes:
          nome_barco:str - Nome do barco a penalizar.
    """
    pescador_escolhido = None
    barco = self._barcos[nome_barco]
    for pescador in barco.pescadores():
      if (pescador_escolhido == None or
          pescador_escolhido.destreza_pesca() > pescador.destreza_pesca()):
          pescador_escolhido = pescador

    pescador_escolhido.remova_redes(1)
        
  def credite_jornadas(self):
    u""" Creditar valor de uma jornada para cada pescador em terra.
    
        Returns:
          [msg:str, ...] - Mensagens descrevendo as operações realizadas.
    """
    mensagens = []
    for pos_porto in self._mapa.portos():
      for pescador in pos_porto.porto().pescadores_em_terra():
        # O Mestre não recebe.
        if (pescador.nome() != _(u'Mestre')):
          pescador.credite(self._preco_jornada)
          mensagens.append(_(u'%s recebeu R$%d,00 para trabalhar em %s.') %
                           (pescador.nome(),self._preco_jornada, pos_porto.nome() ))
    return mensagens
  
  def prepare_jornadas(self):
    u""" Preparar escolhas de jornada para cada barco tripulado.
    
        Returns:
          [(nome_barco:str, [jornada:str, ...]), ...] - Pares com nome do barco
            e lista de jornadas possíveis.
    """
    barcos_jornadas = []
    for nome_barco, barco in self._barcos.items():
      if len(barco.pescadores()) > 0:
        # Apenas barcos tripulados podem navegar ou pescar.
        if barco.em_atraso():
          self._jornadas_pendentes.append((nome_barco, _(u'descontar atraso')))
        else:
          jornadas = []
          posicao = barco.posicao()
          if barco.posicao().pesqueiro() != None:
            jornadas.append(_(u'pescar'))
          for destino in posicao.adjacencias():
            jornadas.append(_(u'navegar para %s') % destino.nome())
          if len(jornadas) > 0:
            barcos_jornadas.append((nome_barco, jornadas))
    return barcos_jornadas

  def adicione_jornada(self, nome_barco, jornada):
    u""" Define jornada para um barco
    
        As jornadas podem ser pescar, descontar atraso ou navegar para um destino.
    
        Attributes:
          nome_barco: str - O barco
          jornada: str - Indica o que o barco irá fazer
    """
    self._jornadas_pendentes.append((nome_barco, jornada))

  def execute_jornadas(self):
    u""" Executa as jornadas pendentes para todos os barcos.
    
        As jornadas pendentes são as que foram incluídas através do método
        adicione_jornada().
        
        Returns:
          [msg:str, ...] - Lista de mensagens relativas às operações realizadas.
    """
    mensagens = [u'']

    while (len(self._jornadas_pendentes) > 0):
      (nome_barco, jornada) = self._jornadas_pendentes.pop()
      barco = self._barcos[nome_barco]
      posicao_atual = barco.posicao()
      
      barco_chegou = False
      barco_pescou = False
      
      prefixo = _(u'navegar para ')

      if jornada.startswith(prefixo):
        destino = jornada[len(prefixo):].strip()

        mensagens.append(_(u'Barco %s navegando de %s a %s.') %
                         (nome_barco, posicao_atual.nome(), destino))

        perigo = posicao_atual.perigo()

        if (perigo != None):
          (resistencia, danos) = barco.caracteristicas()
          destreza = 0
          for pescador in barco.pescadores():
            destreza += pescador.destreza_em_navegacao()

          dano = perigo.teste(destreza, resistencia, danos)
          
          if dano < -1:
            mensagens.append(perigo.descricao())

            # Dano grave
            if perigo.nome() == u'ventania':
              mensagens.append(
                _(u'Barco %s se atrasou 2 dias para chegar a %s.') % (nome_barco, destino))
              barco.atrase(2)
            else:
              # Danos severos fizeram o barco naufragar.
              mensagens.append(_(u'Barco %s naufragou perto de %s.') %
                              (nome_barco, posicao_atual.nome()))
              porto = self._mapa.porto_principal().porto()
              for pescador in barco.pescadores():
                barco.desembarque(pescador)
                porto.retorne_pescador(pescador)
                mensagens.append(_(u'%s foi resgatado e está de volta a %s.') %
                                 (pescador.nome(), self._mapa.porto_principal().nome()))

              # Barco foi destruído. Remover do jogo e do pescador.
              self._barcos.pop(nome_barco)
              for nome_pescador,pescador in self._pescadores.items():
                if barco in pescador.barcos():
                  pescador.remova_barco(barco)
                  break
          elif dano < 0:
            mensagens.append(perigo.descricao())

            # Dano leve
            if perigo.nome() == u'ventania':
              mensagens.append(
                _(u'Barco %s se atrasou 1 dia para chegar a %s.') % (nome_barco, destino))
              barco.atrase(1)
            else:
              mensagens.append(
                _(u'Barco %s perdeu parte da carga.') % nome_barco)
              barco.reduza_carga()
              barco_chegou = True
              
          else:
            barco_chegou = True
        else:
            barco_chegou = True

        if posicao_atual.porto() != None:
          posicao_atual.porto().remova_barco(barco)
          
        barco.defina_posicao(self._mapa.ache_posicao(destino))

      elif (jornada == _(u'pescar')):
        pesca = posicao_atual.pesqueiro()
        mensagens.append(_(u'Barco %s pescando em %s.') %
                         (nome_barco, posicao_atual.nome()))
        
        barco_pescou = True

        destreza = 0
        quantas_redes = 0
        
        for pescador in barco.pescadores():
          destreza += pescador.destreza_na_pesca()
          quantas_redes += pescador.redes()

        if quantas_redes > 2:
          quantas_redes = 2

        for i in range(quantas_redes):
          resultado = pesca.pesque(destreza)
        
          if resultado < -1:
            mensagens.append(_(u'Barco %s perdeu uma rede em %s.') %
                             (nome_barco, posicao_atual.nome()))
            self.destrua_rede(nome_barco)
          elif resultado <= 0:
            mensagens.append(_(u'Rede do barco %s voltou vazia em %s.') %
                             (nome_barco, posicao_atual.nome()))
          else:
            mensagens.append(_(u'Barco %s pescou %d quilos de peixe em %s.') %
                             (nome_barco, resultado, posicao_atual.nome()))
            barco.carregue(resultado)
 

      elif (jornada == _(u'descontar atraso')):
        barco.desconte_atraso()
        if barco.em_atraso():
          mensagens.append(_(u'Barco %s atrasado para chegar a %s.') %
                  (nome_barco, posicao_atual.nome()))
        else:
          barco_chegou = True
      else:
        debug_print(_(u'Jornada desconhecida para barco %s: %s') % (nome_barco, jornada))

      posicao = barco.posicao()
      if (barco_chegou or barco_pescou):
        (x,y) = self._mapa.posicao_na_imagem(posicao)
        mensagens.append(_(u'#coord:barco=%s;x=%d;y=%d') % (nome_barco, x, y))
        
      if barco_chegou:
        mensagens.append(_(u'Barco %s chegou em %s.') % (nome_barco, posicao.nome()))

        if posicao.porto() != None:
          porto = posicao.porto()
          mercado = porto.mercado()
          quota = 0
          # É preciso fazer uma cópia, porque vamos alterar a original.
          pescadores = list(barco.pescadores())

          if mercado != None:
            # Vender o pescado e distribuir entre os pescadores no barco
            valor = mercado.compre_pescado(barco)
            quota = int(valor / len(pescadores))
            
            mensagens.append(_(u'Barco %s vendeu pescado no valor de $R%d,00.') %
                    (nome_barco, valor))

          # Desembarcar pescadores
          for pescador in pescadores:
            pescador.credite(quota)
            porto.retorne_pescador(pescador)
            barco.desembarque(pescador)
            
          porto.adicione_barco(barco)

    msg_racoes = _(u'\nRações restantes: ')

    for (nome, pescador) in self._pescadores.items():
      msg_racoes += _(u'%s tem %d, ') % (nome, pescador.consulte_racoes())

    mensagens.append(msg_racoes)
    return mensagens
  
  def extratos_pescadores(self):
    u""" Retorna dicionário com os saldos em dinheiro de cada pescador no jogo.
    """
    extratos = {}
    for (nome, pescador) in self._pescadores.items():
      extratos[nome] = pescador.consulte_saldo()
    return extratos
  
  def transfira_valor(self, nome_vendedor, nome_comprador, valor, contrato):
    u""" Transfere valor em dinheiro de um pescador para outro, conforme contrato.
    
        Attributes:
          nome_vendedor:str - Nome do pescador que vai receber o valor.
          nome_comprador:str - Nome do pescador a ser debitado.
          valor:int - Valor a ser transferido.
          contrato:str - Razão da transferência.
          
        Returns:
          [msg:str, ...] - Mensagens relativas a operações realizadas.
    """
    mensagens = []
    if (self._pescadores[nome_comprador].debite(valor) and valor > 0):
      self._pescadores[nome_vendedor].credite(valor)
      mensagens.append(_(u'Pagamento de  %s a %s no valor de R$ %d,00 por:\n%s') %
                       (nome_comprador, nome_vendedor, valor, contrato))
    else:
      mensagens.append(_(u'Contrato com %s cancelado por falta de fundos de %s.') %
                       nome_vendedor, nome_comprador)
    return mensagens


if __name__ == '__main__':

  import webbrowser
  
  debug = 0

  # Versão e autor 
  nome_jogo = _(u'Pescadores')
  autor_jogo = _(u'João Vianna <jvianna@gmail.com> e\n Ivan Wermelinger')
  versao_jogo = u'0.95'

  raiz = tkinter.Tk()
  jogo_ativo = Jogo()
  
  def mostre_ajuda(event = None):
    webbrowser.open_new(_(u'./pescadores_manual.html'))

  def mostre_versao():
    u""" Mostra versao atual do programa.
    """
    msg = nome_jogo + _(u'\nVersão ') + versao_jogo + _(u'\nAutor: ') + autor_jogo
    messagebox.showinfo(_(u'Sobre Pescadores'), msg)

  # Parte do código de diálogos inspirada nos exemplos em:
  # http://www.python-course.eu/tkinter_labels.php

  def teste_digitos(valor):
    try:
      for digito in valor:
        if not digito.isdigit():
          debug_print(_(u'Valor não numérico: ') + valor)
          return False
      return True
    except:
        debug_print(_(u'Valor inválido: ') + valor)
        return False


  # Controle do Jogo, mantém o estado corrente.
  #
  # Máquina de estados para as telas do jogo.
  # m: Mensagens iniciais, p: Nomes dos pescadores, a: Alvorada - preparar nova jornada;
  # c: Compras, t: Tripulação - embarcar pescadores nos barcos;
  # r: Rumo - decidir rumo/tipo de jornada;
  # e: Entardecer - execução das jornadas escolhidas; x: terminar o jogo.

  class ControleJogo:
    def __init__(self, estado):
      self._estado = estado
      self._jornal = None
      self._canvas = None

    def defina_jornal(self, jornal):
      self._jornal = jornal

    def jornal(self):
      return self._jornal
      
    def mude_estado(self, estado):
      self._estado = estado
      
    def estado(self):
      return self._estado
    
    def defina_tela(self, canvas):
      self._canvas = canvas
    
    def tela(self):
      return self._canvas

  controle_jogo = ControleJogo(u'm')

  class DlgParticipantes:
    u""" Diálogo para definir nome dos participantes no jogo.
    """
    var_participantes = tkinter.StringVar()
    
    def __init__(self):
      self._janela = tkinter.Toplevel()
      self._janela.title(_(u'Pescadores - Participantes'))
      
      linhas = 0

      tkinter.Label(master = self._janela,
                    text = _(u'Diga o nome dos pescadores separados por vírgula:')).grid(
                      column = 0,
                      row = linhas, 
                      padx = 10, pady = 10,
                      sticky = tkinter.W)
                    
      linhas += 1

      self._participantes_entry = tkinter.Entry(master = self._janela, width = 50,
                                        textvariable = self.var_participantes)
      self._participantes_entry.grid(column = 0, row = linhas,
                                      padx = 10, pady = 10,
                                      sticky = tkinter.W)
      
      self._participantes_entry.focus()
      
      linhas += 1

      tkinter.Button(master = self._janela, text=_(u'Ok'),
                    command = self.adicione_participantes).grid(column = 0, row = linhas,
                                                        padx = 10, pady = 10,
                                                        sticky=tkinter.E)

      tkinter.Button(master = self._janela, text=_(u'Cancelar'),
                    command = self._termine).grid(column = 1, row = linhas,
                                                    padx = 10, pady = 10,
                                                    sticky=tkinter.W)
                    
      linhas += 1

      self._janela.rowconfigure(linhas, weight = 1)
      self._janela.columnconfigure(2, weight = 1)

      self._janela.bind(u'<Return>', self.adicione_participantes)
      self._janela.bind(u'<Escape>', self._termine)

    def adicione_participantes(self, event = None):
      u""" Armazena as opções a partir dos dados na tela.
      """
      participantes = self.var_participantes.get().split(',')
      self.var_participantes.set(u'')
      
      nomes = []

      for nome in participantes:
        nome = nome.strip()

        if nome != u'':
          nomes.append(nome)
          
      jogo_ativo.adicione_pescadores(nomes)
      self._termine()

    def _termine(self, *args):
      u""" Provoca fim do dialogo.
      """
      # self._janela.grab_release()
      self._janela.destroy()

    def show(self):
      u""" Mostra o dialogo e aguarda ateh que o mesmo seja finalizado.
      """
      self.var_participantes.set(u'')

      self._janela.grab_set()
      self._janela.bind(u'<Destroy>', self._termine)
      self._janela.wait_window()  

  opcoes_barco = {_(u'nenhum'), _(u'simples'), _(u'reforçado') }
  opcoes_curso = {_(u'nenhum'), _(u'pesca'), _(u'navegação')}


  class DlgMercado:
    u""" Diálogo do mercado: receber pedido de compras.
    """
    var_racoes = tkinter.StringVar()
    var_redes  = tkinter.StringVar()
    var_curso  = tkinter.StringVar()
    var_tipo_barco = tkinter.StringVar()
    var_nome_barco = tkinter.StringVar()

    
    def __init__(self, nome_pescador, saldo, racoes):
      self._nome_pescador = nome_pescador

      self._janela = tkinter.Toplevel()
      self._janela.title(_(u'Pescadores - Mercado'))
      
      so_digitos = (raiz.register(teste_digitos), u'%P')

      linhas = 0

      tkinter.Label(master = self._janela,
                    text = _(u'%s, você tem ') % nome_pescador).grid(column = 0,
                                                    row = linhas, 
                                                    padx = 10, pady = 10,
                                                    sticky = tkinter.W)

      tkinter.Label(master = self._janela,
                    text = _(u'R$%d,00') % saldo).grid(column = 1,
                                                    row = linhas, 
                                                    padx = 10, pady = 10,
                                                    sticky = tkinter.W)

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'e %d rações') % racoes).grid(column = 1,
                                                    row = linhas, 
                                                    padx = 10, pady = 10,

                                                    sticky = tkinter.W)

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'O que você quer comprar?')).grid(column = 0,
                                                  row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)
      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Rações (Você só pode manter 12!):')).grid(
                                                  column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._racoes_entry = tkinter.Entry(master = self._janela, width = 6,
                                        textvariable = self.var_racoes,
                                        validate = u'all',
                                        validatecommand = so_digitos)
      self._racoes_entry.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      self._racoes_entry.focus()
                    
      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Barco:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._barco_option = tkinter.OptionMenu(self._janela, self.var_tipo_barco, *opcoes_barco)
      
      
      self._barco_option.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      
      self.var_tipo_barco.set(_(u'nenhum'))

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Nome do barco:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._nome_barco_entry = tkinter.Entry(master = self._janela, width = 15,
                                        textvariable = self.var_nome_barco)
      self._nome_barco_entry.grid(column = 1, row = linhas, padx = 10, pady = 10,
                                  sticky = tkinter.E)
      
    
      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Redes:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._redes_entry = tkinter.Entry(master = self._janela, width = 2,
                                        textvariable = self.var_redes,
                                        validate = u'all',
                                        validatecommand = so_digitos)
      self._redes_entry.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Curso:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._curso_option = tkinter.OptionMenu(self._janela, self.var_curso, *opcoes_curso)
      
      
      self._curso_option.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      
      self.var_curso.set(_(u'nenhum'))

      linhas += 1

      tkinter.Button(master = self._janela, text=_(u'Ok'),
                    command = self.envie_pedidos).grid(column = 0, row = linhas,
                                                        padx = 10, pady = 10,
                                                        sticky=tkinter.E)

      tkinter.Button(master = self._janela, text=_(u'Cancelar'),
                    command = self._termine).grid(column = 1, row = linhas,
                                                    padx = 10, pady = 10,
                                                    sticky=tkinter.W)
                    
      linhas += 1

      self._janela.rowconfigure(linhas, weight = 1)
      self._janela.columnconfigure(2, weight = 1)

      self._janela.bind(u'<Return>', self.envie_pedidos)
      self._janela.bind(u'<Escape>', self._termine)

    def envie_pedidos(self, event = None):
      u""" Armazena as opções a partir dos dados na tela.
      """
      tipo_barco = self.var_tipo_barco.get().strip()
      nome_barco = self.var_nome_barco.get().strip()
      self.var_nome_barco.set("")

      racoes = int(self.var_racoes.get().strip())
      self.var_racoes.set(u'0')

      # Ler demais opções, acrescentar na tabela.
      redes = int(self.var_redes.get().strip())
      self.var_redes.set(u'0')

      curso = self.var_curso.get().strip()
      
      # Montar pedidos
      pedidos = []
      
      if (tipo_barco != _(u'nenhum')):
        pedidos.append((_(u'barco'), tipo_barco, nome_barco))
      
      if racoes > 0:
        pedidos.append((_(u'rações'), racoes))
        
      if redes > 0:
        pedidos.append((_(u'redes'), redes))
        
      if (curso != _(u'nenhum')):
        pedidos.append((_(u'curso'), curso))

      jogo_ativo.atenda_pescador(self._nome_pescador, pedidos)
      self._termine()

    def _termine(self, *args):
      u""" Provoca fim do dialogo.
      """
      # self._janela.grab_release()
      self._janela.destroy()

    def show(self):
      u""" Mostra o dialogo e aguarda ateh que o mesmo seja finalizado.
      """
      self.var_racoes.set(u'0')
      self.var_redes.set(u'0')

      self._janela.grab_set()
      self._janela.bind(u'<Destroy>', self._termine)
      self._janela.wait_window()  


  class DlgEmbarque:
    u""" Diálogo de embarque: completar tripulação de um barco.
    """
    def __init__(self, nome_barco, vagas, nomes_pescadores):
      self._nome_barco = nome_barco

      self._janela = tkinter.Toplevel()
      self._janela.title(_(u'Pescadores - Embarque'))
      
      linhas = 0

      tkinter.Label(master = self._janela,
                    text = _(u'O Barco %s tem %d vagas.') % (nome_barco, vagas)).grid(
                                                    column = 0,
                                                    row = linhas, 
                                                    padx = 10, pady = 10,
                                                    sticky = tkinter.W)

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Escolha a tripulação.')).grid(column = 0,
                                                  row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)
                    
                    
      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Pescadores:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      linhas += 1

      self._pescadores_list = tkinter.Listbox(self._janela, selectmode = tkinter.MULTIPLE,
                                              width = 50)

      for nome in nomes_pescadores:
        self._pescadores_list.insert(tkinter.END, nome)
        self._pescadores_list.focus()
        
      self._pescadores_list.grid(column = 0, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      
      linhas += 1

      tkinter.Button(master = self._janela, text=_(u'Ok'),
                    command = self.embarque).grid(column = 0, row = linhas,
                                                        padx = 10, pady = 10,
                                                        sticky=tkinter.E)

      tkinter.Button(master = self._janela, text=_(u'Cancelar'),
                    command = self._termine).grid(column = 1, row = linhas,
                                                    padx = 10, pady = 10,
                                                    sticky=tkinter.W)
                    
      linhas += 1

      self._janela.rowconfigure(linhas, weight = 1)
      self._janela.columnconfigure(2, weight = 1)

      self._janela.bind(u'<Return>', self.embarque)
      self._janela.bind(u'<Escape>', self._termine)

    def embarque(self, event = None):
      u""" Armazena as opções a partir dos dados na tela.
      """
      selecionados = self._pescadores_list.curselection()
      if len(selecionados) > 0:
        pescadores_selecionados = []
        for indice in selecionados:
          pescadores_selecionados.append(self._pescadores_list.get(indice))
          
        mensagens = jogo_ativo.embarque(self._nome_barco, pescadores_selecionados)
        for msg in mensagens:
          controle_jogo.jornal().adicione_mensagem(msg)

      self._termine()

    def _termine(self, *args):
      u""" Provoca fim do dialogo.
      """
      # self._janela.grab_release()
      self._janela.destroy()

    def show(self):
      u""" Mostra o dialogo e aguarda ateh que o mesmo seja finalizado.
      """
      self._janela.grab_set()
      self._janela.bind(u'<Destroy>', self._termine)
      self._janela.wait_window()  
    
  
  class DlgJornada:
    u""" Diálogo para escolher jornada de um barco.
    """
    def __init__(self, nome_barco, jornadas):
      self._nome_barco = nome_barco

      self._janela = tkinter.Toplevel()
      self._janela.title(_(u'Pescadores - Jornada'))
      
      linhas = 0

      tkinter.Label(master = self._janela,
                    text = _(u'Decida a jornada do Barco %s.') % nome_barco).grid(column = 0,
                                                    row = linhas, 
                                                    padx = 10, pady = 10,
                                                    sticky = tkinter.W)

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Jornadas:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      linhas += 1

      self._jornadas_list = tkinter.Listbox(self._janela, selectmode = tkinter.SINGLE,
                                            width = 50)

      for jornada in jornadas:
        self._jornadas_list.insert(tkinter.END, jornada)
        
      self._jornadas_list.grid(column = 0, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      
      self._jornadas_list.activate(0)
      self._jornadas_list.focus()
      
      linhas += 1

      tkinter.Button(master = self._janela, text=_(u'Ok'),
                    command = self.adicione_jornada).grid(column = 0, row = linhas,
                                                        padx = 10, pady = 10,
                                                        sticky=tkinter.E)

      tkinter.Button(master = self._janela, text=_(u'Cancelar'),
                    command = self._termine).grid(column = 1, row = linhas,
                                                    padx = 10, pady = 10,
                                                    sticky=tkinter.W)
                    
      linhas += 1

      self._janela.rowconfigure(linhas, weight = 1)
      self._janela.columnconfigure(2, weight = 1)

      self._janela.bind(u'<Return>', self.adicione_jornada)
      self._janela.bind(u'<Escape>', self._termine)

    def adicione_jornada(self, event = None):
      u""" Armazena a jornada escolhida para um barco.
      """
      selecionado = self._jornadas_list.curselection()
      
      if (len(selecionado) > 0):
        jornada_escolhida = self._jornadas_list.get(selecionado)
        jogo_ativo.adicione_jornada(self._nome_barco, jornada_escolhida)

        self._termine()

    def _termine(self, *args):
      u""" Provoca fim do dialogo.
      """
      # self._janela.grab_release()
      self._janela.destroy()

    def show(self):
      u""" Mostra o dialogo e aguarda ateh que o mesmo seja finalizado.
      """
      self._janela.grab_set()
      self._janela.bind(u'<Destroy>', self._termine)
      self._janela.wait_window()
      
      
  class DlgTransferencias():
    u""" Compra e venda de bens
    """
    var_comprador = tkinter.StringVar()
    var_vendedor = tkinter.StringVar()
    var_valor = tkinter.StringVar()
    var_redes = tkinter.StringVar()
    var_contrato = tkinter.StringVar()

    def __init__(self, extratos):
      self._redes_vendedor = 0
      self._opcoes_comprador = {}
      self._opcoes_vendedor = {}
      
      self._opcoes_comprador[_(u'nenhum')] = 0
      self._opcoes_vendedor[_(u'nenhum')] = 0

      for (nome, saldo) in extratos.items():
        self._opcoes_comprador[_(u'%s: R$%d,00') % (nome, saldo)] = saldo
        self._opcoes_vendedor[nome] = saldo
        
      self.var_valor.set(u'0')
      self.var_redes.set(u'0')
      self.var_contrato.set(u'')

      self._janela = tkinter.Toplevel()
      self._janela.title(_(u'Pescadores - Compra e Venda'))
      
      so_digitos = (raiz.register(teste_digitos), u'%P')

      linhas = 0

      tkinter.Label(master = self._janela,
                    text = _(u'Comprador:')).grid(column = 0,
                                                    row = linhas, 
                                                    padx = 10, pady = 10,
                                                    sticky = tkinter.W)

      self._comprador_option = tkinter.OptionMenu(self._janela, self.var_comprador,
                                               *self._opcoes_comprador)
      
      
      self._comprador_option.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      self._comprador_option.focus()
      self.var_comprador.set(_(u'nenhum'))

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Vendedor:')).grid(column = 0,
                                                  row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._vendedor_option = tkinter.OptionMenu(self._janela, self.var_vendedor,
                                                *self._opcoes_vendedor,
                                                command = self.consulte_bens_vendedor)
      
      self._vendedor_option.grid(column = 1, row = linhas, padx = 10, pady = 10,
                                 sticky = tkinter.E)
      
      self.var_vendedor.set(_(u'nenhum'))

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Barco:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      linhas += 1

      self._barcos_list = tkinter.Listbox(self._janela, selectmode = tkinter.MULTIPLE,
                                          height = 6, width = 50)

      self._barcos_list.grid(columnspan = 2, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)
      
      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Redes:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._redes_entry = tkinter.Entry(master = self._janela, width = 2,
                                        textvariable = self.var_redes,
                                        validate = u'all',
                                        validatecommand = so_digitos)
      self._redes_entry.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)

      linhas += 1


      tkinter.Label(master = self._janela,
                    text = _(u'Valor a transferir:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      self._valor_entry = tkinter.Entry(master = self._janela, width = 6,
                                        textvariable = self.var_valor,
                                        validate = u'all',
                                        validatecommand = so_digitos)

      self._valor_entry.grid(column = 1, row = linhas, padx = 10, pady = 10,
                          sticky = tkinter.E)

      linhas += 1

      tkinter.Label(master = self._janela,
                    text = _(u'Contrato Realizado:')).grid(column = 0, row = linhas, 
                                                  padx = 10, pady = 10,
                                                  sticky = tkinter.W)

      linhas += 1

      self._contrato_entry = tkinter.Entry(master = self._janela, width = 50,
                                            textvariable = self.var_contrato)
                                        
      self._contrato_entry.grid(columnspan = 2, row = linhas,
                                padx = 10, pady = 10,
                                sticky = tkinter.W)
      
      linhas += 1

      tkinter.Button(master = self._janela, text=_(u'Ok'),
                    command = self.transfira_bens).grid(column = 0, row = linhas,
                                                        padx = 10, pady = 10,
                                                        sticky=tkinter.E)

      tkinter.Button(master = self._janela, text=_(u'Cancelar'),
                    command = self._termine).grid(column = 1, row = linhas,
                                                    padx = 10, pady = 10,
                                                    sticky=tkinter.W)
                    
      linhas += 1

      self._janela.rowconfigure(linhas, weight = 1)
      self._janela.columnconfigure(2, weight = 1)

      self._janela.bind(u'<Return>', self.transfira_bens)
      self._janela.bind(u'<Escape>', self._termine)

    def consulte_bens_vendedor(self, nome, event = None):
      u""" Preenche a lista de barcos e n. de redes de acordo com vendedor.
      """
      bens_vendedor = jogo_ativo.inventario_pescador(self.var_vendedor.get().strip())
      
      # Começa com lista vazia
      self._barcos_list.delete(0, tkinter.END)
      self._barcos_list.insert(tkinter.END, _(u'nenhum'))
      for bem in bens_vendedor:
        if bem[0] == _(u'redes'):
          self._redes_vendedor = bem[1]
        elif bem[0] == _(u'barco'):
          self._barcos_list.insert(tkinter.END, bem[2])

    def transfira_bens(self, event = None):
      u""" Realiza a transferência sujeito a suficiência de fundos.
      """
      opcao_comprador  = self.var_comprador.get().strip()

      saldo_comprador = self._opcoes_comprador[opcao_comprador]

      nome_vendedor = self.var_vendedor.get().strip()

      valor = int(self.var_valor.get().strip())

      contrato = self.var_contrato.get().strip()

      if (opcao_comprador != _(u'nenhum') and nome_vendedor != _(u'nenhum')):
        if (valor < saldo_comprador):
          nome_comprador = opcao_comprador.split(u':')[0]

          # Montar lista de bens
          bens = []

          num_redes = int(self.var_redes.get().strip())

          if num_redes > 0:
            if num_redes <= self._redes_vendedor:
              bens.append((_(u'redes'), num_redes))
            else:
              messagebox.showwarning(_(u'Pescadores - Compra e Venda'),
                _(u'O vendedor não tem o número de redes prometido.'))
              # Permanece no mesmo estado.
              return

          selecionados = self._barcos_list.curselection()
          if len(selecionados) > 0:
            for indice in selecionados:
              bens.append((_(u'barco'), u'', self._barcos_list.get(indice)))

          if valor > 0:
            bens.append((_(u'dinheiro'), valor))

          mensagens = jogo_ativo.transfira_bens(nome_vendedor, nome_comprador, bens, contrato)
          for msg in mensagens:
            controle_jogo.jornal().adicione_mensagem(msg)
        else:
          messagebox.showwarning(_(u'Pescadores - Compra e Venda'),
            _(u'O comprador não tem saldo para realizar a transação.'))
          # Permanece no mesmo estado.
          return

      self._termine()

    def _termine(self, *args):
      u""" Provoca fim do dialogo.
      """
      # self._janela.grab_release()
      self._janela.destroy()

    def show(self):
      u""" Mostra o dialogo e aguarda ateh que o mesmo seja finalizado.
      """
      self._janela.grab_set()
      self._janela.bind(u'<Destroy>', self._termine)
      self._janela.wait_window()  


  class PainelJornal:
    u""" Um painel para mostrar as mensagens do jogo
    """
    def __init__(self):
      self._janela = tkinter.Toplevel()
      self._janela.title(_(u'Pescadores - Jornal'))

      self._rolagem = tkinter.Scrollbar(self._janela)
      self._jornal = tkinter.Text(self._janela,
                                  state = tkinter.NORMAL, wrap = tkinter.WORD)

      self._rolagem.pack(side = tkinter.RIGHT, fill = tkinter.Y)
      self._jornal.pack(side = tkinter.LEFT, fill = tkinter.Y)
      
      self._rolagem.config(command = self._jornal.yview)
      self._jornal.config(yscrollcommand=self._rolagem.set)
      
    def adicione_mensagem(self, msg):
      self._jornal.insert(tkinter.END, msg)
      self._jornal.insert(tkinter.END, u'\n')
      self._jornal.see(tkinter.END)


  def avance_tela(event = None):
    if controle_jogo.estado() == u'm':
      mensagens = jogo_ativo.mensagens_iniciais()
      for msg in mensagens:
        controle_jogo.jornal().adicione_mensagem(msg)
      controle_jogo.mude_estado(u'p')
      
      # Muda de estado e continua

    if controle_jogo.estado() == u'p':
      dlg = DlgParticipantes()
      dlg.show()
      if (len(jogo_ativo.pescadores_nos_mercados()) > 0):
        controle_jogo.jornal().adicione_mensagem( 
                          _(u'Esta é uma boa hora para fazer negócios.'))
        raiz.focus_set()
        controle_jogo.mude_estado(u'a')
      else:
        messagebox.showwarning(_(u'Pescadores - Nomes'),
          _(u'Parece que não há nenhum pescador no jogo. Tente incluir algum.'))
        
        # Permanece no mesmo estado, esperando por jogadores.
        return

    if controle_jogo.estado() == u'a':
      mensagens = jogo_ativo.prepare_alvorada()

      for msg in mensagens:
        controle_jogo.jornal().adicione_mensagem(msg)
        
      controle_jogo.mude_estado(u'c')

      # Sem pausa na transição de estado
      # elif controle_jogo.estado() == u'c':
      for nome in jogo_ativo.pescadores_nos_mercados():
        saldo = 0
        racoes = 0
        controle_jogo.jornal().adicione_mensagem( 
                          _(u'\n%s tem os seguintes bens:') % nome)

        for bem in jogo_ativo.inventario_pescador(nome):
          if bem[0] == _(u'rações'):
            controle_jogo.jornal().adicione_mensagem( 
                      u'%d %s' % (bem[1], bem[0]))
            racoes = bem[1]
          elif bem[0] == _(u'redes'):
            controle_jogo.jornal().adicione_mensagem( 
                      u'%d %s' % (bem[1], bem[0]))
          elif (bem[0] == _(u'dinheiro')):
            controle_jogo.jornal().adicione_mensagem( 
                      _(u'R$%d,00') % bem[1])
            saldo = bem[1]
          elif (bem[0] == _(u'barco')):
            controle_jogo.jornal().adicione_mensagem( 
                      _(u'Um %s %s de nome %s') % (bem[0], bem[1], bem[2]))
          elif (bem[0] == _(u'curso')):
            controle_jogo.jornal().adicione_mensagem( 
                      _(u'Proficiência %d em %s') % (bem[2], bem[1]))

        dlg = DlgMercado(nome, saldo, racoes)
        dlg.show()
        
      controle_jogo.mude_estado(u't')

      # elif estado == u't':
      # Para cada barco em um porto:
      #   embarcar pescadores no mesmo porto até a lotação do barco.
      for (nome_barco, vagas) in jogo_ativo.barcos_com_vaga():
        pescadores = jogo_ativo.pescadores_para_barco(nome_barco)
        if (len(pescadores) > 0):
          dlg = DlgEmbarque(nome_barco, vagas, pescadores)
          dlg.show()

      # Para cada pescador que ainda ficou em um porto:
      #   Creditar valor de uma jornada
      mensagens = jogo_ativo.credite_jornadas()

      controle_jogo.jornal().adicione_mensagem(u'\n')
      
      for msg in mensagens:
        # messagebox.showinfo(u'Pescadores - Pagamentos', msg)
        controle_jogo.jornal().adicione_mensagem(msg)

      controle_jogo.mude_estado(u'r')

      # Sem pausa na transição de estado
      # elif estado == u'r':
 
      for (nome_barco, jornadas) in jogo_ativo.prepare_jornadas():
        controle_jogo.jornal().adicione_mensagem(_(u'\nEstado do barco %s:') % nome_barco)

        caracteristicas = jogo_ativo.estado_barco(nome_barco)

        for (tipo, valor) in caracteristicas:
          controle_jogo.jornal().adicione_mensagem(u'  %s: %s' % (tipo, valor))
          
        dlg = DlgJornada(nome_barco, jornadas)
        dlg.show()

      controle_jogo.mude_estado(u'e')

      # Sem pausa na transição de estado
      # elif estado == _(u'e':
      mensagens = jogo_ativo.execute_jornadas()
      
      # Apaga posição de todos os barcos
      controle_jogo.tela().delete(_(u'barco'))

      marcas_barcos = {}
      for msg in mensagens:
        if msg.startswith(u'#coord:'):
          # Diretiva com coordenadas de barco.
          nome_barco = u''
          x = u'0'
          y = u'0'
          for param in msg[7:].split(u';'):
            prefixo = _(u'barco=')
            if param.startswith(prefixo):
              nome_barco = param[len(prefixo):]
            elif param.startswith(_(u'x=')):
              x = int(param[2:])
            elif param.startswith(_(u'y=')):
              y = int(param[2:])
          coord = (x, y)
          lista_barcos = marcas_barcos.get(coord, [])
          lista_barcos.append(nome_barco)
          marcas_barcos[coord] = lista_barcos
        else:
          controle_jogo.jornal().adicione_mensagem(msg)

      for (coord, lista_barcos) in marcas_barcos.items():
        (x,y) = coord
        nomes_barcos = u','.join(lista_barcos)
        controle_jogo.tela().create_text(x, y,
                                          text = nomes_barcos,
                                          tag = _(u'barco'),
                                          fill = u'red',
                                          anchor = tkinter.NW)
        
      controle_jogo.jornal().adicione_mensagem( 
                          _(u'Esta é uma boa hora para fazer negócios.'))
      raiz.focus_set()
      controle_jogo.mude_estado(u'a')
    else:
      messagebox.showerror(_(u'Pescadores - Erro'),
                             _(u'Estado inválido: ') + controle_jogo.estado())

      controle_jogo.mude_estado(u'a')

  def transfira_bens():
    u"""Transferencias de bens (compras, empréstimos/sociedades/pagamentos)
    """
    extratos = jogo_ativo.extratos_pescadores()
    
    dlg = DlgTransferencias(extratos)
    dlg.show()
    
  def termine_jogo(event = None):
    raiz.quit()


  def usage():
    print (_(u'Uso: python pescadores.py\n'))
    

  def my_main(argv, argc):
    if debug:
      print(argc)
      for arg in argv:
        print(u' ' + arg)

    if argc != 0:
      usage()
      return
    
    raiz.geometry(u'1280x720+20+20')
    raiz.title(nome_jogo + u' ' + versao_jogo)

    (largura, altura) = jogo_ativo.dimensoes_imagem()
    
    frame = tkinter.Frame(raiz, width = largura, height = altura)
    frame.pack()
    
    canvas = tkinter.Canvas(frame, width = largura, height = altura, offset = u'0,0')
    canvas.pack()

    img = tkinter.PhotoImage(file= jogo_ativo.arquivo_imagem())
    canvas.create_image(0, 0, anchor=tkinter.NW, image=img)
    
    controle_jogo.defina_tela(canvas)
    
    menu_raiz = tkinter.Menu(raiz)
    raiz.config(menu = menu_raiz)
    
    menu_jogo = tkinter.Menu(menu_raiz)
    menu_raiz.add_cascade(label = _(u'Jogo'), menu = menu_jogo)
    
    menu_jogo.add_command(label = _(u'Avançar'),
                          command = avance_tela, accelerator = u'Right Key')
    menu_jogo.add_command(label = _(u'Compra, Venda, Transferências ...'), command = transfira_bens)
    menu_jogo.add_command(label = _(u'Terminar'), command = termine_jogo)

    menu_ajuda = tkinter.Menu(menu_raiz)
    menu_raiz.add_cascade(label = _(u'Ajuda'), menu = menu_ajuda)
    
    menu_ajuda.add_command(label = _(u'Manual'), command = mostre_ajuda)

    menu_ajuda.add_command(label = _(u'Sobre o Jogo'), command = mostre_versao)
    
    controle_jogo.defina_jornal(PainelJornal())
    
    raiz.bind(u'<Right>', avance_tela)
    
    raiz.mainloop()
    

  my_main(sys.argv[1:], len(sys.argv) - 1)


