import pandas as pd
import random

random.seed(42)

# ── HAM (Legitimate) emails ────────────────────────────────────────────
ham_templates = [
    "Hi {name}, just following up on our meeting scheduled for {day}. Please find the agenda attached. Let me know if you have any questions. Best regards, {sender}",
    "Dear {name}, your appointment has been confirmed for {day} at {time}. Please bring a valid ID. Thank you for choosing us.",
    "Hello {name}, the quarterly report for Q{q} is now ready. Please review it before our team discussion on {day}.",
    "Hi team, reminder that the project deadline is {day}. Please update your tasks on the board by end of day. Thanks, {sender}",
    "Dear {name}, thank you for your payment of ${amount}. Your receipt number is #{receipt}. Please keep this for your records.",
    "Hi {name}, your order #{receipt} has been shipped and will arrive by {day}. Track your package using the link in your account portal.",
    "Hello {name}, your subscription has been renewed successfully. Next billing date: {day}. Contact support if you have any questions.",
    "Dear colleague, please join us for the department meeting on {day} at {time} in Conference Room {room}. Attendance is mandatory.",
    "Hi {name}, I wanted to share the latest project update. We are on track for the {day} delivery milestone. Great work everyone!",
    "Good morning {name}, here is the weekly status report for the week ending {day}. Please review and reply with your comments by Friday.",
    "Hi {name}, your leave request for {day} has been approved. Please coordinate with your team for coverage. Best, HR Team.",
    "Dear {name}, the invoice #{receipt} for ${amount} is attached. Payment is due by {day}. Thank you for your continued business.",
    "Hello {name}, this is a reminder to complete the mandatory compliance training by {day}. Log in to the portal to start the modules.",
    "Hi {name}, the code review for PR #{receipt} has been completed. Please address the inline comments and re-submit for final approval.",
    "Dear {name}, your IT support ticket #{receipt} has been resolved. Please confirm if the issue is fixed by replying to this email.",
    "Hi {name}, following our phone call today I am sending the summary of action items we discussed. Please review and confirm.",
    "Dear team, please note the office will be closed on {day} for the public holiday. Enjoy the long weekend everyone!",
    "Hello {name}, your annual performance review is scheduled for {day} at {time}. Please prepare a brief self-assessment beforehand.",
    "Hi {name}, the updated employee handbook is now available on the company intranet. Please read section 4 regarding the new remote work policy.",
    "Dear {name}, congratulations on completing 5 years with our company! Your loyalty award certificate is attached. Thank you for your dedication.",
    "Hi {name}, I am writing to confirm the details of the conference call on {day} at {time}. The dial-in number will be shared separately.",
    "Dear {name}, please find attached the contract for review. Kindly sign and return by {day}. Let us know if you need any amendments.",
    "Hello {name}, the server maintenance window is scheduled for {day} at {time}. Expect downtime of approximately 2 hours. Plan accordingly.",
    "Hi {name}, this is your monthly account statement for the period ending {day}. Please review and contact us if you notice any discrepancies.",
    "Dear {name}, we are pleased to inform you that your job application has moved to the next stage. We will be in touch by {day}.",
]

ham_names = ["Sarah","James","Priya","David","Aisha","Tom","Linda","Ravi","Emma","Chris","Mohamed","Jennifer","Robert","Keiko","Carlos"]
ham_senders = ["Michael","Jennifer","Robert","Maria","Ahmed","Sunita","Paul","Grace"]
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","next Monday","January 15","February 3","March 10","April 5","December 20"]
times = ["9:00 AM","10:30 AM","2:00 PM","3:30 PM","11:00 AM","4:00 PM"]

ham_rows = []
for i in range(1500):
    t = random.choice(ham_templates)
    text = t.format(
        name=random.choice(ham_names),
        sender=random.choice(ham_senders),
        day=random.choice(days),
        time=random.choice(times),
        q=random.randint(1, 4),
        amount=random.randint(50, 5000),
        receipt=random.randint(10000, 99999),
        room=random.randint(1, 20)
    )
    ham_rows.append({"text": text, "label": "ham"})

