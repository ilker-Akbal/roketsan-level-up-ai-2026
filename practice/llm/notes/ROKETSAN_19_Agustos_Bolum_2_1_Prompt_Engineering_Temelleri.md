# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 2.1: Prompt Engineering Temelleri

Bu not, workshop öncesi tekrar ve uygulama amacıyla hazırlanmıştır.

---

# 1. Prompt Engineering Nedir?

**Prompt Engineering**, bir LLM'in ağırlıklarını değiştirmeden, ona verilen talimatları ve context'i düzenleyerek daha kontrollü, doğru ve kullanılabilir cevaplar üretmesini sağlamaktır.

Temel fikir:

```text
Prompt
  ↓
LLM
  ↓
Controlled Output
```

Prompt engineering sırasında model yeniden eğitilmez.

Yani:

```text
Model Weights = Değişmez
```

Sadece inference sırasında modele verilen input daha iyi tasarlanır.

---

# 2. İyi Bir Promptun Temel Yapısı

Teknik uygulamalarda iyi bir prompt şu 5 ana bölümden oluşabilir:

```text
ROLE
+
TASK
+
CONTEXT
+
CONSTRAINT
+
OUTPUT FORMAT
```

Bunların her biri farklı bir problemi çözer.

---

# 3. ROLE

**Role**, modelin hangi rolde davranmasını istediğimizi belirtir.

Örnek:

```text
ROLE:
Sen teknik doküman analiz asistanısın.
```

Bu, modelin genel cevap tarzını ve bakış açısını yönlendirmeye yardımcı olur.

## Kötü Role Örneği

```text
Sen uzmansın.
```

Bu çok geneldir.

## Daha İyi Role

```text
Sen teknik dokümanları analiz eden bir mühendislik asistanısın.
```

Daha açık ve görevle ilgilidir.

---

# 4. TASK

**Task**, modelden tam olarak ne yapılmasını istediğimizi söyler.

Örnek:

```text
TASK:
Radarın maksimum tespit menzilini bul.
```

Task mümkün olduğunca:

- Açık
- Tek anlamlı
- Ölçülebilir
- Görev odaklı

olmalıdır.

## Kötü Task

```text
Bu dokümana bak.
```

Burada modelin ne yapacağı net değildir.

## Daha İyi Task

```text
Verilen context içinden radarın maksimum tespit menzilini bul.
```

---

# 5. CONTEXT

**Context**, görevin çözülmesi için modelin kullanacağı bilgidir.

Örnek:

```text
CONTEXT:

The ARX-9 radar operates in X-band.
Its maximum detection range is 45 km.
The system weighs 32 kg.
```

Bu bölüm özellikle RAG sistemlerinde çok önemlidir.

RAG ileride ilgili doküman parçalarını otomatik olarak bulup bu bölüme ekleyecek.

```text
Document
   ↓
Retriever
   ↓
Relevant Chunk
   ↓
CONTEXT
   ↓
LLM
```

---

# 6. CONSTRAINT

**Constraint**, modelin hangi kurallara uyması gerektiğini belirtir.

Örnek:

```text
CONSTRAINTS:

- Yalnızca verilen context'i kullan.
- Tahmin yapma.
- Bilgi bulunamazsa "Bulunamadı" de.
```

Constraint'ler özellikle hallucination azaltmak için önemlidir.

Başka constraint örnekleri:

```text
- Cevabı en fazla 2 cümleyle ver.
- Dokümanda bulunmayan bilgi ekleme.
- Sayısal değerlerin birimini koru.
- Kaynak bulunmuyorsa cevap üretme.
```

---

# 7. OUTPUT FORMAT

**Output Format**, modelin cevabı hangi formatta üretmesini istediğimizi söyler.

Örnek:

```text
OUTPUT FORMAT:
JSON formatında cevap ver.
```

Ancak daha kontrollü kullanım için yalnızca:

```text
JSON formatında cevap ver.
```

demek yerine beklenen JSON yapısını açıkça göstermek daha iyidir.

Örneğin:

```json
{
  "maximum_detection_range": "",
  "unit": "",
  "source": ""
}
```

Bu sayede modelden beklenen response yapısı daha nettir.

---

# 8. Kullanıcının Yazdığı Prompt

Senin oluşturduğun prompt:

```text
ROLE:
Sen teknik doküman analiz asistanısın.

TASK:
Radarın maksimum tespit menzili nedir?

CONTEXT:
The ARX-9 radar operates in X-band.
Its maximum detection range is 45 km.
The system weighs 32 kg.

CONSTRAINT:
- Yalnızca verilen context'i kullan.
- Tahmin yapma.
- Bilgi bulunamazsa "Bulunamadı" de.

OUTPUT FORMAT:
Çıktıyı JSON formatında ver.
```

