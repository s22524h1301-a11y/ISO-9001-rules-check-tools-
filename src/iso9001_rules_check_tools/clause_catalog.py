from iso9001_rules_check_tools.models import Clause


CLAUSE_CATALOG: tuple[Clause, ...] = (
    Clause(
        clause_id="4.1",
        clause_title="Understanding the organization and its context",
        clause_title_zh="\u7d44\u7e54\u53ca\u5176\u80cc\u666f",
        keywords=("organization", "context", "internal issues", "external issues", "\u80cc\u666f", "\u5229\u5bb3\u95dc\u4fc2\u4eba"),
        description="Look for text about the organization, its context, and relevant internal or external issues.",
    ),
    Clause(
        clause_id="5.2",
        clause_title="Quality policy",
        clause_title_zh="\u54c1\u8cea\u653f\u7b56",
        keywords=("quality policy", "policy", "communicate", "\u54c1\u8cea\u653f\u7b56", "\u5ba3\u5c0e"),
        description="Look for a quality policy that is established, communicated, and available as a statement of intent.",
    ),
    Clause(
        clause_id="6.2",
        clause_title="Quality objectives and planning to achieve them",
        clause_title_zh="\u54c1\u8cea\u76ee\u6a19\u53ca\u5176\u898f\u5283",
        keywords=("quality objectives", "planning", "objective", "target", "\u54c1\u8cea\u76ee\u6a19", "\u898f\u5283"),
        description="Look for quality objectives, planning, and actions to achieve them.",
    ),
    Clause(
        clause_id="7.5",
        clause_title="Documented information",
        clause_title_zh="\u6210\u6587\u8cc7\u8a0a",
        keywords=("documented information", "document", "records", "\u6587\u4ef6", "\u7d00\u9304"),
        description="Look for controlled documents, records, and other documented information.",
    ),
)


def default_clause_catalog() -> tuple[Clause, ...]:
    return CLAUSE_CATALOG
