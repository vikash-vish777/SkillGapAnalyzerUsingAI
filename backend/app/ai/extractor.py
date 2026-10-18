import re
from app.ai.preprocessor import TextPreprocessor

# Canonical Skill Dictionary with Aliases & Boundary Definitions
# Format: canonical_name: { "category": str, "aliases": list[str], "case_sensitive": bool }
SKILL_DICTIONARY = {
    # Programming Languages
    "Python": {
        "category": "Programming Language",
        "aliases": ["python", "python3", "python2", "py"],
        "case_sensitive": False,
    },
    "JavaScript": {
        "category": "Programming Language",
        "aliases": ["javascript", "js", "ecmascript", "es6", "es2015"],
        "case_sensitive": False,
    },
    "TypeScript": {
        "category": "Programming Language",
        "aliases": ["typescript", "ts"],
        "case_sensitive": False,
    },
    "Java": {
        "category": "Programming Language",
        "aliases": ["java", "core java", "j2se"],
        # Avoid matching 'java' inside 'javascript'
        "case_sensitive": False,
        "negative_lookahead": r"(?!\s*script)",
    },
    "C": {
        "category": "Programming Language",
        "aliases": ["c language", "c programming", "ansi c"],
        # Strictly require context for single letter 'C' to prevent false positives in words like 'Basic', 'Cloud', 'C-suite'
        "case_sensitive": True,
        "exact_pattern": r"\bC\s+programming\b|\bC\s+language\b|\bANSI\s+C\b|(?<=[,\s])C(?=[,\s/&])",
    },
    "C++": {
        "category": "Programming Language",
        "aliases": ["c++", "cpp", "cplusplus"],
        "case_sensitive": False,
    },
    "C#": {
        "category": "Programming Language",
        "aliases": ["c#", "csharp", "c-sharp"],
        "case_sensitive": False,
    },
    "SQL": {
        "category": "Programming Language",
        "aliases": ["sql", "structured query language", "t-sql", "pl-sql", "pl/sql"],
        "case_sensitive": False,
    },
    "HTML5": {
        "category": "Frontend",
        "aliases": ["html", "html5"],
        "case_sensitive": False,
    },
    "CSS3": {
        "category": "Frontend",
        "aliases": ["css", "css3", "sass", "scss", "less"],
        "case_sensitive": False,
    },

    # Frameworks & Libraries
    "React.js": {
        "category": "Frontend",
        "aliases": ["react", "react.js", "reactjs", "react js"],
        "case_sensitive": False,
        "negative_lookahead": r"(?!\s*native)",
    },
    "Node.js": {
        "category": "Backend",
        "aliases": ["node", "node.js", "nodejs", "node js"],
        "case_sensitive": False,
    },
    "Flask": {
        "category": "Backend",
        "aliases": ["flask", "flask framework", "flask api"],
        "case_sensitive": False,
    },
    "Django": {
        "category": "Backend",
        "aliases": ["django", "django rest framework", "drf"],
        "case_sensitive": False,
    },
    "Spring Boot": {
        "category": "Backend",
        "aliases": ["spring boot", "springboot", "spring framework", "spring mvc"],
        "case_sensitive": False,
    },
    "Redux": {
        "category": "Frontend",
        "aliases": ["redux", "redux toolkit", "rtk"],
        "case_sensitive": False,
    },

    # Databases & Storage
    "MySQL": {
        "category": "Database",
        "aliases": ["mysql"],
        "case_sensitive": False,
    },
    "PostgreSQL": {
        "category": "Database",
        "aliases": ["postgresql", "postgres", "psql"],
        "case_sensitive": False,
    },
    "MongoDB": {
        "category": "Database",
        "aliases": ["mongodb", "mongo"],
        "case_sensitive": False,
    },
    "Redis": {
        "category": "Database",
        "aliases": ["redis"],
        "case_sensitive": False,
    },

    # Data Science & AI
    "Machine Learning": {
        "category": "Data Science & AI",
        "aliases": ["machine learning", "ml algorithms", "predictive modeling"],
        "case_sensitive": False,
    },
    "scikit-learn": {
        "category": "Data Science & AI",
        "aliases": ["scikit-learn", "scikit learn", "sklearn"],
        "case_sensitive": False,
    },
    "Pandas": {
        "category": "Data Science & AI",
        "aliases": ["pandas", "pandas dataframe"],
        "case_sensitive": False,
    },
    "NumPy": {
        "category": "Data Science & AI",
        "aliases": ["numpy"],
        "case_sensitive": False,
    },
    "Deep Learning": {
        "category": "Data Science & AI",
        "aliases": ["deep learning", "neural networks", "cnn", "rnn", "transformer models"],
        "case_sensitive": False,
    },
    "spaCy": {
        "category": "Data Science & AI",
        "aliases": ["spacy", "spacy nlp"],
        "case_sensitive": False,
    },

    # DevOps & Cloud
    "Git": {
        "category": "DevOps",
        "aliases": ["git", "github", "gitlab", "bitbucket", "version control"],
        "case_sensitive": False,
    },
    "Docker": {
        "category": "DevOps",
        "aliases": ["docker", "containerization", "docker compose", "docker-compose"],
        "case_sensitive": False,
    },
    "Kubernetes": {
        "category": "DevOps",
        "aliases": ["kubernetes", "k8s"],
        "case_sensitive": False,
    },
    "CI/CD": {
        "category": "DevOps",
        "aliases": ["ci/cd", "ci-cd", "continuous integration", "continuous deployment", "jenkins", "github actions"],
        "case_sensitive": False,
    },
    "AWS": {
        "category": "Cloud",
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda"],
        "case_sensitive": False,
    },
    "Linux": {
        "category": "DevOps",
        "aliases": ["linux", "ubuntu", "debian", "centos", "redhat", "bash scripting", "unix"],
        "case_sensitive": False,
    },

    # Architecture & Practices
    "REST APIs": {
        "category": "Architecture",
        "aliases": ["rest api", "rest apis", "restful api", "restful apis", "restful web services", "rest endpoints"],
        "case_sensitive": False,
    },
    "Agile Methodologies": {
        "category": "Process",
        "aliases": ["agile", "scrum", "kanban", "sprints"],
        "case_sensitive": False,
    },
}

