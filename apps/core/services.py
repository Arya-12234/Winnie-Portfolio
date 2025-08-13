from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from datetime import datetime

def send_contact_email(name, email, subject, message):
    formatted_message = message.replace('\n', '<br>')
    current_year = datetime.now().year

    html_content = f"""
    <div style="font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; background-color: #f8fafc; padding: 2.5rem 1rem; margin: 0;">
        <div style="max-width: 650px; margin: 0 auto; background-color: white; padding: 2.5rem; border-radius: 0.75rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);">
            <div style="border-left: 4px solid #6366f1; padding-left: 1rem; margin-bottom: 2rem;">
                <h2 style="color: #1e293b; font-size: 1.5rem; font-weight: 600; margin: 0 0 0.5rem 0;">New Message Received</h2>
                <p style="color: #64748b; font-size: 0.95rem; margin: 0;">A new inquiry has been submitted through your contact form</p>
            </div>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">
                <tr>
                    <td style="padding: 1rem; border-bottom: 1px solid #f1f5f9; width: 100px; color: #64748b; font-weight: 500;">From</td>
                    <td style="padding: 1rem; border-bottom: 1px solid #f1f5f9; color: #0f172a;">{name} <span style="font-size: 0.875rem; color: #64748b;">({email})</span></td>
                </tr>
                <tr>
                    <td style="padding: 1rem; border-bottom: 1px solid #f1f5f9; color: #64748b; font-weight: 500;">Subject</td>
                    <td style="padding: 1rem; border-bottom: 1px solid #f1f5f9; color: #0f172a;">{subject}</td>
                </tr>
            </table>

            <div style="background-color: #f8fafc; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem;">
                <h3 style="color: #1e293b; font-size: 1.1rem; margin-top: 0; margin-bottom: 1rem; font-weight: 500;">Message</h3>
                <div style="color: #334155; line-height: 1.7; white-space: pre-wrap;">{formatted_message}</div>
            </div>

            <div style="text-align: center; margin-top: 2.5rem;">
                <a href="mailto:{email}" style="display: inline-block; background-color: #6366f1; color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 0.375rem; font-weight: 500; font-size: 0.95rem;">Reply to {name}</a>
            </div>
        </div>

        <div style="text-align: center; padding: 2rem 0; max-width: 650px; margin: 0 auto;">
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">© mutheu {current_year}</p>
        </div>
    </div>
    """

    subject_line = f"New Contact: {subject}"
    text_content = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"

    email_msg = EmailMultiAlternatives(
        subject=subject_line,
        body=text_content,
        from_email=email,
        to=[settings.PERSONAL_EMAIL]
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
