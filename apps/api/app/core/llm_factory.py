"""LLM Factory for managing multiple LLM providers with fallback support."""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional

from anthropic import AsyncAnthropic
from loguru import logger
from openai import AsyncOpenAI


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt."""
        pass

    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream completion from prompt."""
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion from chat messages."""
        pass

    @abstractmethod
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Stream completion from chat messages."""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider."""

    def __init__(self, api_key: str, model: str = "gpt-4o", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                **{k: v for k, v in kwargs.items() if k not in ["temperature", "max_tokens"]},
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise

    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream completion from prompt."""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                stream=True,
                **{k: v for k, v in kwargs.items() if k not in ["temperature", "max_tokens", "stream"]},
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"OpenAI streaming failed: {e}")
            raise

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion from chat messages."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                **{k: v for k, v in kwargs.items() if k not in ["temperature", "max_tokens"]},
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI chat failed: {e}")
            raise

    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Stream completion from chat messages."""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                stream=True,
                **{k: v for k, v in kwargs.items() if k not in ["temperature", "max_tokens", "stream"]},
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"OpenAI chat streaming failed: {e}")
            raise


class AnthropicProvider(BaseLLMProvider):
    """Anthropic LLM provider."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncAnthropic(api_key=api_key)

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise

    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream completion from prompt."""
        try:
            stream = self.client.messages.stream(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
            )
            async with stream as message_stream:
                async for chunk in message_stream:
                    if chunk.type == "content_block_delta":
                        yield chunk.delta.text
        except Exception as e:
            logger.error(f"Anthropic streaming failed: {e}")
            raise

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion from chat messages."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic chat failed: {e}")
            raise

    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Stream completion from chat messages."""
        try:
            stream = self.client.messages.stream(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1)),
            )
            async with stream as message_stream:
                async for chunk in message_stream:
                    if chunk.type == "content_block_delta":
                        yield chunk.delta.text
        except Exception as e:
            logger.error(f"Anthropic chat streaming failed: {e}")
            raise


