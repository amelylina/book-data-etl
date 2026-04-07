#hypothetical ruby parser

# chose to stick to python regex parsing for safety purposes
# although i did recognize the data in orig "json" as an array of ruby hashes
# the idea of doing 'eval' on a file i dont know full contents of seems risky
# as i believe eval would execute any line inside that file, even system("rm -rf")

require 'json'

project_root = File.expand_path('..', __dir__)
input_path   = File.join(project_root, 'raw_data', 'task1_d.json')
output_path  = File.join(project_root, 'output_data', 'parsed_data.json')


raw_hash  = eval(File.read(input_path))
File.write(output_path, JSON.dump(raw_hash))