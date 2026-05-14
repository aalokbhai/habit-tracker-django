from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Helvetica', 'B', 20)
        # Title
        self.cell(0, 15, 'Habit Tracker Project Analysis & Optimization Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        # Arial 12
        self.set_font('Helvetica', 'B', 14)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 10, f' {title}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        # Read text file
        self.set_font('Helvetica', '', 11)
        # Output justified text
        self.multi_cell(0, 6, body)
        # Line break
        self.ln(6)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)

def generate_pdf():
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- Executive Summary ---
    pdf.chapter_title("1. Executive Summary")
    summary_text = (
        "This document details the analysis and subsequent optimization of the Habit Tracker Django project. "
        "The initial analysis uncovered critical security vulnerabilities (IDOR) and significant performance "
        "bottlenecks (N+1 database queries). Furthermore, the frontend lacked dynamic visual engagement. "
        "This report outlines the steps taken to secure the backend, drastically improve database efficiency, "
        "and introduce a premium, motion-graphics-driven user interface."
    )
    pdf.chapter_body(summary_text)

    # --- Initial Analysis: Loopholes & Weak Points ---
    pdf.chapter_title("2. Initial Analysis: Loopholes & Weak Points")
    
    pdf.section_title("2.1 Security Vulnerabilities (IDOR)")
    idor_text = (
        "In the initial implementation, habit deletion (mark_delete) and modification (toggle_today, edit_task) "
        "did not verify user ownership. A malicious user could potentially manipulate or delete habits belonging "
        "to other users by simply altering the task primary key (PK) in the URL. This is known as Insecure Direct "
        "Object Reference (IDOR)."
    )
    pdf.chapter_body(idor_text)
    
    pdf.section_title("2.2 Performance Bottlenecks (N+1 Queries)")
    n1_text = (
        "The 'home' dashboard view calculated daily progress by executing a database query for each day, "
        "for every single habit a user had. For a user with 10 habits over 2 weeks, this resulted in roughly 150+ "
        "individual database queries per page load. This highly inefficient loop structure would cause severe latency "
        "as the user base and habit count scaled."
    )
    pdf.chapter_body(n1_text)

    # --- Backend Optimization ---
    pdf.chapter_title("3. Backend Optimization & Security Hardening")
    
    pdf.section_title("3.1 Securing Views")
    sec_text = (
        "All modifying views were updated to enforce the '@login_required' decorator. Furthermore, database queries "
        "were modified to enforce strict ownership checks using Django's get_object_or_404(task, pk=pk, user=request.user). "
        "Basic input validation was also added to habit creation to prevent empty submissions."
    )
    pdf.chapter_body(sec_text)
    
    pdf.section_title("3.2 Algorithmic Query Optimization")
    opt_text = (
        "The dashboard 'home' view was completely refactored. The nested database query loops were removed. "
        "Instead, the system now computes the required date range, queries all relevant 'TaskProgress' records in a single, "
        "optimized IN query, and constructs an in-memory hash map (dictionary). Progress lookups are now performed in O(1) "
        "time complexity against the dictionary. This reduced the database query count from O(N*Days) to exactly O(1)."
    )
    pdf.chapter_body(opt_text)

    # --- Frontend Motion Graphics ---
    pdf.chapter_title("4. Frontend Motion Graphics & Premium UI")
    ui_text = (
        "To provide a modern, premium user experience, the Animate On Scroll (AOS) library was integrated. "
        "This library leverages hardware-accelerated CSS transitions to animate DOM elements as they enter the viewport. "
        "Elements such as the hero section, statistic cards, and habit lists now feature smooth 'fade-up', 'zoom-in', "
        "and 'fade-left' entrance animations with staggered delays to guide the user's eye."
    )
    pdf.chapter_body(ui_text)

    # --- System Architecture Flowchart ---
    pdf.add_page()
    pdf.chapter_title("5. System Architecture & Flowchart")
    
    flowchart = """
    [ User Web Client ]
          |
          v (HTTP Request)
    [ Django URL Router ]
          |
          +--> /home/ (Dashboard)
          |       |--> Validates Session
          |       |--> O(1) Aggregated Query for TaskProgress
          |       +--> Renders templates/home.html (with AOS animations)
          |
          +--> /Habit/add_task/
          |       |--> Validates Input & User
          |       +--> Creates Task Record --> Redirects to /home/
          |
          +--> /Habit/toggle_today/<pk>
                  |--> Verifies Task Owner == request.user
                  |--> Toggles TaskProgress Record
                  +--> Redirects to /home/

    Database Layer (SQLite):
    [ User Table ] <--- (1:N) ---> [ Task Table ] <--- (1:N) ---> [ TaskProgress Table ]
    """
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 5, flowchart)
    pdf.ln(6)

    # Output the PDF
    pdf_file_path = "project_analysis.pdf"
    pdf.output(pdf_file_path)
    print(f"Successfully generated PDF report at: {pdf_file_path}")

if __name__ == "__main__":
    generate_pdf()
