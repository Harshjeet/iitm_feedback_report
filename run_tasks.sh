#!/bin/bash

# Configuration
BASE_URL="http://localhost:8000/assignment"
DATA_FILE="data.json"
OUTPUT_PDF_DIR="output_pdf"
OUTPUT_HTML_DIR="output_html"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create output directories if they don't exist
mkdir -p "$OUTPUT_PDF_DIR"
mkdir -p "$OUTPUT_HTML_DIR"

if [ ! -f "$DATA_FILE" ]; then
  echo "❌ File $DATA_FILE not found!"
  exit 1
fi

# Submit HTML generation task
echo "🚀 Submitting HTML task..."
html_task_id=$(curl -s -X POST "$BASE_URL/html" \
  -H "Content-Type: application/json" \
  --data-binary @"$DATA_FILE" | jq -r '.task_id')

echo "📎 HTML Task ID: $html_task_id"

# Poll HTML task
echo "⏳ Waiting for HTML task to complete..."
while true; do
  html_response=$(curl -s "$BASE_URL/html/$html_task_id")
  html_status=$(echo "$html_response" | jq -r '.status')

  echo "🔍 HTML Task Status: $html_status"

  if [ "$html_status" == "completed" ]; then
    HTML_FILENAME="report_${TIMESTAMP}.html"
    HTML_PATH="$OUTPUT_HTML_DIR/$HTML_FILENAME"
    echo "$html_response" | jq -r '.html' > "$HTML_PATH"
    echo "✅ HTML saved to $HTML_PATH"
    break
  elif [ "$html_status" == "failed" ]; then
    echo "❌ HTML generation failed"
    exit 1
  fi

  sleep 2
done

# Submit PDF generation task
echo "🚀 Submitting PDF task..."
pdf_task_id=$(curl -s -X POST "$BASE_URL/pdf" \
  -H "Content-Type: application/json" \
  --data-binary @"$DATA_FILE" | jq -r '.task_id')

echo "📎 PDF Task ID: $pdf_task_id"

# Poll PDF task
echo "⏳ Waiting for PDF task to complete..."
while true; do
  content_type=$(curl -s -D - -o /dev/null "$BASE_URL/pdf/$pdf_task_id" | grep -i "Content-Type")

  if echo "$content_type" | grep -iq "application/pdf"; then
    PDF_FILENAME="report_${TIMESTAMP}.pdf"
    PDF_PATH="$OUTPUT_PDF_DIR/$PDF_FILENAME"
    curl -s "$BASE_URL/pdf/$pdf_task_id" -o "$PDF_PATH"
    echo "✅ PDF saved as $PDF_PATH"
    break
  else
    status=$(curl -s "$BASE_URL/pdf/$pdf_task_id" | jq -r '.status')
    echo "🔍 PDF Task Status: $status"
    if [ "$status" == "failed" ]; then
      echo "❌ PDF generation failed"
      exit 1
    fi
    sleep 2
  fi
done
