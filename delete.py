"""
split_pdbqt.py v1.01
Copyright (C) 2023 Zekeriya DUZGUN

Bu script, belirtilen giriş dosyasını okur ve her MODEL-ENDMDL bloğunu ayrı bir dosya olarak kaydeder. 
Her blok için, ZINC ile başlayan kelime dosya adı olarak kullanılır. 
Eğer aynı isimde bir dosya zaten mevcutsa, dosya "dupl" adlı bir klasör içine kaydedilir. 
Çıktı klasörünün adı giriş dosyasının adı ile aynıdır (uzantı hariç).

Kullanım:
    python split_pdbqt.py <input_file.pdbqt>

Örneğin:
    python split_pdbqt.py input.pdbqt

Not:
- input.pdbqt, okunacak dosyanın adıdır.
- Çıktı dosyaları, "input" adlı bir klasör içinde ve "dupl" adlı bir alt klasör içinde oluşturulur.
- Script, toplam model sayısını, yazılan model sayısını ve çift model sayısını yazdırır.

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
"""

import os
import re
import sys

def extract_models(input_file):
    input_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = input_filename
    dupl_dir = os.path.join(output_dir, 'dupl')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(dupl_dir, exist_ok=True)
    
    model_count = 0
    written_count = 0
    duplicate_count = 0

    try:
        with open(input_file) as file:
            content = file.read()
            blocks = content.split('MODEL')
            for block in blocks[1:]:
                block = 'MODEL' + block
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

        print(f"Total Models: {model_count}")
        print(f"Written Models: {written_count}")
        print(f"Duplicate Models: {duplicate_count}")
        print("Extraction completed.")
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_models(sys.argv[1])
    else:
        print("Usage: python script.py <input_file>")
