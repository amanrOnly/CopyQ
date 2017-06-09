#!/usr/bin/python
'''
Parses API for C++ from scriptable README file.
'''

import re

readme_path = 'src/scriptable/README.md'
output_path = 'src/gui/commandcompleterdocumentation.h'

header = '''// Generated by "utils/script_docs_to_cpp.py" from "src/scriptable/README.md".
template <typename AddDocumentationCallback>
void addDocumentation(AddDocumentationCallback addDocumentation)
{
'''

footer = '}'

# Function/variable/type name in the README file
re_title = re.compile(r'''
  # title in Markdown
  ^\#{6}\s*

  (?:
    (?P<function_api>
      # function return value
      .*?
      # function name
      (?P<function_name>\w+)
      # arguments
      \(.*
    )

    |

    # variable name
    (?P<variable_name>\w+)
    # followed by space
    \s
    # followed by opening parenthesis
    (?P<variable_api>\(.*)

    |

    # type name
    (?P<type_name>\w+)$
  )
  ''', re.VERBOSE)

def main():
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        output_file.write(header + '\n')

        with open(readme_path, mode='r', encoding='utf-8') as readme_file:
            match = None
            for line in readme_file:
                line = line.strip()
                if line:
                    if match:
                        name = match.group('function_name') or match.group('variable_name') or match.group('type_name')
                        api = match.group('function_api') or match.group('variable_api') or name
                        output = '    addDocumentation("{}", "{}", "{}");\n'\
                            .format(name, api, line)
                        output_file.write(output)
                        match = None
                    else:
                        match = re.match(re_title, line)

        output_file.write(footer + '\n')

if __name__ == "__main__":
    main()