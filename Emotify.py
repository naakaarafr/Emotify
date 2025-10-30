import streamlit as st
import google.generativeai as genai
import requests
from nrclex import NRCLex
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from dotenv import load_dotenv
import nltk
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown')

# Load environment variables
load_dotenv()

# Get API keys from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GENIUS_API_KEY = os.getenv('GENIUS_API_KEY')

# Page configuration
st.set_page_config(
    page_title="Emotify - Song Emotion Detector",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Hide sidebar completely */
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* Main container styling */
    .main {
        padding: 2rem 3rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        font-weight: 400;
    }
    
    /* Search box styling */
    .search-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning {
        border-radius: 12px;
        padding: 1rem;
        font-weight: 500;
    }
    
    /* API Status Badge */
    .api-status {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem;
        font-size: 0.9rem;
    }
    
    .api-success {
        background-color: #d4edda;
        color: #155724;
    }
    
    .api-error {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    /* Section headers */
    h2, h3 {
        color: #2d3748;
        font-weight: 700;
    }
    
    /* Card-like containers */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #718096;
        font-size: 0.95rem;
        margin-top: 3rem;
        border-top: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎵 Emotify</h1>
    <p>Discover the emotional journey within any song using AI-powered analysis</p>
</div>
""", unsafe_allow_html=True)

# API Status indicator
api_status_html = ""
if GEMINI_API_KEY and GENIUS_API_KEY:
    api_status_html = """
    <div style='text-align: center; margin-bottom: 2rem;'>
        <span class='api-status api-success'>✅ Gemini AI Connected</span>
        <span class='api-status api-success'>✅ Genius API Connected</span>
    </div>
    """
else:
    api_status_html = """
    <div style='text-align: center; margin-bottom: 2rem;'>
        <span class='api-status api-error'>⚠️ API Keys Missing</span>
        <p style='color: #721c24; margin-top: 1rem;'>Please create a .env file with GEMINI_API_KEY and GENIUS_API_KEY</p>
    </div>
    """

st.markdown(api_status_html, unsafe_allow_html=True)

# Search section with enhanced styling

st.markdown("### 🔍 Search for a Song")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    artist_name = st.text_input("🎤 Artist Name", placeholder="e.g., Taylor Swift", label_visibility="visible")

with col2:
    song_name = st.text_input("🎵 Song Title", placeholder="e.g., Anti-Hero", label_visibility="visible")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🔎 Analyze", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

def search_song_genius(artist, song, api_key):
    """Search for a song on Genius API with better matching"""
    try:
        search_url = "https://api.genius.com/search"
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {"q": f"{artist} {song}"}
        
        response = requests.get(search_url, headers=headers, params=params)
        data = response.json()
        
        if data['response']['hits']:
            best_match = None
            best_score = 0
            
            for hit in data['response']['hits'][:5]:
                result = hit['result']
                title = result['title'].lower()
                artist_name = result['primary_artist']['name'].lower()
                
                title_match = song.lower() in title or title in song.lower()
                artist_match = artist.lower() in artist_name or artist_name in artist.lower()
                
                score = (2 if title_match else 0) + (1 if artist_match else 0)
                
                if score > best_score:
                    best_score = score
                    best_match = result
            
            if best_match:
                return {
                    'title': best_match['title'],
                    'artist': best_match['primary_artist']['name'],
                    'url': best_match['url'],
                    'thumbnail': best_match['song_art_image_thumbnail_url'],
                    'id': best_match['id'],
                    'full_title': best_match['full_title']
                }
        return None
    except Exception as e:
        st.error(f"Error searching song: {str(e)}")
        return None

def analyze_with_gemini(song_info, api_key):
    """Use Gemini to provide comprehensive song analysis"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""You are an expert music analyst. Analyze the song "{song_info['title']}" by {song_info['artist']}.

Provide a DETAILED and ACCURATE emotional analysis based on your knowledge of this specific song. Do NOT provide generic responses.

Return a JSON object with this EXACT structure:
{{
    "overall_tone": "A detailed 2-3 sentence description of the song's emotional atmosphere",
    "primary_emotions": [
        {{"emotion": "Emotion1", "intensity": 0-10, "description": "Specific evidence from the song"}},
        {{"emotion": "Emotion2", "intensity": 0-10, "description": "Specific evidence from the song"}},
        {{"emotion": "Emotion3", "intensity": 0-10, "description": "Specific evidence from the song"}},
        {{"emotion": "Emotion4", "intensity": 0-10, "description": "Specific evidence from the song"}}
    ],
    "mood": "Specific mood classification",
    "themes": "Detailed description of thematic elements (3-4 sentences)",
    "emotional_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5", "keyword6", "keyword7", "keyword8", "keyword9", "keyword10", "keyword11", "keyword12", "keyword13", "keyword14", "keyword15"],
    "tempo_energy": "slow/medium/fast",
    "valence": "positive/negative/mixed",
    "lyrical_themes": ["theme1", "theme2", "theme3"],
    "emotional_arc": "Description of how emotions change throughout the song",
    "musical_elements": "Description of how instrumentation/production affects emotions"
}}

Be specific to THIS song. Include actual details about the lyrics' themes, the musical production, and emotional journey."""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response_text)
        
        return result
    except json.JSONDecodeError as e:
        st.error(f"Error parsing Gemini response: {str(e)}")
        st.code(response_text)
        return None
    except Exception as e:
        st.error(f"Error with Gemini analysis: {str(e)}")
        return None

def analyze_emotions_nrclex(keywords):
    """Analyze emotions using NRCLex with improved accuracy"""
    try:
        text = ' '.join(keywords)
        emotion_obj = NRCLex(text)
        raw_scores = emotion_obj.raw_emotion_scores
        
        if raw_scores:
            total = sum(raw_scores.values())
            if total > 0:
                normalized_scores = {k: (v / total) * 100 for k, v in raw_scores.items()}
            else:
                normalized_scores = raw_scores
        else:
            normalized_scores = {}
        
        affect_dict = emotion_obj.affect_dict
        
        return {
            'raw_scores': raw_scores,
            'normalized_scores': normalized_scores,
            'affect_dict': affect_dict,
            'word_count': len(emotion_obj.words)
        }
    except Exception as e:
        st.error(f"Error with NRCLex: {str(e)}")
        return None

def create_emotion_visualizations(nrc_results, gemini_analysis):
    """Create comprehensive visualizations"""
    
    if not nrc_results or not nrc_results.get('normalized_scores'):
        st.warning("No emotion data available for visualization")
        return
    
    normalized_scores = nrc_results['normalized_scores']
    
    col1, col2 = st.columns(2)
    
    with col1:
        emotions = list(normalized_scores.keys())
        scores = list(normalized_scores.values())
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=emotions,
            fill='toself',
            name='Emotion Intensity',
            line_color='#667eea',
            fillcolor='rgba(102, 126, 234, 0.4)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, max(scores) if scores else 100],
                    tickfont=dict(size=10)
                )
            ),
            showlegend=False,
            title="Emotion Distribution (NRCLex)",
            height=400,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        sorted_emotions = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        
        emotions_list = [e[0].capitalize() for e in sorted_emotions]
        scores_list = [e[1] for e in sorted_emotions]
        
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', 
                  '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#a8edea']
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=emotions_list,
                y=scores_list,
                marker_color=colors[:len(emotions_list)],
                text=[f'{s:.1f}%' for s in scores_list],
                textposition='outside'
            )
        ])
        
        fig_bar.update_layout(
            title='Emotion Intensity Rankings',
            xaxis_title='Emotion',
            yaxis_title='Intensity (%)',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    if gemini_analysis and 'primary_emotions' in gemini_analysis:
        st.markdown("### 🎭 AI-Detected Primary Emotions")
        
        gemini_emotions = gemini_analysis['primary_emotions']
        emotion_names = [e['emotion'] for e in gemini_emotions]
        intensities = [e.get('intensity', 5) for e in gemini_emotions]
        
        fig_gemini = go.Figure(data=[
            go.Bar(
                y=emotion_names,
                x=intensities,
                orientation='h',
                marker_color='#764ba2',
                text=[f'{i}/10' for i in intensities],
                textposition='outside'
            )
        ])
        
        fig_gemini.update_layout(
            title='Gemini AI Emotion Intensity Ratings',
            xaxis_title='Intensity (0-10)',
            yaxis_title='Emotion',
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_gemini, use_container_width=True)

if analyze_button:
    if not GEMINI_API_KEY:
        st.error("⚠️ GEMINI_API_KEY not found in .env file")
    elif not GENIUS_API_KEY:
        st.error("⚠️ GENIUS_API_KEY not found in .env file")
    elif not artist_name or not song_name:
        st.error("⚠️ Please enter both artist name and song title")
    else:
        with st.spinner("🔍 Searching for song..."):
            song_info = search_song_genius(artist_name, song_name, GENIUS_API_KEY)
        
        if song_info:
            st.success(f"✅ Found: **{song_info['title']}** by **{song_info['artist']}**")
            
            # Song info card
            st.markdown("---")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(song_info['thumbnail'], width=200)
            with col2:
                st.markdown(f"### {song_info['title']}")
                st.markdown(f"**Artist:** {song_info['artist']}")
                st.markdown(f"[🔗 View on Genius]({song_info['url']})")
            
            st.markdown("---")
            
            # Analyze with Gemini
            with st.spinner("🤖 Analyzing emotions with Gemini AI..."):
                gemini_analysis = analyze_with_gemini(song_info, GEMINI_API_KEY)
            
            if gemini_analysis:
                st.markdown("## 🎭 Comprehensive Emotion Analysis")
                
                # Metrics in cards
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("💭 Mood", gemini_analysis.get('mood', 'N/A'))
                with metric_col2:
                    st.metric("⚡ Tempo/Energy", gemini_analysis.get('tempo_energy', 'N/A').capitalize())
                with metric_col3:
                    st.metric("🎨 Valence", gemini_analysis.get('valence', 'N/A').capitalize())
                
                st.markdown("---")
                
                # Detailed analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🔍 Overall Tone")
                    st.info(gemini_analysis.get('overall_tone', 'N/A'))
                    
                    st.markdown("### 🎨 Thematic Elements")
                    st.write(gemini_analysis.get('themes', 'N/A'))
                    
                    st.markdown("### 🎵 Musical Elements")
                    st.write(gemini_analysis.get('musical_elements', 'N/A'))
                
                with col2:
                    st.markdown("### 💭 Primary Emotions Detected")
                    for emotion_data in gemini_analysis.get('primary_emotions', []):
                        intensity = emotion_data.get('intensity', 5)
                        emotion_name = emotion_data.get('emotion', 'Unknown')
                        description = emotion_data.get('description', 'No description')
                        
                        with st.expander(f"**{emotion_name}** - Intensity: {intensity}/10"):
                            st.write(description)
                    
                    st.markdown("### 📖 Lyrical Themes")
                    themes = gemini_analysis.get('lyrical_themes', [])
                    if themes:
                        for theme in themes:
                            st.markdown(f"• {theme}")
                
                st.markdown("### 🌊 Emotional Arc")
                st.write(gemini_analysis.get('emotional_arc', 'N/A'))
                
                # NRCLex analysis
                st.markdown("---")
                st.markdown("## 📊 Detailed Emotion Metrics")
                
                emotional_keywords = gemini_analysis.get('emotional_keywords', [])
                if emotional_keywords:
                    with st.spinner("📈 Calculating emotion scores..."):
                        nrc_results = analyze_emotions_nrclex(emotional_keywords)
                    
                    if nrc_results and nrc_results.get('normalized_scores'):
                        with st.expander("🔑 Emotional Keywords Analyzed"):
                            st.write(", ".join(emotional_keywords))
                            st.caption(f"Total words analyzed: {nrc_results.get('word_count', 0)}")
                        
                        create_emotion_visualizations(nrc_results, gemini_analysis)
                        
                        st.markdown("### 📋 Detailed Emotion Breakdown")
                        
                        scores_sorted = sorted(
                            nrc_results['normalized_scores'].items(), 
                            key=lambda x: x[1], 
                            reverse=True
                        )
                        
                        cols = st.columns(4)
                        for idx, (emotion, score) in enumerate(scores_sorted):
                            with cols[idx % 4]:
                                raw_score = nrc_results['raw_scores'].get(emotion, 0)
                                st.metric(
                                    emotion.capitalize(), 
                                    f"{score:.1f}%",
                                    f"{raw_score} words"
                                )
                    else:
                        st.warning("Could not calculate NRCLex scores")
                else:
                    st.warning("No emotional keywords available for analysis")
                
                # Summary section
                st.markdown("---")
                st.markdown("## 📋 Analysis Summary")
                
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.markdown("### 🎯 Key Takeaways")
                    st.write(f"**Primary Mood:** {gemini_analysis.get('mood', 'N/A')}")
                    st.write(f"**Emotional Valence:** {gemini_analysis.get('valence', 'N/A').capitalize()}")
                    st.write(f"**Energy Level:** {gemini_analysis.get('tempo_energy', 'N/A').capitalize()}")
                
                with summary_col2:
                    st.markdown("### 🏆 Top 3 Emotions")
                    if nrc_results and nrc_results.get('normalized_scores'):
                        top_3 = sorted(
                            nrc_results['normalized_scores'].items(),
                            key=lambda x: x[1],
                            reverse=True
                        )[:3]
                        for i, (emotion, score) in enumerate(top_3, 1):
                            st.write(f"{i}. **{emotion.capitalize()}**: {score:.1f}%")
        else:
            st.error("❌ Song not found. Please check the artist and song name.")

# Footer
st.markdown("""
<div class="footer">
    <p style='font-size: 0.85rem; color: #a0aec0;'>Powered by advanced AI emotion detection technology</p>
</div>
""", unsafe_allow_html=True)