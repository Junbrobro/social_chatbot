"""
LLM API 호출 모듈 (STEP 6-1)
- 무료 LLM 사용 (Ollama, HuggingFace, OpenAI 호환 API 등)
- 다양한 LLM 백엔드 지원
"""

import os
from typing import List, Dict, Optional, Generator
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """LLM 추상 클래스"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """텍스트 생성"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """채팅 형식 생성"""
        pass


class OllamaLLM(BaseLLM):
    """
    Ollama 로컬 LLM
    설치: https://ollama.ai
    """
    
    def __init__(
        self,
        model: str = "gemma3:4b",
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, **kwargs) -> str:
        import requests
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        import requests
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                **kwargs
            }
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


class OpenAILLM(BaseLLM):
    """
    OpenAI API (또는 호환 API)
    환경변수: OPENAI_API_KEY
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: str = None,
        base_url: str = None
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url
        self.client = None
        self._initialize()
    
    def _initialize(self):
        try:
            from openai import OpenAI
            
            kwargs = {"api_key": self.api_key}
            if self.base_url:
                kwargs["base_url"] = self.base_url
            
            self.client = OpenAI(**kwargs)
        except ImportError:
            print("⚠️ openai 패키지가 설치되어 있지 않습니다.")
            print("   pip install openai")
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return "OpenAI 클라이언트가 초기화되지 않았습니다."
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        if not self.client:
            return "OpenAI 클라이언트가 초기화되지 않았습니다."
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content


