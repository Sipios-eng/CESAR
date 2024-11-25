import requests
import time
import logging

# Configurar el registro
logging.basicConfig(
    filename='website_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_website(url):
    """Verifica si un sitio web está disponible."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logging.info(f"El sitio web {url} está disponible.")
        else:
            logging.warning(f"El sitio web {url} respondió con código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al intentar acceder al sitio web {url}: {e}")

def main(url, interval):
    """Monitoriza un sitio web de manera continua."""
    logging.info(f"Iniciando monitorización del sitio web: {url}")
    try:
        while True:
            check_website(url)
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Monitorización detenida por el usuario.")

if __name__ == "__main__":
    # URL del sitio web a monitorizar
    website_url = "http://localhost:8000"  # Reemplaza con la URL deseada
    # Intervalo de monitorización en segundos
    monitor_interval = 5  # Verifica cada 5 segundos

    main(website_url, monitor_interval)
