LINE_LENGTH=125

for dir in app
do
  black $dir --line-length $LINE_LENGTH --check
  flake8 $dir --max-line-length $LINE_LENGTH
done