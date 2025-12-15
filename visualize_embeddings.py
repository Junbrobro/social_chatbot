"""
벡터 임베딩 시각화 스크립트
- PCA와 t-SNE를 사용하여 고차원 벡터를 2D/3D로 축소
- matplotlib으로 시각화 및 이미지 저장
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# 경로 설정
DATA_DIR = Path("data")
VECTOR_DB_DIR = DATA_DIR / "vector_db"
VIZ_DIR = DATA_DIR / "viz"
VIZ_DIR.mkdir(parents=True, exist_ok=True)

def load_embeddings():
    """임베딩 벡터와 메타데이터 로드"""
    print("📂 임베딩 데이터 로드 중...")
    
    embeddings_path = VECTOR_DB_DIR / "embeddings.npy"
    metadata_path = VECTOR_DB_DIR / "embeddings_metadata.json"
    
    if not embeddings_path.exists():
        raise FileNotFoundError(f"임베딩 파일을 찾을 수 없습니다: {embeddings_path}")
    
    embeddings = np.load(str(embeddings_path))
    print(f"✅ 임베딩 로드 완료: shape={embeddings.shape}")
    
    metadata = None
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✅ 메타데이터 로드 완료: {metadata['total_chunks']}개 청크")
    
    return embeddings, metadata

def reduce_dimensions_pca(embeddings, n_components=2):
    """PCA를 사용하여 차원 축소"""
    print(f"\n🔄 PCA로 {n_components}D 차원 축소 중...")
    pca = PCA(n_components=n_components, random_state=42)
    reduced = pca.fit_transform(embeddings)
    
    explained_variance = pca.explained_variance_ratio_
    print(f"✅ PCA 완료!")
    print(f"   - 설명된 분산 비율: {explained_variance}")
    print(f"   - 총 설명된 분산: {sum(explained_variance):.2%}")
    
    return reduced, pca

def reduce_dimensions_tsne(embeddings, n_components=2, perplexity=30):
    """t-SNE를 사용하여 차원 축소"""
    print(f"\n🔄 t-SNE로 {n_components}D 차원 축소 중... (이 작업은 시간이 걸릴 수 있습니다)")
    
    # 샘플이 많으면 일부만 사용 (t-SNE는 계산 비용이 높음)
    if len(embeddings) > 1000:
        print(f"   ⚠️ 샘플이 많아서 1000개만 사용합니다.")
        indices = np.random.choice(len(embeddings), 1000, replace=False)
        sample_embeddings = embeddings[indices]
        use_indices = True
    else:
        sample_embeddings = embeddings
        indices = np.arange(len(embeddings))
        use_indices = False
    
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=42, n_iter=1000)
    reduced = tsne.fit_transform(sample_embeddings)
    
    print(f"✅ t-SNE 완료!")
    
    return reduced, indices if use_indices else None

def visualize_2d(reduced, metadata=None, method='PCA', save_path=None):
    """2D 시각화"""
    print(f"\n🎨 2D 시각화 생성 중...")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 소스 파일별로 색상 구분
    if metadata and 'chunks' in metadata:
        source_files = [chunk.get('source_file', 'unknown') for chunk in metadata['chunks']]
        unique_sources = list(set(source_files))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_sources)))
        source_to_color = {src: colors[i] for i, src in enumerate(unique_sources)}
        
        for i, (x, y) in enumerate(reduced):
            source = source_files[i] if i < len(source_files) else 'unknown'
            color = source_to_color.get(source, 'gray')
            ax.scatter(x, y, c=[color], alpha=0.6, s=20)
        
        # 범례 추가
        for source, color in source_to_color.items():
            ax.scatter([], [], c=[color], label=source, s=50)
        ax.legend(loc='upper right', fontsize=8)
    else:
        ax.scatter(reduced[:, 0], reduced[:, 1], alpha=0.6, s=20, c='steelblue')
    
    ax.set_xlabel(f'{method} Component 1', fontsize=12)
    ax.set_ylabel(f'{method} Component 2', fontsize=12)
    ax.set_title(f'임베딩 벡터 시각화 ({method} 2D)\n총 {len(reduced)}개 청크', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 이미지 저장: {save_path}")
    
    plt.show()
    return fig

def visualize_3d(reduced, metadata=None, method='PCA', save_path=None):
    """3D 시각화"""
    print(f"\n🎨 3D 시각화 생성 중...")
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 소스 파일별로 색상 구분
    if metadata and 'chunks' in metadata:
        source_files = [chunk.get('source_file', 'unknown') for chunk in metadata['chunks']]
        unique_sources = list(set(source_files))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_sources)))
        source_to_color = {src: colors[i] for i, src in enumerate(unique_sources)}
        
        for i, (x, y, z) in enumerate(reduced):
            source = source_files[i] if i < len(source_files) else 'unknown'
            color = source_to_color.get(source, 'gray')
            ax.scatter(x, y, z, c=[color], alpha=0.6, s=20)
        
        # 범례 추가
        for source, color in source_to_color.items():
            ax.scatter([], [], [], c=[color], label=source, s=50)
        ax.legend(loc='upper right', fontsize=8)
    else:
        ax.scatter(reduced[:, 0], reduced[:, 1], reduced[:, 2], alpha=0.6, s=20, c='steelblue')
    
    ax.set_xlabel(f'{method} Component 1', fontsize=12)
    ax.set_ylabel(f'{method} Component 2', fontsize=12)
    ax.set_zlabel(f'{method} Component 3', fontsize=12)
    ax.set_title(f'임베딩 벡터 시각화 ({method} 3D)\n총 {len(reduced)}개 청크', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 이미지 저장: {save_path}")
    
    plt.show()
    return fig

def main():
    """메인 함수"""
    print("="*60)
    print("🎨 벡터 임베딩 시각화")
    print("="*60)
    
    # 데이터 로드
    embeddings, metadata = load_embeddings()
    
    # PCA 2D 시각화
    print("\n" + "="*60)
    print("📊 PCA 2D 시각화")
    print("="*60)
    reduced_pca_2d, pca = reduce_dimensions_pca(embeddings, n_components=2)
    visualize_2d(
        reduced_pca_2d, 
        metadata=metadata, 
        method='PCA',
        save_path=VIZ_DIR / "embeddings_pca_2d.png"
    )
    
    # PCA 3D 시각화
    print("\n" + "="*60)
    print("📊 PCA 3D 시각화")
    print("="*60)
    reduced_pca_3d, pca_3d = reduce_dimensions_pca(embeddings, n_components=3)
    visualize_3d(
        reduced_pca_3d,
        metadata=metadata,
        method='PCA',
        save_path=VIZ_DIR / "embeddings_pca_3d.png"
    )
    
    # 3D 결과 저장 (나중에 사용할 수 있도록)
    np.save(str(VIZ_DIR / "reduced_embeddings_pca_3d.npy"), reduced_pca_3d)
    print(f"💾 축소된 3D 벡터 저장: {VIZ_DIR / 'reduced_embeddings_pca_3d.npy'}")
    
    # t-SNE 2D 시각화 (선택적, 시간이 오래 걸림)
    print("\n" + "="*60)
    print("📊 t-SNE 2D 시각화 (선택적)")
    print("="*60)
    user_input = input("t-SNE 시각화를 생성하시겠습니까? (시간이 오래 걸릴 수 있습니다) [y/N]: ")
    if user_input.lower() == 'y':
        reduced_tsne_2d, indices = reduce_dimensions_tsne(embeddings, n_components=2)
        
        # 메타데이터도 샘플링
        sample_metadata = None
        if metadata and 'chunks' in metadata and indices is not None:
            sample_metadata = {'chunks': [metadata['chunks'][i] for i in indices]}
        
        visualize_2d(
            reduced_tsne_2d,
            metadata=sample_metadata,
            method='t-SNE',
            save_path=VIZ_DIR / "embeddings_tsne_2d.png"
        )
    
    print("\n" + "="*60)
    print("✅ 시각화 완료!")
    print("="*60)
    print(f"📁 저장 위치: {VIZ_DIR}")
    print(f"   - embeddings_pca_2d.png")
    print(f"   - embeddings_pca_3d.png")
    if user_input.lower() == 'y':
        print(f"   - embeddings_tsne_2d.png")

if __name__ == "__main__":
    main()