Bu prompt genel olarak **doğru yapılandırılmıştır**.

---

# 9. Daha Profesyonel Hale Getirilmiş Sürüm

Aynı promptu biraz daha kontrollü hale getirirsek:

```text
ROLE:
Sen teknik dokümanları analiz eden bir mühendislik asistanısın.

TASK:
Verilen context içinden ARX-9 radarının maksimum tespit menzilini belirle.

CONTEXT:
The ARX-9 radar operates in X-band.
Its maximum detection range is 45 km.
The system weighs 32 kg.

CONSTRAINTS:
- Yalnızca verilen context'i kullan.
- Context dışında bilgi ekleme.
- Tahmin yapma.
- İlgili bilgi bulunamazsa "Bulunamadı" yaz.
- Sayısal değerin birimini koru.

OUTPUT FORMAT:
Sadece aşağıdaki JSON formatında cevap ver:

{
  "maximum_detection_range": "",
  "unit": "",
  "source": ""
}
```

---

# 10. Beklenen Cevap

Bu prompt için beklenen çıktı:

```json
{
  "maximum_detection_range": 45,
  "unit": "km",
  "source": "provided_context"
}
```

Burada cevap:

- Context'e dayanıyor
- Tahmin içermiyor
- Parse edilebilir
- Backend tarafından kolayca işlenebilir

---

# 11. Neden JSON Output Önemlidir?

Bir kullanıcıya doğrudan cevap veren chatbot için serbest metin yeterli olabilir.

Ama backend sistemlerinde structured output çok daha kullanışlıdır.

Örneğin serbest metin:

```text
Radarın maksimum tespit menzili 45 kilometredir.
```

İnsan için okunabilir ama programatik olarak işlemek daha zordur.

JSON:

```json
{
  "range": 45,
  "unit": "km"
}
```

Python tarafından kolayca kullanılabilir:

```python
range_value = response["range"]
unit = response["unit"]
```

Structured output özellikle:

- Backend entegrasyonu
- Database kayıtları
- Agent tool kullanımı
- API response'ları
- Otomatik validation
- Pipeline'lar

için önemlidir.

---

# 12. Prompt Neden Parçalara Ayrılır?

Şu prompt:

```text
Radarın menzilini söyle.
```

çalışabilir.

Ama belirsizlik yüksektir.

Buna karşılık:

```text
ROLE
TASK
CONTEXT
CONSTRAINT
OUTPUT FORMAT
```

şeklinde yapılandırılmış prompt:

- Modelin ne yapacağını netleştirir.
- Kullanılacak bilgiyi sınırlar.
- Hallucination riskini azaltır.
- Output'u daha tahmin edilebilir yapar.
- Backend entegrasyonunu kolaylaştırır.

---

# 13. Prompt Engineering'in Asıl Amacı

Prompt engineering'in amacı:

> Modeli "daha zeki" yapmak değildir.

Asıl amaç:

> **Modelin mevcut yeteneklerini daha kontrollü kullanmasını sağlamaktır.**

Yani:

```text
Belirsiz Prompt
      ↓
Çok geniş olası cevap alanı
```

yerine:

```text
Role
+
Task
+
Context
+
Constraint
+
Output Format
      ↓
Daha kontrollü cevap alanı
```

oluşturulur.

---

# 14. Prompt ve RAG İlişkisi

İleride kuracağımız RAG sisteminde prompt yapısı büyük ölçüde aynı kalacak.

Örneğin:

```text
ROLE:
Sen teknik doküman analiz asistanısın.

TASK:
Kullanıcının sorusunu cevapla.

CONTEXT:
{retriever_tarafından_bulunan_chunklar}

QUESTION:
{kullanıcı_sorusu}

CONSTRAINTS:
- Sadece context'i kullan.
- Tahmin yapma.
- Bilgi yoksa "Bulunamadı" de.

OUTPUT FORMAT:
JSON döndür.
```

Burada değişen şey:

```text
CONTEXT
```

bölümünün elle yazılmaması.

RAG sistemi ilgili context'i otomatik bulur.

---

# 15. Basit Python Prompt Builder

```python
def build_prompt(context, question):
    return f'''
ROLE:
Sen teknik doküman analiz asistanısın.

TASK:
Soruyu verilen context'e göre cevapla.

CONTEXT:
{context}

QUESTION:
{question}

CONSTRAINTS:
- Yalnızca context'i kullan.
- Tahmin yapma.
- Bilgi yoksa "Bulunamadı" de.

OUTPUT FORMAT:
JSON formatında cevap ver.
'''
```

