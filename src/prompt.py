"""
RAG용 프롬프트 설계 모듈
- retrieved 문서 + 사용자 질문 → LLM으로 전달할 prompt 생성
"""

from typing import List, Dict, Optional


# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 사회문화 교과서 내용을 기반으로 질문에 답변하는 AI 튜터입니다.

[역할]
- 사회문화 교과서 내용을 정확하게 설명합니다.
- 학생들이 이해하기 쉽게 답변합니다.
- 제공된 참고 문서를 기반으로 답변합니다.

[규칙]
1. 참고 문서에 있는 내용만을 기반으로 답변하세요.
2. 참고 문서에 없는 내용은 "제공된 자료에서 해당 내용을 찾을 수 없습니다"라고 답변하세요.
3. 답변은 명확하고 구조화된 형식으로 제공하세요.
4. 필요한 경우 예시를 들어 설명하세요.
5. 한국어로 답변하세요.
6. "위의 문서를 통해", "참고 문서에서 찾을 수 있습니다" 같은 불필요한 문구는 사용하지 마세요.
7. 답변은 핵심 내용만 간결하게 제공하세요."""


# RAG 프롬프트 템플릿
RAG_PROMPT_TEMPLATE = """아래는 사회문화 교과서에서 검색된 참고 문서입니다:

{context}

---

위의 참고 문서를 바탕으로 다음 질문에 답변해주세요.

질문: {question}

답변:"""


# 간단한 프롬프트 템플릿
SIMPLE_PROMPT_TEMPLATE = """참고 문서:
{context}

질문: {question}

