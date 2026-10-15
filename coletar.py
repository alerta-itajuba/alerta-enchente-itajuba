import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

# Coordenadas de Itajubá-MG
LAT, LON = -22.4256, -45.4528

url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&hourly=precipitation&past_hours=24&forecast_hours=24"
    "&timezone=America%2FSao_Paulo"
)

with urllib.request.urlopen(url, timeout=30) as r:
    d = json.load(r)

horas = d["hourly"]["time"]
chuva = [x or 0 for x in d["hourly"]["precipitation"]]

# A lista tem 24h passadas + 24h futuras
passado = chuva[:24]
futuro = chuva[24:]

chuva_24h = round(sum(passado), 1)
prox_6h = round(sum(futuro[:6]), 1)
prox_24h = round(sum(futuro), 1)

# Limites de exemplo (depois ajuste com critérios da Defesa Civil)
if chuva_24h >= 80 or prox_6h >= 40:
    status = "ALERTA"
elif chuva_24h >= 50 or prox_6h >= 20:
    status = "ATENCAO"
else:
    status = "NORMAL"

agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

saida = {
    "status": status,
    "chuva_ultimas_24h_mm": chuva_24h,
    "chuva_proximas_6h_mm": prox_6h,
    "chuva_proximas_24h_mm": prox_24h,
    "atualizado_em": agora,
}

with open("dados.json", "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)

print(saida)
