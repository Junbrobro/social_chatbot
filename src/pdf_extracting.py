"""
PDF 텍스트 추출 모듈 (STEP 1)
- PyPDF2, pdfplumber 등을 사용하여 PDF에서 텍스트 추출
- output: data/text/ 아래 txt, json 파일 저장
"""

import os
import json
import pdfplumber
from pathlib import Path
from typing import List, Dict
import sys

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ORIGINAL_DIR = DATA_DIR / "original"
TEXT_DIR = DATA_DIR / "text"


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    PDF 파일에서 텍스트를 추출합니다.
    
    Args:
        pdf_path: PDF 파일 경로
        
    Returns:
        각 페이지별 텍스트 정보를 담은 리스트
    """
    pages_data = []
    
    print(f"📖 PDF 파일 열기: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"📄 총 페이지 수: {total_pages}")
        
        for i, page in enumerate(pdf.pages):
            try:
                text = page.extract_text()
                if text:
                    text = text.strip()
                    
                page_data = {
                    "page_number": i + 1,
                    "text": text if text else "",
                    "char_count": len(text) if text else 0
                }
                pages_data.append(page_data)
                
                if (i + 1) % 50 == 0:
                    print(f"  ⏳ 진행 중: {i + 1}/{total_pages} 페이지 처리 완료")
                    
            except Exception as e:
                print(f"  ⚠️ 페이지 {i + 1} 추출 실패: {e}")
                pages_data.append({
                    "page_number": i + 1,
                    "text": "",
                    "char_count": 0,
                    "error": str(e)
                })
    
    print(f"✅ 텍스트 추출 완료: {len(pages_data)} 페이지")
    return pages_data


def save_as_txt(pages_data: List[Dict], output_path: str) -> None:
    """
    추출된 텍스트를 TXT 파일로 저장합니다.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for page in pages_data:
            f.write(f"\n{'='*60}\n")
            f.write(f"[페이지 {page['page_number']}]\n")
            f.write(f"{'='*60}\n\n")
            f.write(page['text'])
            f.write("\n")
    
    print(f"💾 TXT 파일 저장 완료: {output_path}")


def save_as_json(pages_data: List[Dict], output_path: str) -> None:
    """
    추출된 텍스트를 JSON 파일로 저장합니다.
    """
    output_data = {
        "total_pages": len(pages_data),
        "total_chars": sum(p['char_count'] for p in pages_data),
        "pages": pages_data
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 JSON 파일 저장 완료: {output_path}")


def process_all_pdfs(pdf_dir: Path = None) -> None:
    """
    지정된 디렉토리의 모든 PDF 파일을 처리합니다.
    pdf_dir이 None이면 프로젝트 루트의 PDF 파일들을 처리합니다.
    """
    if pdf_dir is None:
        # 프로젝트 루트에서 PDF 파일 찾기
        pdf_files = list(PROJECT_ROOT.glob("*.pdf"))
    else:
        pdf_files = list(Path(pdf_dir).glob("*.pdf"))
    
    if not pdf_files:
        print("⚠️ 처리할 PDF 파일이 없습니다.")
        return
    
    print(f"\n🔍 발견된 PDF 파일: {len(pdf_files)}개")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # 출력 디렉토리 생성
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    
    for pdf_file in pdf_files:
        print(f"\n{'='*60}")
        print(f"📚 처리 중: {pdf_file.name}")
        print(f"{'='*60}")
        
        # 텍스트 추출
        pages_data = extract_text_from_pdf(str(pdf_file))
        
        # 파일명 생성 (확장자 제거)
        base_name = pdf_file.stem
        
        # TXT 저장
        txt_path = TEXT_DIR / f"{base_name}.txt"
        save_as_txt(pages_data, str(txt_path))
        
        # JSON 저장
        json_path = TEXT_DIR / f"{base_name}.json"
        save_as_json(pages_data, str(json_path))
        
        print(f"✅ {pdf_file.name} 처리 완료!\n")


def process_single_pdf(pdf_path: str) -> None:
    """
    단일 PDF 파일을 처리합니다.
    """
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    # 출력 디렉토리 생성
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"📚 처리 중: {pdf_file.name}")
    print(f"{'='*60}")
    
    # 텍스트 추출
    pages_data = extract_text_from_pdf(str(pdf_file))
    
    # 파일명 생성
    base_name = pdf_file.stem
    
    # TXT 저장
    txt_path = TEXT_DIR / f"{base_name}.txt"
    save_as_txt(pages_data, str(txt_path))
    
    # JSON 저장
    json_path = TEXT_DIR / f"{base_name}.json"
    save_as_json(pages_data, str(json_path))
    
    print(f"✅ {pdf_file.name} 처리 완료!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 PDF 텍스트 추출기 시작")
    print("="*60)
    
    if len(sys.argv) > 1:
        # 특정 PDF 파일 처리
        pdf_path = sys.argv[1]
        process_single_pdf(pdf_path)
    else:
        # 프로젝트 루트의 모든 PDF 처리
        process_all_pdfs()
    
    print("\n" + "="*60)
    print("🎉 모든 처리 완료!")
    print(f"📁 결과 저장 위치: {TEXT_DIR}")
    print("="*60 + "\n")


