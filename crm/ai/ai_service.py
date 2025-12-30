"""Main AI Service orchestrator for CRM"""

import frappe
from typing import Optional, Dict, Any, List
import json


class AIService:
	"""Central AI service for managing LLM interactions"""
	
	def __init__(self):
		self.settings = self._get_settings()
		self.provider = None
		self._initialize_provider()
	
	def _get_settings(self) -> Dict[str, Any]:
		"""Get AI settings from CRM AI Settings doctype"""
		try:
			settings = frappe.get_single("CRM AI Settings")
			return {
				"enabled": settings.enabled,
				"provider": settings.provider,
				"api_key": settings.get_password("api_key"),
				"model": settings.model,
				"temperature": settings.temperature,
				"max_tokens": settings.max_tokens,
			}
		except Exception:
			# Return defaults if settings don't exist yet
			return {
				"enabled": False,
				"provider": "openai",
				"api_key": None,
				"model": "gpt-4o-mini",
				"temperature": 0.7,
				"max_tokens": 1000,
			}
	
	def _initialize_provider(self):
		"""Initialize the LLM provider based on settings"""
		if not self.settings.get("enabled"):
			return
		
		provider = self.settings.get("provider", "openai")
		
		if provider == "openai":
			from crm.ai.providers import OpenAIProvider
			self.provider = OpenAIProvider(
				api_key=self.settings.get("api_key"),
				model=self.settings.get("model", "gpt-4o-mini"),
				temperature=self.settings.get("temperature", 0.7),
				max_tokens=self.settings.get("max_tokens", 1000),
			)
		elif provider == "anthropic":
			from crm.ai.providers import AnthropicProvider
			self.provider = AnthropicProvider(
				api_key=self.settings.get("api_key"),
				model=self.settings.get("model", "claude-3-5-sonnet-20240620"),
				temperature=self.settings.get("temperature", 0.7),
				max_tokens=self.settings.get("max_tokens", 1000),
			)
		elif provider == "ollama":
			from crm.ai.providers import OllamaProvider
			self.provider = OllamaProvider(
				model=self.settings.get("model", "llama3.1"),
				temperature=self.settings.get("temperature", 0.7),
			)
	
	def is_enabled(self) -> bool:
		"""Check if AI is enabled"""
		return self.settings.get("enabled", False) and self.provider is not None
	
	def chat(
		self,
		messages: List[Dict[str, str]],
		system_prompt: Optional[str] = None,
		context: Optional[Dict[str, Any]] = None,
	) -> str:
		"""
		Send a chat message to the LLM
		
		Args:
			messages: List of message dicts with 'role' and 'content'
			system_prompt: Optional system prompt to set context
			context: Optional context dict for RAG
		
		Returns:
			Response text from LLM
		"""
		if not self.is_enabled():
			frappe.throw("AI is not enabled. Please configure AI settings.")
		
		# Add system prompt if provided
		if system_prompt:
			messages = [{"role": "system", "content": system_prompt}] + messages
		
		# If context is provided, add it to the system message
		if context:
			context_text = self._format_context(context)
			if system_prompt:
				messages[0]["content"] += f"\n\nContext:\n{context_text}"
			else:
				messages.insert(0, {"role": "system", "content": f"Context:\n{context_text}"})
		
		return self.provider.chat(messages)
	
	def complete(
		self,
		prompt: str,
		system_prompt: Optional[str] = None,
		context: Optional[Dict[str, Any]] = None,
	) -> str:
		"""
		Simple text completion
		
		Args:
			prompt: The prompt text
			system_prompt: Optional system instruction
			context: Optional context for RAG
		
		Returns:
			Completion text
		"""
		messages = [{"role": "user", "content": prompt}]
		return self.chat(messages, system_prompt, context)
	
	def _format_context(self, context: Dict[str, Any]) -> str:
		"""Format context dict into readable text"""
		lines = []
		for key, value in context.items():
			if isinstance(value, (dict, list)):
				value = json.dumps(value, indent=2)
			lines.append(f"{key}: {value}")
		return "\n".join(lines)


def get_ai_service() -> AIService:
	"""Get or create AI service instance"""
	if not hasattr(frappe.local, "ai_service"):
		frappe.local.ai_service = AIService()
	return frappe.local.ai_service
