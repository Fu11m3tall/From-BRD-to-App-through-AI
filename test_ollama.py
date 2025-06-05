import requests
import json
from typing import Optional

def get_ollama_models() -> list:
    """Get list of available Ollama models."""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        response.raise_for_status()
        return [model['name'] for model in response.json()['models']]
    except Exception as e:
        print(f"Error getting models: {e}")
        return []

def test_model(model_name: str, prompt: str) -> Optional[str]:
    """Test a specific Ollama model with a given prompt."""
    try:
        url = f'http://localhost:11434/api/generate'
        data = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"Error testing model {model_name}: {e}")
        return None

def main():
    print("Available Ollama models:")
    models = get_ollama_models()
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    while True:
        print("\nSelect a model (enter number) or type 'exit' to quit:")
        choice = input("> ")
        
        if choice.lower() == 'exit':
            break
            
        try:
            model_index = int(choice) - 1
            if 0 <= model_index < len(models):
                selected_model = models[model_index]
                print(f"\nTesting model: {selected_model}")
                
                print("Enter your prompt (type 'exit' to return to model selection):")
                while True:
                    prompt = input("Prompt: ")
                    if prompt.lower() == 'exit':
                        break
                        
                    response = test_model(selected_model, prompt)
                    if response:
                        print("\nModel Response:")
                        print(response)
                        print("\n")
            else:
                print("Invalid model number!")
        except ValueError:
            print("Please enter a valid number!")

if __name__ == "__main__":
    main()