# ── SPAM emails ────────────────────────────────────────────────────────
spam_templates = [
    "Congratulations! You have been selected as our lucky winner! Claim your FREE prize of ${amount} cash now. Click here to redeem before it expires. This is a limited time offer. Act NOW!",
    "URGENT: Your account will be suspended in 24 hours. Click here immediately to verify your information and prevent permanent service disruption.",
    "Make money from home! Earn up to ${amount} per week working just 2 hours a day. No experience needed. 100% guaranteed income. Subscribe FREE today!",
    "You have won a ${amount} gift card! To claim your exclusive reward click the link below before it expires in 24 hours. Do not miss this deal!",
    "BULK DISCOUNT OFFER: Buy cheap medications online without prescription. Special discount available for bulk orders. No doctor needed. Order now!",
    "Hot singles near you want to meet! Click here to see their profiles FREE. Limited time access. Join our network now and find your match!",
    "Lose 30 pounds in 30 days with this one weird trick doctors hate! 100% natural solution, no exercise needed. Order your FREE trial today!",
    "Double your Bitcoin investment in 24 hours! Guaranteed returns of 200 percent. Our AI trading bot has never lost. Invest ${amount} and get ${amount2} back!",
    "FINAL NOTICE: You owe a tax debt of ${amount}. Call immediately to avoid legal action and wage garnishment. This is your last warning.",
    "Increase your sales by 500 percent! Our bulk email marketing database has thousands of verified leads. Buy now and start earning today!",
    "You have been pre-approved for a personal loan of ${amount}! No credit check required. Apply online in 2 minutes. Get cash deposited today!",
    "WORK FROM HOME OPPORTUNITY! Earn ${amount} per month packaging products at home. No experience required. Free starter kit included!",
    "Your computer is infected with viruses! Download our FREE antivirus software now to protect your personal data and banking information!",
    "Exclusive investment opportunity with guaranteed returns. Secret formula used by top Wall Street insiders. Only limited spots remaining today!",
    "WIN a FREE smartphone! You are today's lucky visitor number one million. Spin the wheel now and claim your prize before it expires!",
    "Special bulk offer just for you! Cheap prescription drugs shipped discreetly worldwide. No questions asked. Order now for free shipping!",
    "Earn passive income with our proven system. Thousands already earning ${amount} per day from home. Join free and start making money immediately!",
    "CONGRATULATIONS! Your email was randomly selected for our grand prize draw. You have won ${amount}. Claim your winnings by clicking here now!",
    "Get out of debt fast! We settle credit card debt for pennies on the dollar. Guaranteed results. Call now for your free consultation today!",
    "Herbal supplements that actually work! Boost energy, lose weight, and improve performance. Doctor recommended. Order now with free shipping!",
]

spam_rows = []
for i in range(1100):
    t = random.choice(spam_templates)
    text = t.format(
        amount=random.randint(100, 10000),
        amount2=random.randint(200, 20000),
        receipt=random.randint(10000, 99999),
        day=random.choice(days)
    )
    spam_rows.append({"text": text, "label": "spam"})

