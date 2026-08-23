# ROKETSAN 19 Ağustos — Bölüm 5: Agentic AI Temelleri

## 1. Normal LLM vs RAG vs Agent

```text
Normal LLM:
Question
↓
LLM
↓
Answer
```

```text
RAG:
Question
↓
Retriever
↓
Relevant Context
↓
LLM
↓
Answer
```

```text
Agent:
Goal
↓
Decide
↓
Action
↓
Tool
↓
Observation
↓
Decide Again
↓
...
↓
Final Answer
```

## 2. Agent nedir?

Agent, yalnızca metin üreten bir LLM değildir.

Agent:
- kullanıcının hedefini yorumlar,
- hangi aracı kullanacağına karar verir,
- tool input üretir,
- tool sonucunu gözlemler,
- gerekirse başka bir tool çağırır,
- sonunda final answer üretir.

## 3. Temel kavramlar

### Goal
Kullanıcının ulaşmak istediği sonuç.

### Action
Agent'ın bir sonraki adım kararı.

Örnek:

```json
{
  "type": "tool",
  "tool": "rag",
  "input": "thermal treatment temperature threshold"
}
```

### Tool
Agent'ın çağırabildiği dış fonksiyon.

Bu demoda:
- `rag_tool`
- `calculator_tool`

### Observation
Tool'un döndürdüğü sonuç.

### State
Agent'ın o ana kadarki:
- user query,
- action,
- observation,
- önceki tool sonuçları

bilgileridir.

### Agent Loop

```text
Decide
↓
Act
↓
Observe
↓
Update State
↓
Decide
↓
...
↓
Final
```

## 4. Tool calling mantığı

Agent doğrudan Python fonksiyonunu çalıştırmaz.

LLM önce yapılandırılmış bir karar üretir:

```json
{
  "type": "tool",
  "tool": "calculator",
  "input": "177 + 273.15"
}
```

Uygulama bu JSON'u parse eder ve ilgili Python fonksiyonunu çağırır.

Sonuç tekrar LLM'e observation olarak verilir.

## 5. RAG Tool

```text
Agent
↓
rag_tool(query)
↓
Embedding
↓
FAISS
↓
Top-K Chunks
↓
Observation
```

Agent, doküman bilgisini kendi hafızasından üretmemelidir.

Doküman sorularında RAG tool kullanmalıdır.

## 6. Calculator Tool

Amaç:
- arithmetic işlemleri LLM'e tahmin ettirmemek,
- gerçek hesaplama fonksiyonu kullanmak.

Örnek:

```text
177 + 273.15
↓
calculator_tool
↓
450.15
```

## 7. JSON Action Format

Demo agent her adımda JSON üretir.

Tool:

```json
{
  "type": "tool",
  "tool": "rag",
  "input": "..."
}
```

Final:

```json
{
  "type": "final",
  "answer": "..."
}
```

Structured output burada agent kontrolünü kolaylaştırır.

## 8. max_steps

Agent loop sonsuza kadar çalışmamalıdır.

```python
max_steps = 5
```

gibi bir limit güvenlik ve kontrol sağlar.

## 9. Gerçek testte görülen önemli hata

Agent doğru tool sırasını seçti:

```text
RAG
↓
Calculator
↓
Final
```

Ancak RAG yanlış sıcaklık chunk'ını getirdi:

```text
52°C
```

Bu değer mercury heated test method içindeydi.

Kullanıcının istediği `thermal treatment` tanımı ise:

```text
350°F (177°C)
```

idi.

Bu nedenle:

```text
Agent loop doğru olabilir
ama
Tool observation yanlışsa
final answer yanlış olabilir.
```

## 10. Kritik ders

```text
Correct Tool Selection
≠
Correct Final Answer
```

Ayrıca:

```text
Correct Tool
+
Wrong Tool Input
↓
Wrong Observation
↓
Wrong Final Answer
```

Bu nedenle agent sistemlerinde şu üç nokta önemlidir:

```text
1. Tool Selection
2. Tool Input Quality
3. Observation Validation
```

## 11. Agent ile RAG farkı

RAG pipeline'ında akışı programcı belirler:

```text
retrieve()
↓
build_context()
↓
generate_answer()
```

Agent'ta LLM karar verir:

```text
RAG gerekli mi?
↓
Calculator gerekli mi?
↓
Başka tool gerekli mi?
↓
Cevap vermeye hazır mıyım?
```

## 12. Agentic AI'nın çekirdek özeti

```text
LLM
→ Generate

RAG
→ Retrieve + Generate

Agent
→ Decide + Act + Observe + Repeat
```

## 13. Tool result güvenilirliği

Agent'a gelen observation doğru kabul edilirse hata zinciri oluşabilir.

Daha gelişmiş sistemlerde:
- source validation,
- tool result validation,
- confidence checks,
- retry,
- alternative tool calls,
- planner/critic yapıları

kullanılabilir.

Workshop öncesi temel mimariyi anlamak için bunlara girmek zorunlu değildir.

## 14. Frameworkler

Bu demoda framework kullanılmadan saf Python ile agent loop kuruldu.

Daha sonra aynı mantık:
- LangChain
- LangGraph
- LlamaIndex
- çeşitli agent SDK'ları

ile daha hazır abstractions kullanılarak kurulabilir.

Önemli olan framework ezberlemek değil:

```text
Goal
↓
Decision
↓
Action
↓
Tool
↓
Observation
↓
Next Decision
↓
Final
```

mantığını anlamaktır.
