"""
split_pdbqt.py v1.2
Copyright (C) 2023 Zekeriya DUZGUN

Bu script, belirtilen giriş dosyasını okur ve her MODEL-ENDMDL bloğunu ayrı bir dosya olarak kaydeder. 
Her blok için, ZINC ile başlayan kelime dosya adı olarak kullanılır. 
Eğer aynı isimde bir dosya zaten mevcutsa, dosya "dupl" adlı bir klasör içine kaydedilir. 
Her klasörde 20000 dosya oalcak şekilde PART01..999 şeklinde bölüştürür.

Kullanım:
    python3 split_pdbqt_2.py


Not:
- Çıktı dosyaları, "input" adlı bir klasör içinde ve "dupl" adlı bir alt klasör içinde oluşturulur.
- Script, toplam model sayısını, yazılan model sayısını ve çift model sayısını yazdırır.
- Bu kod, mevcut dizindeki tüm .pdbqt uzantılı dosyaları bulur ve her biri için extract_models fonksiyonunu çağırır.
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
                            lines = block.split('\n')[1:]  # ilk satırı atla
                            block = '\n'.join(lines).replace('ENDMDL', '')  # ENDMDL'yi kaldır
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
                                    print(f"Hata dosya yazılırken {output_file}: {e}")
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
                                print(f"Hata dosya yazılırken {output_file}: {e}")

                print(f"Toplam Modeller: {model_count}")
                print(f"Yazılan Modeller: {written_count}")
                print(f"Yinelenen Modeller: {duplicate_count}")
                print("Çıkarma tamamlandı.")
            except Exception as e:
                print(f"Hata dosya okunurken {input_file}: {e}")

if __name__ == '__main__':
    extract_models(os.getcwd())
