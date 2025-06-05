import binascii
import struct
#Receber a string contendo os dados hexadecimais do protocolo "Location Request/Reporting Protocol
print("Dados brutos em hex a serem analisados:")
lrrp = input()

#Separar os binarios para descobrir as coordenadas que estao sendo enviadas, resgatando ignorando os ultimos 8 bytes e extraindo
# para latitude e longitude

longitude_hex = lrrp[-24:-16]
latitude_hex = lrrp[-16:-8]

#Converte para inteiro (big endian)

latitude_hex = ''.join(reversed([latitude_hex[i:i+2] for i in range(0, 8, 2)]))
longitude_hex = ''.join(reversed([longitude_hex[i:i+2] for i in range(0, 8, 2)]))

latitude_int = struct.unpack("<i",bytes.fromhex(latitude_hex))[0]
longitude_int = struct.unpack("<i",bytes.fromhex(longitude_hex))[0]

#Converte para a escala GPS

longitude = ((longitude_int * (360/4294967295))+180)/2*-1
latitude = (latitude_int * (360/4294967295))

print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")
