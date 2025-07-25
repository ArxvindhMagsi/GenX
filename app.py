import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

from api_key import api_key

# Configure Google AI
genai.configure(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="GenX - Healthcare Diagnostic Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem 2rem;
        border-radius: 0;
        margin: -1rem -1rem 3rem -1rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-header h2 {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .main-header p {
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.8;
    }
    
    /* Card components */
    .professional-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .professional-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Status boxes */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Analysis section */
    .analysis-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    /* Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-item h3 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .metric-item p {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Professional disclaimer */
    .medical-disclaimer {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem 0;
    }
    
    .medical-disclaimer h4 {
        color: #92400e;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .medical-disclaimer ul {
        color: #78350f;
        margin: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to create PDF report
def create_pdf_report(analysis_text, analysis_mode, filename, patient_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3c72'),
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2a5298'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("GenX Healthcare Diagnostic Report", title_style))
    story.append(Spacer(1, 20))
    
    # Report details table
    report_data = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Analysis Type:', analysis_mode],
        ['Image File:', filename],
        ['Patient Information:', patient_info if patient_info else 'Not provided']
    ]
    
    report_table = Table(report_data, colWidths=[2*inch, 4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(report_table)
    story.append(Spacer(1, 30))
    
    # Analysis results
    story.append(Paragraph("Medical Analysis Results", header_style))
    
    # Split analysis text into paragraphs
    analysis_paragraphs = analysis_text.split('\n')
    for para in analysis_paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), styles['Normal']))
            story.append(Spacer(1, 10))
    
    story.append(Spacer(1, 30))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#dc2626'),
        leftIndent=20,
        rightIndent=20,
        spaceBefore=20
    )
    
    story.append(Paragraph("IMPORTANT MEDICAL DISCLAIMER", header_style))
    disclaimer_text = """
    This analysis was generated by artificial intelligence and is intended for educational and assistive purposes only. 
    This report should NOT be used as a substitute for professional medical diagnosis, treatment, or advice. 
    Always consult with qualified healthcare professionals for medical decisions. 
    In case of medical emergency, contact emergency services immediately.
    """
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main header
st.markdown("""
<div class="main-header">
    <h1>GenX</h1>
    <h2>Healthcare Diagnostic Platform</h2>
    <p>Advanced AI-powered medical image analysis and diagnostic assistance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### System Configuration")
    
    # Model selection
    model_option = st.selectbox(
        "AI Model Selection",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Flash: Optimized for speed | Pro: Enhanced analytical depth"
    )
    
    # Analysis precision
    temperature = st.slider(
        "Analysis Precision", 
        0.0, 1.0, 0.2, 0.1,
        help="Lower values increase analysis focus and consistency"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Supported analysis types
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### Supported Diagnostic Areas")
    
    capabilities = [
        "Radiological Imaging (X-Ray, CT, MRI)",
        "Dermatological Assessment", 
        "Ophthalmological Examination",
        "Pathological Specimen Review",
        "Medical Laboratory Results",
        "Ultrasound Imaging Analysis",
        "General Medical Image Evaluation"
    ]
    
    for capability in capabilities:
        st.markdown(f"• {capability}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
st.markdown("## Medical Image Analysis")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown("### Image Upload")
    
    uploaded_file = st.file_uploader(
        "Select medical image for analysis",
        type=['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'dcm'],
        help="Supported formats: PNG, JPG, JPEG, TIFF, BMP, DICOM"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Medical Image for Analysis", use_column_width=True)
        
        # Technical details
        st.markdown("**Technical Specifications**")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Dimensions", f"{image.size[0]} × {image.size[1]}")
            st.metric("Format", image.format)
        with col_b:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
            st.metric("Color Mode", image.mode)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown("### Analysis Configuration")
    
    analysis_mode = st.selectbox(
        "Diagnostic Focus Area",
        [
            "General Medical Analysis",
            "Radiological Interpretation", 
            "CT/MRI Scan Review",
            "Dermatological Assessment",
            "Ophthalmological Examination",
            "Pathological Analysis",
            "Laboratory Results Review",
            "Ultrasound Interpretation"
        ]
    )
    
    st.markdown("### Clinical Context")
    patient_info = st.text_area(
        "Patient history and symptoms (optional)",
        placeholder="Enter relevant patient information, symptoms, medical history, or specific areas of concern...",
        height=120
    )
    
    # Analysis execution
    if st.button("Execute Analysis", type="primary", use_container_width=True):
        if uploaded_file is not None:
            with st.spinner("Processing medical image analysis..."):
                try:
                    # Prepare image
                    image = Image.open(uploaded_file)
                    
                    # Initialize model
                    model = genai.GenerativeModel(model_option)
                    
                    # Create comprehensive medical prompt
                    medical_prompt = f"""
                    You are an advanced medical AI assistant specializing in {analysis_mode.lower()}.
                    
                    Clinical Context: {patient_info if patient_info else 'No additional clinical information provided'}
                    
                    Please provide a comprehensive medical analysis structured as follows:
                    
                    1. IMAGE ASSESSMENT
                    - Detailed technical description of the medical image
                    - Quality assessment and any limitations
                    
                    2. CLINICAL FINDINGS
                    - Systematic evaluation of anatomical structures
                    - Identification of normal and abnormal findings
                    - Quantitative measurements where applicable
                    
                    3. DIAGNOSTIC IMPRESSIONS
                    - Primary diagnostic considerations
                    - Differential diagnoses ranked by likelihood
                    - Supporting evidence for each consideration
                    
                    4. CLINICAL RECOMMENDATIONS
                    - Suggested additional imaging or testing
                    - Recommended clinical correlation
                    - Follow-up recommendations
                    
                    5. CONFIDENCE ASSESSMENT
                    - Analysis confidence level with justification
                    - Limitations and uncertainties
                    
                    CRITICAL REQUIREMENTS:
                    - Maintain professional medical terminology
                    - Provide evidence-based analysis
                    - Include appropriate medical disclaimers
                    - Emphasize need for professional medical review
                    
                    Format your response professionally as a medical report.
                    """
                    
                    # Generate analysis
                    response = model.generate_content(
                        [medical_prompt, image],
                        generation_config=genai.types.GenerationConfig(
                            temperature=temperature,
                            max_output_tokens=2048,
                        )
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display results
                    st.markdown("""
                    <div class="status-success">
                        <strong>Analysis Complete</strong> - Diagnostic report generated successfully
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("## Diagnostic Report")
                    
                    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Report export options
                    st.markdown("### Export Options")
                    
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        # Text report
                        report_text = f"""
GenX Healthcare Diagnostic Platform
MEDICAL ANALYSIS REPORT

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Analysis Type: {analysis_mode}
Image File: {uploaded_file.name}
Patient Information: {patient_info if patient_info else 'Not provided'}
AI Model: {model_option}

DIAGNOSTIC ANALYSIS:
{response.text}

DISCLAIMER: This analysis was generated by artificial intelligence for educational and 
assistive purposes only. This report should not replace professional medical diagnosis. 
Always consult qualified healthcare professionals for medical decisions.
                        """
                        
                        st.download_button(
                            label="Download Text Report",
                            data=report_text,
                            file_name=f"genx_medical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    
                    with col_export2:
                        # PDF report
                        try:
                            pdf_buffer = create_pdf_report(
                                response.text, 
                                analysis_mode, 
                                uploaded_file.name, 
                                patient_info
                            )
                            
                            st.download_button(
                                label="Download PDF Report",
                                data=pdf_buffer,
                                file_name=f"genx_medical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf"
                            )
                        except ImportError:
                            st.warning("PDF export requires reportlab library. Install with: pip install reportlab")
                            
                except Exception as e:
                    st.markdown("""
                    <div class="status-error">
                        <strong>Analysis Error</strong> - Unable to process medical image
                    </div>
                    """, unsafe_allow_html=True)
                    st.error(f"Technical Details: {str(e)}")
        else:
            st.markdown("""
            <div class="status-warning">
                <strong>No Image Selected</strong> - Please upload a medical image to proceed
            </div>
            """, unsafe_allow_html=True)
    
    if 'uploaded_file' not in locals() or uploaded_file is None:
        st.markdown('</div>', unsafe_allow_html=True)

# Platform metrics
st.markdown("## Platform Overview")

st.markdown("""
<div class="metric-grid">
    <div class="metric-item">
        <h3>AI-Powered</h3>
        <p>Advanced Machine Learning</p>
    </div>
    <div class="metric-item">
        <h3>HIPAA Aware</h3>
        <p>Privacy Protection</p>
    </div>
    <div class="metric-item">
        <h3>Multi-Modal</h3>
        <p>Various Image Types</p>
    </div>
    <div class="metric-item">
        <h3>Professional</h3>
        <p>Medical Grade Analysis</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Medical disclaimer
st.markdown("""
<div class="medical-disclaimer">
    <h4>Important Medical Disclaimer</h4>
    <ul>
        <li><strong>Professional Use Only:</strong> This platform is designed as a diagnostic aid for healthcare professionals</li>
        <li><strong>Not a Replacement:</strong> AI analysis does not replace clinical judgment or professional medical diagnosis</li>
        <li><strong>Clinical Correlation Required:</strong> All findings must be correlated with clinical presentation and additional testing</li>
        <li><strong>Emergency Situations:</strong> For urgent medical situations, contact emergency services immediately</li>
        <li><strong>Liability:</strong> Users assume full responsibility for clinical decisions based on this analysis</li>
    </ul>
</div>
""", unsafe_allow_html=True)