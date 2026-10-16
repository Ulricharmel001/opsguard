from app.guard import (
    ASK_HUMAN, BLOCK, REFUSE, REVIEW, RUN, SAFE,
    apply_policy, hard_rule_check,
)


def test_safe_high_confidence_runs():
    assert apply_policy(SAFE, 0.95) == RUN


def test_safe_low_confidence_asks_human():
    assert apply_policy(SAFE, 0.80) == ASK_HUMAN


def test_very_low_confidence_asks_human():
    assert apply_policy(SAFE, 0.30) == ASK_HUMAN


def test_review_always_asks_human():
    assert apply_policy(REVIEW, 0.99) == ASK_HUMAN


def test_block_refuses():
    assert apply_policy(BLOCK, 0.70) == REFUSE


def test_unknown_choice_fails_safe():
    assert apply_policy("MAYBE", 0.99) == ASK_HUMAN


def test_hard_rule_blocks_prod_database_delete():
    assert hard_rule_check("delete_database", {}, "production") is not None


def test_hard_rule_allows_staging_list():
    assert hard_rule_check("list_servers", {}, "staging") is None
