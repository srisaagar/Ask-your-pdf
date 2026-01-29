import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def stream_ollama(prompt, model="llama3"):


    """
    Stream tokens from Ollama safely for Flask usage
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    try:
        with requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=60
        ) as response:

            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Stream token
                if "response" in data:
                    yield data["response"]

                # Stop signal
                if data.get("done", False):
                    break

    except requests.exceptions.ConnectionError:
        yield "\n❌ Ollama is not running. Please start Ollama."

    except requests.exceptions.Timeout:
        yield "\n❌ Ollama request timed out."

    except Exception as e:
        yield f"\n❌ Ollama error: {str(e)}"
