import ssl
import certifi

# Windows certificate-store ASN.1 sorununu aşmak için
# güvenilir certifi CA bundle kullanıyoruz.
_original_context = ssl.create_default_context

def create_certifi_context(
    purpose=ssl.Purpose.SERVER_AUTH,
    *,
    cafile=None,
    capath=None,
    cadata=None
):
    return _original_context(
        purpose=purpose,
        cafile=cafile or certifi.where(),
        capath=capath,
        cadata=cadata
    )

ssl.create_default_context = create_certifi_context


from sentence_transformers import SentenceTransformer
sentences = [
    "The radar detects airborne targets.",
    "The battery supplies 24 V DC power.",
    "GNSS provides vehicle position information.",
    "The camera detects pedestrians.",
    "IMU measures acceleration and angular velocity.",
    "Ethernet is used to transmit telemetry data."
]
query = "Havadaki hedefleri hangi sistem algılıyor?"

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

sentence_embedings = model.encode(
    sentences,
    convert_to_tensor = True
)

query_embeding = model.encode(
    [query],
    convert_to_tensor = True
)

scores = model.similarity(
    query_embeding,
    sentence_embedings
)[0]

results = sorted(
    zip(sentences, scores.tolist()),
    key = lambda x: x[1],
    reverse=True
)

print(f"\nQuery: {query}\n")

for sentence, score in results:
    print(f"{score:.4f} -> {sentence}")
    
print("\nBest mach:")
print(results[0][0])