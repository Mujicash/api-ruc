import os

def print_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Excluir directorios específicos
        dirs[:] = [d for d in dirs if d not in ["__pycache__"]]

        # Evitar imprimir directorios excluidos y sus contenidos
        if any(excluded in root for excluded in ["env", "model"]):
            continue

        # Imprimir estructura
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

# Usar la función con la ruta deseada
ruta_carpeta = "src" # Cambia esto por la ruta de tu carpeta
print_directory_structure(ruta_carpeta)