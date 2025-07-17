import struct
from datetime import datetime

def extrair_timestamp_absoluto(pacote_hex):
    b = bytes.fromhex(pacote_hex[10:20])
    if len(b) < 5:
        raise ValueError("Pacote muito curto para conter timestamp absoluto.")
    b0, b1, b2, b3, b4 = b[0:5]

    base_year = 1759
    year   = (b0 << 2) | (b1 >> 6)
    month  = ((b1 & 0x3F) >> 2) + ((b2 >> 6) & 0x03)
    day    = (b2 >> 1) & 0x1F
    hour   = ((b2 & 0x01) << 4) | (b3 >> 4)
    minute = ((b3 & 0x0F) << 2) | (b4 >> 6)
    second = b4 & 0x3F

    return datetime(base_year + year, month, day, hour, minute, second)

def extrair_timestamp_relativo(pacote_hex):
    timestamp_hex = pacote_hex[8:16]
    timestamp_hex = ''.join(reversed([timestamp_hex[i:i+2] for i in range(0, 8, 2)]))
    return struct.unpack("<I", bytes.fromhex(timestamp_hex))[0]

def extrair_lat_lon(pacote_hex):
    longitude_hex = ''.join(reversed([pacote_hex[-24:-16][i:i+2] for i in range(0, 8, 2)]))
    latitude_hex = ''.join(reversed([pacote_hex[-16:-8][i:i+2] for i in range(0, 8, 2)]))
    latitude_int = struct.unpack("<i", bytes.fromhex(latitude_hex))[0]
    longitude_int = struct.unpack("<i", bytes.fromhex(longitude_hex))[0]

    longitude = ((longitude_int * (360 / 4294967295)) + 180) / 2 * -1
    latitude = (latitude_int * (360 / 4294967295))

    return latitude, longitude

# Entrada do usuário
print("Locat Req a ser analisado:")
locat_req = input().strip()
print("Locat Resp a ser analisado:")
locat_resp = input().strip()

# Decodificação
if len(locat_req) == 24:
    print("→ Location Request (12 bytes) detectado")
    try:
        tempo_absoluto = extrair_timestamp_absoluto(locat_req)
        print(f"Tempo Absoluto UTC: {tempo_absoluto}")
    except Exception as e:
        print(f"[X] Erro ao extrair timestamp absoluto: {e}")
else:
    print("→ Location Request não reconhecido ou malformado")

if len(locat_resp) == 42:
    print("→ Location Response (21 bytes) detectado")
    try:
        latitude, longitude = extrair_lat_lon(locat_resp)
        timestamp_rel = extrair_timestamp_relativo(locat_resp)
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Timestamp relativo: {timestamp_rel} ms desde o boot do rádio")
    except Exception as e:
        print(f"[X] Erro ao extrair dados do Location Response: {e}")
else:
    print("→ Location Response não reconhecido ou malformado")
