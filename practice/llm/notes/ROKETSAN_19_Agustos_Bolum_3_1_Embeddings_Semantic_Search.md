# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 3.1: Embeddings, Semantic Search ve Retrieval Mantığı

Bu not; **embedding, embedding dimension, semantic similarity, cosine similarity, keyword search vs semantic search, query embedding, document embedding, vector database ve RAG retrieval akışı** konularını tekrar etmek için hazırlanmıştır.

---

# 1. Embedding Nedir?

**Embedding**, bir metni sayısal bir vektör ile temsil etme yöntemidir.

Örneğin:

```text
"Radar hedef tespiti yapar."
```

bir embedding modeli tarafından temsili olarak şöyle bir vektöre dönüştürülebilir:

```text
[0.12, -0.84, 0.31, 0.55, ...]
```

Temel pipeline:

```text
TEXT
 ↓
Embedding Model
 ↓
VECTOR
```

Embedding modelinin temel amacı metin üretmek değil, metni **anlamsal olarak karşılaştırılabilir bir sayısal uzayda temsil etmektir.**

---

# 2. Embedding Neden Gereklidir?

Bilgisayar için iki farklı cümlenin anlam olarak yakın olduğunu yalnızca kelime eşleşmesiyle anlamak her zaman mümkün değildir.

Örneğin:

```text
"GNSS konum bilgisi sağlar."
```

ve:

```text
"GPS aracın pozisyonunu belirlemek için kullanılır."
```

kelime olarak aynı değildir.

Ancak anlam olarak oldukça benzerdir.

Embedding modeli bu iki cümleyi vektör uzayında birbirine yakın temsil etmeye çalışır.

Temsili örnek:

```text
GNSS konum bilgisi sağlar.
→ [0.80, 0.20, 0.90]

GPS aracın pozisyonunu belirler.
→ [0.79, 0.22, 0.88]
```

Daha farklı bir konu:

```text
Füzenin motoru katı yakıt kullanır.
→ [-0.40, 0.70, -0.20]
```

Bu nedenle embeddinglerin temel fikri:

> **Anlamsal olarak benzer veriler vektör uzayında birbirine yakın temsil edilir.**

---

# 3. Embedding Model ile LLM Aynı Şey Değildir

## LLM

```text
Prompt
 ↓
LLM
 ↓
Generated Text
```

Temel görevi:

```text
metin üretmek
```

## Embedding Model

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Temel görevi:

```text
metni sayısal/anlamsal vektöre dönüştürmek
```

Embedding modeli doğrudan:

```text
"Radarın menzili 45 km'dir."
```

gibi bir cevap üretmez.

Bunun yerine:

```text
[0.023, -0.451, 0.772, ...]
```

gibi bir vektör üretir.

---

# 4. Embedding Dimension Nedir?

Embedding vektöründe bulunan sayı miktarına **dimension** denir.

Basit örnek:

```text
dimension = 3
```

```text
[0.2, 0.5, -0.8]
```

Gerçek embedding modellerinde dimension sayısı yüzlerce veya binlerce olabilir.

Örneğin:

```text
384
768
1024
1536
3072
```

gibi.

---

# 5. Her Dimension Tek Bir Anlama mı Gelir?

Hayır.

Şöyle düşünmek doğru değildir:

```text
dimension 1 = radar
dimension 2 = GNSS
dimension 3 = sıcaklık
```

Semantic bilgi embedding uzayındaki birçok dimension boyunca dağıtılmış biçimde temsil edilir.

Bu nedenle embedding vektörlerini insan gözüyle doğrudan yorumlamayız.

Onları matematiksel olarak karşılaştırırız.

---

# 6. Semantic Similarity Nedir?

**Semantic similarity**, iki metnin anlam açısından birbirine ne kadar yakın olduğunu ifade eder.

Örnek:

```text
"The radar detects airborne targets."
```

ve:

