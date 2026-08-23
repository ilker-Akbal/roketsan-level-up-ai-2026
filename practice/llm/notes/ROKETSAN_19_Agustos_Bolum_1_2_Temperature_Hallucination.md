# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 1.2: Temperature, Message Rolleri ve Hallucination

Bu not, workshop öncesi hızlı tekrar için hazırlanmıştır.

---

# 1. Temperature Nedir?

**Temperature**, LLM'in bir sonraki tokenı seçerken olasılık dağılımını ne kadar keskin veya ne kadar çeşitli kullanacağını etkileyen parametredir.

Model örneğin şu olasılıkları üretmiş olsun:

```text
Ankara      0.96
İstanbul    0.02
İzmir       0.01
Bursa       0.01
```

## Düşük Temperature

Örnek:

```text
temperature = 0.1
```

Genellikle:

- Daha deterministik
- Daha tutarlı
- Daha az çeşitli
- Yüksek olasılıklı tokenlara daha çok yönelen

çıktılar üretir.

Teknik doküman analizi gibi görevlerde genellikle daha uygundur.

## Yüksek Temperature

Örnek:

```text
temperature = 1.0
```

Genellikle:

- Daha çeşitli
- Daha değişken
- Daha yaratıcı

çıktılar oluşturabilir.

---

# Önemli Düzeltme

Temperature:

> Kullanılan veya kontrol edilen token sayısını değiştirmez.

Bunun yerine:

> **Tokenların olasılık dağılımını değiştirir.**

Düşük temperature, yüksek olasılıklı tokenları daha baskın hale getirir.

Yüksek temperature ise düşük olasılıklı alternatiflerin seçilme ihtimalini artırabilir.

Bu nedenle:

```text
Low temperature ≠ doğru cevap garantisi
```

Temperature modelin bilgi seviyesini değiştirmez.

---

# 2. System, User ve Assistant Rolleri

Bir LLM konuşması genellikle mesaj rollerinden oluşur.

```python
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
```

---

## System Message

Modelin genel davranış kurallarını belirler.

Örnek:

```text
Sen teknik doküman analizi yapan bir asistansın.

Sadece verilen dokümana dayanarak cevap ver.

Dokümanda cevap yoksa:
"Dokümanda bulunamadı."
yaz.

Tahmin yapma.
```

Kısa tanım:

> **System message = modelin genel davranış politikası**

---

## User Message

Kullanıcının sorusunu veya görevini içerir.

Örnek:

```text
Maksimum çalışma sıcaklığı nedir?
```

Kısa tanım:

> **User message = kullanıcının isteği**

---

## Assistant Message

Modelin daha önce verdiği cevapları temsil eder.

Örnek:

```text
USER:
Sensörün adı nedir?

ASSISTANT:
XG-200 IMU'dur.

USER:
Peki çalışma sıcaklığı nedir?
```

Önceki assistant mesajları conversation context'in bir parçası olabilir.

---

# 3. Hallucination Nedir?

**Hallucination**, LLM'in yanlış, uydurma veya verilen kaynakla desteklenmeyen bilgiyi doğruymuş gibi üretmesidir.

Örnek doküman:

```text
Operating temperature:
-20°C to +70°C
```

Doğru cevap:

```text
Maximum temperature = +70°C
```

Model:

```text
Maximum temperature = +85°C
```

derse hallucination oluşmuştur.

---

# 4. LLM Neden Hallucination Yapar?

LLM'in temel amacı:

```text
Gerçeği veritabanından doğrula
```

değil,

```text
Context'e göre olası bir sonraki tokenı üret
```

mantığıdır.

Dolayısıyla yeterli bilgi yokken de dilsel olarak mantıklı görünen bir devam üretebilir.

Örneğin:

```text
Maximum speed is ...
```

ifadesinden sonra model eğitim örüntülerine göre:

```text
Mach 2
```

üretebilir.

Ancak bu değerin verilen teknik dokümanda bulunması gerekmez.

---

# 5. Hallucination Nedenleri

Başlıca nedenler:

- Modelin bilgisinin eksik olması
- Bilginin güncel olmaması
- Prompt'un belirsiz olması
- Modelin mutlaka cevap vermeye zorlanması
- Gerekli context'in modele verilmemesi
- RAG sisteminin yanlış doküman parçası getirmesi

---

# 6. Hallucination Nasıl Azaltılır?

## İyi System Prompt

```text
Sadece verilen context'i kullan.

Context'te cevap yoksa:
"Bilgi bulunamadı."
de.

Tahmin yapma.

Kaynak belirt.
```

---

## RAG Kullanmak

```text
User Question
      ↓
Retriever
      ↓
Relevant Document Chunks
      ↓
LLM
      ↓
Grounded Answer
```

Modelin önüne gerçek ve ilgili doküman parçaları verilir.

---

## Structured Output

Örneğin:

```json
{
  "answer": "70°C",
  "source": "chunk_14",
  "status": "found"
}
```

