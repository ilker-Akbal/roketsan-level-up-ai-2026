# ROKETSAN Level Up AI – 19 Ağustos Hazırlık
## Bölüm 2.3: Structured Output ve JSON Output – Uygulama Notu

Bu not, structured output ve JSON mantığını tekrar etmek için hazırlanmıştır.

---

# 1. Kullanılan Context

```text
The TRX-8 radar has a maximum detection range of 72 km.
It operates at 28 V DC.
```

Kullanılacak schema:

```json
{
  "status": "found | not_found",
  "parameter": "",
  "value": null,
  "unit": null,
  "source": ""
}
```

---

# 2. Soru 1

```text
Maksimum tespit menzili nedir?
```

Kullanıcının yazdığı cevap:

```json
{
  "status": "found",
  "parameter": "range",
  "value": 72,
  "unit": range,
  "source": ""
}
```

## Düzeltilmesi Gereken Noktalar

### 1. `unit` alanı yanlış

Şu kullanım:

```json
"unit": range
```

geçerli JSON değildir.

Eğer değer bir string ise tırnak içinde yazılmalıdır:

```json
"unit": "km"
```

Ayrıca `range` birim değil, parametre adıdır.

Doğru birim:

```text
km
```

---

### 2. `parameter` daha açık yazılabilir

Şu kullanım:

```json
"parameter": "range"
```

çalışabilir.

Ancak teknik sistemlerde daha açık isimlendirme daha iyidir:

```json
"parameter": "maximum_detection_range"
```

Bu şekilde backend tarafında field'ın ne ifade ettiği daha nettir.

---

### 3. `source` alanı boş bırakılmamalı

Context doğrudan prompt içinde verildiyse:

```json
"source": "provided_context"
```

yazılabilir.

RAG sisteminde ise ileride:

```json
"source": "chunk_12"
```

gibi gerçek chunk bilgisi kullanılabilir.

---

# 3. Soru 1 İçin Doğru Cevap

```json
{
  "status": "found",
  "parameter": "maximum_detection_range",
  "value": 72,
  "unit": "km",
  "source": "provided_context"
}
```

Bu cevap:

- Geçerli JSON'dur.
- Schema mantığına uygundur.
- Sayısal değeri ve birimi ayırır.
- Kaynak bilgisini gösterir.
- Backend tarafından kolayca parse edilebilir.

---

# 4. Soru 2

```text
Radarın ağırlığı nedir?
```

Kullanıcının yazdığı cevap:

```json
{
  "status": "not_found",
  "parameter": "weight",
  "value": null,
  "unit": kg,
  "source": ""
}
```

Mantıksal olarak `status = not_found` ve `value = null` doğru seçilmiştir.

Ancak iki düzeltme gerekir.

---

# 5. Bilgi Bulunamadığında `unit` Ne Olmalı?

Context içinde ağırlık bilgisi yoktur.

Dolayısıyla model:

```text
kg
```

birimini bile varsaymamalıdır.

Her ne kadar ağırlığın çoğu zaman kg ile ölçülebileceğini bilsek de, verilen context bunu söylememektedir.

Bu yüzden:

```json
"unit": null
```

daha doğrudur.

Bu aynı zamanda hallucination azaltma prensibidir.

---

# 6. Bilgi Bulunamadığında `source` Ne Olmalı?

Ağırlık hakkında bilgi bulunamadığı için:

```json
"source": null
```

kullanmak daha temizdir.

Çünkü cevabı destekleyen herhangi bir kaynak yoktur.

---

# 7. Soru 2 İçin Doğru Cevap

```json
{
  "status": "not_found",
  "parameter": "weight",
  "value": null,
  "unit": null,
  "source": null
}
```

Bu yapı açıkça şunu ifade eder:

```text
İstenen parametre aranmıştır.
Ancak verilen context içinde bulunamamıştır.
```

---

# 8. Geçerli JSON İçin Temel Kurallar

JSON'da string değerler tırnak içinde olmalıdır.

Doğru:

```json
{
  "unit": "km"
}
```

Yanlış:

```json
{
  "unit": km
}
```

---

## Sayılar