```text
"The sensor identifies aircraft in the air."
```

kelime olarak farklıdır.

Ama anlamsal olarak oldukça benzerdir.

Embedding modelleri bu iki metnin vektörlerini birbirine yakın üretmeye çalışır.

---

# 7. Keyword Search Nedir?

Keyword search temel olarak kelime veya ifade eşleşmelerine bakar.

Örneğin query:

```text
vehicle position
```

doküman:

```text
GNSS is used to estimate the location of the car.
```

Burada:

```text
vehicle
position
```

kelimeleri birebir geçmeyebilir.

Basit bir keyword search bu cümleyi kaçırabilir.

---

# 8. Semantic Search Nedir?

Semantic search, birebir kelime eşleşmesinden çok **anlam benzerliğini** kullanır.

Örneğin:

```text
vehicle position
```

ile:

```text
location of the car
```

anlamsal olarak yakın kabul edilebilir.

Kısa ayrım:

```text
Keyword Search
→ Kelime benzerliği / eşleşmesi

Semantic Search
→ Anlam benzerliği
```

---

# 9. RAG İçin Embedding Neden Önemlidir?

Diyelim elimizde binlerce teknik doküman chunk'ı var.

Kullanıcı soruyor:

```text
Radarın maksimum tespit menzili nedir?
```

Her chunk'ı LLM'e göndermek istemeyiz.

Bunun yerine:

```text
Question
 ↓
Embedding Model
 ↓
Query Vector
```

oluştururuz.

Doküman chunk'ları da önceden embedding'e çevrilmiştir:

```text
Chunk 1 → Vector
Chunk 2 → Vector
Chunk 3 → Vector
...
Chunk N → Vector
```

Daha sonra query vector ile document vectorlar karşılaştırılır.

```text
Query Vector
     ↓
Similarity Search
     ↓
Most Relevant Chunks
```

Bu, RAG sisteminin retrieval tarafının temel mantığıdır.

---

# 10. Document Embedding

Doküman tarafında işlem genellikle önceden yapılır.

```text
Document
 ↓
Parse
 ↓
Chunking
 ↓
Chunk 1
Chunk 2
Chunk 3
 ↓
Embedding Model
 ↓
Vectors
 ↓
Vector Database
```

Bu aşama çoğu sistemde **indexing / ingestion** aşamasının bir parçasıdır.

---

# 11. Query Embedding

Kullanıcı soru sorduğunda:

```text
User Question
 ↓
Embedding Model
 ↓
Query Vector
```

oluşturulur.

Bu query vector, vector database içindeki document vectorlarla karşılaştırılır.

Önemli:

> Query ve document embeddingleri aynı veya uyumlu embedding uzayında olmalıdır.

---

# 12. Cosine Similarity Nedir?

Embedding vektörlerinin benzerliğini ölçmek için kullanılan yaygın yöntemlerden biri **cosine similarity**'dir.

Formül:

```text
              A · B
cos(A,B) = -----------
             |A||B|
```

Bu aşamada formülü ezberlemekten çok mantığı anlamak önemlidir.

Cosine similarity vektörlerin yönlerinin ne kadar benzer olduğunu ölçer.

Basitleştirilmiş yorum:

```text
1'e yakın  → çok benzer
0'a yakın  → düşük ilişki
-1'e yakın → ters yön
```

Gerçek embedding modellerinde skorların yorumlanması kullanılan modele göre değişebilir.

---

# 13. Basit Cosine Similarity Örnekleri

## Aynı yön

```text
A = [1, 0]
B = [1, 0]
```

```text
cosine similarity = 1
```

## Dik yön

```text
A = [1, 0]
B = [0, 1]
```

```text
cosine similarity = 0
```

## Ters yön

```text
A = [1, 0]
B = [-1, 0]
```

```text
cosine similarity = -1
```

---

# 14. Python ile Cosine Similarity

