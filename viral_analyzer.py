
import argparse
import re
import csv
from pathlib import Path

# ==========================================
# VIRAL POST ANALYZER
# Version 2.0
# ==========================================

PLATFORMS = {
    "x": {"min": 100, "max": 280, "hashtags": 2},
    "linkedin": {"min": 300, "max": 1300, "hashtags": 5},
    "instagram": {"min": 80, "max": 500, "hashtags": 8},
}

POWER_WORDS = [
    "secret", "amazing", "powerful", "free",
    "proven", "ultimate", "mistake", "simple",
    "learn", "discover", "build", "growth"
]


# ==========================================
# TEXT UTILITIES
# ==========================================

def get_emojis(text):
    return re.findall(
        r"[\U0001F300-\U0001FAFF]",
        text
    )


def get_words(text):
    return re.findall(r"\b\w+\b", text)


# ==========================================
# POST SCORING ENGINE
# ==========================================

def analyze_post(text, platform):

    config = PLATFORMS[platform]

    score = 0
    working = []
    fixes = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    first_line = lines[0] if lines else ""

    words = get_words(text)
    hashtags = re.findall(r"#\w+", text)
    emojis = get_emojis(text)

    # HOOK - 25 POINTS

    if 0 < len(first_line) <= 100:
        score += 15
        working.append("Short first line (good scroll-stopper).")
    else:
        fixes.append("Make your opening line shorter and stronger.")

    if re.search(
        r"\d+|why|how|what|secret|mistake",
        first_line,
        re.I
    ):
        score += 10
        working.append("Hook uses a number, question or strong opener.")
    else:
        fixes.append("Add a number, question or curiosity-driven hook.")

    # LENGTH - 15 POINTS

    if config["min"] <= len(text) <= config["max"]:
        score += 15
        working.append("Good post length for this platform.")
    else:
        fixes.append(
            f"Try keeping your post between "
            f"{config['min']} and {config['max']} characters."
        )

    # READABILITY - 15 POINTS

    avg_word_length = (
        sum(len(word) for word in words) / len(words)
        if words else 0
    )

    if words and avg_word_length <= 6:
        score += 15
        working.append("Easy-to-read language.")
    else:
        fixes.append("Use simpler and shorter words.")

    # ENGAGEMENT - 15 POINTS

    if "?" in text or re.search(
        r"\b(comment|share|follow|reply|tell me)\b",
        text,
        re.I
    ):
        score += 15
        working.append("Invites audience engagement.")
    else:
        fixes.append("End with a question or call to action.")

    # SPECIFICS - 10 POINTS

    if re.search(r"\d+", text):
        score += 10
        working.append("Contains concrete numbers or details.")
    else:
        fixes.append("Include a number, result or specific example.")

    # EMOJI - 5 POINTS

    if 1 <= len(emojis) <= 4:
        score += 5
        working.append("Moderate emoji usage.")
    else:
        fixes.append("Try using 1-4 relevant emojis.")

    # HASHTAGS - 10 POINTS

    if 1 <= len(hashtags) <= config["hashtags"]:
        score += 10
        working.append("Good hashtag usage.")
    else:
        fixes.append(
            f"Use 1-{config['hashtags']} relevant hashtags."
        )

    # POWER WORDS - 5 POINTS

    if any(
        word in text.lower()
        for word in POWER_WORDS
    ):
        score += 5
        working.append("Uses attention-grabbing power words.")
    else:
        fixes.append("Add a strong word that creates curiosity.")

    return score, working, fixes


# ==========================================
# HOOK GENERATOR
# ==========================================

def generate_hooks(topic):

    templates = [
        f"Nobody talks about this side of {topic}...",
        f"5 things I learned about {topic}.",
        f"What if everything you know about {topic} is wrong?",
        f"How I started learning {topic} from zero.",
        f"The biggest mistake beginners make with {topic}.",
        f"Here's a simple way to understand {topic}."
    ]

    print("\n========== HOOK IDEAS ==========\n")

    for i, hook in enumerate(templates, 1):
        print(f"{i}. {hook}")


# ==========================================
# FEATURE ANALYSIS
# ==========================================

