# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 2.2: Zero-Shot ve Few-Shot Prompting

Bu not, workshop öncesi tekrar ve uygulama amacıyla hazırlanmıştır.

---

# 1. Zero-Shot Prompting Nedir?

**Zero-shot prompting**, modele bir görevi açıklayıp herhangi bir örnek göstermeden çıktı istemektir.

Temel yapı:

```text
Instruction
+
Input
↓
LLM
↓
Output
```

Kısa tanım:

> **Zero-shot = görevi anlat, örnek verme.**

---

# 2. Zero-Shot Örneği

Sınıflar:

```text
SENSOR
POWER
COMMUNICATION
```

Prompt:

```text
Aşağıdaki cümleyi şu sınıflardan birine göre sınıflandır:

SENSOR
POWER
COMMUNICATION

Cümle:
"The module transmits telemetry through Ethernet."
```

Beklenen cevap:

```text
COMMUNICATION
```

Burada model herhangi bir örnek görmeden yalnızca:

- görev tanımı,
- sınıflar,
- giriş cümlesi

üzerinden karar verir.

---

# 3. Few-Shot Prompting Nedir?

**Few-shot prompting**, modele görevin yanında birkaç doğru örnek göstererek beklenen davranış biçimini öğretmektir.

Temel yapı:

```text
Instruction
+
Examples
+
New Input
↓
LLM
↓
Output
```

Kısa tanım:

> **Few-shot = görevi anlat + birkaç örnek göster.**

---

# 4. Few-Shot Örneği

Prompt:

```text
Aşağıdaki örneklere göre yeni cümleyi sınıflandır.

"The radar operates in X-band."
→ SENSOR

"The unit requires 28 V DC."
→ POWER

"The controller communicates over CAN bus."
→ COMMUNICATION

Şimdi sınıflandır:

"The module transmits telemetry through Ethernet."
```

Beklenen cevap:

```text
COMMUNICATION
```

Burada model önce üç farklı sınıf için örnek görür ve yeni cümleyi aynı pattern'e göre sınıflandırır.

---

# 5. Kullanıcının Yazdığı Zero-Shot Prompt

Senin yazdığın zero-shot örneği:

```text
SENSOR
POWER
COMMUNICATION

Bu sınıflara göre bu cümleyi sınıflandır:

"The module transmits telemetry through Ethernet."
```

Bu yaklaşım **doğrudur**.

Ancak biraz daha kontrollü hale getirmek için şu şekilde yazılabilir:

```text
Aşağıdaki teknik cümleyi yalnızca şu sınıflardan biriyle sınıflandır:

- SENSOR
- POWER
- COMMUNICATION

Cümle:
"The module transmits telemetry through Ethernet."

Cevabı yalnızca sınıf adı olarak ver.
```

Beklenen çıktı:

```text
COMMUNICATION
```

---

# 6. Kullanıcının Yazdığı Few-Shot Prompt

Senin few-shot promptun:

```text
"The radar operates in X-band."
→ SENSOR

"The unit requires 28 V DC."
→ POWER

"The controller communicates over CAN bus."
→ COMMUNICATION

Bu örneklere göre bu cümleyi sınıflandır:

"The module transmits telemetry through Ethernet."
```

Bu da **doğru bir few-shot prompttur**.

Daha kontrollü hali:

```text
Aşağıdaki örneklerde kullanılan sınıflandırma yapısını takip et.

Example 1:
"The radar operates in X-band."
→ SENSOR

Example 2:
"The unit requires 28 V DC."
→ POWER

Example 3:
"The controller communicates over CAN bus."
→ COMMUNICATION

Şimdi aşağıdaki cümleyi aynı sınıflardan biriyle sınıflandır:

"The module transmits telemetry through Ethernet."

Cevabı yalnızca sınıf adı olarak ver.
```

Beklenen çıktı:

```text
COMMUNICATION
```

---

# 7. Zero-Shot ve Few-Shot Arasındaki Temel Fark

```text
Zero-shot
↓
Instruction var
Example yok
```

```text
Few-shot
↓
Instruction var
Example var
```

Kısa form:

```text
Zero-shot → Söyle
Few-shot  → Göster + söyle
```

---

# 8. Few-Shot Neden İşe Yarar?

Bazı görevler yalnızca açıklamayla yeterince net olmayabilir.

Özellikle:

- sınıflandırma,
- özel etiketleme,
- teknik çıktı formatı,
- JSON schema,
- domain-specific davranış

gibi durumlarda few-shot örnekleri modele bir pattern gösterir.

Örneğin:

```text
Input:
Maximum operating temperature is 70°C.

Output:
{
  "parameter": "maximum_temperature",
  "value": 70,
  "unit": "°C"
}
```

Bundan sonra:

```text
Input:
Nominal voltage is 24 V.
```

verildiğinde model benzer pattern'i takip etmeye daha yatkın hale gelir.

---

# 9. Few-Shot Modeli Eğitir mi?

Hayır.

Bu çok önemli:

```text
Few-shot ≠ Fine-tuning
```

Few-shot sırasında:

```text
Examples
↓
Prompt / Context
↓
Inference
```

