"""
텍스트 청킹 모듈 (STEP 2)
- 추출된 텍스트를 적절한 크기의 청크로 분할
- 문단/문장/토큰 기반 청킹 지원
- output: data/chunks/ 아래 json 파일 저장

청킹 기준:
- chunk_size: 500자 (한국어 기준 적절한 크기)
- overlap: 100자 (문맥 유지를 위한 오버랩)
- 문단 단위로 우선 분할 후, 긴 문단은 문장 단위로 재분할
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
import sys

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEXT_DIR = DATA_DIR / "text"
CHUNKS_DIR = DATA_DIR / "chunks"

# 청킹 설정
DEFAULT_CHUNK_SIZE = 500  # 청크당 최대 글자 수
DEFAULT_OVERLAP = 100     # 청크 간 오버랩 글자 수


def load_text_from_json(json_path: str) -> List[Dict]:
    """
    JSON 파일에서 페이지별 텍스트를 로드합니다.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('pages', [])


def load_text_from_txt(txt_path: str) -> str:
    """
    TXT 파일에서 전체 텍스트를 로드합니다.
    """
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()


def clean_text(text: str) -> str:
    """
    텍스트 전처리: 불필요한 공백, 특수문자 정리
    """
    if not text:
        return ""
    
    # 연속된 공백을 하나로
    text = re.sub(r'[ \t]+', ' ', text)
    # 연속된 줄바꿈을 최대 2개로
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 앞뒤 공백 제거
    text = text.strip()
    
    return text


def split_into_paragraphs(text: str) -> List[str]:
    """
    텍스트를 문단 단위로 분할합니다.
    """
    # 빈 줄을 기준으로 문단 분할
    paragraphs = re.split(r'\n\s*\n', text)
    # 빈 문단 제거 및 정리
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs


def split_into_sentences(text: str) -> List[str]:
    """
    텍스트를 문장 단위로 분할합니다.
    한국어 문장 종결 부호 기준
    """
    # 문장 종결 부호로 분할 (마침표, 물음표, 느낌표)
    sentences = re.split(r'(?<=[.?!。])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def create_chunks_with_overlap(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
) -> List[Dict]:
    """
    텍스트를 오버랩이 있는 청크로 분할합니다.
    
    Args:
        text: 분할할 텍스트
        chunk_size: 청크당 최대 글자 수
        overlap: 청크 간 오버랩 글자 수
        
    Returns:
        청크 정보를 담은 딕셔너리 리스트
    """
    chunks = []
    text = clean_text(text)
    
    if not text:
        return chunks
    
    # 문단으로 먼저 분할
    paragraphs = split_into_paragraphs(text)
    
    current_chunk = ""
    chunk_id = 0
    
    for para in paragraphs:
        # 문단이 chunk_size보다 크면 문장 단위로 분할
        if len(para) > chunk_size:
            sentences = split_into_sentences(para)
            for sent in sentences:
                if len(current_chunk) + len(sent) + 1 <= chunk_size:
                    current_chunk += (" " if current_chunk else "") + sent
                else:
                    if current_chunk:
                        chunks.append({
                            "chunk_id": chunk_id,
                            "text": current_chunk.strip(),
                            "char_count": len(current_chunk.strip())
                        })
                        chunk_id += 1
                        # 오버랩 적용
                        if overlap > 0 and len(current_chunk) > overlap:
                            current_chunk = current_chunk[-overlap:] + " " + sent
                        else:
                            current_chunk = sent
                    else:
                        # 문장 자체가 너무 길면 강제 분할
                        if len(sent) > chunk_size:
                            for i in range(0, len(sent), chunk_size - overlap):
                                chunk_text = sent[i:i + chunk_size]
                                chunks.append({
                                    "chunk_id": chunk_id,
                                    "text": chunk_text.strip(),
                                    "char_count": len(chunk_text.strip())
                                })
                                chunk_id += 1
                        else:
                            current_chunk = sent
        else:
            # 문단을 현재 청크에 추가
            if len(current_chunk) + len(para) + 2 <= chunk_size:
                current_chunk += ("\n\n" if current_chunk else "") + para
            else:
                if current_chunk:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": current_chunk.strip(),
                        "char_count": len(current_chunk.strip())
                    })
                    chunk_id += 1
                    # 오버랩 적용
                    if overlap > 0 and len(current_chunk) > overlap:
                        current_chunk = current_chunk[-overlap:] + "\n\n" + para
                    else:
                        current_chunk = para
                else:
                    current_chunk = para
    
    # 마지막 청크 추가
    if current_chunk:
        chunks.append({
            "chunk_id": chunk_id,
            "text": current_chunk.strip(),
            "char_count": len(current_chunk.strip())
        })
    
    return chunks


