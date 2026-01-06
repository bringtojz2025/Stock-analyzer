"""
Stock Analyzer - Notification System
ระบบแจ้งเตือนเมื่อมี Signal ที่น่าสนใจ
"""

import logging
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationBase(ABC):
    """Base class สำหรับการแจ้งเตือน"""
    
    @abstractmethod
    def send(self, symbol, signal, data):
        """ส่งการแจ้งเตือน"""
        pass


class EmailNotification(NotificationBase):
    """ส่งการแจ้งเตือนผ่าน Email"""
    
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send(self, symbol, signal, data, recipient_email):
        """
        ส่ง Email แจ้งเตือน
        
        Args:
            symbol: สัญลักษณ์หุ้น
            signal: สัญญาณ (BUY, SELL, HOLD)
            data: ข้อมูลเพิ่มเติม
            recipient_email: อีเมลผู้รับ
        """
        try:
            subject = f"🚨 Stock Alert: {symbol} - {signal}"
            
            # สร้างเนื้อหา Email
            body = self._create_email_body(symbol, signal, data)
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # ส่ง Email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {recipient_email} for {symbol}")
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
    
    @staticmethod
    def _create_email_body(symbol, signal, data):
        """สร้างเนื้อหา Email"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .signal-buy {{ background-color: #27ae60; color: white; padding: 10px; }}
                .signal-sell {{ background-color: #e74c3c; color: white; padding: 10px; }}
                .signal-hold {{ background-color: #f39c12; color: white; padding: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #34495e; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Stock Alert Notification</h1>
                </div>
                <div class="content">
                    <div class="signal-{signal.lower()}">
                        <h2>{symbol}: {signal}</h2>
                    </div>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Latest Price</td>
                            <td>${data.get('latest_price', 'N/A'):.2f}</td>
                        </tr>
                        <tr>
                            <td>SMA 20</td>
                            <td>${data.get('sma_20', 'N/A'):.2f}</td>
                        </tr>
                        <tr>
                            <td>SMA 50</td>
                            <td>${data.get('sma_50', 'N/A'):.2f}</td>
                        </tr>
                        <tr>
                            <td>RSI (14)</td>
                            <td>{data.get('rsi', 'N/A'):.2f}</td>
                        </tr>
                        <tr>
                            <td>MACD</td>
                            <td>{data.get('macd', 'N/A'):.4f}</td>
                        </tr>
                        <tr>
                            <td>Bollinger Bands Upper</td>
                            <td>${data.get('bb_upper', 'N/A'):.2f}</td>
                        </tr>
                        <tr>
                            <td>Bollinger Bands Lower</td>
                            <td>${data.get('bb_lower', 'N/A'):.2f}</td>
                        </tr>
                        <tr>
                            <td>Confidence</td>
                            <td>{data.get('confidence', 'N/A'):.2%}</td>
                        </tr>
                    </table>
                    <p>
                        <strong>Reasons:</strong><br>
                        {self._format_reasons(data.get('reasons', []))}
                    </p>
                    <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    @staticmethod
    def _format_reasons(reasons):
        """จัดรูปแบบเหตุผล"""
        if not reasons:
            return "No specific reasons"
        return "<br>".join([f"• {reason}" for reason in reasons])


class WebhookNotification(NotificationBase):
    """ส่งการแจ้งเตือนผ่าน Webhook"""
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def send(self, symbol, signal, data):
        """ส่ง Webhook"""
        import requests
        
        try:
            payload = {
                'symbol': symbol,
                'signal': signal,
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 200:
                logger.info(f"Webhook sent for {symbol}")
            else:
                logger.error(f"Webhook failed with status {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending webhook: {str(e)}")


class TelegramNotification(NotificationBase):
    """ส่งการแจ้งเตือนผ่าน Telegram"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def send(self, symbol, signal, data):
        """ส่ง Telegram message"""
        import requests
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            
            message = self._create_telegram_message(symbol, signal, data)
            
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logger.info(f"Telegram message sent for {symbol}")
            else:
                logger.error(f"Telegram failed with status {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
    
    @staticmethod
    def _create_telegram_message(symbol, signal, data):
        """สร้าง Telegram message"""
        emoji_map = {'BUY': '🟢', 'SELL': '🔴', 'HOLD': '🟡'}
        emoji = emoji_map.get(signal, '📊')
        
        message = f"""
{emoji} <b>{symbol} {signal}</b>

<b>Price Info:</b>
Price: ${data.get('latest_price', 'N/A'):.2f}
SMA20: ${data.get('sma_20', 'N/A'):.2f}
SMA50: ${data.get('sma_50', 'N/A'):.2f}

<b>Indicators:</b>
RSI: {data.get('rsi', 'N/A'):.2f}
MACD: {data.get('macd', 'N/A'):.4f}

<b>Confidence:</b> {data.get('confidence', 'N/A'):.2%}

<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        """
        return message


class NotificationManager:
    """จัดการระบบแจ้งเตือนทั้งหมด"""
    
    def __init__(self):
        self.notifications = []
    
    def add_email_notification(self, smtp_server, smtp_port, sender_email, sender_password):
        """เพิ่ม Email notification"""
        self.notifications.append(
            EmailNotification(smtp_server, smtp_port, sender_email, sender_password)
        )
    
    def add_webhook_notification(self, webhook_url):
        """เพิ่ม Webhook notification"""
        self.notifications.append(WebhookNotification(webhook_url))
    
    def add_telegram_notification(self, bot_token, chat_id):
        """เพิ่ม Telegram notification"""
        self.notifications.append(TelegramNotification(bot_token, chat_id))
    
    def notify_all(self, symbol, signal, data, **kwargs):
        """ส่งการแจ้งเตือนไปยังทั้งหมด"""
        for notification in self.notifications:
            try:
                if isinstance(notification, EmailNotification):
                    notification.send(symbol, signal, data, kwargs.get('recipient_email'))
                else:
                    notification.send(symbol, signal, data)
            except Exception as e:
                logger.error(f"Error sending notification: {str(e)}")