```python
import numpy as np

a = np.array([1.0, 0.8, 0.2])
b = np.array([0.9, 0.7, 0.3])

similarity = np.dot(a, b) / (
    np.linalg.norm(a) * np.linalg.norm(b)
)

print(similarity)
```

Burada:

```python
np.dot(a, b)
```

dot product hesaplar.

```python
np.linalg.norm(a)
```

vektörün büyüklüğünü hesaplar.

---

# 15. Semantic Search Örneği

Elimizde:

```text
Chunk 1:
The radar has a maximum detection range of 72 km.

Chunk 2:
The navigation system uses GNSS and IMU.

Chunk 3:
The module requires a nominal voltage of 28 V.

Chunk 4:
The operating temperature range is -30°C to +60°C.
```

Kullanıcı:

```text
Radar ne kadar uzaktaki hedefi tespit edebilir?
```

Soru kelime olarak Chunk 1 ile birebir aynı değildir.

Ancak anlam olarak:

```text
ne kadar uzaktaki hedefi tespit edebilir
```

ile:

```text
maximum detection range
```

aynı kavrama yakındır.

Temsili similarity skorları:

```text
Chunk 1 → 0.91
Chunk 2 → 0.31
Chunk 3 → 0.17
Chunk 4 → 0.22
```

En ilgili sonuç:

```text
Chunk 1
```

olur.

---

# 16. Embedding ve Token Farkı

Bu iki kavram karıştırılmamalıdır.

## Token

Metnin model tarafından işlenmek üzere parçalanmış birimidir.

```text
Text
 ↓
Tokenizer
 ↓
Tokens
```

## Embedding

Metnin sayısal vektör temsilidir.

```text
Text / Chunk
 ↓
Embedding Model
 ↓
Vector
```

Kısa ayrım:

```text
Token
→ Metni parçalar

Embedding
→ Anlamı sayısal uzayda temsil eder
```

---

# 17. Embedding Bir Özet Değildir

Embedding:

```text
"The radar range is 72 km."
```

cümlesinin kısa metinsel özeti değildir.

Embedding:

```text
[0.31, -0.72, 0.19, ...]
```

gibi bir sayısal temsildir.

Vektörün kendisini insan okuyup anlamını doğrudan çıkaramaz.

Embeddingler similarity search gibi matematiksel işlemler için kullanılır.

---

# 18. Vector Database'de Neler Saklanır?

Bir RAG sisteminde yalnızca vektör saklamak yeterli değildir.

Genellikle:

```text
Vector
+
Original Text
+
Metadata
```

birlikte tutulur.

Örnek:

```text
Vector:
[0.12, -0.82, ...]

Text:
"The radar has a maximum detection range of 72 km."

Metadata:
document = "radar_manual.pdf"
page = 12
chunk_id = "chunk_42"
```

Metadata sayesinde retrieval sonrasında:

- gerçek metni,
- doküman adını,
- sayfa numarasını,
- chunk ID'sini

kullanabiliriz.

Bu kaynak gösterme açısından çok önemlidir.

---

# 19. Top-k Retrieval

Similarity search sonucunda query'ye en yakın `k` adet chunk'ın alınmasına **top-k retrieval** denir.

Örneğin:

```text
top-k = 3
```

Sonuç:

```text
1. chunk_42 → 0.91
2. chunk_18 → 0.86
3. chunk_73 → 0.80
```

Bu üç chunk LLM'e context olarak verilebilir.

---

# 20. Daha Fazla Chunk Her Zaman Daha İyi Değildir

Çok fazla chunk göndermek:

- token kullanımını artırabilir,
- ilgisiz context ekleyebilir,
- LLM'in dikkatini dağıtabilir.

Bu nedenle amaç:

> **En fazla bilgiyi değil, en ilgili bilgiyi getirmektir.**

---

# 21. Embedding'in Sınırları

Embedding sistemleri kusursuz değildir.

