import os
import sys

def build_pdf(filename="manual_instalacion_sqlanywhere.pdf"):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    except ImportError:
        print("ReportLab is not installed. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#1A365D")   # Deep Blue
    secondary_color = colors.HexColor("#2B6CB0") # Slate Blue
    text_color = colors.HexColor("#2D3748")      # Dark Grey
    bg_code_color = colors.HexColor("#EDF2F7")   # Light Grey for code
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        spaceAfter=8,
        alignment=TA_LEFT
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#C53030"),
        spaceAfter=8,
        leftIndent=15
    )
    
    alert_style = ParagraphStyle(
        'Alert',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#9B2C2C"),
        spaceAfter=8
    )

    story = []
    
    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 150))
    story.append(Paragraph("Manual de Instalación y Soporte de<br/>SAP SQL Anywhere en Apache Superset", title_style))
    story.append(Paragraph("Guía Completa de Despliegue Automatizado (Opción A)", subtitle_style))
    story.append(Spacer(1, 200))
    
    meta_data = [
        [Paragraph("<b>Creado por:</b> Antigravity Coding Assistant", body_style)],
        [Paragraph("<b>Fecha:</b> Julio 2026", body_style)],
        [Paragraph("<b>Estado del Proyecto:</b> Integrado", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[200])
    t_meta.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    
    story.append(PageBreak())
    
    # --- PAGE 2: INTRO & CONCEPT ---
    story.append(Paragraph("1. Introducción y Arquitectura", h1_style))
    story.append(Paragraph(
        "Este manual describe la arquitectura y el proceso necesario para dotar a "
        "Apache Superset de soporte nativo para bases de datos SAP SQL Anywhere (anteriormente Sybase SQL Anywhere). "
        "Debido a que SQL Anywhere requiere librerías cliente nativas propietarias compiladas en C, la "
        "conexión directa con Python requiere que estas librerías estén configuradas correctamente en el "
        "sistema operativo donde corre el servidor de Superset.",
        body_style
    ))
    story.append(Paragraph(
        "Con los cambios realizados en el proyecto, la instalación se ha automatizado por completo dentro del contenedor Docker "
        "utilizando la <b>Opción A (Instalador Local)</b>. Esto significa que al desplegar Superset usando Docker Compose, "
        "no es necesario realizar configuraciones manuales en el host de Ubuntu Server.",
        body_style
    ))
    
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("2. Preparación de la Opción A (Flujo de Trabajo)", h1_style))
    story.append(Paragraph(
        "Para que la construcción de la imagen de Docker instale automáticamente el cliente de SQL Anywhere, "
        "debe seguir los siguientes pasos antes de ejecutar el comando de despliegue:",
        body_style
    ))
    story.append(Paragraph("<b>Paso 1: Obtener el Instalador Cliente de SQL Anywhere para Linux</b>", h2_style))
    story.append(Paragraph(
        "Descargue el instalador cliente oficial para Linux de 64 bits (por ejemplo, el archivo "
        "<code>sqla17developerlinux.tar.gz</code> o similar) desde el Centro de Soporte de SAP o la edición Developer.",
        body_style
    ))
    story.append(Paragraph("<b>Paso 2: Colocar el archivo en la raíz del proyecto</b>", h2_style))
    story.append(Paragraph(
        "Coloque el archivo descargado directamente en el directorio raíz de este proyecto Superset. "
        "El nombre del archivo debe comenzar con <code>sqla</code> y terminar en <code>.tar.gz</code>.",
        body_style
    ))
    story.append(Paragraph("<b>Paso 3: Construir y Levantar Superset</b>", h2_style))
    story.append(Paragraph(
        "Inicie la construcción de la imagen docker normal de desarrollo o de producción. El motor de build de Docker detectará "
        "el archivo de instalación automáticamente, ejecutará la instalación silenciosa y registrará las librerías.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # --- PAGE 3: PROJECT INJECTIONS & Docker ---
    story.append(Paragraph("3. Detalles de los Cambios Inyectados en el Proyecto", h1_style))
    story.append(Paragraph(
        "Se han inyectado de forma permanente varios componentes clave en la estructura de Superset:",
        body_style
    ))
    
    story.append(Paragraph("A. Especificación del Motor de Base de Datos (Database Engine Spec)", h2_style))
    story.append(Paragraph(
        "Se creó el archivo <code>superset/db_engine_specs/sqlanywhere.py</code>. Este archivo define la clase "
        "<code>SqlAnywhereEngineSpec</code> que permite a Superset:",
        body_style
    ))
    story.append(Paragraph("• Reconocer el dialecto de SQLAlchemy <code>sqlany+sqlanydb</code>.", body_style))
    story.append(Paragraph("• Manejar correctamente expresiones de agregación de tiempo (segundo, minuto, hora, día, etc.) mediante funciones <code>DATEADD</code> y <code>DATEDIFF</code> nativas de SQL Anywhere.", body_style))
    story.append(Paragraph("• Mostrar 'SAP SQL Anywhere' como una base de datos soportada con su respectivo logo y parámetros de conexión en la UI.", body_style))
    
    story.append(Paragraph("B. Dependencias del Proyecto (pyproject.toml)", h2_style))
    story.append(Paragraph(
        "Se añadieron las dependencias <code>sqlalchemy-sqlany</code> y <code>sqlanydb</code> a las dependencias base de Python. "
        "De este modo, se compilan y se instalan automáticamente en los contenedores <i>lean</i> y <i>dev</i>.",
        body_style
    ))
    
    story.append(Paragraph("C. Automatización en Docker (Dockerfile & Script)", h2_style))
    story.append(Paragraph(
        "• Se agregaron <code>unixodbc</code> y <code>unixodbc-dev</code> a los paquetes de Debian instalados por defecto.",
        body_style
    ))
    story.append(Paragraph(
        "• Se añadió el script <code>docker/install-sqlanywhere.sh</code>, el cual realiza una instalación silenciosa "
        "y sin interfaz gráfica del instalador local, creando un enlace simbólico universal a <code>/opt/sqlanywhere</code>.",
        body_style
    ))
    story.append(Paragraph(
        "• Se exportaron de forma permanente las siguientes variables de entorno para que Superset localice el driver cliente:",
        body_style
    ))
    story.append(Paragraph("<code>ENV SQLANY=/opt/sqlanywhere</code>", code_style))
    story.append(Paragraph("<code>ENV PATH=$PATH:$SQLANY/bin64:$SQLANY/bin32</code>", code_style))
    story.append(Paragraph("<code>ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SQLANY/lib64:$SQLANY/lib32</code>", code_style))
    
    story.append(PageBreak())
    
    # --- PAGE 4: CONFIGURATION IN SUPERSET ---
    story.append(Paragraph("4. Configuración de Conexión en la Interfaz de Superset", h1_style))
    story.append(Paragraph(
        "Una vez desplegado el contenedor, siga estos pasos para conectar su base de datos SQL Anywhere a Superset:",
        body_style
    ))
    story.append(Paragraph("1. Inicie sesión en la interfaz web de Apache Superset (usualmente en el puerto 8088).", body_style))
    story.append(Paragraph("2. Navegue al menú de la esquina superior derecha: <b>Settings (Ajustes) -> Database Connections (Conexiones a Bases de Datos)</b>.", body_style))
    story.append(Paragraph("3. Haga clic en el botón <b>+ Database</b>.", body_style))
    story.append(Paragraph("4. En la ventana emergente, seleccione <b>SAP SQL Anywhere</b> del listado de bases de datos soportadas.", body_style))
    story.append(Paragraph("5. Complete el formulario con los siguientes parámetros de su servidor:", body_style))
    
    # Table of params
    param_data = [
        [Paragraph("<b>Parámetro</b>", body_style), Paragraph("<b>Descripción</b>", body_style), Paragraph("<b>Ejemplo</b>", body_style)],
        [Paragraph("Host", body_style), Paragraph("Dirección IP o dominio del servidor", body_style), Paragraph("192.168.1.50", body_style)],
        [Paragraph("Port", body_style), Paragraph("Puerto de conexión de SQL Anywhere", body_style), Paragraph("2638", body_style)],
        [Paragraph("Database", body_style), Paragraph("Nombre de la base de datos", body_style), Paragraph("mi_bd_produccion", body_style)],
        [Paragraph("Username", body_style), Paragraph("Usuario con permisos de lectura", body_style), Paragraph("dba", body_style)],
        [Paragraph("Password", body_style), Paragraph("Contraseña de acceso", body_style), Paragraph("contraseña_segura", body_style)],
    ]
    t_param = Table(param_data, colWidths=[80, 240, 180])
    t_param.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_param)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("URI de SQLAlchemy alternativa", h2_style))
    story.append(Paragraph(
        "Si prefiere ingresar la URI de conexión de forma directa usando la pestaña 'Advanced' o de forma manual, "
        "utilice la siguiente sintaxis estándar:",
        body_style
    ))
    story.append(Paragraph("<code>sqlany+sqlanydb://usuario:contraseña@host:puerto/nombre_base_datos</code>", code_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Solución de Problemas (Troubleshooting)", h1_style))
    
    story.append(Paragraph("<b>Error: <code>Could not load dbcapi</code></b>", h2_style))
    story.append(Paragraph(
        "Este error ocurre si la librería compartida nativa (<code>libdbcapi_r.so</code>) no está disponible en las rutas declaradas. "
        "Asegúrese de haber colocado el instalador cliente en la raíz del proyecto <i>antes</i> de construir la imagen Docker "
        "y de que la variable <code>LD_LIBRARY_PATH</code> apunte a <code>/opt/sqlanywhere/lib64</code>.",
        body_style
    ))
    
    story.append(Paragraph("<b>Error: <code>Connection refused</code></b>", h2_style))
    story.append(Paragraph(
        "Indica que el contenedor de Superset no puede comunicarse con el puerto de SQL Anywhere. Verifique la conectividad de red, "
        "las reglas de firewall en Ubuntu Server y asegúrese de que el motor de base de datos SQL Anywhere acepte conexiones TCP/IP "
        "y escuche en la IP correcta.",
        body_style
    ))
    
    doc.build(story)
    print(f"Successfully generated PDF manual at: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf()