olur.

Model ağırlıkları değişmez.

Fine-tuning'de ise:

```text
Dataset
↓
Training
↓
Weight Update
```

gerçekleşir.

Kısa ayrım:

```text
Few-shot     → Geçici context örnekleri
Fine-tuning  → Kalıcı weight değişimi
```

---

# 10. Zero-Shot Ne Zaman Yeterlidir?

Görev basit ve açık olduğunda zero-shot çoğu zaman yeterlidir.

Örnek:

```text
Aşağıdaki sıcaklığı Fahrenheit'a çevir:
60°C
```

veya:

```text
Bu cümleyi SENSOR, POWER veya COMMUNICATION olarak sınıflandır.
```

Burada birkaç örnek vermek zorunlu değildir.

---

# 11. Few-Shot Ne Zaman Kullanışlıdır?

Few-shot özellikle şu durumlarda faydalıdır:

- Model görevi yanlış yorumluyorsa
- Özel sınıflar varsa
- Çıktı formatı kesin olmalıysa
- Teknik etiketleme yapılıyorsa
- Pattern göstermek gerekiyorsa
- Tutarlı cevap yapısı isteniyorsa

---

# 12. Teknik Dokümanlarda Few-Shot Kullanımı

MIL-STD veya başka teknik dokümanlarda few-shot şu işler için kullanılabilir:

```text
Requirement Classification
Requirement Extraction
JSON Formatting
found / not_found davranışı
Source Format
Technical Answer Style
```

Örneğin:

```text
"The unit shall operate at 28 V DC."
→ POWER

"The vehicle shall estimate its position using GNSS."
→ NAVIGATION

"The equipment shall operate between -20°C and +60°C."
→ TEMPERATURE
```

Bu örneklerden sonra yeni requirement aynı sınıflardan biriyle sınıflandırılabilir.

---

# 13. Few-Shot ve RAG Aynı Şey Değildir

Bu ayrım çok önemlidir.

## Few-Shot

Modele:

```text
Nasıl davranacağını
```

örneklerle gösterir.

## RAG

Modele:

```text
Hangi bilgiyle cevap vereceğini
```

harici dokümanlardan getirir.

Kısa form:

```text
Few-shot → Behavior Pattern
RAG      → Knowledge / Context
```

---

# 14. Few-Shot'un Dezavantajı

Her örnek context içine eklenir.

Bu nedenle token tüketir.

Örneğin:

```text
10 örnek × 300 token = 3000 token
```

Bu yüzden:

> Daha fazla örnek her zaman daha iyi değildir.

Az ama kaliteli ve temsil gücü yüksek örnekler tercih edilmelidir.

---

# 15. İyi Few-Shot Örneği Nasıl Seçilir?

İyi örnekler:

- Doğru olmalı
- Kısa olmalı
- Görevle ilgili olmalı
- Farklı durumları kapsamalı
- Aynı output yapısını takip etmeli

Örneğin yalnızca başarılı durumları değil, bilgi bulunmayan durumları da göstermek faydalı olabilir.

Örnek:

```text
Context:
Maximum temperature is 70°C.

Question:
Maximum temperature?

Answer:
70°C
```

ve:

```text
Context:
Nominal voltage is 24 V.

Question:
Weight?

Answer:
Bulunamadı
```

Bu sayede model:

```text
Bilgi yoksa uydurma.
```

pattern'ini de görür.

---

# 16. Zero-Shot vs Few-Shot vs Fine-Tuning

| Yöntem | Promptta Örnek Var mı? | Model Ağırlıkları Değişir mi? | Kullanım |
|---|---:|---:|---|
| Zero-shot | Hayır | Hayır | Basit ve açık görev |
| Few-shot | Evet | Hayır | Pattern gösterme |
| Fine-tuning | Eğitim datası | Evet | Kalıcı davranış değişimi |

---

# 17. Workshop İçin Kritik Cümleler

1. **Zero-shot, modele örnek vermeden görev tanımlamaktır.**
2. **Few-shot, modele birkaç örnek göstererek beklenen davranışı tarif etmektir.**
3. **Few-shot model ağırlıklarını değiştirmez.**
4. **Few-shot bir prompting tekniğidir, training değildir.**
5. **Few-shot özel format ve sınıflandırma görevlerinde çok kullanışlıdır.**
6. **RAG bilgi getirir, few-shot davranış örneği verir.**
7. **Daha fazla few-shot örneği daha fazla token tüketir.**

---

# 18. Senin Uygulamanın Sonucu

Yeni cümle:

```text
"The module transmits telemetry through Ethernet."
```

`Ethernet` üzerinden telemetri iletimi bir iletişim davranışıdır.

Bu nedenle doğru sınıf:

```text
COMMUNICATION
```

Hem zero-shot hem few-shot promptun bu sonucu üretmeye uygun şekilde yazılmıştır.

---

# Sonraki Konu

## Bölüm 2.3 — Structured Output ve JSON Output

Sıradaki konular:

```text
Structured Output
JSON Output
Schema
Field Types
Validation
Free Text vs Structured Response
Backend Integration
Reliable Parsing
```
