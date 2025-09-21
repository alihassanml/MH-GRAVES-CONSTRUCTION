from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from fastapi.responses import RedirectResponse

app = FastAPI()

# Static files and templates setup
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

# Email configuration - Use environment variables for security
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "mhgravesconstruction@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "piwnnrexfjnzkvyt")  # Use Gmail App Password

def create_beautiful_email_html(name, email, message):
    """Create a beautiful HTML email template for MH Graves Construction"""
    current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Form Submission - MH Graves Construction</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); padding: 40px 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🏗️ MH Graves Construction
                </h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px;">
                    New Contact Form Submission
                </p>
            </div>

            <!-- Content -->
            <div style="padding: 40px 30px;">
                
                <!-- Contact Info Card -->
                <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #2563eb;">
                    <h2 style="color: #1e293b; margin: 0 0 20px; font-size: 20px; font-weight: 600;">
                        👤 Contact Information
                    </h2>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; width: 80px; vertical-align: top;">
                                <strong style="color: #64748b; font-size: 14px;">NAME:</strong>
                            </td>
                            <td style="padding: 8px 0; color: #1e293b; font-size: 16px; font-weight: 500;">
                                {name}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; vertical-align: top;">
                                <strong style="color: #64748b; font-size: 14px;">EMAIL:</strong>
                            </td>
                            <td style="padding: 8px 0;">
                                <a href="mailto:{email}" style="color: #2563eb; text-decoration: none; font-weight: 500; font-size: 16px;">
                                    {email}
                                </a>
                            </td>
                        </tr>
                    </table>
                </div>

                <!-- Message Card -->
                <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #10b981;">
                    <h2 style="color: #1e293b; margin: 0 0 15px; font-size: 20px; font-weight: 600;">
                        💬 Project Details
                    </h2>
                    <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                        <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 15px; white-space: pre-wrap;">
                            {message if message else 'No message provided.'}
                        </p>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div style="text-align: center; margin: 30px 0;">
                    <a href="mailto:{email}" style="display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 0 10px; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">
                        Reply to {name.split()[0] if name else 'Client'}
                    </a>
                    <a href="tel:532-123-4537" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 0 10px; box-shadow: 0 4px 12px rgba(16,185,129,0.3);">
                        📞 Call Back
                    </a>
                </div>

                <!-- Footer Info -->
                <div style="background-color: #f8fafc; border-radius: 8px; padding: 20px; text-align: center; margin-top: 30px;">
                    <p style="color: #64748b; margin: 0; font-size: 14px;">
                        📅 Received on <strong>{current_date}</strong>
                    </p>
                    <p style="color: #64748b; margin: 5px 0 0; font-size: 12px;">
                        This email was automatically generated from mhgravesconstruction.com contact form.
                    </p>
                </div>
            </div>

            <!-- Footer -->
            <div style="background-color: #1e293b; color: white; padding: 25px 30px; text-align: center;">
                <h3 style="margin: 0 0 10px; font-size: 18px; font-weight: 600;">
                    🏗️ MH Graves Construction
                </h3>
                <p style="margin: 0; opacity: 0.8; font-size: 14px;">
                    Building Your Visions • Licensed General Contractor
                </p>
                <div style="margin-top: 15px;">
                    <a href="mailto:nelo@mhgravesconstruction.com" style="color: #60a5fa; text-decoration: none; font-size: 14px; margin: 0 15px;">
                        nelo@mhgravesconstruction.com
                    </a>
                    <a href="tel:532-123-4537" style="color: #60a5fa; text-decoration: none; font-size: 14px; margin: 0 15px;">
                        (532) 123-4537
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/contact", response_class=JSONResponse)
async def handle_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    """Handle contact form submission and send email"""
    try:
        # Create email message
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # Send to your business email
        msg["Subject"] = f"🏗️ New Project Inquiry from {name}"
        
        # Create plain text version (fallback)
        text_body = f"""
New Contact Form Submission - MH Graves Construction

Contact Information:
Name: {name}
Email: {email}

Project Details:
{message if message else 'No message provided.'}

Received: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---
Reply to this inquiry: {email}
Call: (532) 123-4537
Website: mhgravesconstruction.com
        """
        
        # Create HTML version
        html_body = create_beautiful_email_html(name, email, message)
        
        # Attach both versions
        text_part = MIMEText(text_body, "plain", "utf-8")
        html_part = MIMEText(html_body, "html", "utf-8")
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, [EMAIL_ADDRESS], msg.as_string())
        
        return RedirectResponse(url="/", status_code=303)


    except Exception as e:
        print(f"Error sending email: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Sorry, there was a problem sending your message. Please try calling us at (532) 123-4537."
            }
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)