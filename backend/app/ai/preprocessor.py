import re
import unicodedata

class TextPreprocessor:
    """Preprocesses and normalizes raw resume text while preserving technical terminology."""

    # Bullet point symbols to normalize
    BULLET_PATTERN = re.compile(r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25AB\u25CF\u25CB\u25A0\u25A1\u25BA\u2713\u2714\u2605\u2013\u2014]")
    
    # Common smart quotes and special apostrophes
    QUOTE_PATTERN = re.compile(r"[\u2018\u2019\u201C\u201D]")

    # Technical tokens that must retain special punctuation
    PROTECTED_TERMS = {
        "c++": "C_PLUS_PLUS_PROTECTED",
        "c#": "C_SHARP_PROTECTED",
        ".net": "DOT_NET_PROTECTED",
        "asp.net": "ASP_DOT_NET_PROTECTED",
        "node.js": "NODE_DOT_JS_PROTECTED",
        "react.js": "REACT_DOT_JS_PROTECTED",
        "vue.js": "VUE_DOT_JS_PROTECTED",
        "ci/cd": "CI_SLASH_CD_PROTECTED",
        "tcp/ip": "TCP_SLASH_IP_PROTECTED",
        "pl/sql": "PL_SLASH_SQL_PROTECTED",
    }

    REVERSE_PROTECTED_TERMS = {v: k for k, v in PROTECTED_TERMS.items()}

    @classmethod
    def clean_text(cls, raw_text: str) -> str:
        """Cleans and standardizes raw text without destroying technical identifiers."""
        if not raw_text:
            return ""

        # 1. Normalize Unicode (e.g. NFKC standardizes composite characters)
        text = unicodedata.normalize("NFKC", raw_text)

        # 2. Standardize quotation marks
        text = cls.QUOTE_PATTERN.sub('"', text)

        # 3. Standardize bullet characters to standard list marker
        text = cls.BULLET_PATTERN.sub("\n- ", text)

        # 4. Normalize non-standard whitespace and tabs
        text = re.sub(r"[ \t]+", " ", text)

        # 5. Normalize excessive blank lines (max 2 consecutive newlines)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @classmethod
    def get_sentences_and_bullets(cls, text: str) -> list[str]:
        """Splits normalized text into distinct lines, bullets, and sentences.
        
        This enables pinpointing the exact resume snippet (evidence) where a skill was identified.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        chunks = []

        for line in lines:
            # If line is already a bullet item, keep as is
            if line.startswith("- ") or line.startswith("* "):
                chunks.append(line.lstrip("-* ").strip())
                continue

            # Split standard paragraphs by sentence boundaries (.!?)
            sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", line)
            for s in sentences:
                s_clean = s.strip()
                if len(s_clean) > 3:
                    chunks.append(s_clean)

        return chunks

    @classmethod
    def mask_protected_terms(cls, text: str) -> str:
        """Temporarily substitutes protected technical tokens with safe alphanumeric placeholders."""
        masked_text = text
        for term, placeholder in cls.PROTECTED_TERMS.items():
            # Match term with word boundaries where appropriate
            pattern = re.compile(rf"(?i)(?<!\w){re.escape(term)}(?!\w)")
            masked_text = pattern.sub(placeholder, masked_text)
        return masked_text

    @classmethod
    def unmask_protected_terms(cls, text: str) -> str:
        """Restores protected technical tokens from placeholders back to original form."""
        restored = text
        for placeholder, original in cls.REVERSE_PROTECTED_TERMS.items():
            restored = restored.replace(placeholder, original)
        return restored