위 참고 문서를 바탕으로 질문에 답변해주세요."""


def create_rag_prompt(
    question: str,
    context: str,
    template: str = "default"
) -> str:
    """
    RAG 프롬프트를 생성합니다.
    
    Args:
        question: 사용자 질문
        context: 검색된 문서 컨텍스트
        template: 프롬프트 템플릿 유형 ("default" 또는 "simple")
        
    Returns:
        완성된 프롬프트
    """
    if template == "simple":
        prompt_template = SIMPLE_PROMPT_TEMPLATE
    else:
        prompt_template = RAG_PROMPT_TEMPLATE
    
    return prompt_template.format(
        context=context,
        question=question
    )


def create_context_from_results(
    results: List[Dict],
    max_length: int = 3000,
    include_metadata: bool = True
) -> str:
    """
    검색 결과에서 컨텍스트 문자열을 생성합니다.
    
    Args:
        results: 검색 결과 리스트
        max_length: 최대 컨텍스트 길이
        include_metadata: 메타데이터 포함 여부
        
    Returns:
        컨텍스트 문자열
    """
    context_parts = []
    current_length = 0
    
    for i, result in enumerate(results):
        text = result['text']
        
        if include_metadata:
            page = result.get('metadata', {}).get('page_number', 'N/A')
            part = f"[문서 {i+1}] (페이지 {page})\n{text}"
        else:
            part = f"[문서 {i+1}]\n{text}"
        
        # 길이 체크
        if current_length + len(part) > max_length:
            # 남은 공간만큼만 추가
            remaining = max_length - current_length
            if remaining > 100:  # 최소 100자는 추가
                part = part[:remaining] + "..."
                context_parts.append(part)
            break
        
        context_parts.append(part)
        current_length += len(part) + 10  # 구분자 길이 고려
    
    return "\n\n---\n\n".join(context_parts)


def create_chat_messages(
    question: str,
    context: str,
    chat_history: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    OpenAI 형식의 채팅 메시지를 생성합니다.
    
    Args:
        question: 사용자 질문
        context: 검색된 문서 컨텍스트
        chat_history: 이전 대화 기록 (선택)
        
    Returns:
        메시지 리스트
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # 이전 대화 기록 추가
    if chat_history:
        for msg in chat_history[-6:]:  # 최근 6개 메시지만
            messages.append(msg)
    
    # 현재 질문 (컨텍스트 포함)
    user_message = create_rag_prompt(question, context)
    messages.append({"role": "user", "content": user_message})
    
    return messages


def format_answer(answer: str, sources: List[Dict] = None) -> str:
    """
    답변을 포맷팅합니다.
    
    Args:
        answer: LLM 답변
        sources: 출처 정보 (검색 결과)
        
    Returns:
        포맷팅된 답변
    """
    # 불필요한 문구 제거
    answer = answer.strip()
    unwanted_phrases = [
        "위의 문서를 통해",
        "위의 참고 문서를 분석하여",
        "위의 문서에서",
        "참고 문서에서 찾을 수 있습니다",
        "참고 문서를 통해",
        "위 문서에서",
        "제공된 문서를 통해",
        "위의 문서에서 다음 세 가지를 통해",
        "위의 문서에서 다음과 같이 설명할 수 있습니다",
        "위의 문서를 분석하여",
        "참고 문서를 분석하여"
    ]
    for phrase in unwanted_phrases:
        answer = answer.replace(phrase, "").replace(phrase + " ", "").replace(" " + phrase, "")
    
    # 연속된 공백 정리
    import re
    answer = re.sub(r'\s+', ' ', answer).strip()
    
    formatted = answer
    
    if sources:
        formatted += "\n\n---\n📚 참고 출처:\n"
        seen_sources = set()  # 중복 제거용
        
        # 페이지 번호별로 그룹화
        page_sources = {}  # {pdf_name: [pages]}
        
        for source in sources[:5]:  # 상위 5개까지
            metadata = source.get('metadata', {})
            page = metadata.get('page_number', 'N/A')
            source_file = metadata.get('source_file', '')
            
            # PDF 파일 이름 그대로 사용 (확장자만 제거)
            if source_file:
                # .json, .txt 확장자만 제거
                pdf_name = source_file.replace('.json', '').replace('.txt', '')
            else:
                pdf_name = "알 수 없는 문서"
            
            # 같은 PDF의 페이지들을 모음
            if pdf_name not in page_sources:
                page_sources[pdf_name] = []
            
            # 중복 제거 (같은 PDF, 같은 페이지)
            source_key = (pdf_name, page)
            if source_key not in seen_sources and page != 'N/A':
                seen_sources.add(source_key)
                page_sources[pdf_name].append(page)
        
        # 페이지 번호 중심으로 출력
        for pdf_name, pages in page_sources.items():
            # 페이지 번호 정렬
            try:
                pages = sorted([p for p in pages if isinstance(p, (int, float))], key=int)
                pages_str = ", ".join([f"{int(p)}" for p in pages])
            except:
                pages_str = ", ".join([str(p) for p in pages])
            
            formatted += f"  • {pdf_name} (페이지 {pages_str})\n"
    
    return formatted


if __name__ == "__main__":
    print("\n" + "="*60)
    print("📝 프롬프트 모듈 테스트")
    print("="*60)
    
    # 테스트 데이터
    test_question = "사회화란 무엇인가요?"
    test_context = """[문서 1] (페이지 15)
사회화는 개인이 사회 구성원으로서 필요한 언어, 가치, 규범, 행동 양식 등을 학습하는 과정이다.

[문서 2] (페이지 16)
사회화는 1차 사회화와 2차 사회화로 구분된다. 1차 사회화는 가정에서 이루어지며, 2차 사회화는 학교, 직장 등에서 이루어진다."""
    
    # 프롬프트 생성
    prompt = create_rag_prompt(test_question, test_context)
    
    print(f"\n📋 생성된 프롬프트:")
    print("-"*40)
    print(prompt)
    print("-"*40)
    
    # 채팅 메시지 생성
    messages = create_chat_messages(test_question, test_context)
    
    print(f"\n💬 채팅 메시지 ({len(messages)}개):")
    for msg in messages:
        role = msg['role']
        content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
        print(f"  [{role}] {content}")
    
    print("\n✅ 프롬프트 모듈 테스트 완료!")


