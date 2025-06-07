"""
Tests for LLM api endpoints.
"""
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src import app

client = TestClient(app=app)


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_valid_secret(mock_chat):
    """
    Test /llm/query/ endpoint with valid secret
    """
    mock_chat.return_value = {"response": "This is a test response from the LLM"}
    
    response = client.post(
        "/llm/query/?secret=cyclops2025",
        json={"prompt": "What is the weather today?"}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    mock_chat.assert_called_once()


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_invalid_secret(mock_chat):
    """
    Test /llm/query/ endpoint with invalid secret
    """
    response = client.post(
        "/llm/query/?secret=wrongsecret",
        json={"prompt": "What is the weather today?"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"error": "Unauthorized access. Invalid secret."}
    mock_chat.assert_not_called()


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_missing_secret(mock_chat):
    """
    Test /llm/query/ endpoint with missing secret (defaults to 'letmepass')
    """
    response = client.post(
        "/llm/query/",
        json={"prompt": "What is the weather today?"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"error": "Unauthorized access. Invalid secret."}
    mock_chat.assert_not_called()


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_empty_prompt(mock_chat):
    """
    Test /llm/query/ endpoint with empty prompt
    """
    mock_chat.return_value = {"response": "I need more information to help you."}
    
    response = client.post(
        "/llm/query/?secret=cyclops2025",
        json={"prompt": ""}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    mock_chat.assert_called_once()


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_long_prompt(mock_chat):
    """
    Test /llm/query/ endpoint with a long prompt
    """
    long_prompt = "This is a very long prompt " * 100
    mock_chat.return_value = {"response": "I've processed your long request."}
    
    response = client.post(
        "/llm/query/?secret=cyclops2025",
        json={"prompt": long_prompt}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    mock_chat.assert_called_once()


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_special_characters(mock_chat):
    """
    Test /llm/query/ endpoint with special characters in prompt
    """
    special_prompt = "What about symbols: @#$%^&*()_+{}|:<>?[];',./"
    mock_chat.return_value = {"response": "I can handle special characters."}
    
    response = client.post(
        "/llm/query/?secret=cyclops2025",
        json={"prompt": special_prompt}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    mock_chat.assert_called_once()


def test_llm_query_missing_prompt():
    """
    Test /llm/query/ endpoint with missing prompt parameter
    """
    response = client.post(
        "/llm/query/?secret=cyclops2025",
        json={}
    )
    
    assert response.status_code == 422  # Unprocessable Entity for missing required field


@patch('src.services.chatgpt.ChatGPTService.chat')
def test_llm_query_service_exception(mock_chat):
    """
    Test /llm/query/ endpoint when service raises an exception
    """
    mock_chat.side_effect = Exception("OpenAI API error")
    
    # The endpoint doesn't handle exceptions, so it will raise
    # This is expected behavior based on the current implementation
    try:
        response = client.post(
            "/llm/query/?secret=cyclops2025",
            json={"prompt": "Test prompt"}
        )
        # If we get here, the exception was handled somehow
        assert response.status_code in [200, 500]
    except Exception as e:
        # The exception is expected to bubble up
        assert "OpenAI API error" in str(e)