Örneğin:

```text
Maximum temperature is 70°C.
```

ve:

```text
Minimum temperature is 70°C.
```

kelime ve konu bakımından çok benzerdir.

Embeddingleri birbirine yakın olabilir.

Ancak:

```text
maximum
```

ile:

```text
minimum
```

arasındaki fark teknik açıdan çok önemlidir.

Bu nedenle embedding:

> **Doğru cevabı üretmez.**

Embedding yalnızca:

> **İlgili olabilecek metni bulmaya yardımcı olur.**

Son kararı LLM veya başka bir işlem katmanı verir.

---

# 22. Embedding, Vector Search ve LLM Görevleri

Bu üç katmanı ayırmak çok önemlidir.

```text
Embedding
→ Metni anlamsal vektöre dönüştürür.

Vector Search
→ Query'ye en yakın bilgileri bulur.

LLM
→ Bulunan gerçek metni okuyup cevap üretir.
```

Kısa form:

```text
Embedding → Represent
Search    → Retrieve
LLM       → Answer
```

---

# 23. Mini Kontrol Uygulaması

Cümleler:

```text
1. The radar detects airborne targets.

2. The battery supplies 24 V DC power.

3. GNSS provides vehicle position information.

4. The camera detects pedestrians.

5. IMU measures acceleration and angular velocity.

6. Ethernet is used to transmit telemetry data.
```

Query:

```text
"How does the system know where the vehicle is?"
```

---

# 24. Cevap 1 — En Alakalı Cümle

Doğru cevap:

```text
3. GNSS provides vehicle position information.
```

Çünkü:

```text
know where the vehicle is
```

ifadesi anlamsal olarak:

```text
vehicle position information
```

ile ilişkilidir.

---

# 25. Cevap 2 — Keyword Search Neden Kaçırabilir?

Kullanıcının cevabı:

> Çünkü kelime olarak benzemiyorlar.

Bu **doğrudur**.

Query:

```text
How does the system know where the vehicle is?
```

Doküman:

```text
GNSS provides vehicle position information.
```

İki metin aynı anlamı taşımasına rağmen aynı kelimeleri kullanmaz.

Örneğin:

```text
where
≈ position

know where
≈ determine/provide location
```

Basit keyword search birebir kelime eşleşmesi aradığı için bunu kaçırabilir.

Semantic search ise anlam yakınlığını kullanır.

---

# 26. Cevap 3 — Embedding Modelinin Görevi

Kullanıcının cevabı:

> Hayır, ilgili texti vektöre çevirmektir.

Bu **doğrudur**.

Embedding modelinin görevi:

```text
Question
↓
Answer
```

değildir.

Asıl görev:

```text
Text
↓
Embedding
↓
Vector
```

üretmektir.

Bu vektör daha sonra similarity search için kullanılır.

---

# 27. Cevap 4 — Retrieval Akışındaki Eksik Adımlar

Kullanıcının ilk cevabı:

```text
semantic search → LLM
```

genel fikir olarak yönü doğru gösterir.

Ancak teknik açıdan arada önemli adımlar vardır.

Tam akış:

```text
USER QUERY
     ↓
EMBEDDING MODEL
     ↓
QUERY VECTOR
     ↓
VECTOR DATABASE
     ↓
SIMILARITY SEARCH
     ↓
TOP-K RELEVANT CHUNKS
     ↓
LLM CONTEXT
     ↓
LLM
     ↓
FINAL ANSWER
```

Bu akış workshop için özellikle bilinmelidir.

---

# 28. Query Geldiğinde Adım Adım Ne Olur?

Diyelim cümle embeddingleri vector database'e önceden kaydedildi.

Kullanıcı sorar:

```text
How does the system know where the vehicle is?
```

## Adım 1 — Query Embedding

Soru embedding modeline verilir.

```text
Query
 ↓
Embedding Model
 ↓
Query Vector
```

