from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


OUTPUT = "Practical_Test_2_Presentation_Notes.pdf"


def build_styles():
    base = getSampleStyleSheet()
    base["Normal"].fontName = "Helvetica"
    base["Normal"].fontSize = 10
    base["Normal"].leading = 14
    base["Normal"].spaceAfter = 6

    styles = {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#374151"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": base["Normal"],
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            leftIndent=13,
            firstLineIndent=-8,
            spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Normal"],
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#e5e7eb"),
            borderPadding=5,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#065f46"),
            backColor=colors.HexColor("#ecfdf5"),
            borderColor=colors.HexColor("#a7f3d0"),
            borderPadding=7,
            spaceBefore=8,
            spaceAfter=10,
        ),
    }
    return styles


def p(text, style):
    return Paragraph(text, style)


def bullet(text, styles):
    return p(f"- {text}", styles["bullet"])


def code(text, styles):
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return p(safe, styles["code"])


def stage_table(styles):
    rows = [
        ["Requirement", "How the pipeline satisfies it"],
        ["Trigger", "Runs automatically on push to the main branch."],
        ["Build", "Checks out code, sets up PHP 8.2, installs Composer packages, validates Composer, and lints PHP."],
        ["Test", "Runs PHPUnit unit tests and integration tests against a temporary MySQL 8.0 service container."],
        ["Security scan", "Runs Composer audit and OWASP Dependency-Check, then uploads the security report artifact."],
        ["Deploy", "Deploys a blue preview slot, smoke-tests it, then deploys the green production slot on Vercel."],
    ]

    table = Table(rows, colWidths=[42 * mm, 118 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ffffff")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, 12 * mm, "Cloud Application Development: Practical Test 2")
    canvas.drawRightString(192 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Practical Test 2 Presentation Notes",
        author="Cxuku",
    )

    story = []
    story.append(p("Practical Test 2 Presentation Notes", styles["title"]))
    story.append(p("PHP Customer Records App and CI/CD Pipeline", styles["subtitle"]))
    story.append(
        p(
            "Use this document as speaking notes when explaining the PHP script and the CI/CD pipeline to your lecturer.",
            styles["callout"],
        )
    )

    story.append(p("Question 1: PHP Script customers.php", styles["h1"]))
    story.append(
        p(
            "The purpose of customers.php is to connect to a MySQL database using PDO, retrieve customer records, "
            "and display them in a styled HTML table. The script also handles database failures safely.",
            styles["body"],
        )
    )

    sections = [
        (
            "Strict typing and autoloading",
            "The script starts with strict typing and loads Composer's autoloader so external packages and project classes can be used.",
            'declare(strict_types=1);\nrequire_once __DIR__ . "/../vendor/autoload.php";\nuse App\\Database;',
        ),
        (
            "Loading environment variables",
            "The dotenv block loads a local .env file during local development. In production, Vercel supplies the same values as environment variables.",
            'if (file_exists(__DIR__ . "/../.env")) {\n    $dotenv = Dotenv\\Dotenv::createImmutable(__DIR__ . "/..");\n    $dotenv->load();\n}',
        ),
        (
            "Default variables",
            "The script starts with an empty customer list and no error. These values are updated depending on whether the database query succeeds.",
            "$customers = [];\n$error = null;",
        ),
        (
            "PDO connection",
            "The Database class creates a PDO connection using DB_HOST, DB_PORT, DB_NAME, DB_USER, and DB_PASSWORD.",
            "$db = new Database();\n$pdo = $db->getConnection();",
        ),
        (
            "Prepared statement",
            "The SQL query is prepared and then executed. This satisfies the prepared-statement requirement and is the safe pattern for database work.",
            "$stmt = $pdo->prepare(\n    'SELECT id, name, email, created_at FROM customers ORDER BY created_at DESC'\n);\n$stmt->execute();",
        ),
        (
            "Fetching records",
            "fetchAll(PDO::FETCH_ASSOC) returns the database rows as associative arrays, so the table can access fields by name.",
            "$customers = $stmt->fetchAll(PDO::FETCH_ASSOC);",
        ),
        (
            "Graceful failure handling",
            "If PDO throws an exception, the user sees a friendly message. The real technical error is logged instead of being exposed on the page.",
            "catch (PDOException $e) {\n    $error = 'Unable to connect to the database. Please try again later.';\n    error_log(...);\n}",
        ),
        (
            "Safe HTML output",
            "Every displayed database value is escaped with htmlspecialchars to prevent stored XSS attacks.",
            "htmlspecialchars($customer['name'], ENT_QUOTES, 'UTF-8')",
        ),
    ]

    for heading, explanation, snippet in sections:
        story.append(KeepTogether([p(heading, styles["h2"]), p(explanation, styles["body"]), code(snippet, styles)]))

    story.append(p("What Database.php Does", styles["h1"]))
    for item in [
        "Reads connection settings from environment variables.",
        "Builds a MySQL DSN using host, port, database name, and utf8mb4 charset.",
        "Creates the PDO object.",
        "Sets PDO::ATTR_ERRMODE to exceptions so connection/query failures can be caught.",
        "Sets PDO::ATTR_DEFAULT_FETCH_MODE to associative arrays.",
        "Disables emulated prepares so MySQL handles prepared statements directly.",
    ]:
        story.append(bullet(item, styles))

    story.append(PageBreak())

    story.append(p("Question 2: Complete CI/CD Pipeline", styles["h1"]))
    story.append(
        p(
            "The pipeline is defined in .github/workflows/pipeline.yml. It uses GitHub Actions to automate build, "
            "testing, security scanning, and deployment to the cloud PaaS.",
            styles["body"],
        )
    )
    story.append(stage_table(styles))
    story.append(Spacer(1, 8))

    stage_notes = [
        (
            "Trigger: Push to main",
            "The pipeline runs whenever code is pushed to the main branch. workflow_dispatch is also included so the workflow can be run manually.",
        ),
        (
            "Build stage",
            "The build job checks out the code, sets up PHP 8.2 with pdo_mysql, installs Composer dependencies, validates Composer configuration, and lints the code.",
        ),
        (
            "Test stage",
            "The test job starts a temporary MySQL 8.0 service container. Unit tests check small pieces of logic, while integration tests insert and fetch rows from a real test database.",
        ),
        (
            "Security scan stage",
            "The security job uses composer audit for PHP dependency advisories and OWASP Dependency-Check for a broader dependency scan. The OWASP report is uploaded as an artifact.",
        ),
        (
            "Deploy stage",
            "The deployment job uses Vercel CLI. It creates a preview deployment first, smoke-tests it, and then deploys the production version. Railway hosts the MySQL database.",
        ),
        (
            "Zero-downtime blue-green idea",
            "Blue is the preview slot, where the new version is deployed and checked first. Green is the production slot. Vercel keeps the old production version available until the new production deployment is ready.",
        ),
    ]

    for heading, explanation in stage_notes:
        story.append(KeepTogether([p(heading, styles["h2"]), p(explanation, styles["body"])]))

    story.append(p("How To Explain The Final Architecture", styles["h1"]))
    for item in [
        "GitHub stores the source code and runs GitHub Actions.",
        "Vercel hosts the PHP web application as the cloud PaaS.",
        "Railway hosts the MySQL database.",
        "GitHub Actions reads deployment and database values from encrypted secrets.",
        "The app reads database settings from environment variables, not from hardcoded passwords.",
    ]:
        story.append(bullet(item, styles))

    story.append(p("Short Speaking Summary", styles["h1"]))
    story.append(
        p(
            "My PHP application connects to MySQL using PDO, retrieves customer records using a prepared statement, "
            "and displays them in a styled HTML table. It handles connection failures gracefully by showing a safe "
            "message to the user while logging the real error for debugging. My CI/CD pipeline runs on every push to "
            "main. It builds and lints the app, runs unit and integration tests against MySQL, performs security scans, "
            "and deploys to Vercel using a preview-then-production flow for zero-downtime deployment.",
            styles["body"],
        )
    )

    story.append(p("Evidence To Show The Lecturer", styles["h1"]))
    for item in [
        "customers.php and Database.php source code.",
        "schema.sql showing the customers table structure.",
        "GitHub Actions run #13 showing all stages passing.",
        "Vercel production URL: https://practical-test-steel.vercel.app.",
        "Railway MySQL public TCP host/port and variables, without exposing the password.",
    ]:
        story.append(bullet(item, styles))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
