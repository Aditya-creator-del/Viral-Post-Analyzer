# 🚀 Viral Post Analyzer

**Write better social media posts. Understand your audience. Improve your engagement.**

Viral Post Analyzer is a zero-dependency Python CLI tool that analyzes social media drafts, generates attention-grabbing hooks, and studies engagement patterns from your previous posts.

Supports **X (Twitter), LinkedIn, and Instagram**.

## ✨ Features

- 📊 **Viral Score:** Scores posts out of 100.
- 🎯 **Hook Analysis:** Evaluates your opening line.
- 💡 **Smart Suggestions:** Identifies areas for improvement.
- 🪝 **Hook Generator:** Generates six hook ideas for any topic.
- 📈 **Engagement Analytics:** Ranks your previous posts using likes, comments, and shares.
- 🧠 **Feature Analysis:** Compares engagement for posts containing questions, numbers, hashtags, emojis, and power words.
- 🐍 **Zero Dependencies:** Uses only the Python standard library.

## 🛠️ Requirements

- Python 3.8 or later
- Git (optional)

No external Python packages required.

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/Aditya-creator-del/Viral-Post-Analyzer.git
```

Enter the project folder:

```bash
cd Viral-Post-Analyzer
```

## 🚀 Usage

### 1. Analyze a social media post

```bash
python viral_analyzer.py "I built my first Python project 🚀 What should I build next? #Python" --platform x
```

Available platforms:

- `x`
- `linkedin`
- `instagram`

### 2. Analyze a draft file

```bash
python viral_analyzer.py --file draft.txt --platform x
```

### 3. Generate hook ideas

```bash
python viral_analyzer.py --hooks "Artificial Intelligence"
```

### 4. Analyze previous posts

Prepare a CSV file with these columns:

```csv
text,likes,comments,shares
"Built my first Python project",120,25,15
"5 AI tools developers should know",350,80,90
```

Run:

```bash
python viral_analyzer.py --csv sample_posts.csv
```

The analyzer ranks posts by total engagement and compares writing features.

## 📊 Scoring System

| Category | Points |
|---|---:|
| Hook | 25 |
| Length | 15 |
| Readability | 15 |
| Engagement prompt | 15 |
| Specific details | 10 |
| Emoji usage | 5 |
| Hashtags | 10 |
| Power words | 5 |
| **Total** | **100** |

Scores are heuristic estimates based on writing characteristics, not predictions or guarantees of virality.

## 🗺️ Roadmap

- [x] Core post scoring
- [x] Hook generator
- [x] CSV engagement analyzer
- [x] Feature comparison
- [ ] Automatic post rewriting
- [ ] Thread and carousel generator
- [ ] Best-time-to-post analysis
- [ ] Web dashboard
- [ ] Optional AI-powered features

## 🤝 Contributing

Contributions are welcome!

You can help by improving scoring algorithms, adding platform support, creating hook templates, or suggesting new features.

## 💰 Project Vision

The goal is to develop Viral Post Analyzer into a practical creator toolkit, with a free open-source CLI and potential premium features.

## 📄 License

This project is licensed under the MIT License.

---

**Built with Python ❤️**

If you find this project useful, consider giving it a ⭐ on GitHub!
