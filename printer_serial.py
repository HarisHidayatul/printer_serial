import requests

# Ganti dengan nama printer yang sesuai
printer_name = "EPSON_TM_U220B"

# URL untuk mendapatkan status printer melalui CUPS
cups_url = f"http://localhost:631/printers/{printer_name}"

# Mengirim permintaan GET ke CUPS untuk mendapatkan status printer
try:
    response = requests.get(cups_url)
    if response.status_code == 200:
        # Mencetak status printer
        print(f"Printer Status: {response.text}")
    else:
        print(f"Failed to retrieve printer status. Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
