# 🎵 Emotify - AI-Powered Song Emotion Analyzer

![Emotify Banner](https://img.shields.io/badge/Emotify-Song%20Emotion%20Detector-purple?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

Emotify is an advanced AI-powered application that analyzes the emotional landscape of songs using cutting-edge natural language processing and machine learning technologies. Discover the hidden emotional journey within any song through comprehensive sentiment analysis, emotion detection, and interactive visualizations.

## 🌟 Features

### 🎯 Core Capabilities
- **AI-Powered Analysis**: Leverages Google's Gemini 2.0 Flash for deep emotional understanding
- **Multi-Dimensional Emotion Detection**: Uses NRCLex for sophisticated emotion scoring across 10 emotional categories
- **Song Metadata Integration**: Fetches accurate song information via Genius API
- **Interactive Visualizations**: Beautiful charts and graphs using Plotly
- **Comprehensive Reports**: Detailed breakdowns of mood, themes, and emotional arcs

### 📊 Analysis Components

#### 1. **Gemini AI Analysis**
- Overall emotional tone and atmosphere
- Primary emotions with intensity ratings (0-10 scale)
- Mood classification
- Thematic element identification
- Emotional arc throughout the song
- Musical element impact on emotions
- Lyrical theme extraction

#### 2. **NRCLex Emotion Scoring**
- Quantitative emotion analysis across categories:
  - Joy
  - Sadness
  - Anger
  - Fear
  - Trust
  - Anticipation
  - Surprise
  - Disgust
  - Positive sentiment
  - Negative sentiment
- Normalized percentage scores
- Raw word count metrics

#### 3. **Visual Analytics**
- Radar chart for emotion distribution
- Bar chart for intensity rankings
- Horizontal bar chart for AI-detected emotions
- Color-coded emotion metrics

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API Keys:
  - Google Gemini API Key ([Get one here](https://ai.google.dev/))
  - Genius API Key ([Get one here](https://genius.com/api-clients))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/naakaarafr/Emotify.git
   cd Emotify
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GENIUS_API_KEY=your_genius_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run Emotify.py
   ```

6. **Access the application**
   
   Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

```txt
streamlit>=1.28.0
google-generativeai>=0.3.0
requests>=2.31.0
nrclex>=3.0.0
plotly>=5.17.0
python-dotenv>=1.0.0
nltk>=3.8.0
```

## 💻 Usage

### Basic Workflow

1. **Enter Song Information**
   - Artist Name (e.g., "Taylor Swift")
   - Song Title (e.g., "Anti-Hero")

2. **Click "Analyze"**
   - The app searches for the song on Genius
   - Confirms the match with song artwork and details

3. **Review Analysis**
   - Overall tone and mood
   - Primary emotions with descriptions
   - Thematic elements
   - Musical element analysis
   - Emotional arc throughout the song
   - Interactive visualizations

4. **Explore Metrics**
   - Emotion distribution radar chart
   - Intensity ranking bar chart
   - Detailed emotion breakdowns
   - Top 3 emotions summary

### Example Use Cases

#### Music Research
- Analyze emotional patterns across an artist's discography
- Compare emotional content of songs within a genre
- Study the evolution of emotional themes over time

#### Content Creation
- Choose music that matches desired emotional tones
- Understand emotional impact for playlist curation
- Select appropriate songs for video/film soundtracks

#### Personal Discovery
- Understand why certain songs resonate emotionally
- Explore the emotional depth of favorite tracks
- Discover new music based on emotional profiles

## 🏗️ Architecture

### Application Flow

```
User Input (Artist + Song)
    ↓
Genius API Search
    ↓
Song Metadata Retrieval
    ↓
Gemini AI Analysis
    ↓
NRCLex Emotion Processing
    ↓
Visualization Generation
    ↓
Comprehensive Report Display
```

### Key Components

#### `search_song_genius(artist, song, api_key)`
- Searches Genius API for song matches
- Implements intelligent matching algorithm
- Returns song metadata including artwork and URL

#### `analyze_with_gemini(song_info, api_key)`
- Sends structured prompt to Gemini AI
- Requests JSON-formatted emotional analysis
- Parses and validates AI response

#### `analyze_emotions_nrclex(keywords)`
- Processes emotional keywords through NRCLex
- Calculates raw and normalized emotion scores
- Returns comprehensive emotion metrics

#### `create_emotion_visualizations(nrc_results, gemini_analysis)`
- Generates interactive Plotly charts
- Creates radar and bar chart visualizations
- Displays AI emotion intensity ratings

## 🎨 User Interface

### Design Features
- Modern gradient-based color scheme (purple/blue theme)
- Responsive layout with card-based components
- Clean, intuitive search interface
- Status indicators for API connectivity
- Expandable sections for detailed information
- Professional metrics display

### Color Palette
- Primary: `#667eea` (Purple Blue)
- Secondary: `#764ba2` (Deep Purple)
- Accents: Various gradient combinations
- Success: `#d4edda` (Light Green)
- Error: `#f8d7da` (Light Red)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API authentication key | Yes |
| `GENIUS_API_KEY` | Genius API authentication key | Yes |

### NLTK Data

The application automatically downloads required NLTK datasets:
- `punkt` - Tokenization models
- `stopwords` - Common stopword lists
- `averaged_perceptron_tagger` - POS tagging
- `brown` - Brown corpus

## 📈 Technical Details

### API Integrations

#### Google Gemini AI
- Model: `gemini-2.0-flash-exp`
- Purpose: Deep emotional and thematic analysis
- Output: Structured JSON with comprehensive metrics

#### Genius API
- Endpoint: Search API
- Purpose: Song metadata and matching
- Rate Limits: Respect API guidelines

### Emotion Categories (NRCLex)

The NRC Emotion Lexicon analyzes text across 10 categories:
- **Basic Emotions**: Joy, Sadness, Anger, Fear, Trust, Anticipation, Surprise, Disgust
- **Sentiment**: Positive, Negative

### Data Processing

1. **Text Analysis**: Emotional keywords extracted by Gemini
2. **Tokenization**: NLTK processes text into analyzable units
3. **Emotion Mapping**: NRCLex maps words to emotion categories
4. **Normalization**: Scores converted to percentages
5. **Visualization**: Data transformed into interactive charts

## 🛠️ Troubleshooting

### Common Issues

**"API Keys Missing" Error**
- Ensure `.env` file exists in project root
- Verify API keys are correctly formatted
- Check for extra spaces or quotes in `.env`

**"Song not found" Error**
- Verify spelling of artist and song name
- Try variations (e.g., with/without "feat.")
- Check if song exists on Genius.com

**NLTK Download Errors**
- Run `python -m nltk.downloader all` manually
- Check internet connection
- Ensure sufficient disk space

**Visualization Not Displaying**
- Clear browser cache
- Try different browser
- Check console for JavaScript errors

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - Advanced language understanding
- **Genius API** - Comprehensive music database
- **NRCLex** - Emotion lexicon analysis
- **Streamlit** - Rapid web app development
- **Plotly** - Interactive visualizations

## 📧 Contact

**Project Maintainer**: [@naakaarafr](https://github.com/naakaarafr)

**Project Link**: [https://github.com/naakaarafr/Emotify](https://github.com/naakaarafr/Emotify)


⭐ Star this repo if you find it helpful!

</div>