Sayılar tırnaksız yazılır:

```json
{
  "value": 72
}
```

---

## Boolean

```json
{
  "detected": true
}
```

---

## Null

Bilgi mevcut değilse:

```json
{
  "value": null
}
```

kullanılabilir.

---

# 9. String ve Number Ayrımı

Kötü:

```json
{
  "range": "72 km"
}
```

Daha iyi:

```json
{
  "value": 72,
  "unit": "km"
}
```

Neden?

Çünkü backend:

```python
if result["value"] > 50:
    print("Long range radar")
```

gibi doğrudan sayısal işlem yapabilir.

---

# 10. `not_found` Durumunda Tahmin Yapmama

Context:

```text
Maximum detection range = 72 km
Voltage = 28 V
```

Ağırlık bilgisi yoktur.

Yanlış:

```json
{
  "status": "found",
  "value": 45,
  "unit": "kg"
}
```

Bu hallucination'dır.

Yanlış:

```json
{
  "status": "not_found",
  "value": null,
  "unit": "kg"
}
```

Bu daha iyi görünse de `kg` bilgisi yine context'ten gelmemektedir.

En güvenli cevap:

```json
{
  "status": "not_found",
  "value": null,
  "unit": null,
  "source": null
}
```

---

# 11. Structured Output İçin Önerilen Genel Schema

Teknik doküman asistanı için kullanılabilecek temiz bir yapı:

```json
{
  "status": "found | not_found",
  "parameter": "",
  "value": null,
  "unit": null,
  "source": null
}
```

## `found` örneği

```json
{
  "status": "found",
  "parameter": "maximum_detection_range",
  "value": 72,
  "unit": "km",
  "source": "chunk_12"
}
```

## `not_found` örneği

```json
{
  "status": "not_found",
  "parameter": "weight",
  "value": null,
  "unit": null,
  "source": null
}
```

---

# 12. Valid JSON ile Doğru Structured Output Aynı Şey Değildir

Örneğin:

```json
{
  "banana": "72 km"
}
```

geçerli JSON'dur.

Ama bizim schema'mıza uygun değildir.

Bu nedenle iki kontrol gerekir:

```text
1. JSON syntax olarak geçerli mi?
2. Beklenen schema'ya uygun mu?
```

---

# 13. Python ile Parse Etme

Örnek:

```python
import json

raw_response = '''
{
  "status": "found",
  "parameter": "maximum_detection_range",
  "value": 72,
  "unit": "km",
  "source": "provided_context"
}
'''

data = json.loads(raw_response)

print(data["value"])
print(data["unit"])
```

Çıktı:

```text
72
km
```

---

# 14. Bu Uygulamadan Çıkan Ana Dersler

1. **JSON string değerleri tırnak içinde olmalıdır.**
2. **Sayısal değer ve birim ayrı field'larda tutulmalıdır.**
3. **`not_found` durumunda model bilgi uydurmamalıdır.**
4. **Bilgi yoksa `value`, `unit` ve `source` alanları `null` olabilir.**
5. **Parametre isimleri mümkün olduğunca açık yazılmalıdır.**
6. **Structured output backend tarafından kolayca parse edilebilir.**
7. **Geçerli JSON olması tek başına yeterli değildir; schema'ya da uygun olmalıdır.**
8. **Structured output, ileride RAG ve agent/tool calling sistemlerinde çok önemlidir.**

---

# Düzeltilmiş İki Nihai Cevap

## Maksimum Tespit Menzili

```json
{
  "status": "found",
  "parameter": "maximum_detection_range",
  "value": 72,
  "unit": "km",
  "source": "provided_context"
}
```

## Radarın Ağırlığı

```json
{
  "status": "not_found",
  "parameter": "weight",
  "value": null,
  "unit": null,
  "source": null
}
```

---

# Sonraki Konu

## Bölüm 2.4 — Context Kullanımı, Hallucination Azaltma ve Teknik Doküman Promptları

Sıradaki konular:

```text
Context injection
Grounding
Source restriction
Not-found behavior
Technical document prompts
Prompt injection temel farkındalığı
RAG'e hazırlık
```