def chunk_by_pages(
    pages_data: List[Dict],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
) -> List[Dict]:
    """
    페이지별 데이터를 청킹하고 페이지 정보를 메타데이터로 포함합니다.
    """
    all_chunks = []
    global_chunk_id = 0
    
    for page in pages_data:
        page_num = page.get('page_number', 0)
        text = page.get('text', '')
        
        if not text:
            continue
        
        page_chunks = create_chunks_with_overlap(text, chunk_size, overlap)
        
        for chunk in page_chunks:
            chunk['global_chunk_id'] = global_chunk_id
            chunk['page_number'] = page_num
            chunk['source_type'] = 'page'
            all_chunks.append(chunk)
            global_chunk_id += 1
    
    return all_chunks


def save_chunks_to_json(chunks: List[Dict], output_path: str, metadata: Dict = None) -> None:
    """
    청크 데이터를 JSON 파일로 저장합니다.
    """
    output_data = {
        "metadata": metadata or {},
        "total_chunks": len(chunks),
        "total_chars": sum(c['char_count'] for c in chunks),
        "avg_chunk_size": sum(c['char_count'] for c in chunks) / len(chunks) if chunks else 0,
        "chunks": chunks
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 청크 파일 저장 완료: {output_path}")


def process_text_file(
    input_path: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
) -> None:
    """
    단일 텍스트 파일을 청킹합니다.
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {input_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"📄 처리 중: {input_file.name}")
    print(f"{'='*60}")
    
    # JSON 파일이면 페이지별 처리
    if input_file.suffix == '.json':
        pages_data = load_text_from_json(str(input_file))
        chunks = chunk_by_pages(pages_data, chunk_size, overlap)
        print(f"📖 {len(pages_data)} 페이지에서 텍스트 로드")
    else:
        # TXT 파일이면 전체 텍스트 처리
        text = load_text_from_txt(str(input_file))
        chunks = create_chunks_with_overlap(text, chunk_size, overlap)
        print(f"📖 텍스트 파일 로드 완료")
    
    print(f"✂️  총 {len(chunks)}개 청크 생성")
    
    # 출력 디렉토리 생성
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 출력 파일명 생성
    base_name = input_file.stem.replace('.json', '').replace('.txt', '')
    output_path = CHUNKS_DIR / f"{base_name}_chunks.json"
    
    # 메타데이터 생성
    metadata = {
        "source_file": input_file.name,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "chunking_method": "paragraph_based_with_sentence_fallback"
    }
    
    # 저장
    save_chunks_to_json(chunks, str(output_path), metadata)
    
    # 통계 출력
    if chunks:
        avg_size = sum(c['char_count'] for c in chunks) / len(chunks)
        min_size = min(c['char_count'] for c in chunks)
        max_size = max(c['char_count'] for c in chunks)
        print(f"\n📊 청킹 통계:")
        print(f"   - 총 청크 수: {len(chunks)}")
        print(f"   - 평균 크기: {avg_size:.1f}자")
        print(f"   - 최소 크기: {min_size}자")
        print(f"   - 최대 크기: {max_size}자")


def process_all_text_files(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
) -> None:
    """
    data/text/ 디렉토리의 모든 JSON 파일을 청킹합니다.
    """
    json_files = list(TEXT_DIR.glob("*.json"))
    
    if not json_files:
        print("⚠️ 처리할 텍스트 파일이 없습니다.")
        print(f"   먼저 pdf_extracting.py를 실행하여 PDF에서 텍스트를 추출하세요.")
        return
    
    print(f"\n🔍 발견된 텍스트 파일: {len(json_files)}개")
    for f in json_files:
        print(f"   - {f.name}")
    
    for json_file in json_files:
        process_text_file(str(json_file), chunk_size, overlap)
    
    print(f"\n✅ 모든 파일 청킹 완료!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("✂️  텍스트 청킹 시작")
    print(f"   - 청크 크기: {DEFAULT_CHUNK_SIZE}자")
    print(f"   - 오버랩: {DEFAULT_OVERLAP}자")
    print("="*60)
    
    if len(sys.argv) > 1:
        # 특정 파일 처리
        input_path = sys.argv[1]
        chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CHUNK_SIZE
        overlap = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_OVERLAP
        process_text_file(input_path, chunk_size, overlap)
    else:
        # 모든 텍스트 파일 처리
        process_all_text_files()
    
    print("\n" + "="*60)
    print("🎉 청킹 완료!")
    print(f"📁 결과 저장 위치: {CHUNKS_DIR}")
    print("="*60 + "\n")


