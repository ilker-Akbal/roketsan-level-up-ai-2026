# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 1: LLM Temelleri

Bu not, workshop öncesi hızlı tekrar için hazırlanmıştır.

---

# 1. LLM Nedir?

**LLM (Large Language Model)**, verilen bağlama göre bir sonraki en olası token'ı tahmin ederek çıktı üreten büyük bir dil modelidir.

Temel mantık:

```text
Önceki tokenlar
      ↓
     LLM
      ↓
Bir sonraki token olasılıkları
      ↓
Token seçimi
      ↓
Tekrar modele verilir
      ↓
Sonraki token
```

Bu işlem cevap tamamlanana kadar tekrar eder.

Önemli fikir:

> **LLM = context'e göre next-token prediction yapan model**

LLM'in temel amacı doğrudan "gerçeği bulmak" değil, bağlama göre olası devamı üretmektir. Bu yüzden yanlış ama kulağa mantıklı gelen cevaplar üretebilir.

---

# 2. Transformer Nedir?

Modern LLM'lerin temel mimarisi çoğunlukla **Transformer** yapısıdır.

Bu aşamada matematiksel detaydan çok şu kavram önemlidir:

## Attention

Attention mekanizması, bir token işlenirken diğer tokenlardan hangilerinin önemli olduğunu belirlemeye yardımcı olur.

Örnek:

```text
Araç GPS sinyalini kaybetti fakat IMU çalışmaya devam etti.
```

Model, `IMU`, `GPS`, `araç`, `çalışmaya devam etti` gibi tokenlar arasındaki ilişkileri değerlendirir.

## Self-Attention

Bir dizideki tokenların aynı dizideki diğer tokenlarla ilişkisini değerlendirmesidir.

Kısa tanım:

> **Self-attention = tokenlar arasındaki bağlamsal ilişkileri değerlendirme mekanizması**

---

# 3. Token Nedir?

LLM'ler doğrudan kelimelerle değil, **tokenlarla** çalışır.

Token şunlardan biri olabilir:

- Tam bir kelime
- Kelimenin bir parçası
- Noktalama işareti
- Özel karakter
- Bazı durumlarda boşlukla birlikte bir metin parçası

Örnek:

```text
electromagnetic
```

Tokenizer'a bağlı olarak:

```text
electro
magnetic
```

şeklinde ayrılabilir.

Türkçe gibi eklemeli dillerde bir kelime birden fazla tokena ayrılabilir.

Önemli:

> **Token ≠ kelime**

---

# 4. Tokenization Nedir?

Metnin tokenlara ayrılması işlemidir.

Pipeline:

```text
Text
 ↓
Tokenizer
 ↓
Tokens
 ↓
Token IDs
 ↓
LLM
```

Örnek:

```text
"ROKETSAN yapay zekâ geliştiriyor."
```

Tokenizer bunu modele göre farklı parçalara ayırabilir.

Daha sonra her token sayısal bir ID ile temsil edilir.

Temsili örnek:

```text
ROKETSAN → 18342
yapay    → 4281
zekâ     → 9372
```

LLM, metin stringlerini doğrudan değil bu sayısal temsilleri işler.

---

# 5. Token Neden Önemlidir?

Token sayısı şu konuları etkiler:

- Context window
- API maliyeti
- Input büyüklüğü
- Output büyüklüğü
- RAG sistemlerinde doküman parçalama ihtiyacı

Örneğin çok büyük bir teknik dokümanın tamamını modele tek seferde vermek mümkün olmayabilir.

Bu problem ileride:

```text
Chunking
+
Embedding
+
Retrieval
+
RAG
```

ile çözülecek.

---

# 6. Context Window Nedir?

**Context window**, modelin tek bir inference sırasında işleyebileceği toplam token bütçesidir.

Bu bütçeye şunlar dahil olabilir:

```text
System prompt
+
Conversation history
+
User prompt
+
RAG context
+
Tool results
+
Model output
```

Dolayısıyla context window sadece kullanıcının son mesajını sınırlandırmaz.

Örnek:

```text
Context Window = 128.000 token
```

Toplam input ve üretilecek output bu bütçe içinde kalmalıdır.

---

# 7. Context Window ve Memory Farkı

Bunlar aynı şey değildir.

## Context

Modelin **şu anda önünde bulunan bilgiler**.

## Memory

Geçmişteki bilgileri saklayıp gerektiğinde yeniden context'e ekleyen mekanizma.

