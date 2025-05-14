"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    import pandas as pd
    import re

    with open('files/input/clusters_report.txt', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "Cluster" in line and "Cantidad" in line:
            header_line = lines[i]
            header_line2 = lines[i+1]
            start_data = i + 4 
            break

    header = (header_line.strip() + " " + header_line2.strip())
    header = re.sub(r'\s+', ' ', header)
    columnas = [
        'cluster',
        'cantidad_de_palabras_clave',
        'porcentaje_de_palabras_clave',
        'principales_palabras_clave'
    ]

    data = []
    registro = []
    for line in lines[start_data:]:
        if re.match(r'^\s*\d+', line):
            if registro:
                data.append(registro)
            registro = []
            parts = re.split(r'\s{2,}', line.strip(), maxsplit=3)
            registro.extend(parts[:3])
            if len(parts) > 3:
                registro.append(parts[3].strip())
            else:
                registro.append('')
        else:
            if registro:
                registro[-1] += ' ' + line.strip()
    if registro:
        data.append(registro)

    for row in data:
        row[2] = row[2].replace('%', '').replace(',', '.').strip()
        palabras = row[3]
        palabras = palabras.replace('\n', ' ').replace('.', '').strip()
        palabras = re.sub(r'\s+', ' ', palabras)
        palabras = ', '.join([p.strip() for p in palabras.split(',') if p.strip()])
        row[3] = palabras

    df = pd.DataFrame(data, columns=columnas)
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].astype(float)
    df = df.rename(columns=lambda x: x.lower().replace(' ', '_'))

    return df