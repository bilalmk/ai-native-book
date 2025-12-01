"""
Test script for RAG Chatbot API
Tests all endpoints and validates responses
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health_check():
    """Test the health check endpoint"""
    print_section("Testing Health Check")

    try:
        response = requests.get(f"{BASE_URL}/api/health")
        data = response.json()

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")

        if data['status'] == 'healthy':
            print("✓ Health check passed!")
            if data['qdrant_connected'] and data['database_connected']:
                print("✓ All services connected!")
                return True
            else:
                print("✗ Some services are not connected")
                return False
        else:
            print("✗ Health check failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_chat_basic():
    """Test basic chat functionality"""
    print_section("Testing Basic Chat")

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "message": "What is Physical AI?"
            }
        )

        data = response.json()

        print(f"Status Code: {response.status_code}")
        print(f"\nQuestion: What is Physical AI?")
        print(f"\nAnswer: {data['message']}")
        print(f"\nSources ({len(data.get('sources', []))}):")

        for i, source in enumerate(data.get('sources', []), 1):
            print(f"  {i}. {source['title']}")
            print(f"     Path: {source['file_path']}")
            print(f"     Relevance: {source['score']*100:.1f}%")

        print(f"\nSession ID: {data['session_id']}")

        if response.status_code == 200 and data['message']:
            print("\n✓ Basic chat test passed!")
            return data['session_id']
        else:
            print("\n✗ Basic chat test failed")
            return None

    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def test_chat_with_context(session_id):
    """Test chat with conversation context"""
    print_section("Testing Chat with Context")

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "session_id": session_id,
                "message": "Can you give me more details about the perception-action loop?"
            }
        )

        data = response.json()

        print(f"Status Code: {response.status_code}")
        print(f"\nQuestion: Can you give me more details about the perception-action loop?")
        print(f"\nAnswer: {data['message']}")

        if response.status_code == 200 and data['session_id'] == session_id:
            print("\n✓ Context-aware chat test passed!")
            return True
        else:
            print("\n✗ Context-aware chat test failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_chat_with_selected_text():
    """Test chat with selected text"""
    print_section("Testing Chat with Selected Text")

    selected_text = """
    Embodied intelligence is built upon a continuous cycle of three
    interconnected components: perception, cognition, and action.
    """

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "message": "Explain this concept in simple terms",
                "selected_text": selected_text.strip()
            }
        )

        data = response.json()

        print(f"Status Code: {response.status_code}")
        print(f"\nSelected Text: {selected_text.strip()}")
        print(f"\nQuestion: Explain this concept in simple terms")
        print(f"\nAnswer: {data['message']}")

        if response.status_code == 200 and data['message']:
            print("\n✓ Selected text chat test passed!")
            return True
        else:
            print("\n✗ Selected text chat test failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_session_history(session_id):
    """Test retrieving session history"""
    print_section("Testing Session History Retrieval")

    try:
        response = requests.get(f"{BASE_URL}/api/sessions/{session_id}/history")
        data = response.json()

        print(f"Status Code: {response.status_code}")
        print(f"\nSession ID: {data['session_id']}")
        print(f"Total Messages: {len(data['messages'])}")

        print("\nConversation:")
        for i, msg in enumerate(data['messages'], 1):
            role_emoji = "👤" if msg['role'] == 'user' else "🤖"
            print(f"\n{i}. {role_emoji} {msg['role'].upper()}")
            print(f"   {msg['content'][:100]}...")
            if msg.get('selected_text'):
                print(f"   [Selected text was used]")

        if response.status_code == 200 and len(data['messages']) >= 2:
            print("\n✓ Session history test passed!")
            return True
        else:
            print("\n✗ Session history test failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{'#'*60}")
    print(f"#  RAG Chatbot API Test Suite")
    print(f"#  Base URL: {BASE_URL}")
    print(f"#  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")

    results = []

    # Test 1: Health check
    results.append(("Health Check", test_health_check()))

    # Test 2: Basic chat
    session_id = test_chat_basic()
    results.append(("Basic Chat", session_id is not None))

    if session_id:
        # Test 3: Chat with context
        results.append(("Context-Aware Chat", test_chat_with_context(session_id)))

        # Test 4: Session history
        results.append(("Session History", test_session_history(session_id)))

    # Test 5: Chat with selected text
    results.append(("Selected Text Chat", test_chat_with_selected_text()))

    # Summary
    print_section("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print(f"{'='*60}\n")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
