from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen3-coder:30b")

response = llm.invoke("Explain SOLID principles in 3 lines.")
print(response)





