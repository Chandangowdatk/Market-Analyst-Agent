#!/bin/bash

# Market Analyst Agent - Initialize Vector Store

PROJECT_DIR="/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

echo "=========================================="
echo "📚 Initialize Vector Store (Pinecone)"
echo "=========================================="

# Navigate to project
cd "$PROJECT_DIR" || exit 1

# Check .env file
if [ ! -f .env ]; then
    echo ""
    echo "❌ Error: .env file not found!"
    echo "Please create .env file first. See RUN_GUIDE.md"
    exit 1
fi

# Activate venv
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run initialization
echo "✅ Loading document..."
python -c "
import sys
sys.path.insert(0, '.')

from src.services.vector_store import VectorStoreManager
from src.services.document_processor import DocumentProcessor

print('📚 Loading and processing document...')
processor = DocumentProcessor()
text = processor.load_document('data/innovate_inc_report.txt')
documents = processor.process_document(text, 'innovate_inc_report.txt')

print(f'✅ Created {len(documents)} chunks')
print('🔄 Uploading to Pinecone...')

vector_store = VectorStoreManager()
result = vector_store.ingest_documents(documents)

if result['status'] == 'success':
    print(f'✅ Successfully ingested {result[\"chunks_processed\"]} chunks')
    print(f'📦 Namespace: {result[\"namespace\"]}')
    print('')
    print('🎉 Vector store initialized! You can now run: ./start.sh')
else:
    print(f'❌ Error: {result[\"error\"]}')
    sys.exit(1)
"

