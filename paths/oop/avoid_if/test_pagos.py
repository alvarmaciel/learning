import pytest
from pagos import TarjetaDeCredito, PayPal, Bitcoin

"""
Imagina que estás desarrollando un sistema de pagos en línea.
Crea una jerarquía de clases para representar diferentes métodos de pago: TarjetaDeCredito, PayPal y Bitcoin.
Cada clase debe implementar un método procesar_pago(cantidad) que procese el pago de manera específica.
Usa polimorfismo para evitar estructuras if al procesar una lista de pagos.
"""

def test_procesar_pago_tarjeta():
    tarjeta = TarjetaDeCredito()
    assert tarjeta.procesar_pago(100) == "Pago de 100 procesado con Tarjeta de Crédito"

def test_procesar_pago_paypal():
    paypal = PayPal()
    assert paypal.procesar_pago(200) == "Pago de 200 procesado con PayPal"

def test_procesar_pago_bitcoin():
    bitcoin = Bitcoin()
    assert bitcoin.procesar_pago(300) == "Pago de 300 procesado con Bitcoin"

def test_procesar_varios_pagos():
    pagos = [TarjetaDeCredito(), PayPal(), Bitcoin()]
    resultados = [pago.procesar_pago(100 * (i+1)) for i, pago in enumerate(pagos)]
    assert resultados == [
        "Pago de 100 procesado con Tarjeta de Crédito",
        "Pago de 200 procesado con PayPal",
        "Pago de 300 procesado con Bitcoin"
    ]
