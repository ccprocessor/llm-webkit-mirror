import os

base_dir = '/nvme/pzx/llm-webkit-mirror/tests/llm_web_kit/pipeline/extractor/html/recognizer/assets/ccmath'  
expected_file_path = os.path.join(base_dir, 'p_test_gt_inline.html')
output_dir = os.path.join(base_dir, 'p_test_gt_inline')

os.makedirs(output_dir, exist_ok=True)

with open(expected_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

for idx, line in enumerate(lines):
    file_name = f"{idx + 1}.html"
    file_path = os.path.join(output_dir, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(line.strip()) 

print(f"Successfully created {len(lines)} HTML files in '{output_dir}'.")