def analyze_features(results):

    features = {
        "Questions": lambda t: "?" in t,

        "Numbers": lambda t: bool(
            re.search(r"\d+", t)
        ),

        "Hashtags": lambda t: bool(
            re.findall(r"#\w+", t)
        ),

        "Emojis": lambda t: bool(
            get_emojis(t)
        ),

        "Power words": lambda t: any(
            word in t.lower()
            for word in POWER_WORDS
        )
    }

    print("\n========== WHAT WORKS IN YOUR POSTS ==========")

    for name, check in features.items():

        with_feature = [
            post["engagement"]
            for post in results
            if check(post["text"])
        ]

        without_feature = [
            post["engagement"]
            for post in results
            if not check(post["text"])
        ]

        if not with_feature or not without_feature:
            print(f"\n{name}: Not enough data to compare.")
            continue

        avg_yes = sum(with_feature) / len(with_feature)
        avg_no = sum(without_feature) / len(without_feature)

        print(f"\n{name}:")
        print(f"  With feature: {avg_yes:.1f} average engagement")
        print(f"  Without feature: {avg_no:.1f} average engagement")

        if avg_yes > avg_no:
            print("  Observation: Higher engagement with this feature.")
        elif avg_yes < avg_no:
            print("  Observation: Lower engagement with this feature.")
        else:
            print("  Observation: No difference in this dataset.")

    print(
        "\nNote: These are correlations, not proof of causation."
    )


# ==========================================
# CSV HISTORY ANALYZER
# ==========================================

def analyze_csv(filename):

    try:

        with open(
            filename,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(
                (line for line in file if line.strip())
            )

            if not reader.fieldnames:
                print("CSV is empty.")
                return

            reader.fieldnames = [
                name.strip().lower()
                for name in reader.fieldnames
            ]

            required = {
                "text",
                "likes",
                "comments",
                "shares"
            }

            if not required.issubset(reader.fieldnames):
                print(
                    "CSV must contain: "
                    "text, likes, comments, shares"
                )
                return

            results = []

            for row in reader:

                try:

                    text = row["text"].strip()

                    if not text:
                        continue

                    engagement = (
                        int(row["likes"]) +
                        int(row["comments"]) +
                        int(row["shares"])
                    )

                    if engagement < 0:
                        continue

                    results.append({
                        "text": text,
                        "engagement": engagement
                    })

                except (ValueError, TypeError, KeyError):
                    continue

        if not results:
            print("No valid posts found.")
            return

        results.sort(
            key=lambda post: post["engagement"],
            reverse=True
        )

        total = sum(
            post["engagement"]
            for post in results
        )

        average = total / len(results)

        print("\n========== TOP PERFORMING POSTS ==========\n")

        for post in results[:5]:

            print(f"Engagement: {post['engagement']}")
            print(f"Post: {post['text']}\n")

        print("------------------------------------------")
        print(f"Posts analyzed: {len(results)}")
        print(f"Total engagement: {total}")
        print(f"Average engagement: {average:.1f}")

        # Feature analysis
        analyze_features(results)

    except FileNotFoundError:
        print(f"CSV file not found: {filename}")

    except PermissionError:
        print("Permission denied while reading CSV file.")

    except UnicodeDecodeError:
        print("Could not decode CSV. Save it as UTF-8.")


# ==========================================
# MAIN CLI
# ==========================================

def main():

    parser = argparse.ArgumentParser(
        description="Viral Post Analyzer - Version 2.0"
    )

    parser.add_argument(
        "text",
        nargs="?",
        help="Social media post text"
    )

    parser.add_argument(
        "--platform",
        choices=PLATFORMS,
        default="x"
    )

    parser.add_argument(
        "--file",
        help="Read post from a text file"
    )

    parser.add_argument(
        "--hooks",
        help="Generate hooks for a topic"
    )

    parser.add_argument(
        "--csv",
        help="Analyze past posts from a CSV file"
    )

    args = parser.parse_args()

    # HOOK GENERATOR

    if args.hooks:
        generate_hooks(args.hooks)
        return

    # CSV ANALYZER

    if args.csv:
        analyze_csv(args.csv)
        return

    # READ POST

    if args.file:

        try:
            text = Path(args.file).read_text(
                encoding="utf-8-sig"
            )

        except FileNotFoundError:
            print("Draft file not found.")
            return

        except OSError as error:
            print(f"Could not read draft: {error}")
            return

    elif args.text:
        text = args.text

    else:
        parser.error(
            "Provide post text, --file, --hooks or --csv"
        )

    if not text.strip():
        print("Post cannot be empty.")
        return

    # ANALYZE POST

    score, working, fixes = analyze_post(
        text,
        args.platform
    )

    label = (
        "Strong" if score >= 75
        else "Average" if score >= 45
        else "Needs work"
    )

    print("\n========== VIRAL POST ANALYZER ==========")

    print(
        f"\nViral score for {args.platform}: "
        f"{score}/100 ({label})"
    )

    print("\nWhat's working:")

    if working:
        for item in working:
            print("  +", item)
    else:
        print("  No strong features detected yet.")

    print("\nWhat to improve:")

    if fixes:
        for item in fixes:
            print("  -", item)
    else:
        print("  No major improvements suggested.")

    print("\n==========================================")


if __name__ == "__main__":
    main()