Kullanım:

```python
context = '''
The ARX-9 radar operates in X-band.
Its maximum detection range is 45 km.
The system weighs 32 kg.
'''

question = "Radarın maksimum tespit menzili nedir?"

prompt = build_prompt(context, question)

print(prompt)
```

Bu yapı daha sonra RAG içinde tekrar kullanılabilir.

---

# 16. Daha Güvenli JSON Prompt Örneği

Daha kontrollü bir çıktı için:

```python
def build_prompt(context, question):
    return f'''
ROLE:
Sen teknik doküman analiz asistanısın.

TASK:
Soruyu yalnızca verilen context'e göre cevapla.

CONTEXT:
{context}

QUESTION:
{question}

CONSTRAINTS:
- Context dışına çıkma.
- Tahmin yapma.
- Bilgi yoksa status alanını "not_found" yap.
- Sayısal birimleri koru.

OUTPUT FORMAT:
Sadece şu JSON yapısını döndür:

{{
    "status": "found | not_found",
    "answer": "",
    "unit": "",
    "source": ""
}}
'''
```

Bu tarz output formatı gerçek uygulamalarda daha sağlamdır.

---

# 17. Prompt Tasarlarken Yapılan Yaygın Hatalar

## Hata 1 — Çok genel task

```text
Bu dokümanı analiz et.
```

Daha iyi:

```text
Dokümandaki maksimum çalışma sıcaklığını bul.
```

---

## Hata 2 — Context vermemek

Modelin bilmediği özel teknik bilgiyi context olmadan sormak hallucination riskini artırabilir.

---

## Hata 3 — Constraint vermemek

```text
Menzil nedir?
```

yerine:

```text
Sadece verilen context'i kullan.
Tahmin yapma.
```

eklemek daha kontrollüdür.

---

## Hata 4 — Output formatını belirsiz bırakmak

```text
JSON ver.
```

yerine:

```json
{
  "answer": "",
  "source": ""
}
```

gibi schema göstermek daha iyidir.

---

## Hata 5 — Gereksiz uzun role yazmak

Şöyle bir role gerek yok:

```text
Sen dünyanın en iyi, çok deneyimli, mükemmel,
asla hata yapmayan, çok dikkatli bir asistansın...
```

Daha iyi:

```text
Sen teknik doküman analiz asistanısın.
```

Netlik, uzunluktan daha önemlidir.

---

# 18. Workshop İçin Ezberlenmesi Gereken Yapı

```text
ROLE
↓
Model hangi rolde?

TASK
↓
Ne yapacak?

CONTEXT
↓
Hangi bilgiyi kullanacak?

CONSTRAINT
↓
Hangi kurallara uyacak?

OUTPUT FORMAT
↓
Cevabı nasıl döndürecek?
```

Kısa form:

```text
ROLE      → Kim?
TASK      → Ne yapacak?
CONTEXT   → Hangi bilgi?
CONSTRAINT→ Hangi kurallar?
FORMAT    → Nasıl çıktı?
```

---

# 19. Hızlı Tekrar

## ROLE

```text
Sen teknik doküman analiz asistanısın.
```

## TASK

```text
Radarın maksimum tespit menzilini bul.
```

## CONTEXT

```text
Maximum detection range is 45 km.
```

## CONSTRAINT

```text
Sadece context'i kullan.
Tahmin yapma.
```

## OUTPUT FORMAT

```json
{
  "maximum_detection_range": "",
  "unit": ""
}
```

---

# 20. Bu Bölümün Ana Çıkarımları

1. **Prompt engineering model ağırlıklarını değiştirmez.**
2. **İyi prompt açık ve kontrollüdür.**
3. **Role modelin hangi rolde davranacağını belirtir.**
4. **Task yapılacak işi açıklar.**
5. **Context modelin kullanacağı bilgiyi sağlar.**
6. **Constraint modelin sınırlarını belirler.**
7. **Output format cevabın biçimini belirler.**
8. **JSON gibi structured output backend sistemleri için çok kullanışlıdır.**
9. **RAG sistemlerinde ilgili chunklar prompt'un context bölümüne eklenir.**
10. **Prompt ne kadar uzun olduğu için değil, ne kadar net olduğu için iyidir.**

---

# Sonraki Konu

## Bölüm 2.2 — Zero-Shot ve Few-Shot Prompting

Sıradaki kavramlar:

```text
Zero-shot
Few-shot
Examples
Pattern learning
Classification prompts
Technical document extraction examples
```
