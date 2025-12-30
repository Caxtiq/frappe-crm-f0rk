"""LLM Provider implementations"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseProvider(ABC):
	"""Base class for LLM providers"""
	
	def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 1000):
		self.model = model
		self.temperature = temperature
		self.max_tokens = max_tokens
	
	@abstractmethod
	def chat(self, messages: List[Dict[str, str]]) -> str:
		"""Send chat messages and get response"""
		pass


class OpenAIProvider(BaseProvider):
	"""OpenAI GPT provider"""
	
	def __init__(
		self,
		api_key: str,
		model: str = "gpt-4o-mini",
		temperature: float = 0.7,
		max_tokens: int = 1000,
	):
		super().__init__(model, temperature, max_tokens)
		from openai import OpenAI
		self.client = OpenAI(api_key=api_key)
	
	def chat(self, messages: List[Dict[str, str]]) -> str:
		"""Send chat completion request to OpenAI"""
		try:
			response = self.client.chat.completions.create(
				model=self.model,
				messages=messages,
				temperature=self.temperature,
				max_tokens=self.max_tokens,
			)
			return response.choices[0].message.content
		except Exception as e:
			import frappe
			frappe.throw(f"OpenAI API Error: {str(e)}")


class AnthropicProvider(BaseProvider):
	"""Anthropic Claude provider"""
	
	def __init__(
		self,
		api_key: str,
		model: str = "claude-3-5-sonnet-20240620",
		temperature: float = 0.7,
		max_tokens: int = 1000,
	):
		super().__init__(model, temperature, max_tokens)
		from anthropic import Anthropic
		self.client = Anthropic(api_key=api_key)
	
	def chat(self, messages: List[Dict[str, str]]) -> str:
		"""Send message to Claude"""
		try:
			# Extract system message if present
			system = None
			user_messages = []
			
			for msg in messages:
				if msg["role"] == "system":
					system = msg["content"]
				else:
					user_messages.append(msg)
			
			response = self.client.messages.create(
				model=self.model,
				max_tokens=self.max_tokens,
				temperature=self.temperature,
				system=system if system else None,
				messages=user_messages,
			)
			return response.content[0].text
		except Exception as e:
			import frappe
			frappe.throw(f"Anthropic API Error: {str(e)}")


class OllamaProvider(BaseProvider):
	"""Ollama local LLM provider"""
	
	def __init__(
		self,
		model: str = "llama3.1",
		temperature: float = 0.7,
		base_url: str = "http://localhost:11434",
	):
		super().__init__(model, temperature)
		self.base_url = base_url
	
	def chat(self, messages: List[Dict[str, str]]) -> str:
		"""Send chat to Ollama"""
		try:
			import requests
			
			response = requests.post(
				f"{self.base_url}/api/chat",
				json={
					"model": self.model,
					"messages": messages,
					"stream": False,
					"options": {
						"temperature": self.temperature,
					},
				},
			)
			response.raise_for_status()
			return response.json()["message"]["content"]
		except Exception as e:
			import frappe
			frappe.throw(f"Ollama API Error: {str(e)}")


class LiteLLMProvider(BaseProvider):
	"""LiteLLM unified provider (supports all providers)"""
	
	def __init__(
		self,
		model: str,
		api_key: Optional[str] = None,
		temperature: float = 0.7,
		max_tokens: int = 1000,
	):
		super().__init__(model, temperature, max_tokens)
		import litellm
		self.litellm = litellm
		if api_key:
			self.api_key = api_key
	
	def chat(self, messages: List[Dict[str, str]]) -> str:
		"""Send chat using LiteLLM"""
		try:
			response = self.litellm.completion(
				model=self.model,
				messages=messages,
				temperature=self.temperature,
				max_tokens=self.max_tokens,
			)
			return response.choices[0].message.content
		except Exception as e:
			import frappe
			frappe.throw(f"LiteLLM API Error: {str(e)}")
