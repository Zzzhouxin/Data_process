import json
from collections import defaultdict
import os
from concurrent.futures import ProcessPoolExecutor, as_completed


def process_file(file_path):
    count_dict = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_data = json.loads(line)
            production = json_data['production']
            count_dict[production] += 1
    return count_dict


def count_productions_multi_process(folder_path, max_workers=None):
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.json')]
    final_count_dict = defaultdict(int)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, file_path): file_path for file_path in file_paths}

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                count_dict = future.result()
                for production, count in count_dict.items():
                    final_count_dict[production] += count

                print(count_dict.items())
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")

    return final_count_dict


if __name__ == "__main__":
    folder_path = "./process_pip/pip/"
    result = count_productions_multi_process(folder_path)
    print(result)