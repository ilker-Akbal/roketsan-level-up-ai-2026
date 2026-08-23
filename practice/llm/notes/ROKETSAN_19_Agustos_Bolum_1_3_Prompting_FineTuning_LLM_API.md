# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 1.3: Prompting vs Fine-Tuning + LLM API Mantığı

Bu not, workshop öncesi hızlı tekrar için hazırlanmıştır.

---

# 1. Prompting Nedir?

**Prompting**, modelin ağırlıklarını değiştirmeden, verilen talimat ve context ile modelin davranışını yönlendirmektir.

Örnek:

```text
Sen teknik doküman analiz asistanısın.
Sadece verilen kaynağa göre cevap ver.
Cevabı JSON formatında döndür.
```

Burada model yeniden eğitilmez.

```text
Prompt
  ↓
LLM
  ↓
Desired Output
```

Kısa tanım:

> **Prompting = modeli yeniden eğitmeden yönlendirmek**

---

# 2. Fine-Tuning Nedir?

**Fine-tuning**, önceden eğitilmiş bir modelin özel bir dataset ile yeniden eğitilmesidir.

Bu işlem sırasında model ağırlıkları değişir.

```text
Pretrained LLM
      ↓
Special Dataset
      ↓
Training
      ↓
Weight Update
      ↓
Fine-Tuned Model
```

Fine-tuning özellikle şu alanlarda düşünülebilir:

- Belirli cevap stili
- Belirli format
- Domain davranışı
- Tekrarlanan görev kalıpları
- Sınıflandırma
- Özel instruction-following davranışı

Kısa tanım:

> **Fine-tuning = eğitim yoluyla model davranışını değiştirmek**

---

# 3. Prompting ve Fine-Tuning Farkı

| Prompting | Fine-Tuning |
|---|---|
| Ağırlık değişmez | Ağırlık değişir |
| Hızlı uygulanır | Eğitim gerekir |
| Prompt ile yönlendirilir | Dataset ile davranış öğretilir |
| Esnektir | Daha özelleşmiş olabilir |
| Başlangıç maliyeti düşüktür | Eğitim maliyeti vardır |

Workshop için kritik cümle:

> **Prompting modeli yönlendirir, fine-tuning modeli değiştirir.**

---

# 4. RAG ile Fine-Tuning Aynı Şey Değildir

Teknik dokümanların sürekli güncellendiği bir sistemde çoğu zaman bilgiyi modele fine-tune etmek yerine **RAG** kullanılır.

## RAG

```text
Question
   ↓
Search Documents
   ↓
Relevant Information
   ↓
LLM
   ↓
Answer
```

Model ağırlıkları değişmez.

Bilgi harici kaynaktan getirilip context'e eklenir.

## Fine-Tuning

```text
Dataset
   ↓
Training
   ↓
Weight Update
   ↓
Fine-Tuned Model
```

Model ağırlıkları değişir.

---

# 5. Prompting vs RAG vs Fine-Tuning

Üçlü ayrım:

```text
Prompting     → Model nasıl cevap versin?
RAG           → Model hangi bilgiyle cevap versin?
Fine-Tuning   → Modelin davranışı nasıl değişsin?
```

Bir başka kısa gösterim:

```text
Prompting     → Instruction
RAG           → Knowledge / Context
Fine-Tuning   → Behavior / Weights
```

Bu ayrım workshop ve teknik sınav açısından çok önemlidir.

---

# 6. LLM API Nedir?

LLM API, bir Python uygulamasının LLM servisiyle iletişim kurmasını sağlar.

```text
Python Application
        ↓
      API
        ↓
    LLM Service
        ↓
     Response
        ↓
Python Application
```

Genellikle API'ye şunlar gönderilir:

- Model bilgisi
- Messages
- Temperature
- Output limitleri
- Diğer üretim parametreleri

---

# 7. Basit API Request Mantığı

Genel yapı:

```python
request = {
    "model": "some-llm",
    "messages": [
        {
            "role": "system",
            "content": "Sen teknik asistansın."
        },
        {
            "role": "user",
            "content": "Kalman filtresi nedir?"
        }
    ],
    "temperature": 0.2
}
```

API tarafında:

```text
Request
   ↓
LLM Inference
   ↓
Response
```

---

# 8. Basit API Response Mantığı

Temsili response:

```json
{
  "message": {
    "role": "assistant",
    "content": "Kalman filtresi, gürültülü ölçümlerden..."
  }
}
```

Python uygulaması response içinden cevabı alır ve:

- UI'a gösterebilir
- Backend'de işleyebilir
- Veritabanına kaydedebilir
- Başka bir pipeline'a aktarabilir

---

# 9. RAG Sisteminde LLM API'nin Yeri

İleride kuracağımız pipeline:

```text
User Question
      ↓
Retriever
      ↓
Relevant Chunks
      ↓
Prompt Oluştur
      ↓
LLM API
      ↓
Answer
      ↓
UI
```

Yani LLM API bütün sistem değildir.

Sistemin yalnızca:

> **LLM inference katmanıdır.**

RAG, retrieval ve doküman işleme tarafları ayrıca geliştirilir.

---

# 10. API Key

