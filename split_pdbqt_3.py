'''split_pdbqt.py v1.2
Copyright (C) 2023 Zekeriya DUZGUN

This script reads the specified input file and saves each MODEL-ENDMDL block as a separate file. 
The word starting with ZINC is used as the file name for each block. 
If a file with the same name already exists, the file is saved inside a folder named "dupl". 
The name of the output folder is the same as the name of the input file (excluding the extension).

Usage:
    python3 split_pdbqt_3.py


Note:
- Output files are created inside a folder named "input" and inside a subfolder named "dupl".
- The script prints the total number of models, the number of written models, and the number of duplicate models.
- If there are less than 20000 files in the newly created folder, they are organized as PART1..PART30.
- This code finds all .pdbqt files in the current directory and calls the extract_models function for each of them.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import os
import re

def extract_models(input_dir):
    part_count = 1
    model_count = 0
    written_count = 0
    duplicate_count = 0
    output_dir = f'PART{str(part_count).zfill(2)}'
    dupl_dir = os.path.join(output_dir, 'dupl')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(dupl_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdbqt"):
            input_file = os.path.join(input_dir, file)
            try:
                with open(input_file) as file:
                    content = file.read()
                    if 'MODEL' in content and 'ENDMDL' in content:
                        blocks = content.split('MODEL')
                        for block in blocks[1:]:
                            lines = block.split('\n')[1:]  # Skip the first line
                            block = '\n'.join(lines).replace('ENDMDL', '')  # Remove ENDMDL
                            model_count += 1
                            zinc_name = re.search(r'ZINC\d+', block)
                            if zinc_name:
                                zinc_name = zinc_name.group()
                                output_file = os.path.join(output_dir, f'{zinc_name}.pdbqt')
                                if os.path.exists(output_file):
                                    duplicate_count += 1
                                    output_file = os.path.join(dupl_dir, f'{zinc_name}.pdbqt')
                                try:
                                    with open(output_file, 'w') as out_file:
                                        out_file.write(block)
                                    written_count += 1
                                except Exception as e:
                                    print(f"Error writing file {output_file}: {e}")
                            if model_count % 20000 == 0:
                                part_count += 1
                                output_dir = f'PART{str(part_count).zfill(2)}'
                                dupl_dir = os.path.join(output_dir, 'dupl')
                                os.makedirs(output_dir, exist_ok=True)
                                os.makedirs(dupl_dir, exist_ok=True)
                    else:
                        zinc_name = re.search(r'ZINC\d+', content)
                        if zinc_name:
                            zinc_name = zinc_name.group()
                            output_file = os.path.join(output_dir, f'{zinc_name}.pdbqt')
                            try:
                                with open(output_file, 'w') as out_file:
                                    out_file.write(content)
                                written_count += 1
                            except Exception as e:
                                print(f"Error writing file {output_file}: {e}")

                print(f"Total Models: {model_count}")
                print(f"Written Models: {written_count}")
                print(f"Duplicate Models: {duplicate_count}")
                print("Extraction completed.")
            except Exception as e:
                print(f"Error reading file {input_file}: {e}")

if __name__ == '__main__':
    extract_models(os.getcwd())