class SkillExtractor:
    """Extracts technical skills from text using pre-compiled regex boundaries and alias resolution."""

    def __init__(self, dictionary: dict = None):
        self.dictionary = dictionary or SKILL_DICTIONARY
        self._compiled_patterns = self._build_patterns()

    def _build_patterns(self) -> dict[str, list[re.Pattern]]:
        """Pre-compiles boundary-safe regular expressions for each skill."""
        patterns = {}
        for canonical, config in self.dictionary.items():
            compiled_list = []

            # Custom explicit pattern if configured
            if "exact_pattern" in config:
                flags = 0 if config.get("case_sensitive") else re.IGNORECASE
                compiled_list.append(re.compile(config["exact_pattern"], flags))
            else:
                for alias in config.get("aliases", []):
                    # Mask/escape alias characters (e.g. C++, .NET)
                    escaped_alias = re.escape(alias)
                    lookahead = config.get("negative_lookahead", "")

                    # Word boundary handling:
                    # For aliases ending with special symbols (like ++ or #), \b does not match after +, so we use (?!\w)
                    if alias.endswith(("+", "#")):
                        pattern_str = rf"(?<!\w){escaped_alias}(?!\w){lookahead}"
                    elif alias.startswith("."):
                        pattern_str = rf"(?<!\w){escaped_alias}\b{lookahead}"
                    else:
                        pattern_str = rf"\b{escaped_alias}\b{lookahead}"

                    flags = 0 if config.get("case_sensitive") else re.IGNORECASE
                    compiled_list.append(re.compile(pattern_str, flags))

            patterns[canonical] = compiled_list
        return patterns

    def extract_skills(self, text: str) -> dict[str, dict]:
        """Scans text and extracts matched canonical skills with evidence snippets.
        
        Returns:
            dict[str, dict]: Mapping of canonical_skill_name -> {
                "name": str,
                "category": str,
                "evidence": str,
                "confidence": float
            }
        """
        if not text:
            return {}

        sentences = TextPreprocessor.get_sentences_and_bullets(text)
        found_skills = {}

        # 1. Search sentence by sentence to capture the most relevant evidence snippet
        for sentence in sentences:
            for canonical, patterns in self._compiled_patterns.items():
                if canonical in found_skills:
                    continue  # Already recorded evidence

                for pattern in patterns:
                    match = pattern.search(sentence)
                    if match:
                        found_skills[canonical] = {
                            "name": canonical,
                            "category": self.dictionary[canonical]["category"],
                            "evidence": sentence.strip(),
                            "confidence": 1.0,
                        }
                        break

        # 2. Global fallback check on full text if some multi-line phrase was split
        if len(found_skills) < len(self._compiled_patterns):
            for canonical, patterns in self._compiled_patterns.items():
                if canonical in found_skills:
                    continue
                for pattern in patterns:
                    match = pattern.search(text)
                    if match:
                        # Extract 80 character window around match as evidence
                        start = max(0, match.start() - 30)
                        end = min(len(text), match.end() + 50)
                        snippet = text[start:end].replace("\n", " ").strip()
                        found_skills[canonical] = {
                            "name": canonical,
                            "category": self.dictionary[canonical]["category"],
                            "evidence": f"...{snippet}...",
                            "confidence": 0.95,
                        }
                        break

        return found_skills

