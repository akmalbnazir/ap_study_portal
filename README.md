# 🎓 AP Study Portal

The **AP Study Portal** is a full-featured web application built with Flask, Stripe, and OpenAI. It provides unlimited access to AP exam preparation tools, including vocabulary flashcards, AI-generated practice questions, and full mock exams — all for a one-time $5 lifetime payment.

---

## 🚀 Features

- 🔐 **User Authentication**
  - Login and signup functionality
  - Session-based access control
  - Device restriction: Each account can be used on a maximum of **two devices** via device ID locking

- 📚 **Course Dashboard**
  - Course enrollment per user account
  - Supported courses:
    - AP Psychology
    - AP Human Geography
    - AP African American Studies
    - AP US Government and Politics
    - AP US History
    - AP Computer Science Principles
    - AP World History

- 🧠 **AI-Powered Practice**
  - GPT-generated MCQs for every unit
  - CollegeBoard-style formatting
  - Limited to 1 generation per unit every 24 hours

- 🗂 **Vocabulary Flashcards**
  - Cleanly structured flashcard system per unit
  - Content stored as structured JSON files

- 📝 **Mock Exams**
  - Multiple-Choice Section
  - Free-Response Section
  - All stored locally in static data files

- 💳 **Stripe Monetization**
  - Integrated Stripe Checkout
  - Webhook and success URL support to update user payment status
  - $5 one-time payment for lifetime access

- 🔒 **Account Security**
  - Hardware-bound login via JavaScript-collected `device_id`
  - Blocks login on more than 2 devices per user

- ⚙️ **Admin Panel**
  - View all users and payment status
  - Manually add users (email/password/paid flag)

---

## 📁 Project Structure

```
.
├── app.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── vocab.html
│   ├── practice.html
│   ├── mock_exam.html
├── static/
│   ├── data/
│   │   ├── ap_psychology_vocab.json
│   │   ├── ap_us_history_vocab.json
│   │   └── practice_questions/
│   │       ├── ap_psychology.json
│   └── device.js
├── models/
│   ├── __init__.py
│   ├── user.py
├── course/
│   ├── routes.py
│   └── models.py
├── auth/
│   └── routes.py
├── utils/
│   └── ai_generate.py
├── stripe_integration/
│   └── routes.py
└── README.md
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ap-study-portal.git
   cd ap-study-portal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file and include the following:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLIC_KEY=your-stripe-publishable-key
   STRIPE_ENDPOINT_SECRET=your-stripe-webhook-secret
   ```

5. **Run the app**
   ```bash
   flask run
   ```

---

## 🌐 Deployment Notes

- Hosted and tested successfully on **Replit**
- Replit resets file system on deploy; make sure your database is saved in a persistent mount or external storage
- Stripe webhook requires public access. Use [ngrok](https://ngrok.com/) for local development testing.

---

## 🛡️ Security & Integrity

- All account logins are limited to 2 devices
- `device.js` script assigns a unique UUID and stores it in `localStorage`
- Admins can view registered devices and manually remove or add users

---

## ✅ Future Roadmap

- Mobile-friendly redesign
- AI-powered FRQ grading and feedback
- Adaptive question difficulty engine
- Admin analytics dashboard

---

## 🤝 Contributing

1. Fork the repository
2. Make your changes
3. Submit a pull request with a meaningful message and description

---

## 🧠 Credits

- **Backend:** Flask, SQLAlchemy
- **Frontend:** Jinja2, Tailwind CSS
- **AI Questions:** OpenAI GPT-4 API
- **Payments:** Stripe Checkout

---

## 📧 Contact

Maintained by **Akmal Nazir**  
📬 [akmal.nazirbusiness@gmail.com](mailto:akmal.nazirbusiness@gmail.com)

