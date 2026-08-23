# ROKETSAN 19 Ağustos — Bölüm 3.3: Gerçek PDF RAG, Chunking ve Retrieval Problemleri

## 1. Gerçek PDF pipeline

Bu bölümde hard-coded cümlelerden gerçek bir MIL-STD PDF dokümanına geçildi.

```text
PDF
↓
PyMuPDF
↓
Page-based Text Extraction
↓
Word-based Chunking
↓
Metadata
↓
Embeddings
↓
FAISS
↓
Retriever
↓
Context Builder
↓
Local LLM
↓
Grounded Answer + Citation
```

Kullanılan doküman 30 sayfalık MIL-STD-2041F(SH) idi. İlk chunking sonucunda 127 chunk, minimum chunk filtresi sonrasında 119 chunk üretildi.

## 2. Chunking ayarları

```python
chunk_size = 120
overlap = 30
min_chunk_words = 30
```

- `chunk_size`: chunk başına hedef maksimum kelime sayısı.
- `overlap`: ardışık chunk'ların ortak kelime miktarı.
- `min_chunk_words`: sayfa sonunda oluşan çok küçük ve anlamsız parçaları engeller.

Örneğin yalnızca `use.` gibi bir chunk oluşması retrieval kalitesini bozabilir.

## 3. Metadata

Her chunk şu yapıda tutuldu:

```python
{
    "text": "...",
    "document": "manual.pdf",
    "page": 18,
    "chunk_id": "chunk_0066"
}
```

Bu yapı citation için kullanıldı.

## 4. İlk gerçek retrieval testi

Soru:

```text
Bu standardın amacı nedir?
```

Doğru `1.1 Purpose` chunk'ı:

```text
Page 4
chunk_0006
Score: 0.5443
Rank 1
```

olarak bulundu.

## 5. Sayısal bilgi testi

Soru:

```text
Suda izin verilen maksimum klorür iyonu miktarı nedir?
```

Doğru cevap chunk'ı Rank 3'te bulundu:

```text
Page 18
chunk_0066
Score: 0.6693
```

LLM doğru şekilde:

```text
1.0 ppm, maximum
```

cevabını verdi.

Önemli:

```text
Top-1 result
≠
her zaman answer-containing chunk
```

## 6. Teknik değerleri koruma

Prompt'a şu kural eklendi:

```text
Preserve technical values, units, limits and identifiers exactly as stated in the context.
```

Amaç; değer, birim ve teknik identifier'ların cevabın içinde bozulmamasıdır.

## 7. Mercury testi ve recall problemi

Türkçe sorgu:

```text
Cıvanın donanım yüzeyleriyle temasına izin veriliyor mu?
```

Doğru açık hükmü içeren:

```text
Page 9
chunk_0027
```

Türkçe sorguda:

```text
Rank 21
Score: 0.5207
```

olarak bulundu.

Bu retrieval recall problemidir.

### Recall
Doğru chunk candidate set'in içine girebildi mi?

### Precision
Getirilen candidate chunk'ların ne kadarı gerçekten ilgili?

Top-K büyüdükçe recall artabilir; precision ve context kalitesi düşebilir.

## 8. Query rewriting

Aynı soru doküman diline yakın İngilizce sorguyla:

```text
Is contact between hardware surfaces and mercury or mercury compounds permitted?
```

sorulduğunda doğru chunk:

```text
Rank 3
Score: 0.6703
```

seviyesine yükseldi.

Bu, query representation'ın retrieval sıralamasını ciddi biçimde etkileyebildiğini gösterdi.

## 9. Query drift

Local LLM ile otomatik rewrite sırasında `cıva` yanlışlıkla `copper` olarak çevrildi.

Bu, query/entity drift örneğidir.

Teknik dokümanlarda özellikle şu öğeler korunmalıdır:

- kimyasal isimler
- malzemeler
- parça isimleri
- sayılar
- birimler
- standard identifier'ları

## 10. Güvenli minimal yaklaşım

Workshop öncesi zaman nedeniyle gelişmiş reranking detaylarına girilmedi.

Minimal güvenli iyileştirme:

```text
Original Query → FAISS
         +
Rewritten Query → FAISS
         ↓
Merge + Deduplicate
         ↓
Candidate Chunks
```

Böylece rewrite tek retrieval kaynağı olmaz.

## 11. Groundedness vs factual correctness

Bir cevap dokümana göre doğru olabilir fakat retrieved context tarafından desteklenmiyorsa grounded değildir.

```text
Factual correctness
≠
Groundedness
```

RAG'de cevabın retrieved source tarafından desteklenmesi gerekir.

## 12. Sonraya bırakılan gelişmiş konular

- Cross-encoder reranking
- Reciprocal Rank Fusion
- Hybrid search
- Query expansion
- Semantic chunking
- Section-aware chunking
- Threshold calibration
- Retrieval evaluation metrics
- Automated groundedness evaluation

## 13. Bu bölümde pratikte görülen kavramlar

```text
PDF parsing
Chunking
Chunk overlap
Minimum chunk size
Metadata
Embeddings
FAISS
IndexFlatIP
Cosine similarity
Top-K
Retriever
Similarity threshold
Context builder
Prompt grounding
not_found
Local LLM
Citation
Recall
Precision
Query rewriting
Query drift
```

## 14. Sonraki konu

```text
MEMORY
```

Ardından:

```text
AGENTIC AI
```