Temsili:

```text
[0.21, -0.54, 0.81, ...]
```

## Adım 2 — Similarity Search

Query vector, database içindeki document vectorlarla karşılaştırılır.

```text
Query Vector
     ↓
Compare
     ↓
Document Vectors
```

## Adım 3 — Ranking

Her chunk için benzerlik skoru elde edilir.

Temsili:

```text
Sentence 1 → 0.41
Sentence 2 → 0.18
Sentence 3 → 0.92
Sentence 4 → 0.32
Sentence 5 → 0.55
Sentence 6 → 0.20
```

## Adım 4 — Top-k Retrieval

En yüksek skorlu sonuçlar alınır.

Örneğin:

```text
top-k = 2
```

ise:

```text
1. GNSS provides vehicle position information.
2. IMU measures acceleration and angular velocity.
```

dönebilir.

## Adım 5 — Original Text Geri Alınır

LLM'e vektörün kendisini değil, vektörle ilişkili gerçek metni veririz.

Normal RAG akışında:

```text
GNSS provides vehicle position information.
```

metni context'e eklenir.

## Adım 6 — LLM Cevap Üretir

```text
CONTEXT:
GNSS provides vehicle position information.

QUESTION:
How does the system know where the vehicle is?
```

LLM:

```text
The system obtains vehicle position information using GNSS.
```

gibi grounded bir cevap üretebilir.

---

# 29. Kritik Ayrım

Şunu özellikle ezberle:

```text
Semantic Search
≠
LLM
```

Semantic search:

```text
ilgili bilgiyi bulur
```

LLM:

```text
bulunan bilgiyi kullanarak cevap üretir
```

---

# 30. RAG'in Retrieval Kısmı

Şu ana kadar öğrendiğimiz parçalar bir araya geldiğinde:

```text
DOCUMENT
   ↓
CHUNKING
   ↓
DOCUMENT EMBEDDINGS
   ↓
VECTOR DATABASE

USER QUERY
   ↓
QUERY EMBEDDING
   ↓
SIMILARITY SEARCH
   ↓
TOP-K CHUNKS
```

Bu bölüm RAG'in:

```text
Retrieval
```

kısmıdır.

Daha sonra:

```text
TOP-K CHUNKS
+
USER QUESTION
↓
LLM
↓
ANSWER
```

eklenince RAG pipeline oluşur.

---

# 31. Workshop İçin Ezberlenmesi Gereken 10 Cümle

1. **Embedding, metni sayısal bir vektörle temsil eder.**
2. **Anlamsal olarak benzer metinler embedding uzayında yakın olabilir.**
3. **Embedding modeli doğrudan cevap üretmez.**
4. **Keyword search kelime benzerliğine, semantic search anlam benzerliğine odaklanır.**
5. **Query de embedding'e çevrilir.**
6. **Query vector, document vectorlarla karşılaştırılır.**
7. **Cosine similarity yaygın benzerlik ölçülerinden biridir.**
8. **Top-k, query'ye en yakın k adet sonucu getirir.**
9. **LLM'e genellikle vektör değil, retrieval ile bulunan gerçek metin/chunk verilir.**
10. **Embedding → Vector Search → Relevant Chunks → LLM, RAG'in temel retrieval-to-generation akışıdır.**

---

# 32. Sonraki Uygulama

Bir sonraki adımda küçük bir Python semantic-search uygulaması yapılacaktır.

Amaç:

```text
5–10 Teknik Cümle
      ↓
Embedding
      ↓
Query Embedding
      ↓
Cosine Similarity
      ↓
Similarity Scores
      ↓
En Yakın Cümleyi Bul
```

Bu uygulama sayesinde embedding ve semantic search mantığı gerçek kod üzerinde görülecektir.

Daha sonra:

```text
Vector Database
↓
FAISS / Chroma
↓
RAG
```

aşamalarına geçilecektir.
