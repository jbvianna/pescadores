#!/usr/bin/env python3
# -*- coding: utf8 -*-
u""" Pescadores Tests - Regression tests for the pescadores library.

    Copyleft 2018 João Vianna (jvianna@gmail.com) e Ivan Wermelinger
    Este produto é distribuído sob os termos de licenciamento da
      'Apache License, Version 2.0'
    
    __author__ = "João Vianna <jvianna@gmail.com> e Ivan Wermelinger"
    __date__ = "18 Novembro 2018"
    __version__ = "0.10"
    
    History:
    Version 0.10 - Versão Inicial
"""
import unittest
import pescadores

# TODO: Testes para: Jogo, Mapa, Mercado, Porto

class TestPerigo(unittest.TestCase):
  def setUp(self):
    self.ventania = pescadores.Perigo(u'ventania', u'Ocorreu uma forte ventania.', 6, 5)
    self.tempestade = pescadores.Perigo(u'tempestade', u'Ocorreu uma tempestade!', 4, 7)

  def test_1_atributos(self):
    u""" Uma vez criados e inalterados, testar atributos e características básicas.
    """
    self.assertEqual(self.ventania.nome(), u'ventania')

    self.assertEqual(self.tempestade.nome(), u'tempestade')
    
  def test_2_valide_ventania(self):
    u""" Verifica se o método teste() funciona como esperado.
    """
    quantos_danos_graves = 0
    quantos_danos_leves = 0
    soma_testes_0_1 = 0
    
    for i in range(100):
      valor_teste = self.ventania.teste(0, 1, 0)
      if (valor_teste < -1):
        quantos_danos_graves += 1
      elif (valor_teste < 0):
        quantos_danos_leves += 1
      soma_testes_0_1 += valor_teste
        
    self.assertTrue(quantos_danos_leves > 0,
                    u'Testes não produziram danos leves.')
    self.assertTrue(quantos_danos_graves > 0,
                    u'Testes não produziram danos graves.')

    soma_testes_2_1 = 0

    for i in range(100):
      valor_teste = self.ventania.teste(2, 1, 0)
      soma_testes_2_1 += valor_teste
      
    # Com maior destreza, devia haver menos danos.
    self.assertTrue(soma_testes_0_1 < soma_testes_2_1,
                    u'Testes com maior destreza causaram mais danos.')

    soma_testes_0_3 = 0

    for i in range(100):
      valor_teste = self.ventania.teste(0, 3, 0)
      soma_testes_0_3 += valor_teste
      
    # Com maior resistencia, devia haver menos danos.
    self.assertTrue(soma_testes_0_1 < soma_testes_0_3,
                    u'Testes com maior resistência causaram mais danos.')

  def test_2_valide_tempestade(self):
    u""" Verifica se o método teste() funciona como esperado.
    """
    quantos_danos_graves = 0
    quantos_danos_leves = 0
    soma_testes_0_1 = 0
    
    for i in range(100):
      valor_teste = self.tempestade.teste(0, 1, 0)
      if (valor_teste < -1):
        quantos_danos_graves += 1
      elif (valor_teste < 0):
        quantos_danos_leves += 1
      soma_testes_0_1 += valor_teste
        
    self.assertTrue(quantos_danos_leves > 0,
                    u'Testes não produziram danos leves.')
    self.assertTrue(quantos_danos_graves > 0,
                    u'Testes não produziram danos graves.')

    soma_testes_2_1 = 0

    for i in range(100):
      valor_teste = self.tempestade.teste(2, 1, 0)
      soma_testes_2_1 += valor_teste
      
    # Com maior destreza, devia haver menos danos.
    self.assertTrue(soma_testes_0_1 < soma_testes_2_1,
                    u'Testes com maior destreza causaram mais danos.')

    soma_testes_0_3 = 0

    for i in range(100):
      valor_teste = self.tempestade.teste(0, 3, 0)
      soma_testes_0_3 += valor_teste
      
    # Com maior resistencia, devia haver menos danos.
    self.assertTrue(soma_testes_0_1 < soma_testes_0_3,
                    u'Testes com maior resistência causaram mais danos.')


