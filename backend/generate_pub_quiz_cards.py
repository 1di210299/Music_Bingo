"""
generate_pub_quiz_cards.py - Pub Quiz Answer Sheet Generator with ReportLab
Creates printable answer sheets for pub quiz teams

Features:
- Professional layout for answer recording
- Space for team name and table number
- Round-by-round organization
- Support for written answers and multiple choice
- Perfect DJ branding
- A4/Letter format
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from io import BytesIO

# ReportLab imports
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, Image, PageBreak, Frame, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent if (SCRIPT_DIR.parent / "data").exists() else SCRIPT_DIR

# Perfect DJ Logo paths
PERFECT_DJ_LOGO_PATHS = [
    PROJECT_ROOT / "frontend" / "assets" / "perfect-dj-logo-pdf.png",
    PROJECT_ROOT / "frontend" / "assets" / "perfect-dj-logo.png",
    PROJECT_ROOT / "assets" / "perfect-dj-logo.png",
    Path("/app/frontend/assets/perfect-dj-logo-pdf.png"),
    Path("/app/frontend/assets/perfect-dj-logo.png"),
]


def find_logo() -> Optional[Path]:
    """Find Perfect DJ logo"""
    for path in PERFECT_DJ_LOGO_PATHS:
        if path.exists():
            return path
    return None


def generate_quiz_answer_sheet(
    venue_name: str = "Perfect DJ Pub Quiz",
    session_date: str = "",
    total_rounds: int = 6,
    questions_per_round: int = 10,
    team_name: str = "",
    output_path: Optional[Path] = None,
    include_mc_bubbles: bool = True
) -> BytesIO:
    """
    Generate a PDF answer sheet for pub quiz
    
    Args:
        venue_name: Name of the venue
        session_date: Date of the quiz
        total_rounds: Number of rounds
        questions_per_round: Questions per round
        team_name: Team name (if pre-filled, otherwise blank)
        output_path: Where to save PDF (if None, returns BytesIO)
        include_mc_bubbles: Include multiple choice bubbles
    
    Returns:
        BytesIO object containing the PDF
    """
    
    # Create PDF buffer
    if output_path:
        buffer = str(output_path)
    else:
        buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
        title=f"{venue_name} - Answer Sheet"
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#16213e'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    round_title_style = ParagraphStyle(
        'RoundTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.white,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leftIndent=5,
        spaceBefore=8,
        spaceAfter=4
    )
    
    # Add logo if available
    logo_path = find_logo()
    if logo_path:
        try:
            logo = Image(str(logo_path), width=40*mm, height=40*mm)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 5*mm))
        except Exception as e:
            print(f"Could not load logo: {e}")
    
    # Title
    elements.append(Paragraph(venue_name, title_style))
    
    # Date
    if session_date:
        elements.append(Paragraph(f"Quiz Date: {session_date}", subtitle_style))
    
    elements.append(Spacer(1, 5*mm))
    
    # Team Information Section
    team_info_data = [
        ['Team Name:', team_name if team_name else '_' * 40],
        ['Table Number:', '_' * 10]
    ]
    
    team_table = Table(team_info_data, colWidths=[35*mm, 135*mm])
    team_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(team_table)
    elements.append(Spacer(1, 8*mm))
    
    # Generate answer sections for each round
    for round_num in range(1, total_rounds + 1):
        # Round header
        round_header = Paragraph(f"Round {round_num}", round_title_style)
        round_header_table = Table([[round_header]], colWidths=[170*mm])
        round_header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#667eea')),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(round_header_table)
        elements.append(Spacer(1, 2*mm))
        
        # Questions for this round
        question_rows = []
        
        for q_num in range(1, questions_per_round + 1):
            if include_mc_bubbles:
                # Multiple choice bubbles: A B C D
                bubbles = "○ A    ○ B    ○ C    ○ D"
                question_rows.append([
                    f"Q{q_num}",
                    bubbles,
                    '_' * 40
                ])
            else:
                # Just answer space
                question_rows.append([
                    f"Q{q_num}",
                    '_' * 70
                ])
        
        if include_mc_bubbles:
            col_widths = [12*mm, 35*mm, 123*mm]
        else:
            col_widths = [12*mm, 158*mm]
        
        questions_table = Table(question_rows, colWidths=col_widths)
        questions_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(questions_table)
        
        # Add page break after every 2 rounds (except last)
        if round_num % 2 == 0 and round_num < total_rounds:
            elements.append(PageBreak())
        else:
            elements.append(Spacer(1, 5*mm))
    
    # Footer
    elements.append(Spacer(1, 5*mm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph("Good luck and have fun! 🎉", footer_style))
    elements.append(Paragraph("www.perfectdj.co.uk", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Return buffer
    if isinstance(buffer, BytesIO):
        buffer.seek(0)
        return buffer
    else:
        return None


def generate_blank_templates(
    venue_name: str = "Perfect DJ Pub Quiz",
    session_date: str = "",
    total_rounds: int = 6,
    questions_per_round: int = 10,
    num_sheets: int = 30,
    output_path: Optional[Path] = None
) -> BytesIO:
    """
    Generate multiple blank answer sheets
    
    Args:
        venue_name: Venue name
        session_date: Quiz date
        total_rounds: Number of rounds
        questions_per_round: Questions per round
        num_sheets: How many blank sheets to generate
        output_path: Output file path
    
    Returns:
        BytesIO with PDF
    """
    from pypdf import PdfWriter, PdfReader
    
    # Generate single template
    template_buffer = generate_quiz_answer_sheet(
        venue_name=venue_name,
        session_date=session_date,
        total_rounds=total_rounds,
        questions_per_round=questions_per_round,
        team_name="",
        output_path=None
    )
    
    # Read template
    template_reader = PdfReader(template_buffer)
    
    # Create writer and duplicate pages
    writer = PdfWriter()
    for _ in range(num_sheets):
        for page in template_reader.pages:
            writer.add_page(page)
    
    # Write output
    if output_path:
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        return None
    else:
        output_buffer = BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Pub Quiz Answer Sheets')
    parser.add_argument('--venue', default='Perfect DJ Pub Quiz', help='Venue name')
    parser.add_argument('--date', default='', help='Quiz date')
    parser.add_argument('--rounds', type=int, default=6, help='Number of rounds')
    parser.add_argument('--questions', type=int, default=10, help='Questions per round')
    parser.add_argument('--num-sheets', type=int, default=30, help='Number of blank sheets')
    parser.add_argument('--output', default='pub_quiz_answer_sheets.pdf', help='Output filename')
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    
    generate_blank_templates(
        venue_name=args.venue,
        session_date=args.date,
        total_rounds=args.rounds,
        questions_per_round=args.questions,
        num_sheets=args.num_sheets,
        output_path=output_path
    )
    
    print(f"✅ Generated {args.num_sheets} answer sheets: {output_path}")
