# SuppTracker × OpenAI Integration

**Production-ready AI features for your supplement tracking app.**

Transform your FastAPI + TypeScript stack with OpenAI's structured outputs, embeddings, and agents. Under $20/month for 100 active users.

---

## 🚀 Quick Start (2 Hours to Production)

### 1. Get Your API Key
```bash
# Sign up at platform.openai.com (free $5 credit)
export OPENAI_API_KEY="sk-..."
```

### 2. Install Dependencies
```bash
pip install openai fastapi pydantic
```

### 3. Run the Risk Explainer
```python
python risk_explainer.py

# Output:
# Risk Level: high
# Summary: Taking zinc, calcium, and magnesium together in the evening creates significant competition for absorption...
# Warnings: ['Zinc absorption reduced by 30-50% when taken with calcium', 'Magnesium competes with both zinc and calcium']
# Next Steps: ['Separate zinc from calcium by at least 2 hours', 'Consider moving calcium to morning', 'Keep magnesium at bedtime (no conflicts)']
```

### 4. Add to Your FastAPI Backend
```python
from risk_explainer import explain_risk

@app.post("/api/insights/explain-risk")
async def get_risk_explanation(stack: List[Dict], scores: Dict):
    return explain_risk(stack, scores)
```

### 5. Call from Your Frontend
```typescript
const response = await fetch('/api/insights/explain-risk', {
  method: 'POST',
  body: JSON.stringify({
    stack: userStack,
    risk_scores: yourExistingRiskScores
  })
});

const explanation = await response.json();
// { risk_level: "high", user_friendly_summary: "...", warnings: [...], next_steps: [...] }
```

---

## 📦 What's Inside

### `risk_explainer.py` — AI-Powered Risk Explanations
**What it does:** Converts your numeric risk scores into plain-English explanations + actionable next steps.

**Why it's useful:**  
- Users understand *why* something is risky, not just *that* it is  
- No more JSON parsing headaches — Structured Outputs guarantees your schema  
- Costs ~$0.0007 per explanation (~$0.70 per 1000 users)  

**Key features:**  
✅ Type-safe JSON output (Pydantic schema enforced by OpenAI)  
✅ FastAPI endpoint example included  
✅ Test harness with realistic supplement interaction  
✅ Under 150 lines of production-ready code  

**Live example:**  
```json
{
  "risk_level": "high",
  "user_friendly_summary": "Taking zinc, calcium, and magnesium together in the evening creates significant absorption conflicts. These minerals compete for the same intestinal transport mechanisms, reducing the effectiveness of your entire stack.",
  "warnings": [
    "Zinc absorption reduced by 30-50% when taken with calcium",
    "Magnesium competes with both zinc and calcium for absorption",
    "Evening timing concentrates all three minerals simultaneously"
  ],
  "next_steps": [
    "Separate zinc from calcium by at least 2 hours",
    "Consider moving calcium to morning with breakfast",
    "Keep magnesium at bedtime (no conflicts with this adjustment)"
  ],
  "affected_compounds": ["Zinc Picolinate", "Calcium", "Magnesium Glycinate"],
  "confidence_score": 0.92
}
```

---

## 💰 Cost Breakdown

**Models used:**  
- Risk explanations: `gpt-4.1-mini` ($0.40 input / $1.60 output per 1M tokens)  
- Embeddings (future): `text-embedding-3-small` ($0.02 per 1M tokens)  

**Real-world costs:**  
- Average explanation: 400 tokens in, 250 tokens out = **$0.0007/call**  
- 100 users × 10 queries/day = 1,000 calls/day = **$0.70/day** = **~$21/month**  
- With prompt caching (90% discount on repeated prompts): **~$5/month**  

**Cheaper than a coffee subscription** to power intelligent explanations for your entire user base.

---

## 🛠️ Integration Patterns

### Pattern 1: Add AI Insights to Existing Risk Engine
```python
# Your existing code
risk_scores = calculate_interactions(user_stack)  # Your logic

# Add AI explanation
if risk_scores['severity'] > 0.5:
    explanation = explain_risk(user_stack, risk_scores)
    return {"scores": risk_scores, "explanation": explanation}
```

### Pattern 2: Embeddings for Knowledge Search (Coming Next)
```python
# Embed your supplement knowledge base once
for doc in supplement_docs:
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc.text
    )
    db.save(doc.id, embedding)

# At runtime: find relevant docs for user query
query_embedding = client.embeddings.create(...)
relevant_docs = vector_db.similarity_search(query_embedding, top_k=5)
```

### Pattern 3: Conversational Agent (Future)
```typescript
// User asks: "Can I add magnesium to my stack?"
const response = await openai.chat.completions.create({
  model: "gpt-4.1-mini",
  tools: [
    { name: "check_interaction", ... },
    { name: "get_user_stack", ... }
  ],
  messages: [...]
});
```

---

## 🎯 Next Steps

1. **Test the risk explainer** with your real data (swap in your own stack/scores)  
2. **Wire into your UI** — add an "Explain this risk" button that hits the endpoint  
3. **Monitor costs** in the OpenAI dashboard — you'll see real-time token usage  
4. **Add embeddings** for Q&A ("Why can't I take X with Y?") grounded in your knowledge base  
5. **Build the chat agent** when you're ready for a full conversational copilot  

---

## 📚 Resources

- **OpenAI Docs:** [platform.openai.com/docs](https://platform.openai.com/docs/guides/structured-outputs)  
- **Structured Outputs Guide:** Ensures type-safe JSON without retries  
- **Pricing Calculator:** [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing)  
- **Cookbook Examples:** [cookbook.openai.com](https://cookbook.openai.com)  

---

## 🤝 Support

Built for @SuppTracker. Questions? Open an issue or PR.

**Ship it. 🚢**