class TestPesca(unittest.TestCase):
  u""" Testes para a classe Pesca
  """
  def setUp(self):
    self.pesqueiro_facil   = pescadores.Pesca(3, 50)
    self.pesqueiro_dificil = pescadores.Pesca(4, 50)
    self.pesqueiro_farto   = pescadores.Pesca(3, 250)

  def test_pesque(self):
    u""" Verifica se o método pesque() funciona como esperado.
    """
    quantos_danos_graves = 0
    quantos_danos_leves = 0
    soma_facil = 0
    
    for i in range(100):
      valor_teste = self.pesqueiro_facil.pesque(0)
      if (valor_teste < -1):
        quantos_danos_graves += 1
      elif (valor_teste < 0):
        quantos_danos_leves += 1
      else:
        soma_facil += valor_teste
        
    self.assertTrue(quantos_danos_leves > 0,
                    u'Testes não produziram danos leves.')
    self.assertTrue(quantos_danos_graves == 0,
                    u'Pesca fácil gerou danos graves.')
    
    self.assertTrue(soma_facil > 10,
                    u'Pesca fácil não resultou em peixes.')

    quantos_danos_graves = 0
    soma_dificil = 0

    for i in range(100):
      valor_teste = self.pesqueiro_dificil.pesque(0)
      if valor_teste < 1:
        quantos_danos_graves += 1
      elif valor_teste > 0:
        soma_dificil += valor_teste
      
    # Com maior dificuldade, devia haver menos pescado.
    self.assertTrue(soma_dificil < soma_facil,
                    u'Testes com maior dificuldade renderam mais pescado.')

    self.assertTrue(quantos_danos_graves > 0,
                    u'Pesca difícil não gerou danos graves.')
    
    soma_dificil_1 = 0

    for i in range(100):
      valor_teste = self.pesqueiro_dificil.pesque(1)
      if valor_teste > 0:
        soma_dificil_1 += valor_teste
        
    self.assertTrue(soma_dificil_1 > soma_dificil,
                    u'Pesca com maior habilidade não gerou resultado melhor.')

    soma_farto = 0

    for i in range(100):
      valor_teste = self.pesqueiro_farto.pesque(0)
      if valor_teste > 0:
        soma_farto += valor_teste
      
    # Com maior resistencia, devia haver menos danos.
    self.assertTrue(soma_facil < soma_farto,
                    u'Pesqueiro farto rendeu menos que o fácil.')