LLM servisleri genellikle bir **API key** ile erişim kontrolü yapar.

API key'i kaynak kodun içine doğrudan yazmak doğru değildir.

Yanlış:

```python
api_key = "secret-key"
```

Daha iyi yaklaşım:

```env
LLM_API_KEY=secret-key
```

Python:

```python
import os

api_key = os.getenv("LLM_API_KEY")
```

Ayrıca:

```text
.env
```

dosyası `.gitignore` içine eklenmelidir.

---

# 11. Input ve Output Tokenları

LLM API kullanımında:

```text
Input Tokens
+
Output Tokens
```

önemlidir.

Input tarafına şunlar girebilir:

- System prompt
- Conversation history
- User message
- RAG chunks
- Tool results

Bu yüzden RAG'da çok fazla alakasız chunk göndermek iyi değildir.

Amaç:

> **En ilgili bilgiyi context'e koymaktır.**

---

# 12. API Hata Türleri

Karşılaşılabilecek tipik hatalar:

```text
401 → Authentication / API key sorunu
429 → Rate limit
5xx → Servis tarafı hata
Timeout → Yanıt süresi aşıldı
Context limit → Fazla token
```

Bunlar production uygulamalarda backend tarafından yönetilir.

---

# 13. LLM API ve Memory

Temel LLM API çağrılarının kendiliğinden bütün geçmişi hatırladığını varsaymamak gerekir.

Örnek:

İlk çağrı:

```text
USER:
Benim aracım F-16.
```

Daha sonra tamamen ayrı bir çağrı:

```text
USER:
Benim aracım neydi?
```

Eğer önceki bilgi yeni request'in context'ine eklenmezse model bunu bilemeyebilir.

Çözüm:

```text
Memory
   ↓
Relevant Previous Information
   ↓
Context
   ↓
LLM
```

Örneğin memory sistemi:

```text
User vehicle = F-16
```

bilgisini saklar.

Sonraki soruda bu bilgi tekrar context'e eklenir.

Önemli:

> Bunun için fine-tuning gerekmez.

---

# 14. Kontrol Soruları ve Cevaplar

## Senaryo A

Modelin her cevabı şu formatta vermesi isteniyor:

```json
{
  "answer": "",
  "source": ""
}
```

### Cevap:

**Prompting**

Çünkü sadece modelin nasıl cevap vermesi gerektiğini belirliyoruz.

---

## Senaryo B

Her hafta yeni teknik PDF'ler geliyor ve modelin bunlar hakkında soru cevaplaması isteniyor.

### Cevap:

**RAG**

Çünkü sürekli güncellenen harici bilgiyi modele gerektiğinde getirip context'e eklemek istiyoruz.

Yeni doküman geldiğinde modeli yeniden eğitmek gerekmez.

---

## Senaryo C

Model sürekli uzun cevap veriyor ve binlerce örnek üzerinden şirketin kısa teknik cevap stilini öğrenmesi isteniyor.

### Cevap:

**Fine-Tuning**

Çünkü modelin kalıcı davranış biçimini çok sayıda eğitim örneğiyle değiştirmek istiyoruz.

---

## Senaryo D

Kullanıcı:

```text
Benim aracım F-16.
```

diyor.

Daha sonra:

```text
Benim aracım neydi?
```

diye soruyor.

### Cevap:

**Fine-tuning gerekmez.**

Bu bilgi ayrı bir **memory sistemi** içinde tutulabilir.

Daha sonra kullanıcı ilgili soruyu sorduğunda:

```text
Memory
   ↓
"User vehicle = F-16"
   ↓
Context
   ↓
LLM
```

şeklinde modelin context'ine tekrar eklenebilir.

---

# 15. Workshop İçin Ezberlenmesi Gereken 8 Cümle

1. **Prompting modeli yeniden eğitmeden yönlendirir.**
2. **Fine-tuning sırasında model ağırlıkları değişir.**
3. **RAG model ağırlıklarını değiştirmez; harici bilgiyi context'e getirir.**
4. **Prompting = nasıl cevap versin?**
5. **RAG = hangi bilgiyle cevap versin?**
6. **Fine-tuning = modelin davranışı nasıl değişsin?**
7. **LLM API, uygulama ile LLM inference servisi arasındaki iletişim katmanıdır.**
8. **Conversation memory için modeli fine-tune etmek gerekmez; bilgi saklanıp gerektiğinde context'e eklenebilir.**

---

# Bölüm 1 Sonu

Bu noktada tamamlanan LLM temel konuları:

- LLM
- Transformer
- Self-Attention
- Token
- Tokenization
- Context Window
- Inference
- Training vs Inference
- Autoregressive Generation
- Temperature
- System / User / Assistant Messages
- Hallucination
- Grounded Answer
- Prompting
- Fine-Tuning
- RAG ile temel fark
- LLM API mantığı
- API Key
- Input / Output Token
- Memory ile context ilişkisi

---

# Sonraki Ana Bölüm

## Bölüm 2 — Prompt Engineering

Sıradaki konular:

```text
Role
Task
Context
Constraint
Output Format
Zero-shot
Few-shot
Structured Output
JSON Output
Hallucination Reduction
Technical Document Prompts
```
