import pytest

from src.leilao.excecoes import LanceInvalido
from src.leilao.dominio import Leilao, Usuario


@pytest.fixture
def vini():
    return Usuario("Vini", 100.0)


@pytest.fixture
def leilao():
    return Leilao("Celular")


def test_lance_decreases_from_carteira(vini, leilao):
    vini.propoe_lance(leilao, 50.0)

    assert vini.carteira == 50.0


def test_lance_smaller_than_carteira(vini, leilao):
    vini.propoe_lance(leilao, 1.0)

    assert vini.carteira == 99.0


def test_lance_equal_to_carteira(vini, leilao):
    vini.propoe_lance(leilao, 100.0)

    assert vini.carteira == 0.0


def test_lance_bigger_than_carteira(vini, leilao):
    with pytest.raises(LanceInvalido):
        vini.propoe_lance(leilao, 200.0)
