"""
Quick test script to verify Market Analyst Agent setup.
Run this before starting the full application.
"""
import sys
from pathlib import Path

print("=" * 60)
print("Market Analyst Agent - Setup Verification")
print("=" * 60)

# Test 1: Python Version
print("\n1. Python Version:")
print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
if sys.version_info < (3, 9):
    print("   ⚠️  Warning: Python 3.9+ recommended for LangChain 1.0.3")

# Test 2: Environment File
print("\n2. Environment File:")
env_file = Path(".env")
if env_file.exists():
    print("   ✓ .env file exists")
    with open(env_file) as f:
        content = f.read()
        keys = ["GOOGLE_API_KEY", "OPENAI_API_KEY", "PINECONE_API_KEY"]
        for key in keys:
            if key in content and "your_" not in content.split(key)[1].split("\n")[0]:
                print(f"   ✓ {key} is configured")
            else:
                print(f"   ✗ {key} is missing or not configured")
else:
    print("   ✗ .env file not found")
    print("   → Copy env.example.txt to .env and add your API keys")

# Test 3: Required Packages
print("\n3. Required Packages:")
packages = [
    ("langchain", "LangChain Core"),
    ("langchain_google_genai", "Google Gemini Integration"),
    ("langchain_openai", "OpenAI Integration"),
    ("pinecone", "Pinecone Vector DB"),
    ("fastapi", "FastAPI Framework"),
    ("pydantic", "Pydantic (should be v2.x)"),
]

for package, name in packages:
    try:
        mod = __import__(package)
        version = getattr(mod, "__version__", "unknown")
        print(f"   ✓ {name}: {version}")
    except ImportError:
        print(f"   ✗ {name}: NOT INSTALLED")

# Test 4: Data File
print("\n4. Data Files:")
data_file = Path("data/innovate_inc_report.txt")
if data_file.exists():
    print(f"   ✓ Sample report exists ({data_file.stat().st_size} bytes)")
else:
    print("   ✗ Sample report not found")

# Test 5: Import Test
print("\n5. Import Test:")
try:
    from Market_Analyst_Agent.src.config import Config
    print("   ✓ Config module imports successfully")
    print(f"   ✓ Gemini Model: {Config.GEMINI_MODEL}")
    print(f"   ✓ Embedding Model: {Config.EMBEDDING_MODEL}")
except Exception as e:
    print(f"   ✗ Import error: {e}")

try:
    from Market_Analyst_Agent.src.tools.qa_tool import qa_tool
    from Market_Analyst_Agent.src.tools.insights_tool import insights_tool
    from Market_Analyst_Agent.src.tools.extract_tool import extract_tool
    print("   ✓ All tools import successfully")
except Exception as e:
    print(f"   ✗ Tool import error: {e}")

try:
    from Market_Analyst_Agent.src.agent import agent_executor
    print("   ✓ Agent imports successfully")
except Exception as e:
    print(f"   ✗ Agent import error: {e}")

# Summary
print("\n" + "=" * 60)
print("Setup Verification Complete!")
print("=" * 60)
print("\nNext Steps:")
print("1. If any packages are missing: pip install -r requirements.txt")
print("2. If .env is missing: Copy env.example.txt to .env and add API keys")
print("3. If all checks pass: python src/main.py")
print("\n")