class LLMFactory:
    """Factory for managing multiple LLM providers with fallback support."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.specialized_providers: Dict[str, BaseLLMProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all configured providers."""
        providers_config = self.config.get("providers", {})

        # Primary provider
        primary = providers_config.get("primary", {})
        if primary.get("provider") == "openai" and primary.get("api_key"):
            self.providers["primary"] = OpenAIProvider(
                api_key=primary.get("api_key"),
                model=primary.get("model", "gpt-4o"),
                **{k: v for k, v in primary.items() if k not in ["provider", "api_key", "model"]},
            )
        elif primary.get("provider") == "anthropic" and primary.get("api_key"):
            self.providers["primary"] = AnthropicProvider(
                api_key=primary.get("api_key"),
                model=primary.get("model", "claude-3-5-sonnet-20241022"),
                **{k: v for k, v in primary.items() if k not in ["provider", "api_key", "model"]},
            )

        # Fallback providers
        for i, fallback in enumerate(providers_config.get("fallback", [])):
            if fallback.get("provider") == "openai" and fallback.get("api_key"):
                self.providers[f"fallback_{i}"] = OpenAIProvider(
                    api_key=fallback.get("api_key"),
                    model=fallback.get("model", "gpt-4o"),
                    **{k: v for k, v in fallback.items() if k not in ["provider", "api_key", "model"]},
                )
            elif fallback.get("provider") == "anthropic" and fallback.get("api_key"):
                self.providers[f"fallback_{i}"] = AnthropicProvider(
                    api_key=fallback.get("api_key"),
                    model=fallback.get("model", "claude-3-5-sonnet-20241022"),
                    **{k: v for k, v in fallback.items() if k not in ["provider", "api_key", "model"]},
                )

        # Specialized providers
        specialized = providers_config.get("specialized", {})
        for task_name, task_config in specialized.items():
            if task_config.get("provider") == "openai" and task_config.get("api_key"):
                self.specialized_providers[task_name] = OpenAIProvider(
                    api_key=task_config.get("api_key"),
                    model=task_config.get("model", "gpt-4o"),
                    **{k: v for k, v in task_config.items() if k not in ["provider", "api_key", "model"]},
                )
            elif task_config.get("provider") == "anthropic" and task_config.get("api_key"):
                self.specialized_providers[task_name] = AnthropicProvider(
                    api_key=task_config.get("api_key"),
                    model=task_config.get("model", "claude-3-5-sonnet-20241022"),
                    **{k: v for k, v in task_config.items() if k not in ["provider", "api_key", "model"]},
                )

        logger.info(
            f"Initialized {len(self.providers)} general providers and {len(self.specialized_providers)} specialized providers"
        )

    async def get_completion(
        self,
        prompt: str,
        use_fallback: bool = True,
        provider_type: str = "primary",
        specialized_task: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Get completion with fallback support."""
        # Use specialized provider if specified
        if specialized_task and specialized_task in self.specialized_providers:
            try:
                provider = self.specialized_providers[specialized_task]
                return await provider.generate(prompt, **kwargs)
            except Exception as e:
                logger.error(f"Specialized provider {specialized_task} failed: {e}")
                if not use_fallback:
                    raise

        # Try primary provider
        try:
            provider = self.providers.get(provider_type, self.providers.get("primary"))
            if provider:
                return await provider.generate(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Primary provider failed: {e}")
            if not use_fallback:
                raise

        # Try fallback providers
        if use_fallback:
            for key, provider in self.providers.items():
                if key.startswith("fallback"):
                    try:
                        logger.info(f"Trying fallback provider: {key}")
                        return await provider.generate(prompt, **kwargs)
                    except Exception as fallback_error:
                        logger.error(f"Fallback provider {key} failed: {fallback_error}")
                        continue

        raise Exception("All providers failed")

    async def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        use_fallback: bool = True,
        provider_type: str = "primary",
        specialized_task: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Get chat completion with fallback support."""
        # Use specialized provider if specified
        if specialized_task and specialized_task in self.specialized_providers:
            try:
                provider = self.specialized_providers[specialized_task]
                return await provider.chat(messages, **kwargs)
            except Exception as e:
                logger.error(f"Specialized provider {specialized_task} failed: {e}")
                if not use_fallback:
                    raise

        # Try primary provider
        try:
            provider = self.providers.get(provider_type, self.providers.get("primary"))
            if provider:
                return await provider.chat(messages, **kwargs)
        except Exception as e:
            logger.error(f"Primary provider failed: {e}")
            if not use_fallback:
                raise

        # Try fallback providers
        if use_fallback:
            for key, provider in self.providers.items():
                if key.startswith("fallback"):
                    try:
                        logger.info(f"Trying fallback provider: {key}")
                        return await provider.chat(messages, **kwargs)
                    except Exception as fallback_error:
                        logger.error(f"Fallback provider {key} failed: {fallback_error}")
                        continue

        raise Exception("All providers failed")

    async def stream_completion(
        self, prompt: str, provider_type: str = "primary", specialized_task: Optional[str] = None, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream completion from provider."""
        # Use specialized provider if specified
        if specialized_task and specialized_task in self.specialized_providers:
            provider = self.specialized_providers[specialized_task]
            async for chunk in provider.stream(prompt, **kwargs):
                yield chunk
            return

        # Use specified or primary provider
        provider = self.providers.get(provider_type, self.providers.get("primary"))
        if provider:
            async for chunk in provider.stream(prompt, **kwargs):
                yield chunk
        else:
            raise Exception(f"Provider {provider_type} not found")

    async def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        provider_type: str = "primary",
        specialized_task: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion from provider."""
        # Use specialized provider if specified
        if specialized_task and specialized_task in self.specialized_providers:
            provider = self.specialized_providers[specialized_task]
            async for chunk in provider.stream_chat(messages, **kwargs):
                yield chunk
            return

        # Use specified or primary provider
        provider = self.providers.get(provider_type, self.providers.get("primary"))
        if provider:
            async for chunk in provider.stream_chat(messages, **kwargs):
                yield chunk
        else:
            raise Exception(f"Provider {provider_type} not found")

    def get_available_providers(self) -> List[str]:
        """Get list of available provider names."""
        return list(self.providers.keys())

    def get_specialized_tasks(self) -> List[str]:
        """Get list of available specialized tasks."""
        return list(self.specialized_providers.keys())

    def get_provider_info(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific provider."""
        provider = self.providers.get(provider_name) or self.specialized_providers.get(provider_name)
        if provider:
            return {"model": provider.model, "config": provider.config, "type": type(provider).__name__}
        return None