class HuggingFaceLLM(BaseLLM):
    """
    HuggingFace 로컬 모델 (무료)
    소형 모델 사용으로 로컬에서 실행 가능
    """
    
    def __init__(self, model_name: str = "google/gemma-2-2b-it"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self._initialized = False
    
    def _initialize(self):
        if self._initialized:
            return
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            print(f"🤖 HuggingFace 모델 로드 중: {self.model_name}")
            print("   (처음 실행 시 모델 다운로드에 시간이 걸릴 수 있습니다)")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            self._initialized = True
            print("✅ 모델 로드 완료!")
            
        except Exception as e:
            print(f"⚠️ 모델 로드 실패: {e}")
    
    def generate(self, prompt: str, max_new_tokens: int = 512, **kwargs) -> str:
        self._initialize()
        
        if not self.model:
            return "모델이 로드되지 않았습니다."
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        if hasattr(self.model, 'device'):
            inputs = inputs.to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            **kwargs
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # 입력 프롬프트 제거
        response = response[len(prompt):].strip()
        return response
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        # 채팅 형식을 프롬프트로 변환
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Assistant: "
        return self.generate(prompt, **kwargs)


class GroqLLM(BaseLLM):
    """
    Groq API - 초고속 무료 LLM
    """
    
    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        api_key: str = None
    ):
        self.model = model
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY 환경 변수가 설정되지 않았습니다. 환경 변수를 설정하거나 api_key 파라미터를 제공하세요.")
        self.client = None
        self._initialize()
    
    def _initialize(self):
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            print(f"✅ Groq 모델 로드 완료: {self.model}")
        except ImportError:
            print("⚠️ groq 패키지가 설치되어 있지 않습니다.")
            print("   pip install groq")
        except Exception as e:
            print(f"⚠️ Groq 초기화 실패: {e}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return "Groq 클라이언트가 초기화되지 않았습니다."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq 응답 오류: {e}"
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        if not self.client:
            return "Groq 클라이언트가 초기화되지 않았습니다."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq 응답 오류: {e}"


class GeminiLLM(BaseLLM):
    """
    Google Gemini API
    """
    
    def __init__(
        self,
        model: str = "gemini-2.0-flash-lite",
        api_key: str = None
    ):
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY 또는 GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. 환경 변수를 설정하거나 api_key 파라미터를 제공하세요.")
        self.client = None
        self._initialize()
    
    def _initialize(self):
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            print(f"✅ Gemini 모델 로드 완료: {self.model}")
            
        except ImportError:
            print("⚠️ google-generativeai 패키지가 설치되어 있지 않습니다.")
            print("   pip install google-generativeai")
        except Exception as e:
            print(f"⚠️ Gemini 초기화 실패: {e}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return "Gemini 클라이언트가 초기화되지 않았습니다."
        
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini 응답 오류: {e}"
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        if not self.client:
            return "Gemini 클라이언트가 초기화되지 않았습니다."
        
        try:
            # 메시지를 하나의 프롬프트로 변환
            prompt = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    prompt += f"[시스템 지시사항]\n{content}\n\n"
                elif role == "user":
                    prompt += f"[사용자]\n{content}\n\n"
                elif role == "assistant":
                    prompt += f"[어시스턴트]\n{content}\n\n"
            
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini 응답 오류: {e}"


class SimpleLLM(BaseLLM):
    """
    간단한 규칙 기반 응답 (LLM 없이 테스트용)
    """
    
    def generate(self, prompt: str, **kwargs) -> str:
        # 컨텍스트에서 핵심 내용 추출
        if "참고 문서:" in prompt or "[문서" in prompt:
            # 문서 내용이 있으면 요약 형태로 응답
            return self._summarize_context(prompt)
        return "죄송합니다. 질문을 이해하지 못했습니다."
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        # 마지막 사용자 메시지 처리
        for msg in reversed(messages):
            if msg["role"] == "user":
                return self.generate(msg["content"])
        return "메시지가 없습니다."
    
    def _summarize_context(self, prompt: str) -> str:
        """컨텍스트 기반 간단 응답"""
        # 질문 추출
        if "질문:" in prompt:
            question = prompt.split("질문:")[-1].split("\n")[0].strip()
        else:
            question = "알 수 없는 질문"
        
        # 문서 내용 추출
        docs = []
        if "[문서" in prompt:
            import re
            doc_matches = re.findall(r'\[문서 \d+\][^\[]*', prompt)
            docs = [d.strip() for d in doc_matches]
        
        if docs:
            response = f"'{question}'에 대한 답변입니다.\n\n"
            response += "참고 문서에 따르면:\n"
            for i, doc in enumerate(docs[:2], 1):
                # 문서 내용 간략화
                content = doc.split('\n', 1)[-1] if '\n' in doc else doc
                content = content[:200] + "..." if len(content) > 200 else content
                response += f"\n{i}. {content}\n"
            return response
        
        return f"'{question}'에 대한 정보를 찾지 못했습니다."


def get_llm(
    provider: str = "simple",
    **kwargs
) -> BaseLLM:
    """
    LLM 인스턴스를 반환합니다.
    
    Args:
        provider: LLM 제공자 ("simple", "ollama", "openai", "huggingface")
        **kwargs: 추가 설정
        
    Returns:
        LLM 인스턴스
    """
    providers = {
        "simple": SimpleLLM,
        "ollama": OllamaLLM,
        "openai": OpenAILLM,
        "huggingface": HuggingFaceLLM,
        "gemini": GeminiLLM,
        "groq": GroqLLM
    }
    
    if provider not in providers:
        print(f"⚠️ 알 수 없는 provider: {provider}")
        print(f"   사용 가능: {list(providers.keys())}")
        provider = "simple"
    
    return providers[provider](**kwargs)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 LLM 모듈 테스트")
    print("="*60)
    
    # Simple LLM 테스트
    print("\n📝 Simple LLM 테스트:")
    llm = get_llm("simple")
    
    test_prompt = """참고 문서:
[문서 1] (페이지 15)
사회화는 개인이 사회 구성원으로서 필요한 언어, 가치, 규범을 학습하는 과정이다.

질문: 사회화란 무엇인가요?"""
    
    response = llm.generate(test_prompt)
    print(f"\n응답:\n{response}")
    
    print("\n" + "="*60)
    print("✅ LLM 모듈 테스트 완료!")
    print("\n💡 실제 LLM 사용 시:")
    print("   - Ollama: ollama pull llama3.2 후 get_llm('ollama')")
    print("   - OpenAI: OPENAI_API_KEY 환경변수 설정 후 get_llm('openai')")
    print("="*60 + "\n")


