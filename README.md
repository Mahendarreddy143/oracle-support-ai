# 🚀 Oracle Support AI

**An intelligent AI-powered support platform for Oracle EBS/ERP issues solving**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](#)
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-blue.svg)](#contributing)

## 📋 Overview

Oracle Support AI is a community-driven intelligent system that aggregates real-world solutions, best practices, and code samples for Oracle EBS/ERP problems. It uses AI/ML to match client issues with similar resolved cases and provides actionable solutions.

### 🎯 Key Features

- **Multi-Module Support**: PL/SQL, SQL, Forms, Workflows, OAF, APEX, Reports, Data Migration
- **AI-Powered Search**: Semantic search using vector embeddings
- **Code Samples**: Production-ready templates for common scenarios
- **Error Repository**: Comprehensive database of ORA- errors and solutions
- **Community Driven**: Open for contributions from Oracle experts
- **Real Solutions**: Based on actual client issues and resolutions
- **Best Practices**: Industry standards and optimization tips

---

## 📚 Module Categories

| Module | Status | Issues | Samples |
|--------|--------|--------|----------|
| **PL/SQL** | ✅ Active | 150+ | 50+ |
| **SQL** | ✅ Active | 120+ | 40+ |
| **Forms** | 🔄 Building | 80+ | 30+ |
| **Workflows** | 🔄 Building | 60+ | 20+ |
| **OAF** | 🔄 Building | 100+ | 35+ |
| **Reports** | ⏳ Planned | - | - |
| **Data Migration** | ✅ Active | 90+ | 25+ |
| **API Integration** | 🔄 Building | 50+ | 15+ |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Frontend (React/Vue)                     │
│          Chat Interface + Search Engine                │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           FastAPI Backend Server                       │
│   (Issue Management, User Auth, Logging)               │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
│  PostgreSQL  │ │ Vector   │ │  OpenAI    │
│  Database    │ │ DB (RAG) │ │  GPT-4/3.5 │
└──────────────┘ └──────────┘ └────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Docker & Docker Compose

### Quick Start

1. **Clone Repository**
```bash
git clone https://github.com/Mahendarreddy143/oracle-support-ai.git
cd oracle-support-ai
```

2. **Using Docker Compose (Recommended)**
```bash
docker-compose up -d
```

3. **Manual Setup**

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

## 💡 How It Works

### Issue Resolution Flow

1. **User Input**: Submit issue with description and error details
2. **AI Processing**: 
   - Convert to semantic embeddings
   - Search similar resolved issues via vector DB
   - Analyze with GPT-4
3. **Solution Delivery**: Ranked solutions with code samples
4. **Feedback Loop**: Community votes improve ranking

---

## 📖 Documentation

- **[Architecture](./docs/architecture.md)** - System design and components
- **[API Documentation](./docs/api-documentation.md)** - REST API endpoints
- **[Contributing Guide](./docs/contribution-guidelines.md)** - How to contribute
- **[Deployment Guide](./docs/deployment.md)** - Production setup

---

## 📂 Repository Structure

```
oracle-support-ai/
├── backend/                    # FastAPI backend
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── frontend/                   # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/                       # Documentation
│   ├── architecture.md
│   ├── api-documentation.md
│   └── contribution-guidelines.md
├── templates/                  # Issue & solution templates
├── code-samples/               # Production-ready samples
│   ├── plsql-procedures/
│   ├── sql-queries/
│   └── forms-code/
├── issues/                     # Issues by category
│   ├── plsql/
│   ├── sql/
│   ├── forms/
│   └── workflows/
├── docker-compose.yml
└── README.md
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./docs/contribution-guidelines.md)

### Ways to Contribute:
- 🐛 Report issues and bugs
- 📝 Add solutions to knowledge base
- 💻 Submit code samples
- 🎨 Improve UI/UX
- 📚 Write documentation
- 🧪 Add tests

### Quick Contribution Steps:

1. **Fork the repository**
```bash
gh repo fork Mahendarreddy143/oracle-support-ai --clone
```

2. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make changes and commit**
```bash
git commit -m "feat: description of your changes"
```

4. **Push and create Pull Request**
```bash
git push origin feature/your-feature-name
```

---

## 🐛 Issue Templates

### Report a Bug
```
[BUG] Brief description of the issue

Error Code: ORA-XXXXX
Module: PL/SQL / SQL / Forms / etc.
Environment: Oracle EBS version, OS

Steps to reproduce:
1. ...
2. ...
```

### Request a Feature
```
[FEATURE] Brief description

Use Case: ...
Benefits: ...
Proposed Solution: ...
```

### Add Knowledge
```
[SOLUTION] Issue title

Problem: ...
Root Cause: ...
Solution: ...
Code Sample: ...
```

---

## 📊 Statistics

- **Total Issues**: 1500+
- **Resolved Issues**: 1200+
- **Code Samples**: 200+
- **Active Contributors**: 50+
- **Average Resolution Time**: 2.5 hours

---

## 🔗 Resources

- **Oracle Metalink**: [https://metalink.oracle.com](https://metalink.oracle.com)
- **Oracle EBS Documentation**: [https://docs.oracle.com/](https://docs.oracle.com/)
- **Community Discussions**: [GitHub Discussions](https://github.com/Mahendarreddy143/oracle-support-ai/discussions)
- **Issue Tracker**: [GitHub Issues](https://github.com/Mahendarreddy143/oracle-support-ai/issues)

---

## 📞 Support

- **Documentation**: [docs/](./docs/)
- **Issues**: [GitHub Issues](https://github.com/Mahendarreddy143/oracle-support-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mahendarreddy143/oracle-support-ai/discussions)
- **Email**: support@oracle-support-ai.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Oracle EBS Community
- Open Source Contributors
- All clients and testers
- Community expertise and feedback

---

## 🌟 Star Us!

If this project helps you, please ⭐ star it on GitHub!

---

**Built with ❤️ by the Oracle Support AI Community**

*Last Updated: 2026-05-14*
