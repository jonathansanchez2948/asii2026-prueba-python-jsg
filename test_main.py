"""Pruebas básicas de la página de despliegue continuo."""

import main


def test_html_contiene_titulo():
    assert "<h1>Despliegue continuo</h1>" in main.construir_html()


def test_html_contiene_info_ci():
    html = main.construir_html()
    for clave, valor in main.INFO_CI.items():
        assert clave in html
        assert valor in html


def test_html_contiene_todos_los_pasos():
    html = main.construir_html()
    for paso in main.PASOS_CI:
        assert paso in html
