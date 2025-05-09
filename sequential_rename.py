'''
executar a partir da linha de comando:

    python sequential_rename.py /directory "base_name" [--start N] [--digits M] [--dry-run]
    
    onde:

    directory: diretório onde os arquivos estão localizados
    base_name: nome base que será usado para renomear os arquivos
    start: número inicial para o sufixo (padrão é 0)
    digits: número de dígitos para o preenchimento do sufixo (padrão é 2)
    dry_run: se True, o script apenas mostrará as mudanças que seriam feitas, sem realmente renomear os arquivos

'''

import os
import argparse
import uuid

def rename_files(directory, base_name, start=0, digits=2, dry_run=False):
    # validando diretório
    if not os.path.isdir(directory):
        print(f"Error: {directory} não é um diretório válido.")
        return

    # obtem lista de arquivos (excluindo diretórios)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    if not files:
        print("Diretório de arquivos não encontrado.")
        return

    # gerar novos nomes
    format_str = f"{{:0{digits}d}}"
    new_names = []
    for i, filename in enumerate(files, start=start):
        suffix = format_str.format(i)
        root, ext = os.path.splitext(filename)
        new_name = f"{base_name}{suffix}{ext}"
        new_names.append(new_name)

    # verifica se há conflitos
    existing_entries = set(os.listdir(directory))
    conflicts = []
    for new_name in new_names:
        if new_name in existing_entries and new_name not in files:
            conflicts.append(new_name)
    if conflicts:
        print("Error: Os seguintes novos nomes já existem no diretório:")
        for name in conflicts:
            print(name)
        print("Abortando para evitar substituição.")
        return

    # saída de teste
    if dry_run:
        print("Execução de teste: As seguintes alterações seriam feitas:")
        for filename, new_name in zip(files, new_names):
            print(f"'{filename}' → '{new_name}'")
        return

    # gera nomes temporários
    temp_names = []
    for filename in files:
        while True:
            temp_name = f"temp_{uuid.uuid4().hex}"
            temp_path = os.path.join(directory, temp_name)
            if not os.path.exists(temp_path):
                break
        temp_names.append(temp_name)

    # primeiro: renomeia para nomes temporários
    for filename, temp_name in zip(files, temp_names):
        old_path = os.path.join(directory, filename)
        temp_path = os.path.join(directory, temp_name)
        os.rename(old_path, temp_path)

    # segundo: renomeia os nomes temporários para novos nomes
    for temp_name, new_name in zip(temp_names, new_names):
        temp_path = os.path.join(directory, temp_name)
        new_path = os.path.join(directory, new_name)
        os.rename(temp_path, new_path)

    print(f"{len(files)} Arquivos renomeados com sucesso.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renomear arquivos com sufixos sequenciais')
    parser.add_argument('directory', help='Diretório contendo arquivos para renomear')
    parser.add_argument('base_name', help='Nome base para novos nomes de arquivo')
    parser.add_argument('--start', type=int, default=0, help='Número inicial (padrão: 0)')
    parser.add_argument('--digits', type=int, default=2, help='Número de dígitos para preenchimento (padrão: 2)')
    parser.add_argument('--dry-run', action='store_true', help='Visualizar alterações sem renomear')
    args = parser.parse_args()

    rename_files(
        args.directory,
        args.base_name,
        start=args.start,
        digits=args.digits,
        dry_run=args.dry_run
    )
