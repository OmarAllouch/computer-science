#!/usr/bin/bash

# Write a program that takes in a pdf filename and a question, and outputs the generated text
# Check if the user has provided the correct number of arguments
if [ $# -ne 2 ]; then
    echo "
USAGE:
  ./ask_pdf.sh <pdf-file> \"<question>\"

DESCRIPTION:
  ask_pdf.sh is a command-line tool that answers a specific question based on
  the content of the provided PDF document.

PARAMETERS:
  <pdf-file>
    The full path or name of the PDF document to analyze. This parameter is
    required.

  \"<question>\"
    The question to ask about the PDF content. This parameter is required and
    must be enclosed in quotes."
    exit 1
fi

# Check if the pdf file exists
if [ ! -f $1 ]; then
    echo "Error: File $1 does not exist"
    exit 1
fi

# Check if the file is a pdf file
if [ ${1: -4} != ".pdf" ]; then
    echo "Error: File $1 is not a pdf file"
    exit 1
fi

# Use the ollama api to query the model using the curl program.
# Pipe the output of the command above with the jq command-line JSON processor to print out the response content.
# find and install a command-line program to extract the text content of some PDF file
# Write a bash script ask_pdf.sh that satisfies the documentation below:

# Extract the text content of the PDF file
text=$(pdftotext $1 -)
text=$(echo $text | sed 's/\\/ /g' | sed 's/\\n//g' | sed 's/\\f//g' | tr -d '\n\f\r' | sed 's/[[:space:]]\+/ /g')
# Escape special characters in the text
text=$(echo $text | sed 's/"/\\"/g')

# Pull the llama3.1 model
model="llama3.1"

# Create the prompt by combining the PDF content with the user's question
prompt="You are provided with the following text from a PDF file:\n\n'$text'\n\nQuestion: $2"

# Ask the question using the ollama API
response=$(curl -s -X POST "http://localhost:11434/api/generate" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "'"$model"'",
        "prompt": "'"$prompt"'"
      }')

# Extract the answer from the response
answer=$(echo $response | jq -r '.response')

# Print the answer
echo $answer