class TestPosicao(unittest.TestCase):
  def setUp(self):
    self.parati = pescadores.Posicao(u'Parati', u'Vila no RJ',
                                      -44.718944, -23.213494)
    
    self.parati.crie_porto()

    self.algodao = pescadores.Posicao(u'Ilha do Algodão', u'Pesqueiro abrigado',
                                      -44.593240, -23.225626)

    self.pendao = pescadores.Posicao(u'Lages do Pendão',
                                     u'Bom pesqueiro com ventos fortes',
                                     -44.401589, -23.180241)
    self.juatinga = pescadores.Posicao(u'Ponta da Juatinga',
                                       u'Local perigoso, sujeito a tempestades',
                                       -44.469046, -23.293542)

    self.pendao.defina_perigo(pescadores.Perigo(u'ventania',
                                                u'Ocorreu uma forte ventania.',
                                                6, 5))

    self.juatinga.defina_perigo(pescadores.Perigo(u'tempestade',u'Ocorreu uma tempestade!',
                                                  4, 7))

    self.parati.adicione_adjacencia(self.algodao)
    self.algodao.adicione_adjacencia(self.parati)
    self.algodao.adicione_adjacencia(self.pendao)
    self.algodao.adicione_adjacencia(self.juatinga)
    self.pendao.adicione_adjacencia(self.algodao)
    self.juatinga.adicione_adjacencia(self.algodao)

  def test_1_atributos(self):
    u""" Uma vez criados e inalterados, testar atributos e características básicas.
    """
    self.assertEqual(self.parati.nome(), u'Parati')
    self.assertEqual(self.parati.coordenadas(), (-44.718944, -23.213494))
    self.assertIsNotNone(self.parati.porto())
    self.assertIsInstance(self.parati.porto(), pescadores.Porto)
    self.assertIsNone(self.parati.perigo())
    self.assertIsNone(self.parati.pesqueiro())

    self.assertEqual(self.algodao.nome(), u'Ilha do Algodão')
    self.assertEqual(self.algodao.coordenadas(), (-44.593240, -23.225626))
    self.assertIsNone(self.algodao.porto())
    self.assertIsNone(self.algodao.perigo())
    self.assertIsNone(self.algodao.pesqueiro())

    self.assertEqual(self.pendao.nome(), u'Lages do Pendão')
    self.assertEqual(self.pendao.coordenadas(), (-44.401589, -23.180241))
    self.assertIsNone(self.pendao.porto())
    self.assertIsNotNone(self.pendao.perigo())
    self.assertIsInstance(self.pendao.perigo(), pescadores.Perigo)
    self.assertEqual(self.pendao.perigo().nome(), u'ventania')
    self.assertIsNone(self.pendao.pesqueiro())

    self.assertEqual(self.juatinga.nome(), u'Ponta da Juatinga')
    self.assertEqual(self.juatinga.coordenadas(), (-44.469046, -23.293542))
    self.assertIsNone(self.juatinga.porto())
    self.assertIsNotNone(self.juatinga.perigo())
    self.assertIsInstance(self.juatinga.perigo(), pescadores.Perigo)
    self.assertEqual(self.juatinga.perigo().nome(), u'tempestade')
    self.assertIsNone(self.juatinga.pesqueiro())
    
  def test_2_adjacencias(self):
    u""" Testar se adjacencias formam rede interligada e coerente.
    """
    self.assertEqual(len(self.parati.adjacencias()), 1)
    self.assertIn(self.algodao, self.parati.adjacencias())

    self.assertEqual(len(self.algodao.adjacencias()), 3)
    self.assertIn(self.parati, self.algodao.adjacencias())
    self.assertIn(self.pendao, self.algodao.adjacencias())
    self.assertIn(self.juatinga, self.algodao.adjacencias())

    self.assertEqual(len(self.pendao.adjacencias()), 1)
    self.assertIn(self.algodao, self.pendao.adjacencias())

    self.assertEqual(len(self.juatinga.adjacencias()), 1)
    self.assertIn(self.algodao, self.juatinga.adjacencias())


class TestBarco(unittest.TestCase):
  u""" Testes para a classe Barco
  """
  
  def setUp(self):
    self.saga = pescadores.Barco(u'simples', u'Saga', 1, 150, 1)
    self.fortuna = pescadores.Barco(u'reforçado', u'Fortuna', 2, 450, 3)
    self.fartura = pescadores.Barco(u'grande', u'Fartura', 5, 1200, 4)
    
  def test_1_atributos(self):
    u""" Uma vez criados e inalterados, testar atributos e características básicas.
    """
    self.assertEqual(self.saga.tipo(), u'simples')
    self.assertEqual(self.saga.nome(), u'Saga')
    self.assertIsNone(self.saga.posicao())
    self.assertEqual(self.saga.vagas(), 1)
    self.assertEqual(self.saga.carga_livre(), 150)
    self.assertEqual(self.saga.caracteristicas(), (1, 0))
    self.assertFalse(self.saga.em_atraso())
    
    self.assertEqual(self.fortuna.tipo(), u'reforçado')
    self.assertEqual(self.fortuna.nome(), u'Fortuna')
    self.assertEqual(self.fortuna.vagas(), 2)
    self.assertEqual(self.fortuna.carga_livre(), 450)
    self.assertEqual(self.fortuna.caracteristicas(), (3, 0))
    self.assertFalse(self.fortuna.em_atraso())

    self.assertEqual(self.fartura.tipo(), u'grande')
    self.assertEqual(self.fartura.nome(), u'Fartura')
    self.assertEqual(self.fartura.vagas(), 5)
    self.assertEqual(self.fartura.carga_livre(), 1200)
    self.assertEqual(self.fartura.caracteristicas(), (4, 0))
    self.assertFalse(self.fartura.em_atraso())
    
    