Bu yapı cevabı kontrol etmeyi kolaylaştırır.

---

# 7. Grounded Answer Nedir?

**Grounded answer**, modelin cevabının verilen gerçek kaynağa veya context'e dayanmasıdır.

Örnek context:

```text
[Chunk 14]
The operating temperature range is -20°C to +70°C.
```

Cevap:

```text
Maksimum çalışma sıcaklığı +70°C'dir.
Kaynak: Chunk 14
```

Bu bir grounded answer'dır.

## Önemli Düzeltme

Grounded answer yalnızca:

```text
cevabın sonuna kaynak yazmak
```

değildir.

Asıl önemli olan:

> **Cevaptaki bilginin gerçekten verilen kaynak tarafından desteklenmesidir.**

Kaynak göstermek bunun doğrulanabilir olmasını sağlar.

---

# 8. Basit LLM API Mantığı

Genel yapı:

```python
messages = [
    {
        "role": "system",
        "content": "Sadece verilen kaynağa göre cevap ver."
    },
    {
        "role": "user",
        "content": "Maksimum çalışma sıcaklığı nedir?"
    }
]

response = llm.generate(
    messages=messages,
    temperature=0.1
)
```

Burada:

```text
messages
```

→ modelin context'i

```text
temperature
```

→ token seçimindeki olasılık davranışı

```text
response
```

→ inference sonucu

---

# 9. Teknik Doküman Örneği

Context:

```text
[Source: MIL-STD-X, chunk 27]

The equipment shall operate within
a temperature range of -30°C to +65°C.
```

System:

```text
Answer only from the supplied context.

If the answer is unavailable,
say that it is unavailable.

Always provide the source.
```

User:

```text
Maksimum çalışma sıcaklığı nedir?
```

Doğru assistant davranışı:

```text
Maksimum çalışma sıcaklığı +65°C'dir.

Kaynak: MIL-STD-X, chunk 27
```

---

# 10. Normal LLM ve RAG Arasındaki İlk Fark

## Normal LLM

```text
Question
   ↓
LLM
   ↓
Modelin mevcut bilgilerine göre cevap
```

## RAG

```text
Question
   ↓
Document Retrieval
   ↓
Relevant Context
   ↓
LLM
   ↓
Document-grounded Answer
```

---

# Kontrol Soruları ve Düzeltilmiş Cevaplar

## 1. Temperature 0.1 ile 1.0 arasındaki temel fark nedir?

**Temperature 0.1**, olasılık dağılımını daha keskin hale getirerek yüksek olasılıklı tokenların seçilmesini daha baskın yapar. Çıktı daha deterministik olur.

**Temperature 1.0**, alternatif tokenların seçilme ihtimalini artırarak daha çeşitli sonuçlar üretebilir.

> Temperature token sayısını değiştirmez.

---

## 2. Temperature'ı düşürmek neden cevabı otomatik olarak doğru yapmaz?

Çünkü temperature yalnızca token seçimindeki olasılık dağılımını değiştirir.

Modelin sahip olmadığı veya yanlış bildiği bir bilgi, düşük temperature ile de yanlış üretilebilir.

---

## 3. System message'ın görevi nedir?

Modelin:

- Genel davranış kurallarını
- Kısıtlarını
- Rolünü
- Nasıl cevap vermesi gerektiğini

belirlemektir.

---

## 4. Hallucination nedir?

LLM'in yeterli veya doğru bilgi olmadığı halde yanlış, uydurma veya kaynaksız bir bilgiyi doğruymuş gibi üretmesidir.

---

## 5. Dokümanda bilgi yokken iyi bir teknik asistan ne yapmalıdır?

```text
Bilgi bulunamadı.
```

veya benzeri açık bir cevap vermelidir.

Tahmin, yaklaşık değer veya uydurma bilgi üretmemelidir.

---

## 6. Grounded answer ne demektir?

Cevabın verilen kaynak veya context tarafından gerçekten desteklenmesi demektir.

Kaynak/chunk bilgisi göstermek, bu cevabın doğrulanmasını kolaylaştırır.

---

# Workshop İçin Ezberlenmesi Gereken 7 Cümle

1. **Temperature token sayısını değil, token olasılık dağılımını etkiler.**
2. **Düşük temperature daha deterministik çıktı üretir.**
3. **Düşük temperature doğru cevap garantisi değildir.**
4. **System message modelin genel davranış kurallarını belirler.**
5. **Hallucination yanlış veya kaynaksız bilginin gerçekmiş gibi üretilmesidir.**
6. **Bilgi kaynakta yoksa teknik asistan tahmin yapmak yerine bunu açıkça söylemelidir.**
7. **Grounded answer, cevabın gerçek bir kaynak/context tarafından desteklenmesidir.**

---

# Sonraki Konu

**Prompting vs Fine-Tuning → LLM API Mantığı → LLM Temellerinin Tamamlanması**
