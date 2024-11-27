---

# 📝 **Summary App**  
An intelligent tool to summarize text, YouTube videos, and documents seamlessly using **AI-powered summarization models**. 🌟

---

## 🚀 **Features**
- 📄 Summarize **plain text** for quick insights.
- 🎥 Extract and summarize **YouTube video transcripts**.
- 📁 Upload and summarize **PDFs, Word documents, or text files**.
- 🤖 Powered by **Hugging Face's BART model** for high-quality summaries.
- 🌐 Cross-origin support enabled via **Flask CORS**.
- 🔗 Modern, responsive **React frontend** integrated with Tailwind CSS.

---

## 🌟 **Technologies Used**
### Backend
- 🐍 **Flask**: Backend framework for API handling.
- 🔗 **Flask-CORS**: Enable cross-origin requests.
- 🎥 **YouTube Transcript API**: Fetch YouTube video transcripts.
- 🤖 **Hugging Face API**: AI-based text summarization.
- 📂 **PyPDF2** & **python-docx**: File parsing for PDFs and Word documents.

### Frontend
- ⚛️ **React**: Frontend framework for building a modern UI.
- 🎨 **Tailwind CSS**: For sleek and responsive design.



---

## 🛠️ **Installation and Usage**

### Prerequisites
- Python 3.9+ 🐍
- Node.js 16+ (for frontend) ⚛️


---

### **Backend Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/summary-app.git
   cd summary-app
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```env
   HUGGING_FACE_API_KEY=your_huggingface_api_key
   ```

4. Run the backend:
   ```bash
   python app.py
   ```

---

### **Frontend Setup**
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the production files:
   ```bash
   npm run build
   ```







## 🎉 **Live Demo**
# 🚀 Comming soon

---

## 🛡️ **Production Deployment**
# ⭕ Ongoing

---

## 📄 **API Endpoints**

| **Endpoint**          | **Method** | **Description**                     |
|------------------------|------------|-------------------------------------|
| `/summary/text`        | `POST`     | Summarizes plain text input.         |
| `/summary/youtube`     | `POST`     | Summarizes a YouTube video.          |
| `/summary/file`        | `POST`     | Summarizes uploaded files.           |
| `/summary/combined`    | `POST`     | Summarizes combined inputs.          |
| `/summary/all`         | `POST`     | Summarizes text, video, and file.    |




## 🤝 **Contributing**
Contributions are welcome! 🌟  
- Fork the repo.
- Create a feature branch:  
  ```bash
  git checkout -b feature-name
  ```
- Commit and push changes:
  ```bash
  git commit -m "Add feature-name"
  git push origin feature-name
  ```
- Open a Pull Request.

---


## Happy Coding 🔥🪄⚙️