# ── PHISHING emails ────────────────────────────────────────────────────
phish_templates = [
    "Dear {bank} Customer, we have detected unusual activity on your account. Your account has been temporarily suspended. Please verify your identity immediately by clicking the link below and entering your login credentials. Failure to verify within 24 hours will result in permanent account closure and loss of funds.",
    "Your {service} account password will expire in 24 hours. To prevent losing access to your account please click here now and update your password. Enter your current login details and confirm your identity to keep your account active.",
    "SECURITY ALERT: Your {service} account was accessed from an unknown device in {location}. If this was not you please click here immediately to secure your account, reset your credentials, and review your recent activity.",
    "Dear valued customer, your PayPal account has been limited due to suspicious activity. Please confirm your billing information by clicking the link below. You must provide your credit card number and social security number to restore full access.",
    "IT Security Notification: Your Microsoft account will be permanently closed unless you verify your login details within 48 hours. Click here to sign in immediately and confirm your account information to avoid service interruption.",
    "Your Apple ID has been locked for security reasons. Someone attempted to sign in to your account from {location}. To unlock your account click here and enter your Apple ID credentials and payment card information.",
    "Dear {bank} account holder, your debit card has been blocked due to suspicious transactions totaling ${amount}. Please click the link below and enter your card number, expiry date, and PIN to unblock your card immediately.",
    "URGENT Netflix account suspended: We were unable to process your payment method. Please update your billing information immediately. Click here and enter your credit card details to reactivate your subscription and avoid losing your watchlist.",
    "Your Amazon account has been flagged for security review. An unauthorized purchase of ${amount} was attempted from your account. Please verify your identity by clicking here and entering your account credentials and payment information.",
    "Dear employee, HR requires you to update your direct deposit banking information immediately. Please click the secure link below and enter your bank account number and routing number by end of business day to ensure your payroll is not disrupted.",
    "FINAL SECURITY WARNING: Your email account has been compromised and your password exposed. Hackers currently have access. Click here immediately and enter your current credentials so our security team can help you secure your account.",
    "Dear customer, we were unable to deliver your package. To reschedule delivery please click here and confirm your delivery address and provide your credit card details for the small redelivery fee of $2.99.",
    "Tax Refund Notification from the IRS: You are eligible for a tax refund of ${amount}. To receive your refund please click here and enter your social security number and bank account details within 48 hours before the claim expires.",
    "Dear {service} user, your account storage is 99 percent full and your account will be suspended. Upgrade now for free by verifying your account credentials. Click here and enter your login and credit card information to claim free storage.",
    "ACCOUNT VERIFICATION REQUIRED: Dear {bank} member, as part of our mandatory security upgrade all customers must re-verify their account details. Click here and enter your account number, online banking password and security answers immediately.",
    "URGENT: Your {service} account has been reported for suspicious activity. To avoid permanent suspension please click the link below within 24 hours and verify your personal information including your date of birth and account password.",
    "Dear customer, your {bank} credit card ending in {card} has been used for an unauthorized transaction of ${amount} at {location}. If you did not make this purchase click here immediately and enter your full card details to dispute the charge.",
    "SYSTEM ALERT: Your email inbox is over its storage limit. Your account will be deactivated in 24 hours. Click here and sign in with your email and password to upgrade your storage and prevent losing all your emails and contacts.",
    "Dear {service} Premium subscriber, your payment of ${amount} has failed. To avoid losing your premium benefits please click here and update your payment method by entering your new credit card number and billing address.",
    "IMPORTANT NOTICE from {bank}: We have updated our online banking security policy. All customers must re-confirm their account credentials by clicking this link and entering their username, password, and one-time PIN before {day}.",
]

phish_locations = ["Russia", "China", "Brazil", "Nigeria", "Romania", "Unknown Location", "Vietnam", "Eastern Europe"]
phish_banks = ["Chase", "Bank of America", "Wells Fargo", "Citibank", "HDFC Bank", "SBI", "Barclays", "HSBC", "TD Bank"]
phish_services = ["Google", "Microsoft", "Apple", "PayPal", "Netflix", "Amazon", "Dropbox", "Facebook", "Instagram", "LinkedIn"]
phish_cards = ["4521", "7832", "1294", "5601", "9034"]

phish_rows = []
for i in range(1100):
    t = random.choice(phish_templates)
    text = t.format(
        bank=random.choice(phish_banks),
        service=random.choice(phish_services),
        location=random.choice(phish_locations),
        amount=random.randint(50, 2000),
        card=random.choice(phish_cards),
        day=random.choice(days)
    )
    phish_rows.append({"text": text, "label": "phishing"})

# ── Combine & save ─────────────────────────────────────────────────────
all_rows = ham_rows + spam_rows + phish_rows
random.shuffle(all_rows)
df = pd.DataFrame(all_rows)
df.to_csv("/home/claude/phishguard/dataset/emails.csv", index=False)
print(f"Dataset saved: {len(df)} rows")
print(df['label'].value_counts())
