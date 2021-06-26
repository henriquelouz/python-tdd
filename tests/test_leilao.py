from unittest import TestCase
from src.leilao.excecoes import LanceInvalido
from src.leilao.dominio import Leilao, Usuario, Lance


class TestAvaliador(TestCase):
    def setUp(self):
        self.gui = Usuario("Gui", 500.0)
        self.lance_do_gui = Lance(self.gui, 150.0)
        self.leilao = Leilao("Celular")

    def test_range_lance_asc(self):
        yuri = Usuario("Yuri", 500.0)

        lance_do_yuri = Lance(yuri, 100.0)

        self.leilao.propoe(lance_do_yuri)
        self.leilao.propoe(self.lance_do_gui)

        menor_valor_esperado = 100.0
        maior_valor_esperado = 150.0

        self.assertEqual(menor_valor_esperado, self.leilao.menor_lance)
        self.assertEqual(maior_valor_esperado, self.leilao.maior_lance)

    def test_do_not_allow_desc_lance(self):
        with self.assertRaises(LanceInvalido):
            yuri = Usuario("Yuri", 500.0)

            lance_do_yuri = Lance(yuri, 100.0)

            self.leilao.propoe(self.lance_do_gui)
            self.leilao.propoe(lance_do_yuri)

    def test_single_entry(self):
        self.leilao.propoe(self.lance_do_gui)

        self.assertEqual(150.0, self.leilao.menor_lance)
        self.assertEqual(150.0, self.leilao.menor_lance)

    def test_triple_entry(self):
        vini = Usuario("Vini", 500.0)
        yuri = Usuario("Yuri", 500.0)

        lance_do_yuri = Lance(yuri, 100.0)
        lance_do_vini = Lance(vini, 200.0)

        self.leilao.propoe(lance_do_yuri)
        self.leilao.propoe(self.lance_do_gui)
        self.leilao.propoe(lance_do_vini)

        menor_valor_esperado = 100.0
        maior_valor_esperado = 200.0

        self.assertEqual(menor_valor_esperado, self.leilao.menor_lance)
        self.assertEqual(maior_valor_esperado, self.leilao.maior_lance)

    # se o leilao não tiver lances, deve permitir propor um lance
    def test_allow_without_lance(self):
        self.leilao.propoe(self.lance_do_gui)

        self.assertEqual(1, len(self.leilao.lances))

    # se o último usuário for diferente, deve permitir propor o lance
    def test_allow_user_different_from_last(self):
        yuri = Usuario("Yuri", 500.0)
        lance_do_yuri = Lance(yuri, 200.0)

        self.leilao.propoe(self.lance_do_gui)
        self.leilao.propoe(lance_do_yuri)

        self.assertEqual(2, len(self.leilao.lances))

    # se o último usuário for o mesmo, não deve permitir propor lance
    def test_do_not_allow_same_user_twice(self):
        lance_do_gui_2 = Lance(self.gui, 200.0)

        with self.assertRaises(LanceInvalido):
            self.leilao.propoe(self.lance_do_gui)
            self.leilao.propoe(lance_do_gui_2)