Örnek:

```text
Kullanıcı: Benim aracım F-16.
```

Bu mesaj context'ten çıktıysa model doğal olarak bunu göremez.

Bir memory sistemi bilgiyi saklayabilir:

```text
User vehicle = F-16
```

Daha sonra gerektiğinde:

```text
Memory
  ↓
Relevant information
  ↓
Context
  ↓
LLM
```

şeklinde modele tekrar verilir.

---

# 8. Inference Nedir?

**Inference**, eğitilmiş bir modelin mevcut ağırlıklarını kullanarak çıktı üretmesidir.

YOLO örneği:

```text
Image
 ↓
Trained YOLO
 ↓
Inference
 ↓
Detections
```

LLM örneği:

```text
Prompt
 ↓
Trained LLM
 ↓
Inference
 ↓
Generated Response
```

---

# 9. Training vs Inference

## Training

```text
Data
 ↓
Model
 ↓
Loss
 ↓
Backpropagation
 ↓
Weight Update
```

Model ağırlıkları değiştirilir.

## Inference

```text
Input
 ↓
Trained Model
 ↓
Prediction
```

Ağırlıklar değiştirilmez.

> **Training = öğrenme**
>
> **Inference = öğrenilmiş ağırlıkları kullanarak tahmin üretme**

---

# 10. Autoregressive Generation

LLM genellikle bütün cevabı tek seferde üretmez.

Token token ilerler:

```text
"Kalman filtresi"
       ↓
"bir"
       ↓
"tahmin"
       ↓
"algoritmasıdır"
```

Her yeni token, bir sonraki tahmin için context'in bir parçası olur.

Buna:

**Autoregressive generation**

denir.

---

# 11. Tam LLM Pipeline'ı

```text
USER TEXT
    │
    ▼
TOKENIZER
    │
    ▼
TOKENS / TOKEN IDs
    │
    ▼
TRANSFORMER
(Self-Attention)
    │
    ▼
NEXT TOKEN PROBABILITIES
    │
    ▼
TOKEN SELECTION
    │
    └─────────────┐
                  │
                  ▼
             tekrar modele
                  │
                  ▼
             FINAL ANSWER
```

---

# 12. Neden LLM Yanlış Cevap Verebilir?

LLM'in temel görevi:

```text
"Doğru bilgiyi veritabanından bul"
```

değil,

```text
"Context'e göre en olası devamı üret"
```

mantığıdır.

Bu nedenle model bazen gerçek olmayan ama dilsel olarak ikna edici cevaplar oluşturabilir.

Bu konu bir sonraki bölümde:

- Hallucination
- Temperature
- System/User/Assistant rolleri
- Prompt tasarımı

ile devam edecek.

---

# Hızlı Tekrar Soruları

## 1. LLM'in en temel görevi nedir?

Verilen context ve önceki tokenlara göre **bir sonraki tokenı tahmin ederek anlamlı bir çıktı oluşturmaktır.**

## 2. Token ile kelime aynı şey midir?

Hayır.

Token bir:

- tam kelime,
- kelime parçası,
- noktalama işareti,
- özel karakter

olabilir.

## 3. Transformer'daki attention kabaca ne yapar?

**Tokenlar arasındaki ilişkileri ve bir token için hangi diğer tokenların önemli olduğunu değerlendirir.**

## 4. Context window neyi sınırlar?

Bir inference sırasında modelin işleyebileceği **toplam token bütçesini** sınırlar.

Bu bütçeye input context ve modelin üreteceği output da dahildir.

## 5. Training ile inference arasındaki temel fark nedir?

**Training sırasında model ağırlıkları güncellenir.**

**Inference sırasında ağırlıklar değiştirilmez; mevcut ağırlıklar kullanılarak tahmin üretilir.**

---

# Workshop İçin Ezberlenmesi Gereken 6 Cümle

1. **LLM, context'e göre next-token prediction yapar.**
2. **Token her zaman kelime değildir.**
3. **Transformer'ın temel mekanizmalarından biri self-attention'dır.**
4. **Context window, modelin tek inference sırasında kullanabileceği toplam token bütçesidir.**
5. **Training ağırlıkları değiştirir, inference mevcut ağırlıkları kullanır.**
6. **LLM'in olası bir cevap üretmesi, o cevabın doğru olduğunu garanti etmez.**

---

## Sonraki Konu

**Temperature → System/User/Assistant Messages → Hallucination → LLM neden yanlış cevap verir?**
