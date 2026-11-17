"""Página web básica con información del despliegue continuo (CI) del proyecto.

Uso:
    python main.py            # inicia el servidor en http://localhost:8000
    PORT=9000 python main.py  # usa otro puerto
"""

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Información del flujo de trabajo definido en .github/workflows/ci.yml
INFO_CI = {
    "Archivo": ".github/workflows/ci.yml",
    "Plataforma": "GitHub Actions",
    "Disparadores": "push y pull request hacia la rama main",
    "Sistema operativo": "ubuntu-latest",
    "Versiones de Python": "3.10, 3.11 y 3.12",
}

PASOS_CI = [
    "Descargar el código (actions/checkout)",
    "Configurar Python con caché de pip (actions/setup-python)",
    "Instalar dependencias (flake8, pytest y requirements.txt si existe)",
    "Análisis estático con flake8",
    "Ejecutar pruebas con pytest",
]


def construir_html():
    """Genera el HTML de la página con la información del despliegue continuo."""
    filas = "".join(
        f"<tr><th>{clave}</th><td>{valor}</td></tr>" for clave, valor in INFO_CI.items()
    )
    pasos = "".join(f"<li>{paso}</li>" for paso in PASOS_CI)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Despliegue continuo</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; color: #222; }}
    h1 {{ color: #0b5cad; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; }}
    th {{ background: #f2f6fb; width: 35%; }}
  </style>
</head>
<body>
  <h1>Despliegue continuo</h1>
  <p>Información del flujo de integración continua de este proyecto.</p>
  <h2>Configuración</h2>
  <table>{filas}</table>
  <h2>Pasos del flujo</h2>
  <ol>{pasos}</ol>
</body>
</html>"""


class Manejador(BaseHTTPRequestHandler):
    """Responde con la página de información a cualquier petición GET."""

    def do_GET(self):
        cuerpo = construir_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)


def main():
    puerto = int(os.environ.get("PORT", "8000"))
    servidor = HTTPServer(("0.0.0.0", puerto), Manejador)
    print(f"Servidor iniciado en http://localhost:{puerto}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("Servidor detenido")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