class TestPescador(unittest.TestCase):
  def setUp(self):
    self.joao = pescadores.Pescador(u'João')
    self.pedro = pescadores.Pescador(u'Pedro')
    
    self.saga = pescadores.Barco(u'simples', u'Saga', 1, 150, 1)
    
  def test_1_atributos(self):
    u""" Uma vez criados e inalterados, testar atributos e características básicas.
    """
    self.assertEqual(self.joao.nome(), u'João')
    self.assertEqual(self.joao.consulte_racoes(), 0)
    self.assertEqual(self.joao.consulte_saldo(), 0)
    self.assertEqual(self.joao.redes(), 0)
    self.assertEqual(self.joao.destreza_em_navegacao(), 0)
    self.assertEqual(self.joao.destreza_na_pesca(), 0)
    self.assertEqual(len(self.joao.barcos()), 0)

    self.assertEqual(self.pedro.nome(), u'Pedro')
    
  def test_2_bens(self):
    self.joao.adicione_barco(self.saga)
    self.joao.adicione_redes(2)
    self.joao.aumentar_destreza_na_pesca()
    
    self.pedro.aumentar_destreza_em_navegacao()
    
    self.assertEqual(self.joao.redes(), 2)
    self.assertEqual(self.joao.destreza_em_navegacao(), 0)
    self.assertEqual(self.joao.destreza_na_pesca(), 1)
    self.assertEqual(len(self.joao.barcos()), 1)
    self.assertIn(self.saga, self.joao.barcos())
    
    self.assertEqual(self.pedro.redes(), 0)
    self.assertEqual(self.pedro.destreza_em_navegacao(), 1)
    self.assertEqual(self.pedro.destreza_na_pesca(), 0)
    self.assertEqual(len(self.pedro.barcos()), 0)
    
    self.joao.aumentar_destreza_na_pesca()
    self.joao.remova_rede()
    self.joao.remova_barco(self.saga)
    
    self.assertEqual(self.joao.redes(), 1)
    self.assertEqual(self.joao.destreza_em_navegacao(), 0)
    self.assertEqual(self.joao.destreza_na_pesca(), 2)
    self.assertEqual(len(self.joao.barcos()), 0)
    
  def test_3_racoes(self):
    self.joao.adicione_racoes(10)
    self.pedro.adicione_racoes(6)
    
    self.assertEqual(self.joao.consulte_racoes(), 10)
    self.assertEqual(self.pedro.consulte_racoes(), 6)

    self.joao.adicione_racoes(5)
    self.pedro.desconte_racao()

    self.assertEqual(self.joao.consulte_racoes(), 12)
    self.assertEqual(self.pedro.consulte_racoes(), 5)
    
  def test_4_dinheiro(self):
    self.joao.credite(1000)
    self.pedro.credite(1800)
    
    self.assertEqual(self.joao.consulte_saldo(), 1000)
    self.assertEqual(self.pedro.consulte_saldo(), 1800)
    
    self.assertFalse(self.joao.debite(1200))
    self.assertEqual(self.joao.consulte_saldo(), 1000)
    
    self.pedro.credite(300)
    self.assertEqual(self.pedro.consulte_saldo(), 2100)

    self.assertTrue(self.joao.debite(300))
    self.assertEqual(self.joao.consulte_saldo(), 700)
    

    
if __name__ == '__main__':
  unittest.main()
  
