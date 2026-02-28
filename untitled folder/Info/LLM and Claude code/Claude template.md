# Commit documentation slash command
Mark codes with EACC for endureair custom code

use context from git commit difference
```bash
#!/bin/bash

# Number of commits to process
NUM_COMMITS=9
OUTPUT_FILE="commit_context.txt"

# Clear output file if it exists
> "$OUTPUT_FILE"

# Process each of the last N commits
git log -n $NUM_COMMITS --pretty=format:"%H" | while read commit; do
  echo "===== Commit: $commit =====" >> "$OUTPUT_FILE"
  git show "$commit" --unified=5 --pretty=format:"" --no-color >> "$OUTPUT_FILE"
  echo -e "\n\n" >> "$OUTPUT_FILE"
done

echo "Context for last $NUM_COMMITS commits saved to $OUTPUT_FILE"
```

and create a template system prompt to use markdown features for documenting
Also create template for defining what to write, and what not to write, how to keep the commit doc clean
# Searching existing implementation
Search for existing implementations of the individual subtask in the given task.
Once you find the individual implementation, and the working, go on to implementation.
# Improving code
Here is a code I have written to implement a mission resume functionality in arducopter, of ardupilot opensource firmware

```cpp
// your code
```

1) Improve the code following industry standard cpp coding practices
2) improve variable naming if anywhere required
3) make docstring comments for function description, add line comments wherever required, remove comments where not required
4) handle edge cases or exceptions
5) heavily use DRY (dont repeat yourself) and KISS (keep it simple stupid) principle to improve overall coding style and understandability
6) Add humor in comments, the code should make the life a little happier for the reader who is reading it at 3 in the night, 4 peg down (of coffee)

