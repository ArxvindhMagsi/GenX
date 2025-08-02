# GenX 🚀

An intelligent document analysis and report generation application powered by Google's Gemini AI. GenX transforms your images and documents into comprehensive, professional reports with just a few clicks.

## ✨ Features

- **Smart Image Analysis**: Upload images and get detailed AI-powered insights
- **Intelligent Report Generation**: Automatically generate professional reports from your content
- **PDF Export**: Download your reports as beautifully formatted PDF documents
- **User-Friendly Interface**: Clean, intuitive Streamlit-based web interface
- **Secure**: Environment-based API key management for enhanced security

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Engine**: Google Gemini AI (generative-ai)
- **Image Processing**: Pillow (PIL)
- **PDF Generation**: ReportLab
- **Environment Management**: python-dotenv

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ArxvindhMagsi/GenX.git
   cd GenX
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   API_KEY=your_google_ai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📋 Usage

1. **Upload Content**: Add your images or documents to the application
2. **AI Analysis**: Let GenX analyze your content using advanced AI
3. **Generate Report**: Create comprehensive reports automatically
4. **Export PDF**: Download your professional reports as PDF files

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | Google AI API Key | Yes |

### Getting Google AI API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 📁 Project Structure

```
GenX/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
└── .streamlit/        # Streamlit configuration
    └── config.toml
```

## 🚀 Deployment

### Render

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.port $PORT --server.headless true`
4. Add environment variable: `API_KEY`

### Vercel

1. Import project from GitHub
2. Add environment variable: `API_KEY`
3. Deploy with default settings

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security

- API keys are managed through environment variables
- Sensitive files are excluded from version control
- Follow security best practices for deployment

## 📞 Support

If you encounter any issues or have questions:

- Open an [issue](https://github.com/ArxvindhMagsi/GenX/issues)
- Contact: [Your Email]

## 🙏 Acknowledgments

- Google AI for providing the Gemini API
- Streamlit team for the amazing framework
- ReportLab for PDF generation capabilities

---

**Made with ❤️ by [Aravindh Magsi](https://github.com/ArxvindhMagsi)**

⭐ Star this repo if you found it helpful!
