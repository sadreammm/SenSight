# SenSight

**SenSight** is an AI-powered GitHub Pull Request reviewer that provides senior-level code insights, identifies potential bugs, security vulnerabilities, and code quality issues, and suggests actionable improvements. Reviews are stored in a database for historical tracking and future model training.

---

## Features

- **Automatic GitHub Pull Request analysis** on `opened` or `synchronize` events.
- Combines **static analysis** (Bandit & Pylint) with **LLM-generated AI insights**.
- Stores reviews in **PostgreSQL** for future reference or training.
- Supports **full file context retrieval** if needed to improve analysis.
- Designed for **scalability**: can integrate multiple LLMs in the future.

---

## Architecture

1. **GitHub Webhook** triggers the analysis on PR events.
2. **Diff Extraction** identifies added and removed code.
3. **Context Detection** decides whether full file content is required.
4. **Static Analysis** checks for security and quality issues.
5. **AI Review** uses Google Gemini API to generate senior-level review.
6. **Database Storage** saves review data in PostgreSQL for historical tracking.

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/SenSight.git
cd SenSight
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables** in a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
access_token=your_github_access_token_here
DATABASE_URL=postgresql+psycopg2://username:password@host:port/dbname
```

4. **Initialize the database:**

```python
from models.database import init_db
init_db()
```

---

## Usage

1. **Start the FastAPI server:**

```bash
uvicorn app:app --reload
```

2. **Add a webhook to your GitHub repository** pointing to:

```
POST https://your-server.com/webhook/github
```

3. Payloads for **PR opened** and **synchronize** events will trigger analysis.

---

## Example Review Flow

1. Developer opens a PR.
2. **SenSight** fetches the diff, static analysis results, and PR context.
3. AI generates a detailed review including:
   - Bugs and issues
   - Security risks
   - Design and architecture suggestions
   - Alignment with task requirements
4. Review stored in PostgreSQL with metadata for future training.

---

## Database Schema

### Table: `code_reviews`

| Column       | Type      | Description                            |
| ------------ | --------- | -------------------------------------- |
| `id`         | String    | Unique review ID (UUID)                |
| `repo`       | String    | Repository URL                         |
| `pr_number`  | Integer   | Pull Request number                    |
| `pr_data`    | JSON      | Full review data including AI analysis |
| `created_at` | TIMESTAMP | Timestamp of review creation           |

---

## Configuration

- **LLM Model**: Gemini 2.5 Flash
- **Static Analysis**: Bandit (security), Pylint (quality)
- **Database**: PostgreSQL

---

## Project Structure

```
SenSight/
├── app.py                         
├── config/
│   └── settings.py                 
├── models/
│   └── database.py                 
├── services/
│   ├── github_service.py           
│   ├── code_analysis_service.py    
│   ├── ai_service.py               
│   └── context_service.py          
├── utils/
│   ├── diff_parser.py              
│   └── code_inspector.py           
├── routers/
│   └── webhook.py                  
├── requirements.txt                
├── .env                    
└── README.md                       
```

---

## Future Enhancements

- **Local LLM Training**: Use stored reviews to train or fine-tune a smaller Hugging Face model, reducing dependency on API calls.
- **Multi-Language Support**: Extend PR analysis to JavaScript, Java, and other languages.
- **Inline code comments**: Automatically generate context-aware suggestions and explanations directly within the changed lines of code.
- **Interactive Dashboard**: Visualize PR trends, code quality metrics, and common issues over time.
- **Enhanced Context Understanding**: Use code embeddings for better cross-file and project-level insights.
- **Configurable Rules**: Allow teams to define custom code quality or security rules.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Open a Pull Request
